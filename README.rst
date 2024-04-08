Scripts for Phonopy with QE
===========================

Some useful scripts for preparing, running and postprocessing Phonopy calculations using Quantum ESPRESSO on a cluster running Slurm.

**Usage:**

First create a `header.in` file from `pwscf.in`. Then:

.. code:: shell

  # Create displaced structures (modify command below as needed)
  phonopy --qe -d --dim="1 1 1" -c pwscf.in

  # Prepare and run SCF calculations
  bash run_scfs.sh

  # Get FORCE_SETS
  python make_fs_command.py > fs_command.sh
  bash fs_command.sh

