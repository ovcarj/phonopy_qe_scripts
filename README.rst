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

The average displacement in ``MPOSCAR-*`` files may be checked by:

.. code:: shell

    python check_displacements.py
