import sys
import pickle

from ase.io import read
from ase.data import atomic_numbers
from seekpath import getpaths

### [1] https://github.com/materialscloud-org/tools-barebone/blob/develop/tools_barebone/structure_importers/__init__.py
### [2] https://github.com/materialscloud-org/tools-seekpath/blob/develop/compute/seekpath_web_module.py

# Utility functions to save and load pickle files

def save_to_pickle(object, path_to_file):
    with open(path_to_file, 'wb') as handle:
        pickle.dump(object, handle, protocol=pickle.HIGHEST_PROTOCOL)


def load_pickle(path_to_file):
    with open(path_to_file, 'rb') as handle:
        return pickle.load(handle)

# Copied from [1]

def get_atomic_numbers(symbols):
    """
    Given a list of symbols, return the corresponding atomic numbers.

    :raise ValueError: if the symbol is not recognized
    """
    retlist = []
    for s in symbols:
        try:
            retlist.append(atomic_numbers[s])
        except KeyError:
            raise ValueError("Unknown symbol '{}'".format(s))
    return retlist

# Copied from [1]

def tuple_from_ase(asestructure):
    """
    Given an ASE structure, return a structure tuple as expected from seekpath

    :param asestructure: a ASE Atoms object

    :return: a structure tuple (cell, positions, numbers) as accepted
        by seekpath.
    """
    atomic_numbers = get_atomic_numbers(asestructure.get_chemical_symbols())
    structure_tuple = (
        asestructure.cell.tolist(),
        asestructure.get_scaled_positions().tolist(),
        atomic_numbers,
    )
    return structure_tuple

# Partially adapted from [2]

def get_pw_kpath(filename):
    """
    Given an ASE readable structure, return a k-path for QE pw.x input

    :param filename: ASE readable structure filename

    :return: k-path string, high-symmetry points.
    """

    asestructure = read(filename)
    tuplestructure = tuple_from_ase(asestructure)

    seek_output = getpaths.get_explicit_k_path_orig_cell(tuplestructure)

    kplines = []
    kplines.append('K_POINTS crystal')
    kplines.append(str(len(seek_output['explicit_kpoints_rel'])))

    for kp in seek_output['explicit_kpoints_rel']:
        kplines.append('{:16.10f} {:16.10f} {:16.10f} 1'.format(*kp))

    return "\n".join(kplines), seek_output['path'], seek_output['explicit_kpoints_labels']

def write_to_files(kplines, path, explicit_labels):
    """ 
    Save data to kpath.dat, path.pkl and explicit_labels.pkl 
    """

    with open('kpath.dat', 'w') as f:
        f.writelines(kplines)

    save_to_pickle(path, 'path.pkl')
    save_to_pickle(explicit_labels, 'explicit_labels.pkl')

if __name__ == '__main__':

    structure_filename = sys.argv[1]

    kplines, path, explicit_labels = get_pw_kpath(structure_filename)

    write_to_files(kplines, path, explicit_labels)
