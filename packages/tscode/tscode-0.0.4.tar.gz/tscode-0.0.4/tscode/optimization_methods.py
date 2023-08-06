'''

TSCODE: Transition State Conformational Docker
Copyright (C) 2021 Nicolò Tampellini

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

'''

import os
import time
import itertools as it
from copy import deepcopy
from subprocess import DEVNULL, STDOUT, check_call

import numpy as np
from ase import Atoms
from sella import Sella
import networkx as nx
from rmsd import kabsch
from cclib.io import ccread
from ase.dyneb import DyNEB
from ase.optimize import BFGS, LBFGS
from ase.calculators.mopac import MOPAC
from ase.calculators.orca import ORCA
from ase.calculators.gaussian import Gaussian
from ase.constraints import FixInternals
from ase.vibrations import Vibrations
from scipy.spatial.transform import Rotation as R

from settings import COMMANDS, MEM_GB
from parameters import nci_dict
from hypermolecule_class import graphize
from utils import (
                   center_of_mass,
                   clean_directory,
                   diagonalize,
                   dihedral,
                   findPaths,
                   get_double_bonds_indexes,
                   HiddenPrints,
                   kronecker_delta,
                   neighbors,
                   norm,
                   pt,
                   time_to_string,
                   write_xyz
                   )

class MopacReadError(Exception):
    '''
    Thrown when reading MOPAC output files fails for some reason.
    '''

class Spring:
    '''
    ASE Custom Constraint Class
    Adds an harmonic force between a pair of atoms.
    Spring constant is very high to achieve tight convergence,
    but force is dampened so as not to ruin structures.
    '''
    def __init__(self, i1, i2, d_eq, k=1000):
        self.i1, self.i2 = i1, i2
        self.d_eq = d_eq
        self.k = k

    def adjust_positions(self, atoms, newpositions):
        pass

    def adjust_forces(self, atoms, forces):

        direction = atoms.positions[self.i2] - atoms.positions[self.i1]
        # vector connecting atom1 to atom2

        spring_force = self.k * (np.linalg.norm(direction) - self.d_eq)
        # absolute spring force (float). Positive if spring is overstretched.

        # spring_force = np.clip(spring_force, -10, 10)
        # force is clipped at 10 eV/A

        forces[self.i1] += (norm(direction) * spring_force)
        forces[self.i2] -= (norm(direction) * spring_force)
        # applying harmonic force to each atom, directed toward the other one

    def __repr__(self):
        return f'Spring - ids:{self.i1}/{self.i2} - d_eq:{self.d_eq}, k:{self.k}'

def get_ase_calc(calculator, procs, method):
    '''
    Attach the correct ASE calculator
    to the ASE Atoms object
    '''

    if calculator == 'XTB':
        try:
            from xtb.ase.calculator import XTB
        except ImportError:
            raise Exception(('Cannot import xtb python bindings. Install them with:\n'
                             '>>> conda install -c conda-forge xtb-python\n'
                             '(See https://github.com/grimme-lab/xtb-python)'))
        return XTB(method=method)

    
    command = COMMANDS[calculator]

    if calculator == 'MOPAC':
        return MOPAC(label='temp',
                    command=f'{command} temp.mop > temp.cmdlog 2>&1',
                    method=method)

    elif calculator == 'ORCA':
        if procs > 1:
            orcablocks = f'%pal nprocs {procs} end'
            return ORCA(label='temp',
                        command=f'{command} temp.inp > temp.out 2>&1',
                        orcasimpleinput=method,
                        orcablocks=orcablocks)
        return ORCA(label='temp',
                    command=f'{command} temp.inp > temp.out 2>&1',
                    orcasimpleinput=method)

    elif calculator == 'GAUSSIAN':

        # firstline = method if procs == 1 else f'%nprocshared={procs}\n{method}'

        calc = Gaussian(label='temp',
                        command=f'{command} temp.com',
                        method=method,
                        nprocshared=procs,
                        mem=str(MEM_GB)+'GB',
                        )

        if 'g09' in command:

            from ase.io import read
            def g09_read_results(self=calc):
                output = read(self.label + '.out', format='gaussian-out')
                self.calc = output.calc
                self.results = output.calc.results

            calc.read_results = g09_read_results

            # Adapting for g09 outputting .out files instead of g16 .log files.
            # This is a bad fix and the issue should be corrected in
            # the ASE source code: pull request on GitHub pending

            return calc

def scramble(array, sequence):
    return np.array([array[s] for s in sequence])

def read_mop_out(filename):
    '''
    Reads a MOPAC output looking for optimized coordinates and energy.
    :params filename: name of MOPAC filename (.out extension)
    :return coords, energy: array of optimized coordinates and absolute energy, in kcal/mol
    '''
    coords = []
    with open(filename, 'r') as f:
        while True:
            line = f.readline()

            if 'Too many variables. By definition, at least one force constant is exactly zero' in line:
                success = False
                return None, np.inf, success

            if not line:
                break
            
            if 'SCF FIELD WAS ACHIEVED' in line:
                    while True:
                        line = f.readline()
                        if not line:
                            break

                        if 'FINAL HEAT OF FORMATION' in line:
                            energy = float(line.split()[5])
                            # in kcal/mol

                        if 'CARTESIAN COORDINATES' in line:
                            line = f.readline()
                            line = f.readline()
                            while line != '\n':
                                splitted = line.split()
                                # symbols.append(splitted[1])
                                coords.append([float(splitted[2]),
                                               float(splitted[3]),
                                               float(splitted[4])])
                                            
                                line = f.readline()
                                if not line:
                                    break
                            break
                    break

    coords = np.array(coords)

    if coords.shape[0] != 0:
        success = True
        return coords, energy, success
    
    raise MopacReadError(f'Cannot read file {filename}: maybe a badly specified MOPAC keyword?')

def mopac_opt(coords, atomnos, constrained_indexes=None, method='PM7', title='temp', read_output=True):
    '''
    This function writes a MOPAC .mop input, runs it with the subprocess
    module and reads its output. Coordinates used are mixed
    (cartesian and internal) to be able to constrain the reactive atoms
    distances specified in constrained_indexes.

    :params coords: array of shape (n,3) with cartesian coordinates for atoms
    :params atomnos: array of atomic numbers for atoms
    :params constrained_indexes: array of shape (n,2), with the indexes
                                 of atomic pairs to be constrained
    :params method: string, specifiyng the first line of keywords for the MOPAC input file.
    :params title: string, used as a file name and job title for the mopac input file.
    :params read_output: Whether to read the output file and return anything.
    '''

    constrained_indexes_list = constrained_indexes.ravel() if constrained_indexes is not None else []
    constrained_indexes = constrained_indexes if constrained_indexes is not None else []

    order = []
    s = [method + '\n' + title + '\n\n']
    for i, num in enumerate(atomnos):
        if i not in constrained_indexes:
            order.append(i)
            s.append(' {} {} 1 {} 1 {} 1\n'.format(pt[num].symbol, coords[i][0], coords[i][1], coords[i][2]))

    free_indexes = list(set(range(len(atomnos))) - set(constrained_indexes_list))
    # print('free indexes are', free_indexes, '\n')

    if len(constrained_indexes_list) == len(set(constrained_indexes_list)):
    # block pairs of atoms if no atom is involved in more than one distance constrain

        for a, b in constrained_indexes:
            
            order.append(b)
            order.append(a)

            c, d = np.random.choice(free_indexes, 2)
            while c == d:
                c, d = np.random.choice(free_indexes, 2)
            # indexes of reference atoms, from unconstraind atoms set

            dist = np.linalg.norm(coords[a] - coords[b]) # in Angstrom
            # print(f'DIST - {dist} - between {a} {b}')

            angle = np.arccos(norm(coords[a] - coords[b]) @ norm(coords[c] - coords[b]))*180/np.pi # in degrees
            # print(f'ANGLE - {angle} - between {a} {b} {c}')

            d_angle = dihedral([coords[a],
                                coords[b],
                                coords[c],
                                coords[d]])
            d_angle += 360 if d_angle < 0 else 0
            # print(f'D_ANGLE - {d_angle} - between {a} {b} {c} {d}')

            list_len = len(s)
            s.append(' {} {} 1 {} 1 {} 1\n'.format(pt[atomnos[b]].symbol, coords[b][0], coords[b][1], coords[b][2]))
            s.append(' {} {} 0 {} 1 {} 1 {} {} {}\n'.format(pt[atomnos[a]].symbol, dist, angle, d_angle, list_len, free_indexes.index(c)+1, free_indexes.index(d)+1))
            # print(f'Blocked bond between mopac ids {list_len} {list_len+1}\n')

    elif len(set(constrained_indexes_list)) == 3:
    # three atoms, the central bound to the other two
    # OTHERS[0]: cartesian
    # CENTRAL: internal (self, others[0], two random)
    # OTHERS[1]: internal (self, central, two random)
        
        central = max(set(constrained_indexes_list), key=lambda x: list(constrained_indexes_list).count(x))
        # index of the atom that is constrained to two other

        others = list(set(constrained_indexes_list) - {central})

    # OTHERS[0]

        order.append(others[0])
        s.append(' {} {} 1 {} 1 {} 1\n'.format(pt[atomnos[others[0]]].symbol, coords[others[0]][0], coords[others[0]][1], coords[others[0]][2]))
        # first atom is placed in cartesian coordinates, the other two have a distance constraint and are expressed in internal coordinates

    #CENTRAL

        order.append(central)
        c, d = np.random.choice(free_indexes, 2)
        while c == d:
            c, d = np.random.choice(free_indexes, 2)
        # indexes of reference atoms, from unconstraind atoms set

        dist = np.linalg.norm(coords[central] - coords[others[0]]) # in Angstrom

        angle = np.arccos(norm(coords[central] - coords[others[0]]) @ norm(coords[others[0]] - coords[c]))*180/np.pi # in degrees

        d_angle = dihedral([coords[central],
                            coords[others[0]],
                            coords[c],
                            coords[d]])
        d_angle += 360 if d_angle < 0 else 0

        list_len = len(s)
        s.append(' {} {} 0 {} 1 {} 1 {} {} {}\n'.format(pt[atomnos[central]].symbol, dist, angle, d_angle, list_len-1, free_indexes.index(c)+1, free_indexes.index(d)+1))

    #OTHERS[1]

        order.append(others[1])
        c1, d1 = np.random.choice(free_indexes, 2)
        while c1 == d1:
            c1, d1 = np.random.choice(free_indexes, 2)
        # indexes of reference atoms, from unconstraind atoms set

        dist1 = np.linalg.norm(coords[others[1]] - coords[central]) # in Angstrom

        angle1 = np.arccos(norm(coords[others[1]] - coords[central]) @ norm(coords[others[1]] - coords[c1]))*180/np.pi # in degrees

        d_angle1 = dihedral([coords[others[1]],
                             coords[central],
                             coords[c1],
                             coords[d1]])
        d_angle1 += 360 if d_angle < 0 else 0

        list_len = len(s)
        s.append(' {} {} 0 {} 1 {} 1 {} {} {}\n'.format(pt[atomnos[others[1]]].symbol, dist1, angle1, d_angle1, list_len-1, free_indexes.index(c1)+1, free_indexes.index(d1)+1))

    else:
        raise NotImplementedError('The constraints provided for MOPAC optimization are not yet supported')


    s = ''.join(s)
    with open(f'{title}.mop', 'w') as f:
        f.write(s)
    
    try:
        check_call(f'{COMMANDS["MOPAC"]} {title}.mop'.split(), stdout=DEVNULL, stderr=STDOUT)
    except KeyboardInterrupt:
        print('KeyboardInterrupt requested by user. Quitting.')
        quit()

    os.remove(f'{title}.mop')
    # delete input, we do not need it anymore

    if read_output:

        inv_order = [order.index(i) for i in range(len(order))]
        # undoing the atomic scramble that was needed by the mopac input requirements

        opt_coords, energy, success = read_mop_out(f'{title}.out')
        os.remove(f'{title}.out')

        opt_coords = scramble(opt_coords, inv_order) if opt_coords is not None else coords
        # If opt_coords is None, that is if TS seeking crashed,
        # sets opt_coords to the old coords. If not, unscrambles
        # coordinates read from mopac output.

        return opt_coords, energy, success

def orca_opt(coords, atomnos, constrained_indexes=None, method='PM3', procs=1, title='temp', read_output=True):
    '''
    This function writes an ORCA .inp file, runs it with the subprocess
    module and reads its output.

    :params coords: array of shape (n,3) with cartesian coordinates for atoms.
    :params atomnos: array of atomic numbers for atoms.
    :params constrained_indexes: array of shape (n,2), with the indexes
                                 of atomic pairs to be constrained.
    :params method: string, specifiyng the first line of keywords for the MOPAC input file.
    :params title: string, used as a file name and job title for the mopac input file.
    :params read_output: Whether to read the output file and return anything.
    '''

    s = '! %s Opt\n\n# ORCA input generated by TSCoDe\n\n' % (method)

    if procs > 1:
        s += f'%pal nprocs {procs} end\n'

    if constrained_indexes is not None:
        s += '%geom\nConstraints\n'

        for a, b in constrained_indexes:
            s += '{B %s %s C}\n' % (a, b)

        s += 'end\nend\n\n'

    s += '*xyz 0 1\n'

    for i, atom in enumerate(coords):
        s += '%s     % .6f % .6f % .6f\n' % (pt[atomnos[i]].symbol, atom[0], atom[1], atom[2])

    s += '*\n'

    s = ''.join(s)
    with open(f'{title}.inp', 'w') as f:
        f.write(s)
    
    try:
        check_call(f'{COMMANDS["ORCA"]} {title}.inp'.split(), stdout=DEVNULL, stderr=STDOUT)

    except KeyboardInterrupt:
        print('KeyboardInterrupt requested by user. Quitting.')
        quit()

    if read_output:

        try:
            opt_coords = ccread(f'{title}.xyz').atomcoords[0]
            energy = read_orca_property(f'{title}_property.txt')

            clean_directory()

            return opt_coords, energy, True

        except FileNotFoundError:
            return None, None, False

def read_orca_property(filename):
    '''
    Read energy from ORCA property output file
    '''
    energy = None

    with open(filename, 'r') as f:

        while True:
            line = f.readline()

            if not line:
                break

            if 'SCF Energy:' in line:
                energy = float(line.split()[2])

    return energy

def gaussian_opt(coords, atomnos, constrained_indexes=None, method='PM6', procs=1, title='temp', read_output=True):
    '''
    This function writes a Gaussian .inp file, runs it with the subprocess
    module and reads its output.

    :params coords: array of shape (n,3) with cartesian coordinates for atoms.
    :params atomnos: array of atomic numbers for atoms.
    :params constrained_indexes: array of shape (n,2), with the indexes
                                 of atomic pairs to be constrained.
    :params method: string, specifiyng the first line of keywords for the MOPAC input file.
    :params title: string, used as a file name and job title for the mopac input file.
    :params read_output: Whether to read the output file and return anything.
    '''

    s = ''

    if MEM_GB is not None:
        s += f'%mem{MEM_GB}GB\n'

    if procs > 1:
        s += f'%nprocshared={procs}\n'

    s += '# ' + method
    
    if constrained_indexes is not None:
        s += 'opt=modredundant'
        
    s += '\n\nGaussian input generated by TSCoDe\n\n0 1\n'

    for i, atom in enumerate(coords):
        s += '%s     % .6f % .6f % .6f\n' % (pt[atomnos[i]].symbol, atom[0], atom[1], atom[2])

    s += '\n'

    if constrained_indexes is not None:

        for a, b in constrained_indexes:
            s += 'B %s %s F\n' % (a, b)

    s = ''.join(s)
    with open(f'{title}.com', 'w') as f:
        f.write(s)
    
    try:
        check_call(f'{COMMANDS["GAUSSIAN"]} {title}.com'.split(), stdout=DEVNULL, stderr=STDOUT)

    except KeyboardInterrupt:
        print('KeyboardInterrupt requested by user. Quitting.')
        quit()

    if read_output:

        try:
            data = ccread(f'{title}.out')
            opt_coords = data.atomcoords[0]
            energy = data.scfenergies[-1] * 23.060548867 # eV to kcal/mol

            clean_directory()

            return opt_coords, energy, True

        except FileNotFoundError:
            return None, None, False

def xtb_opt(coords, atomnos, constrained_indexes=None, method='GFN2-xTB', title='temp', read_output=True):
    '''
    This function writes an XTB .inp file, runs it with the subprocess
    module and reads its output.

    :params coords: array of shape (n,3) with cartesian coordinates for atoms.
    :params atomnos: array of atomic numbers for atoms.
    :params constrained_indexes: array of shape (n,2), with the indexes
                                 of atomic pairs to be constrained.
    :params method: string, specifiyng the first line of keywords for the MOPAC input file.
    :params title: string, used as a file name and job title for the mopac input file.
    :params read_output: Whether to read the output file and return anything.
    '''

    with open(f'{title}.xyz', 'w') as f:
        write_xyz(coords, atomnos, f, title=title)

    s = f'$opt\n   logfile={title}_opt.log\n$end'
         
    if constrained_indexes is not None:
        s += '\n$constrain\n'
        for a, b in constrained_indexes:
            s += '   distance: %s, %s, %s\n' % (a+1, b+1, round(np.linalg.norm(coords[a]-coords[b]), 5))
    
    if method.upper() in ('GFN-XTB', 'GFNXTB'):
        s += '\n$gfn\n   method=1\n'

    elif method.upper() in ('GFN2-XTB', 'GFN2XTB'):
        s += '\n$gfn\n   method=2\n'
    
    s += '\n$end'

    s = ''.join(s)
    with open(f'{title}.inp', 'w') as f:
        f.write(s)
    
    flags = '--opt'
    if method in ('GFN-FF', 'GFNFF'):
        flags += ' --gfnff'

    try:
        check_call(f'xtb --input {title}.inp {title}.xyz {flags} > temp.log 2>&1'.split(), stdout=DEVNULL, stderr=STDOUT)

    except KeyboardInterrupt:
        print('KeyboardInterrupt requested by user. Quitting.')
        quit()

    if read_output:

        try:
            outname = 'xtbopt.xyz'
            opt_coords = ccread(outname).atomcoords[0]
            energy = read_xtb_energy(outname)

            clean_directory()
            os.remove(outname)

            for filename in ('gfnff_topo', 'charges', 'wbo', 'xtbrestart', 'xtbtopo.mol', '.xtboptok'):
                try:
                    os.remove(filename)
                except FileNotFoundError:
                    pass

            return opt_coords, energy, True

        except FileNotFoundError:
            return None, None, False

def read_xtb_energy(filename):
    '''
    returns energy in kcal/mol from an XTB
    .xyz result file (xtbotp.xyz)
    '''
    with open(filename, 'r') as f:
        line = f.readline()
        line = f.readline() # second line is where energy is printed
        return float(line.split()[1]) * 627.5096080305927 # Eh to kcal/mol

def optimize(calculator, TS_structure, TS_atomnos, mols_graphs, constrained_indexes=None, method='PM6', procs=1, max_newbonds=0, title='temp', debug=False):
    '''
    Performs a geometry partial optimization (POPT) with MOPAC, ORCA or Gaussian at $method level, 
    constraining the distance between the specified atom pair. Moreover, performs a check of atomic
    pairs distances to ensure to have preserved molecular identities and prevented atom scrambling.

    :params calculator: Calculator to be used. Either 'MOPAC' or 'ORCA'
    :params TS_structure: list of coordinates for each atom in the TS
    :params TS_atomnos: list of atomic numbers for each atom in the TS
    :params constrained_indexes: indexes of constrained atoms in the TS geometry
    :params mols_graphs: list of molecule.graph objects, containing connectivity information
    :params method: Level of theory to be used in geometry optimization. Default if UFF.

    :return opt_coords: optimized structure
    :return energy: absolute energy of structure, in kcal/mol
    :return not_scrambled: bool, indicating if the optimization shifted up some bonds (except the constrained ones)
    '''
    assert len(TS_structure) == sum([len(graph.nodes) for graph in mols_graphs])

    if constrained_indexes is None:
        constrained_indexes = np.array(())

    if calculator == 'MOPAC':
        opt_coords, energy, success = mopac_opt(TS_structure, TS_atomnos, constrained_indexes, method=method, title=title)

    elif calculator == 'ORCA':
        opt_coords, energy, success = orca_opt(TS_structure, TS_atomnos, constrained_indexes, method=method, procs=procs, title=title)

    elif calculator == 'GAUSSIAN':
        opt_coords, energy, success = gaussian_opt(TS_structure, TS_atomnos, constrained_indexes, method=method, procs=procs, title=title)

    elif calculator == 'XTB':
        opt_coords, energy, success = xtb_opt(TS_structure, TS_atomnos, constrained_indexes, method=method, title=title)


    if success:
        success = scramble_check(opt_coords, TS_atomnos, constrained_indexes, mols_graphs, max_newbonds=max_newbonds)

    return opt_coords, energy, success

def molecule_check(old_coords, new_coords, atomnos, max_newbonds=0):
    '''
    Checks if two molecules have the same bonds between the same atomic indexes
    '''
    old_bonds = {(a, b) for a, b in list(graphize(old_coords, atomnos).edges) if a != b}
    new_bonds = {(a, b) for a, b in list(graphize(new_coords, atomnos).edges) if a != b}

    delta_bonds = (old_bonds | new_bonds) - (old_bonds & new_bonds)

    if len(delta_bonds) > max_newbonds:
        return False

    return True

def scramble_check(TS_structure, TS_atomnos, constrained_indexes, mols_graphs, max_newbonds=0) -> bool:
    '''
    Check if a transition state structure has scrambled during some optimization
    steps. If more than a given number of bonds changed (formed or broke) the
    structure is considered scrambled, and the method returns False.
    '''
    assert len(TS_structure) == sum([len(graph.nodes) for graph in mols_graphs])

    bonds = []
    for i, graph in enumerate(mols_graphs):

        pos = 0
        while i != 0:
            pos += len(mols_graphs[i-1].nodes)
            i -= 1

        for bond in [tuple(sorted((a+pos, b+pos))) for a, b in list(graph.edges) if a != b]:
            bonds.append(bond)

    bonds = set(bonds)
    # creating bond set containing all bonds present in the desired transition state

    new_bonds = {tuple(sorted((a, b))) for a, b in list(graphize(TS_structure, TS_atomnos).edges) if a != b}
    delta_bonds = (bonds | new_bonds) - (bonds & new_bonds)
    delta_bonds -= {tuple(sorted(pair)) for pair in constrained_indexes}
    # removing constrained indexes couples: they are not counted as scrambled bonds

    if len(delta_bonds) > max_newbonds:
        return False

    return True

def dump(filename, images, atomnos):
    with open(filename, 'w') as f:
                for i, image in enumerate(images):
                    coords = image.get_positions()
                    write_xyz(coords, atomnos, f, title=f'{filename[:-4]}_image_{i}')

def ase_adjust_spacings(docker, structure, atomnos, constrained_indexes, title=0, traj=None):
    '''
    docker: TSCoDe docker object
    structure: TS candidate coordinates to be adjusted
    atomnos: 1-d array with element numbering for the TS
    constrained_indexes: (n,2)-shaped array of indexes to be distance constrained
    mols_graphs: list of NetworkX graphs, ordered as the single molecules in the TS
    title: number to be used for referring to this structure in the docker log
    traj: if set to a string, traj+'.traj' is used as a filename for the refinement trajectory.
    '''
    atoms = Atoms(atomnos, positions=structure)

    atoms.calc = get_ase_calc(docker.options.calculator, docker.options.procs, docker.options.theory_level)
    
    springs = []

    for i1, i2 in constrained_indexes:
        pair = tuple(sorted((i1, i2)))
        springs.append(Spring(i1, i2, docker.target_distances[pair]))

    atoms.set_constraint(springs)

    t_start_opt = time.time()
    with LBFGS(atoms, maxstep=0.2, logfile=None, trajectory=traj) as opt:
        opt.run(fmax=0.05, steps=500)
        iterations = opt.nsteps

    new_structure = atoms.get_positions()

    success = scramble_check(new_structure, atomnos, constrained_indexes, docker.graphs)
    exit_str = 'REFINED' if success else 'SCRAMBLED'

    docker.log(f'    - {docker.options.calculator} {docker.options.theory_level} refinement: Structure {title} {exit_str} ({iterations} iterations, {time_to_string(time.time()-t_start_opt)})', p=False)

    return new_structure, atoms.get_total_energy(), success

def ase_saddle(coords, atomnos, calculator, method, procs=1, title='temp', logfile=None, traj=None, freq=False, maxiterations=200):
    '''
    Runs a first order saddle optimization through the ASE package
    '''
    atoms = Atoms(atomnos, positions=coords)

    atoms.calc = get_ase_calc(calculator, procs, method)
    
    t_start = time.time()
    with HiddenPrints():
        with Sella(atoms,
                   logfile=None,
                   order=1,
                   trajectory=traj) as opt:

            opt.run(fmax=0.05, steps=maxiterations)
            iterations = opt.nsteps

    if logfile is not None:
        t_end_berny = time.time()
        elapsed = t_end_berny - t_start
        exit_str = 'converged' if iterations < maxiterations else 'stopped'
        logfile.write(f'{title} - {exit_str} in {iterations} steps ({time_to_string(elapsed)})\n')

    new_structure = atoms.get_positions()
    energy = atoms.get_total_energy() * 23.06054194532933 #eV to kcal/mol

    if freq:
        vib = Vibrations(atoms, name='temp')
        with HiddenPrints():
            vib.run()
        freqs = vib.get_frequencies()

        if logfile is not None:
            elapsed = time.time() - t_end_berny
            logfile.write(f'{title} - frequency calculation completed ({time_to_string(elapsed)})\n')
        
        return new_structure, energy, freqs

    # if logfile is not None:
    #     logfile.write('\n')

    return new_structure, energy

def ase_neb(docker, reagents, products, atomnos, n_images=6, title='temp', optimizer=LBFGS, logfile=None):
    '''
    docker: tscode docker object
    reagents: coordinates for the atom arrangement to be used as reagents
    products: coordinates for the atom arrangement to be used as products
    atomnos: 1-d array of atomic numbers
    n_images: number of optimized images connecting reag/prods
    title: name used to write the final MEP as a .xyz file
    optimizer: ASE optimizer to be used in 
    logfile: filename to dump the optimization data to. If None, no file is written.

    return: 2- element tuple with coodinates of highest point along the MEP and its energy in kcal/mol
    '''

    first = Atoms(atomnos, positions=reagents)
    last = Atoms(atomnos, positions=products)

    images =  [first]
    images += [first.copy() for i in range(n_images)]
    images += [last]

    neb = DyNEB(images, fmax=0.05, climb=False,  method='eb', scale_fmax=1, allow_shared_calculator=True)
    neb.interpolate()

    dump(f'{title}_MEP_guess.xyz', images, atomnos)
    
    neb_method = docker.options.theory_level + (' GEO-OK' if docker.options.calc == 'MOPAC' else '')
    # avoid MOPAC from rejecting structures with atoms too close to each other

    # Set calculators for all images
    for i, image in enumerate(images):
        image.calc = get_ase_calc(docker.options.calculator, docker.options.procs, neb_method)

    # Set the optimizer and optimize
    try:
        with optimizer(neb, maxstep=0.1, logfile=logfile) as opt:

            opt.run(fmax=0.05, steps=20)
            # some free relaxation before starting to climb

            neb.climb = True
            opt.run(fmax=0.05, steps=500)

    except Exception as e:
        print(f'Stopped NEB for {title}:')
        print(e)

    energies = [image.get_total_energy() for image in images]
    ts_id = energies.index(max(energies))
    # print(f'TS structure is number {ts_id}, energy is {max(energies)}')

    os.remove(f'{title}_MEP_guess.xyz')
    dump(f'{title}_MEP.xyz', images, atomnos)
    # Save the converged MEP (minimum energy path) to an .xyz file


    return images[ts_id].get_positions(), images[ts_id].get_total_energy()

def hyperNEB(docker, coords, atomnos, ids, constrained_indexes, title='temp'):
    '''
    Turn a geometry close to TS to a proper TS by getting
    reagents and products and running a climbing image NEB calculation through ASE.
    '''

    reagents = get_reagent(coords, atomnos, ids, constrained_indexes, method=docker.options.theory_level)
    products = get_product(coords, atomnos, ids, constrained_indexes, method=docker.options.theory_level)
    # get reagents and products for this reaction

    reagents -= np.mean(reagents, axis=0)
    products -= np.mean(products, axis=0)
    # centering both structures on the centroid of reactive atoms

    aligment_rotation = R.align_vectors(reagents, products)
    products = np.array([aligment_rotation @ v for v in products])
    # rotating the two structures to minimize differences

    ts_coords, ts_energy = ase_neb(docker, reagents, products, atomnos, title=title)
    # Use these structures plus the TS guess to run a NEB calculation through ASE

    return ts_coords, ts_energy

def get_product(coords, atomnos, ids, constrained_indexes, method='PM7'):
    '''
    Part of the automatic NEB implementation.
    Returns a structure that presumably is the association reaction product
    ([cyclo]additions reactions in mind)
    '''

    bond_factor = 1.2
    # multiple of sum of covalent radii for two atoms.
    # If two atoms are closer than this times their sum
    # of c_radii, they are considered to converge to
    # products when their geometry is optimized. 

    step_size = 0.1
    # in Angstroms

    if len(ids) == 2:

        mol1_center = np.mean([coords[a] for a, _ in constrained_indexes], axis=0)
        mol2_center = np.mean([coords[b] for _, b in constrained_indexes], axis=0)
        motion = norm(mol2_center - mol1_center)
        # norm of the motion that, when applied to mol1,
        # superimposes its reactive atoms to the ones of mol2

        threshold_dists = [bond_factor*(pt[atomnos[a]].covalent_radius +
                                        pt[atomnos[b]].covalent_radius) for a, b in constrained_indexes]

        reactive_dists = [np.linalg.norm(coords[a] - coords[b]) for a, b in constrained_indexes]
        # distances between reactive atoms

        while not np.all([reactive_dists[i] < threshold_dists[i] for i in range(len(constrained_indexes))]):
            # print('Reactive distances are', reactive_dists)

            coords[:ids[0]] += motion*step_size

            coords, _, _ = mopac_opt(coords, atomnos, constrained_indexes, method=method)

            reactive_dists = [np.linalg.norm(coords[a] - coords[b]) for a, b in constrained_indexes]

        newcoords, _, _ = mopac_opt(coords, atomnos, method=method)
        # finally, when structures are close enough, do a free optimization to get the reaction product

        new_reactive_dists = [np.linalg.norm(newcoords[a] - newcoords[b]) for a, b in constrained_indexes]

        if np.all([new_reactive_dists[i] < threshold_dists[i] for i in range(len(constrained_indexes))]):
        # return the freely optimized structure only if the reagents did not repel each other
        # during the optimization, otherwise return the last coords, where partners were close
            return newcoords

        return coords

    else:
    # trimolecular TSs: the approach is to bring the first pair of reactive
    # atoms closer until optimization bounds the molecules together

        index_to_be_moved = constrained_indexes[0,0]
        reference = constrained_indexes[0,1]
        moving_molecule_index = next(i for i,n in enumerate(np.cumsum(ids)) if index_to_be_moved < n)
        bounds = [0] + [n+1 for n in np.cumsum(ids)]
        moving_molecule_slice = slice(bounds[moving_molecule_index], bounds[moving_molecule_index+1])
        threshold_dist = bond_factor*(pt[atomnos[constrained_indexes[0,0]]].covalent_radius +
                                      pt[atomnos[constrained_indexes[0,1]]].covalent_radius)

        motion = (coords[reference] - coords[index_to_be_moved])
        # vector from the atom to be moved to the target reactive atom

        while np.linalg.norm(motion) > threshold_dist:
        # check if the reactive atoms are sufficiently close to converge to products

            for i, atom in enumerate(coords[moving_molecule_slice]):
                dist = np.linalg.norm(atom - coords[index_to_be_moved])
                # for any atom in the molecule, distance from the reactive atom

                atom_step = step_size*np.exp(-0.5*dist)
                coords[moving_molecule_slice][i] += norm(motion)*atom_step
                # the more they are close, the more they are moved

            # print('Reactive dist -', np.linalg.norm(motion))
            coords, _, _ = mopac_opt(coords, atomnos, constrained_indexes, method=method)
            # when all atoms are moved, optimize the geometry with the previous constraints

            motion = (coords[reference] - coords[index_to_be_moved])

        newcoords, _, _ = mopac_opt(coords, atomnos, method=method)
        # finally, when structures are close enough, do a free optimization to get the reaction product

        new_reactive_dist = np.linalg.norm(newcoords[constrained_indexes[0,0]] - newcoords[constrained_indexes[0,0]])

        if new_reactive_dist < threshold_dist:
        # return the freely optimized structure only if the reagents did not repel each other
        # during the optimization, otherwise return the last coords, where partners were close
            return newcoords

        return coords

def get_reagent(coords, atomnos, ids, constrained_indexes, method='PM7'):
    '''
    Part of the automatic NEB implementation.
    Returns a structure that presumably is the association reaction reagent.
    ([cyclo]additions reactions in mind)
    '''

    bond_factor = 1.5
    # multiple of sum of covalent radii for two atoms.
    # Putting reactive atoms at this times their bonding
    # distance and performing a constrained optimization
    # is the way to get a good guess for reagents structure. 

    if len(ids) == 2:

        mol1_center = np.mean([coords[a] for a, _ in constrained_indexes], axis=0)
        mol2_center = np.mean([coords[b] for _, b in constrained_indexes], axis=0)
        motion = norm(mol2_center - mol1_center)
        # norm of the motion that, when applied to mol1,
        # superimposes its reactive centers to the ones of mol2

        threshold_dists = [bond_factor*(pt[atomnos[a]].covalent_radius + pt[atomnos[b]].covalent_radius) for a, b in constrained_indexes]

        reactive_dists = [np.linalg.norm(coords[a] - coords[b]) for a, b in constrained_indexes]
        # distances between reactive atoms

        coords[:ids[0]] -= norm(motion)*(np.mean(threshold_dists) - np.mean(reactive_dists))
        # move reactive atoms away from each other just enough

        coords, _, _ = mopac_opt(coords, atomnos, constrained_indexes=constrained_indexes, method=method)
        # optimize the structure but keeping the reactive atoms distanced

        return coords

    # trimolecular TSs: the approach is to bring the first pair of reactive
    # atoms apart just enough to get a good approximation for reagents

    index_to_be_moved = constrained_indexes[0,0]
    reference = constrained_indexes[0,1]
    moving_molecule_index = next(i for i,n in enumerate(np.cumsum(ids)) if index_to_be_moved < n)
    bounds = [0] + [n+1 for n in np.cumsum(ids)]
    moving_molecule_slice = slice(bounds[moving_molecule_index], bounds[moving_molecule_index+1])
    threshold_dist = bond_factor*(pt[atomnos[constrained_indexes[0,0]]].covalent_radius +
                                    pt[atomnos[constrained_indexes[0,1]]].covalent_radius)

    motion = (coords[reference] - coords[index_to_be_moved])
    # vector from the atom to be moved to the target reactive atom

    displacement = norm(motion)*(threshold_dist-np.linalg.norm(motion))
    # vector to be applied to the reactive atom to push it far just enough

    for i, atom in enumerate(coords[moving_molecule_slice]):
        dist = np.linalg.norm(atom - coords[index_to_be_moved])
        # for any atom in the molecule, distance from the reactive atom

        coords[moving_molecule_slice][i] -= displacement*np.exp(-0.5*dist)
        # the closer they are to the reactive atom, the further they are moved

    coords, _, _ = mopac_opt(coords, atomnos, constrained_indexes=np.array([constrained_indexes[0]]), method=method)
    # when all atoms are moved, optimize the geometry with only the first of the previous constraints

    newcoords, _, _ = mopac_opt(coords, atomnos, method=method)
    # finally, when structures are close enough, do a free optimization to get the reaction product

    new_reactive_dist = np.linalg.norm(newcoords[constrained_indexes[0,0]] - newcoords[constrained_indexes[0,0]])

    if new_reactive_dist > threshold_dist:
    # return the freely optimized structure only if the reagents did not approached back each other
    # during the optimization, otherwise return the last coords, where partners were further away
        return newcoords
    
    return coords

def get_nci(coords, atomnos, constrained_indexes, ids):
    '''
    Returns a list of guesses for intermolecular non-covalent
    interactions between molecular fragments/atoms. Used to get
    a hint of the most prominent NCIs that drive stereo/regio selectivity.
    '''
    nci = []
    print_list = []
    cum_ids = np.cumsum(ids)
    symbols = [pt[i].symbol for i in atomnos]
    constrained_indexes = constrained_indexes.ravel()

    for i1 in range(len(coords)):
    # check atomic pairs (O-H, N-H, ...)

            start_of_next_mol = cum_ids[next(i for i,n in enumerate(np.cumsum(ids)) if i1 < n)]
            # ensures that we are only taking into account intermolecular NCIs

            for i2 in range(len(coords[start_of_next_mol:])):
                i2 += start_of_next_mol

                if i1 not in constrained_indexes:
                    if i2 not in constrained_indexes:
                    # ignore atoms involved in constraints

                        s = ''.join(sorted([symbols[i1], symbols[i2]]))
                        # print(f'Checking pair {i1}/{i2}')

                        if s in nci_dict:
                            threshold, nci_type = nci_dict[s]
                            dist = np.linalg.norm(coords[i1]-coords[i2])

                            if dist < threshold:

                                print_list.append(nci_type + f' ({round(dist, 2)} A, indexes {i1}/{i2})')
                                # string to be printed in log

                                nci.append((nci_type, i1, i2))
                                # tuple to be used in identifying the NCI

    # checking group contributions (aromatic rings)

    aromatic_centers = []
    masks = []

    for mol in range(len(ids)):

        if mol == 0:
            mol_mask = slice(0, cum_ids[0])
            filler = 0
        else:
            mol_mask = slice(cum_ids[mol-1], cum_ids[mol])
            filler = cum_ids[mol-1]

        aromatics_indexes = np.array([i+filler for i, s in enumerate(symbols[mol_mask]) if s in ('C','N')])

        if len(aromatics_indexes) > 5:
        # only check for phenyls in molecules with more than 5 C/N atoms

            masks.append(list(it.combinations(aromatics_indexes, 6)))
            # all possible combinations of picking 6 C/N/O atoms from this molecule

    if len(masks) > 0:

        masks = np.concatenate(masks)

        for mask in masks:

            phenyl, center = is_phenyl(coords[mask])
            if phenyl:
                owner = next(i for i,n in enumerate(np.cumsum(ids)) if np.all(mask < n))
                # index of the molecule that owns that phenyl ring

                aromatic_centers.append((owner, center))

    # print(f'structure has {len(aromatic_centers)} phenyl rings')

    # checking phenyl-atom pairs
    for owner, center in aromatic_centers:
        for i, atom in enumerate(coords):

            if i < cum_ids[0]:
                atom_owner = 0
            else:
                atom_owner = next(i for i,n in enumerate(np.cumsum(ids)) if i < n)

            if atom_owner != owner:
            # if this atom belongs to a molecule different than the one that owns the phenyl

                s = ''.join(sorted(['Ph', symbols[i]]))
                if s in nci_dict:

                    threshold, nci_type = nci_dict[s]
                    dist = np.linalg.norm(center - atom)

                    if dist < threshold:

                        print_list.append(nci_type + f' ({round(dist, 2)} A, atom {i}/ring)')
                        # string to be printed in log

                        nci.append((nci_type, i, 'ring'))
                        # tuple to be used in identifying the NCI

    # checking phenyl-phenyl pairs
    for i, owner_center in enumerate(aromatic_centers):
        owner1, center1 = owner_center
        for owner2, center2 in aromatic_centers[i+1:]:
            if owner1 != owner2:
            # if this atom belongs to a molecule different than owner

                    threshold, nci_type = nci_dict['PhPh']
                    dist = np.linalg.norm(center1 - center2)

                    if dist < threshold:

                        print_list.append(nci_type + f' ({round(dist, 2)} A, ring/ring)')
                        # string to be printed in log

                        nci.append((nci_type, 'ring', 'ring'))
                        # tuple to be used in identifying the NCI

               

    return nci, print_list

def is_phenyl(coords):
    '''
    :params coords: six coordinates of C/N atoms
    :return tuple: bool indicating if the six atoms look like part of a
                   phenyl/naphtyl/pyridine system, coordinates for the center of that ring

    NOTE: quinones would show as aromatic: it is okay, since they can do π-stacking as well.
    '''
    for i, p in enumerate(coords):
        mask = np.array([True if j != i else False for j in range(6)], dtype=bool)
        others = coords[mask]
        if not max(np.linalg.norm(p-others, axis=1)) < 3:
            return False, None
    # if any atomic couple is more than 3 A away from each other, this is not a Ph

    threshold_delta = 1 - np.cos(10 * np.pi/180)
    flat_delta = 1 - np.abs(np.cos(dihedral(coords[[0,1,2,3]]) * np.pi/180))

    if flat_delta < threshold_delta:
        flat_delta = 1 - np.abs(np.cos(dihedral(coords[[0,1,2,3]]) * np.pi/180))
        if flat_delta < threshold_delta:
            # print('phenyl center at', np.mean(coords, axis=0))
            return True, np.mean(coords, axis=0)
    
    return False, None

class OrbitalSpring:
    '''
    ASE Custom Constraint Class
    Adds a series of forces based on a pair of orbitals, that is
    virtual points "bonded" to a given atom.

    :params i1, i2: indexes of reactive atoms
    :params orb1, orb2: 3D coordinates of orbitals
    :params neighbors_of_1, neighbors_of_2: lists of indexes for atoms bonded to i1/i2
    :params d_eq: equilibrium target distance between orbital centers
    '''
    def __init__(self, i1, i2, orb1, orb2, neighbors_of_1, neighbors_of_2, d_eq, k=1000):
        self.i1, self.i2 = i1, i2
        self.orb1, self.orb2 = orb1, orb2
        self.neighbors_of_1, self.neighbors_of_2 = neighbors_of_1, neighbors_of_2
        self.d_eq = d_eq
        self.k = k

    def adjust_positions(self, atoms, newpositions):
        pass

    def adjust_forces(self, atoms, forces):

        # First, assess if we have to move atoms 1 and 2 at all

        sum_of_distances = (np.linalg.norm(atoms.positions[self.i1] - self.orb1) +
                            np.linalg.norm(atoms.positions[self.i2] - self.orb2) + self.d_eq)

        reactive_atoms_distance = np.linalg.norm(atoms.positions[self.i1] - atoms.positions[self.i2])

        orb_direction = self.orb2 - self.orb1
        # vector connecting orb1 to orb2

        spring_force = self.k * (np.linalg.norm(orb_direction) - self.d_eq)
        # absolute spring force (float). Positive if spring is overstretched.

        # spring_force = np.clip(spring_force, -50, 50)
        # # force is clipped at 5 eV/A

        force_direction1 = np.sign(spring_force) * norm(np.mean((norm(+orb_direction),
                                                                    norm(self.orb1-atoms.positions[self.i1])), axis=0))

        force_direction2 = np.sign(spring_force) * norm(np.mean((norm(-orb_direction),
                                                                    norm(self.orb2-atoms.positions[self.i2])), axis=0))

        # versors specifying the direction at which forces act, that is on the
        # bisector of the angle between vector connecting atom to orbital and
        # vector connecting the two orbitals

        if np.abs(sum_of_distances - reactive_atoms_distance) > 0.2:

            forces[self.i1] += (force_direction1 * spring_force)
            forces[self.i2] += (force_direction2 * spring_force)
            # applying harmonic force to each atom, directed toward the other one

        # Now applying to neighbors the force derived by torque, scaled to match the spring_force,
        # but only if atomic orbitals are more than two Angstroms apart. This improves convergence.

        if np.linalg.norm(orb_direction) > 2:
            torque1 = np.cross(self.orb1 - atoms.positions[self.i1], force_direction1)
            for i in self.neighbors_of_1:
                forces[i] += norm(np.cross(torque1, atoms.positions[i] - atoms.positions[self.i1])) * spring_force

            torque2 = np.cross(self.orb2 - atoms.positions[self.i2], force_direction2)
            for i in self.neighbors_of_2:
                forces[i] += norm(np.cross(torque2, atoms.positions[i] - atoms.positions[self.i2])) * spring_force

def PreventScramblingConstraint(graph, atoms, double_bond_protection=False, fix_angles=False):
    '''
    graph: NetworkX graph of the molecule
    atoms: ASE atoms object

    return: FixInternals constraint to apply to ASE calculations
    '''
    angles_deg = None
    if fix_angles:
        allpaths = []

        for node in graph:
            allpaths.extend(findPaths(graph, node, 2))

        allpaths = {tuple(sorted(path)) for path in allpaths}

        angles_deg = []
        for path in allpaths:
            angles_deg.append([atoms.get_angle(*path), list(path)])

    bonds = []
    for bond in [[a, b] for a, b in graph.edges if a != b]:
        bonds.append([atoms.get_distance(*bond), bond])

    dihedrals_deg = None
    if double_bond_protection:
        double_bonds = get_double_bonds_indexes(atoms.positions, atoms.get_atomic_numbers())
        if double_bonds != []:
            dihedrals_deg = []
            for a, b in double_bonds:
                n_a = neighbors(graph, a)
                n_a.remove(b)

                n_b = neighbors(graph, b)
                n_b.remove(a)

                d = [n_a[0], a, b, n_b[0]]
                dihedrals_deg.append([atoms.get_dihedral(*d), d])

    return FixInternals(dihedrals_deg=dihedrals_deg, angles_deg=angles_deg, bonds=bonds, epsilon=1)

def ase_bend(docker, original_mol, pivot, threshold, title='temp', traj=None, check=True):
    '''
    docker: TSCoDe docker object
    original_mol: Hypermolecule object to be bent
    pivot: pivot connecting two Hypermolecule orbitals to be approached/distanced
    threshold: target distance for the specified pivot, in Angstroms
    title: name to be used for referring to this structure in the docker log
    traj: if set to a string, traj+'.traj' is used as a filename for the bending trajectory.
          not only the atoms will be printed, but also all the orbitals and the active pivot.
    check: if True, after bending checks that the bent structure did not scramble.
           If it did, returns the initial molecule.
    '''

    identifier = np.sum(original_mol.atomcoords[0])

    if hasattr(docker, "ase_bent_mols_dict"):
        try:
            return docker.ase_bent_mols_dict[(identifier, tuple(sorted(pivot.index)), round(threshold, 3))]
        except KeyError:
            # ignore structure cacheing if we do not already have this structure 
            pass

    if traj is not None:

        from ase.io.trajectory import Trajectory

        def orbitalized(atoms, orbitals, pivot=None):
            positions = np.concatenate((atoms.positions, orbitals))

            if pivot is not None:
                positions = np.concatenate((positions, [pivot.start], [pivot.end]))

            symbols = list(atoms.numbers) + [0 for _ in range(len(orbitals))]

            if pivot is not None:
                symbols += [9 for _ in range(2)]
            # Fluorine (9) represents active orbitals
    
            new_atoms = Atoms(symbols, positions=positions)
            return new_atoms

        try:
            os.remove(traj)
        except FileNotFoundError:
            pass

    i1, i2 = original_mol.reactive_indexes

    neighbors_of_1 = list([(a, b) for a, b in original_mol.graph.adjacency()][i1][1].keys())
    neighbors_of_1.remove(i1)

    neighbors_of_2 = list([(a, b) for a, b in original_mol.graph.adjacency()][i2][1].keys())
    neighbors_of_2.remove(i2)

    mols = [deepcopy(original_mol) for _ in range(len(original_mol.atomcoords))]
    for m, mol in enumerate(mols):
        mol.atomcoords = np.array([mol.atomcoords[m]])

    final_mol = deepcopy(original_mol)

    for conf, mol in enumerate(mols):

        for p in mol.pivots:
            if p.index == pivot.index:
                active_pivot = p
                break
        
        dist = np.linalg.norm(active_pivot.pivot)

        atoms = Atoms(mol.atomnos, positions=mol.atomcoords[0])

        atoms.calc = get_ase_calc(docker.options.calculator, docker.options.procs, docker.options.theory_level)
        
        if traj is not None:
            traj_obj = Trajectory(traj + f'_conf{conf}.traj', mode='a', atoms=orbitalized(atoms, np.vstack([atom.center for atom in mol.reactive_atoms_classes_dict.values()]), active_pivot))
            traj_obj.write()

        unproductive_iterations = 0
        break_reason = 'MAX ITER'
        t_start = time.time()

        for iteration in range(500):

            atoms.positions = mol.atomcoords[0]

            orb_memo = {index:np.linalg.norm(atom.center[0]-atom.coord) for index, atom in mol.reactive_atoms_classes_dict.items()}

            orb1, orb2 = active_pivot.start, active_pivot.end

            c1 = OrbitalSpring(i1, i2, orb1, orb2, neighbors_of_1, neighbors_of_2, d_eq=threshold)

            c2 = PreventScramblingConstraint(mol.graph,
                                             atoms,
                                             double_bond_protection=docker.options.double_bond_protection,
                                             fix_angles=docker.options.fix_angles_in_deformation)

            atoms.set_constraint([
                                  c1,
                                  c2,
                                  ])

            opt = BFGS(atoms, maxstep=0.2, logfile=None, trajectory=None)

            try:
                opt.run(fmax=0.5, steps=1)
            except ValueError:
                # Shake did not converge
                break_reason = 'CRASHED'
                break

            if traj is not None:
                traj_obj.atoms = orbitalized(atoms, np.vstack([atom.center for atom in mol.reactive_atoms_classes_dict.values()]))
                traj_obj.write()

            # check if we are stuck
            if np.max(np.abs(np.linalg.norm(atoms.get_positions() - mol.atomcoords[0], axis=1))) < 0.01:
                unproductive_iterations += 1

                if unproductive_iterations == 10:
                    break_reason = 'STUCK'
                    break

            else:
                unproductive_iterations = 0

            mol.atomcoords[0] = atoms.get_positions()

            # Update orbitals and get temp pivots
            for index, atom in mol.reactive_atoms_classes_dict.items():
                atom.init(mol, index, update=True, orb_dim=orb_memo[index])
                # orbitals positions are calculated based on the conformer we are working on

            temp_pivots = docker._get_pivots(mol)

            for p in temp_pivots:
                if p.index == pivot.index:
                    active_pivot = p
                    break
            # print(active_pivot)

            dist = np.linalg.norm(active_pivot.pivot)
            # print(f'{iteration}. {mol.name} conf {conf}: pivot is {round(dist, 3)} (target {round(threshold, 3)})')

            if dist - threshold < 0.1:
                break_reason = 'CONVERGED'
                break
            # else:
                # print('delta is ', round(dist - threshold, 3))

        docker.log(f'    {title} - conformer {conf} - {break_reason}{" "*(9-len(break_reason))} ({iteration+1}{" "*(3-len(str(iteration+1)))} iterations, {time_to_string(time.time()-t_start)})', p=False)

        if check:
            if not molecule_check(original_mol.atomcoords[conf], mol.atomcoords[0], mol.atomnos, max_newbonds=1):
                mol.atomcoords[0] = original_mol.atomcoords[conf]
            # keep the bent structures only if no scrambling occurred between atoms

        final_mol.atomcoords[conf] = mol.atomcoords[0]

    # Now align the ensembles on the new reactive atoms positions

    reference, *targets = final_mol.atomcoords
    reference = np.array(reference)
    targets = np.array(targets)

    r = reference - np.mean(reference[final_mol.reactive_indexes], axis=0)
    ts = np.array([t - np.mean(t[final_mol.reactive_indexes], axis=0) for t in targets])

    output = []
    output.append(r)
    for target in ts:
        matrix = kabsch(r, target)
        output.append([matrix @ vector for vector in target])

    final_mol.atomcoords = np.array(output)

    # Update orbitals and pivots
    for index, atom in final_mol.reactive_atoms_classes_dict.items():
        atom.init(final_mol, index, update=True, orb_dim=orb_memo[index])

    docker._set_pivots(final_mol)

    # add result to cache (if we have it) so we avoid recomputing it
    if hasattr(docker, "ase_bent_mols_dict"):
        docker.ase_bent_mols_dict[(identifier, tuple(sorted(pivot.index)), round(threshold, 3))] = final_mol

    return final_mol

def get_inertia_moments(coords, atomnos):
    '''
    Returns the diagonal of the diagonalized inertia tensor, that is
    a shape (3,) array with the moments of inertia along the main axes.
    (I_x, I_y and largest I_z last)
    '''

    coords -= center_of_mass(coords, atomnos)
    inertia_moment_matrix = np.zeros((3,3))

    for i in range(3):
        for j in range(3):
            k = kronecker_delta(i,j)
            inertia_moment_matrix[i][j] = np.sum([pt[atomnos[n]].mass*((np.linalg.norm(coords[n])**2)*k - coords[n][i]*coords[n][j]) for n in range(len(atomnos))])

    inertia_moment_matrix = diagonalize(inertia_moment_matrix)

    return np.diag(inertia_moment_matrix)

def prune_enantiomers(structures, atomnos, max_delta=10):
    '''
    Remove duplicate (enantiomeric) structures based on the
    moments of inertia on principal axes. If all three MOI
    are within max_delta from another structure, they are
    classified as enantiomers and therefore only one of them
    is kept.
    '''

    l = len(structures)
    mat = np.zeros((l,l), dtype=int)
    for i in range(l):
        for j in range(i+1,l):
            im_i = get_inertia_moments(structures[i], atomnos)
            im_j = get_inertia_moments(structures[j], atomnos)
            delta = np.abs(im_i - im_j)
            mat[i,j] = 1 if np.all(delta < max_delta) else 0

    where = np.where(mat == 1)
    matches = [(i,j) for i,j in zip(where[0], where[1])]

    g = nx.Graph(matches)

    subgraphs = [g.subgraph(c) for c in nx.connected_components(g)]
    groups = [tuple(graph.nodes) for graph in subgraphs]

    best_of_cluster = [group[0] for group in groups]

    rejects_sets = [set(a) - {b} for a, b in zip(groups, best_of_cluster)]
    rejects = []
    for s in rejects_sets:
        for i in s:
            rejects.append(i)

    mask = np.array([True for _ in range(l)], dtype=bool)
    for i in rejects:
        mask[i] = False

    return structures[mask], mask

def xtb_metadyn_augmentation(coords, atomnos, constrained_indexes=None, new_structures:int=5, title=0, debug=False):
    '''
    Runs a metadynamics simulation (MTD) through
    the XTB program to obtain new conformations.
    The GFN-FF force field is used.
    '''
    with open(f'temp.xyz', 'w') as f:
        write_xyz(coords, atomnos, f, title='temp')

    s = (
        '$md\n'
        '   time=%s\n' % (new_structures) +
        '   step=1\n'
        '   temp=300\n'
        '$end\n'
        '$metadyn\n'
        '   save=%s\n' % (new_structures) +
        '$end'
        )
         
    if constrained_indexes is not None:
        s += '\n$constrain\n'
        for a, b in constrained_indexes:
            s += '   distance: %s, %s, %s\n' % (a+1, b+1, round(np.linalg.norm(coords[a]-coords[b]), 5))

    s = ''.join(s)
    with open(f'temp.inp', 'w') as f:
        f.write(s)

    try:
        check_call(f'xtb --md --input temp.inp temp.xyz --gfnff > Structure{title}_MTD.log 2>&1'.split(), stdout=DEVNULL, stderr=STDOUT)

    except KeyboardInterrupt:
        print('KeyboardInterrupt requested by user. Quitting.')
        quit()

    structures = [coords]
    for n in range(1,new_structures):
        name = 'scoord.'+str(n)
        structures.append(parse_xtb_out(name))
        os.remove(name)

    for filename in ('gfnff_topo', 'xtbmdoc', 'mdrestart'):
        try:
            os.remove(filename)
        except FileNotFoundError:
            pass

    # if debug:
    os.rename('xtb.trj', f'Structure{title}_MTD_traj.xyz')

    # else:
    #     os.remove('xtb.traj')  

    structures = np.array(structures)

    return structures

def parse_xtb_out(filename):
    '''
    '''
    with open(filename, 'r') as f:
        lines = f.readlines()

    coords = np.zeros((len(lines)-3,3))

    for l, line in enumerate(lines[1:-2]):
        coords[l] = line.split()[:-1]

    return coords * 0.529177249 # Bohrs to Angstroms

from settings import OPENBABEL_OPT_BOOL

if OPENBABEL_OPT_BOOL:
    
    from openbabel import openbabel as ob

    def openbabel_opt(structure, atomnos, constrained_indexes, graphs, method='UFF'):
        '''
        return : MM-optimized structure (UFF/MMFF)
        '''

        filename='temp_ob_in.xyz'

        with open(filename, 'w') as f:
            write_xyz(structure, atomnos, f)

        outname = 'temp_ob_out.xyz'

        # Standard openbabel molecule load
        conv = ob.OBConversion()
        conv.SetInAndOutFormats('xyz','xyz')
        mol = ob.OBMol()
        more = conv.ReadFile(mol, filename)
        i = 0

        # Define constraints
        constraints = ob.OBFFConstraints()

        for a, b in constrained_indexes:

            first_atom = mol.GetAtom(int(a+1))
            length = first_atom.GetDistance(int(b+1))

            constraints.AddDistanceConstraint(int(a+1), int(b+1), length)       # Angstroms
            # constraints.AddAngleConstraint(1, 2, 3, 120.0)      # Degrees
            # constraints.AddTorsionConstraint(1, 2, 3, 4, 180.0) # Degrees

        # Setup the force field with the constraints
        forcefield = ob.OBForceField.FindForceField(method)
        forcefield.Setup(mol, constraints)
        forcefield.SetConstraints(constraints)

        # Do a 500 steps conjugate gradient minimization
        # (or less if converges) and save the coordinates to mol.
        forcefield.ConjugateGradients(500)
        forcefield.GetCoordinates(mol)

        # Write the mol to a file
        conv.WriteFile(mol,outname)
        conv.CloseOutFile()

        opt_coords = ccread(outname).atomcoords[0]

        success = scramble_check(opt_coords, atomnos, constrained_indexes, graphs)

        return opt_coords, success