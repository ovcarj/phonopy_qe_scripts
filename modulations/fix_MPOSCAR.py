import glob
from phonopy.units import Bohr #0.529177207423948

MPOSCAR_files = glob.glob('MPOSCAR*')

for MPOSCAR_file in MPOSCAR_files:

    with open(MPOSCAR_file, 'r') as f:
        lines = f.readlines()

        for i in [2, 3, 4]:

            cell_vector = [float(x) for x in lines[i].split()]
            cell_vector_angstrom = [x * Bohr for x in cell_vector]

            lines[i] = ' '.join(str(x) for x in cell_vector_angstrom)
            lines[i] += '\n'

    with open(MPOSCAR_file, 'w') as f:
        f.writelines(lines)
