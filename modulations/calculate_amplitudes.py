import numpy as np
import sys

avg_displacement = float(sys.argv[1])
band_indices = [index for index in sys.argv[2:]]

masses = []
n_atoms = 0

with open('phonopy.yaml', 'r') as f:

    lines = f.readlines()

    for i, line in enumerate(lines):

        if '- symbol:' in line:

            mass_line = lines[i + 2]
            mass = float(mass_line.split()[1])
            masses.append(mass)

            n_atoms += 1

        if 'reciprocal_lattice:' in line:
            break


eigenvectors = np.empty((len(band_indices), n_atoms, 3))

with open('qpoints.yaml', 'r') as f:

    lines = f.readlines()
    
    for i, line in enumerate(lines):

        if any(f'- # {band_index}\n' in line for band_index in band_indices):

            j = [k for k, band_index in enumerate(band_indices) if f'- # {band_index}' in line][0]

            eigenvector_lines = lines[i + 1 : i + 1 + 4 * n_atoms + 2]

            for n in range(n_atoms):

                start_n = 3 + 4 * n 
                eigenvector_lines_n = eigenvector_lines[start_n : start_n + 3]
                eigenvector = [float(eln.split()[2][:-1]) for eln in eigenvector_lines_n]

                eigenvectors[j][n] = eigenvector


modulation_string = 'MODULATION = 1 1 1, '

for i, band_index in enumerate(band_indices):

    print(f'Band #{band_index}')

    numerator = n_atoms**1.5 * avg_displacement
    denominator = np.sum(np.linalg.norm(eigenvectors[i], axis=1) / np.sqrt(masses))

    amplitude = numerator / denominator

    print(f'Amplitude = {amplitude}')
    print('---------------')

    modulation_string += f'0 0 0 {band_index} {amplitude}, 0 0 0 {band_index} {-amplitude}, '

print("Possible MODULATION tag:")

print(f'{modulation_string[:-2]}')
