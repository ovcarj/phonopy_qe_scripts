Scripts for Phonopy with QE
===========================

Some useful scripts for preparing, running and postprocessing Phonopy calculations using Quantum ESPRESSO on a cluster running Slurm.

**Get FORCE_SETS**

First create a ``header.in`` file from ``pwscf.in``. Then:

.. code:: shell

  # Create displaced structures (modify command below as needed)
  phonopy --qe -d --dim="1 1 1" -c pwscf.in

  # Prepare and run SCF calculations
  bash run_scfs.sh

  # Get FORCE_SETS
  python make_fs_command.py > fs_command.sh
  bash fs_command.sh

**Create modulations along eigenvectors**

Eigenvectors at ``q = (0, 0, 0)`` may be printed to ``qpoints.yaml`` using 

.. code:: shell

    phonopy qpoints.conf

Modulations of the original structure along phonon eigenvectors may be created using:

.. code:: shell

    phonopy modulation.conf

as decribed in the Phonopy documentation. To calculate the amplitudes of modulations in Bohr, such that the average displacement of the atoms in a modulation is equal to ``avg_displacement``, use

.. code:: shell

    python calculate_amplitudes.py <avg_displacement> <band indices>

The unit cell vectors in the resulting ``MPOSCAR-*`` files have incorrect units (Phonopy v2.21.2). This is fixed by:

.. code:: shell

    python fix_MPOSCAR.py

The average displacement in ``MPOSCAR-*`` files may be checked by (requires ASE):

.. code:: shell

    python check_displacements.py

**Band structures and other calculations**

To create a k-point path for ``pw.x`` using SeeK-path from an ASE readable structure, use

.. code:: shell

    python get_pw_kpath.py <structure_filename>

The results will be stored in ``kpoints.dat``, ``path.pkl`` and ``explicit_labels.pkl``.
To create the ``ATOMIC COORDINATES`` and ``CELL PARAMETERS`` cards for ``pw.x`` from an ASE readable structure, use

.. code:: shell

    python get_pw_structure.py <structure_filename>

The results will be stored in ``structure_pw.dat``.

The previous two scripts are used to create all inputs for an electronic band structure and PDOS calculations at once:

.. code:: shell

    bash create_qe_inputs.sh <structure_filename>

which requires a ``header_pw.in`` file.

``create_qe_inputs.sh`` can be run in batch (for multiple structures) using:

.. code:: shell

    bash create_batch_qe_inputs.sh

The structure filenames are searched for using the ``structure_names`` variable defined in ``create_batch_qe_inputs.sh``. Inputs for the calculations are created in ``batch_$structure_filename`` directories.

A batch of calculations may be run using:

.. code:: shell

    bash batch_sub.sh <submission script filename>

``batch_sub.sh`` will enter each subdirectory of current directory named ``batch_*`` and run ``sbatch <submission script filename``.
