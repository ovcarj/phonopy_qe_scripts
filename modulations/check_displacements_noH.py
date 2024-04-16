import numpy as np
import glob

from ase.io import read
from phonopy.units import Bohr

from ase import Atoms

original_file = 'MPOSCAR-orig'
original = read(original_file)
original_cell = original.cell

original_noH = Atoms([atom for atom in original if atom.symbol != 'H'])
original_noH.set_cell(original_cell)

modulated_files = glob.glob('MPOSCAR-*')
modulated_files.remove(original_file)
modulated_files.sort()

n_atoms = len(original)
n_atoms_noH = len(original_noH)

for i, modulated_file in enumerate(modulated_files):

    displacements = np.zeros(n_atoms)
    displacements_noH = np.zeros(n_atoms_noH)

    modulated = read(modulated_file)
    combined = original + modulated

    combined_cell = combined.cell

    combined_noH = Atoms([atom for atom in combined if atom.symbol != 'H'])
    combined_noH.set_cell(combined_cell) 
    combined_noH.pbc=True

    all_distances = combined.get_all_distances(mic=True)
    all_distances_noH = combined_noH.get_all_distances(mic=True)

    for j in range(n_atoms):

            distance = all_distances[j][j + n_atoms]
            displacements[j] = distance
            
    for j in range(n_atoms_noH):

            distance_noH = all_distances_noH[j][j + n_atoms_noH]
            displacements_noH[j] = distance_noH

    average = np.average(displacements)
    maximum = np.max(displacements)

    average_noH = np.average(displacements_noH)
    maximum_noH = np.max(displacements_noH)

    print(f'Average displacement in {modulated_file} is')
    print(f'{average} Angstrom')
    print(f'{average / Bohr} Bohr')

    print(f'Maximum displacement in {modulated_file} is')
    print(f'{maximum} Angstrom')

    print('/////////')

    print(f'Average displacement in {modulated_file}, disregarding H is')
    print(f'{average_noH} Angstrom')
    print(f'{average_noH / Bohr} Bohr')

    print(f'Maximum displacement in {modulated_file}, disregarding H is')
    print(f'{maximum_noH} Angstrom')

    print('------------')
    print('------------')

