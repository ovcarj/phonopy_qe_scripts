import sys
from ase.io import read

def get_pw_structure(filename):

    atoms = read(filename)

    struct_lines = []

    # Positions header

    struct_lines.append('ATOMIC_POSITIONS angstrom\n')

    # Get atom positions

    for atom in atoms:
        symbol = atom.symbol
        x, y, z = atom.position
        index = atom.index
    
        struct_lines.append(f'{symbol} {x} {y} {z}')
        struct_lines.append('\n')

    # Cell header

    struct_lines.append('CELL_PARAMETERS angstrom\n')

    # Write cell

    cell = atoms.get_cell()

    for i in range(3):

        for j in range(3):

            struct_lines.append(f'{str(cell[i][j])} ')

        struct_lines.append('\n')

    return struct_lines

def write_pw_structure(pw_file, struct_lines):

    with open(pw_file, 'w') as f:
        f.writelines(struct_lines)

if __name__ == '__main__':

    structure_filename = sys.argv[1]
    struct_lines = get_pw_structure(structure_filename)
    write_pw_structure('structure_pw.dat', struct_lines)
