import shutil
import pickle
import glob
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.ticker as tck

from matplotlib import rcParamsDefault

def load_pickle(path_to_file):

    with open(path_to_file, 'rb') as handle:
        return pickle.load(handle)

def save_to_pickle(object, path_to_file):
    with open(path_to_file, 'wb') as handle:
        pickle.dump(object, handle, protocol=pickle.HIGHEST_PROTOCOL)

def check_for_latex(plt):

    if shutil.which('latex'):

        plt.rcParams.update({
            "text.usetex": True,
            "font.family": 'serif',
            "text.latex.preamble": r'\usepackage{amsmath}'
            })

def get_Fermi_energy(scf_out_filename='pwscf.out'):

    with open(scf_out_filename, 'r') as f:

        lines = f.readlines()

        for line in lines:

            if 'Fermi' in line:
                ef = float(line.split()[-2])

    return ef

def get_number_of_ks(explicit_labels_filename='explicit_labels.pkl'):

    explicit_labels = load_pickle(explicit_labels_filename)

    nk = len(explicit_labels)

    return nk

def load_gnu_data(gnu_data_filename):

    # Get number of k points
    nk = get_number_of_ks()

    data = np.loadtxt(gnu_data_filename)

    k = data[:, 0][0:nk]
    bands = np.reshape(data[:, 1], (-1, len(k)))

    return k, bands

def check_piecewise(kpoints):

    piecewise = False
    k_pieces = []
    pieces_indices = []
    k_piece_np = np.empty(0)
    pieces_indices_np = np.empty(0, dtype='int')
    
    for i, kp in enumerate(k):

        if k[i] == k[i-1]:

            k_pieces.append(k_piece_np)
            pieces_indices.append(pieces_indices_np)
    
            k_piece_np = np.empty(0)
            pieces_indices_np = np.empty(0, dtype='int')
    
            k_piece_np = np.append(k_piece_np, kp)
            pieces_indices_np = np.append(pieces_indices_np, i)
    
        else:

            k_piece_np = np.append(k_piece_np, kp)
            pieces_indices_np = np.append(pieces_indices_np, i)

    if k[-1] != k[-2]:
        k_pieces.append(k_piece_np)
        pieces_indices.append(pieces_indices_np)
    
    if len(k_pieces) != 0:
        piecewise = True

    return piecewise, k_pieces, pieces_indices

def get_high_sym_points(pp_out_filename='pp_bands.out'):

    hsp = []

    with open(pp_out_filename, 'r') as f:

        lines = f.readlines()

        for line in lines:

            if 'high-symmetry point' in line:

                hsp.append(float(line.split()[-1]))

    unique_hsp = list(dict.fromkeys(hsp))

    return unique_hsp

def get_labels(explicit_labels_filename='explicit_labels.pkl'):

    explicit_labels = load_pickle(explicit_labels_filename)

    nonempty_indices = [i for i, label in enumerate(explicit_labels) if label != '']
    nonempty_distances = [nonempty_indices[i+1] - nonempty_indices[i] 
            for i in range(0, len(nonempty_indices) - 1)]
    ones_indices = [nonempty_indices[i] for i, distance in enumerate(nonempty_distances) if distance == 1]

    labels = []

    for i, nonempty_index in enumerate(nonempty_indices):

        if nonempty_index in ones_indices:

            labels.append(f'${explicit_labels[nonempty_index]}|{explicit_labels[nonempty_index+1]}$')

        elif (nonempty_indices[i-1] not in ones_indices):
            
            labels.append(f'${explicit_labels[nonempty_index]}$')

    for i, label in enumerate(labels):

        if 'GAMMA' in label:

            labels[i] = labels[i].replace('GAMMA', '\Gamma')
    
    return labels

def plot_bands(fig, ax, ef, k, bands, piecewise, k_pieces, pieces_indices, high_sym, labels,
        ymin=-0.5, ymax=0.5, colors=['blue', 'green', 'orange']):

    # Plot bands
    for i, band in enumerate(bands):

        band -= ef

        if len(colors) > 1:
            c = colors[i % 3]

        else:
            c = colors

        if piecewise:

            for j, piece in enumerate(k_pieces):

                b = band[pieces_indices[j]]
                ax.plot(k_pieces[j], b, linewidth=1.5, alpha=0.5, color=c)
 
        else:

            ax.plot(k, band, linewidth=1.5, alpha=0.5, color=c)
    
    # Plot limits
    ax.set_xlim(min(k), max(k))
    ax.set_ylim(ymin, ymax)
    
    # Plot Fermi energy
    ax.axhline(0.0, linestyle=(0, (5, 5)), linewidth=1.0, color='k', alpha=0.5)
    
    # High symmetry labels, etc.
    for hs in high_sym:
        ax.axvline(hs, linewidth=0.5, color='k', alpha=0.5)
    
    ax.set_xticks(ticks=high_sym)
    ax.set_xticklabels(labels, fontsize=14)
    ax.xaxis.set_tick_params(bottom=False)
    
    ax.yaxis.set_minor_locator(tck.AutoMinorLocator())
    ax.yaxis.set_tick_params(labelsize=12, direction='in', which='both')
    ax.set_ylabel(r'$E$ (eV)', fontsize=14)
    
    fig.tight_layout()

if __name__ == '__main__':
    
    # Check if LaTeX is installed
    check_for_latex(plt)
    
    # Fermi energy
    ef = get_Fermi_energy()
    
    # Find and load data
    gnu_data_filename = glob.glob('*dat.gnu')[0]
    
    k, bands = load_gnu_data(gnu_data_filename)
    
    # Check if piecewise
    piecewise, k_pieces, pieces_indices = check_piecewise(k)
    
    # Get high-symmetry k-points
    high_sym = get_high_sym_points()
    
    # Get high-symmetry labels
    labels = get_labels()
    
    # Plot
    
    fig, ax = plt.subplots(1, 1, figsize=(8.0, 6.0))
    
    plot_bands(fig, ax, ef, k, bands, piecewise, k_pieces, pieces_indices, high_sym, labels,
            ymin=-0.6, ymax=0.3, colors=['blue', 'green', 'orange'])

    plt.savefig('bands.png', format='png', bbox_inches='tight', dpi=400)

    # Save data to bands.pkl

    data = {
    'ef': ef,
    'k': k,
    'bands': bands,
    'piecewise': piecewise,
    'k_pieces': k_pieces,
    'pieces_indices': pieces_indices,
    'high_sym': high_sym,
    'labels': labels
    }

    save_to_pickle(data, 'bands.pkl')
