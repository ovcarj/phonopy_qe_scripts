import numpy as np
import glob

from ase.io import read
from phonopy.units import Bohr

original_file = 'MPOSCAR-orig'
original = read(original_file)

modulated_files = glob.glob('MPOSCAR-*')
modulated_files.remove(original_file)
modulated_files.sort()

n_atoms = len(original)

for i, modulated_file in enumerate(modulated_files):

    displacements = np.zeros(n_atoms)

    modulated = read(modulated_file)
    combined = original + modulated

    all_distances = combined.get_all_distances(mic=True)

    for j in range(n_atoms):

            distance = all_distances[j][j + n_atoms]
            displacements[j] = distance

    average = np.average(displacements)
    maximum = np.max(displacements)

    print(f'Average displacement in {modulated_file} is')
    print(f'{average} Angstrom')
    print(f'{average / Bohr} Bohr')

    print(f'Maximum displacement in {modulated_file} is')
    print(f'{maximum} Angstrom')

    print('------------')

