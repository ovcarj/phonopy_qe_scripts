Scripts for Phonopy with QE
===========================

Some useful scripts for preparing, running and postprocessing Phonopy calculations using Quantum ESPRESSO on a cluster running Slurm.

**Get FORCE_SETS**

Inputs for this part are given in ``get_FORCE_SETS``.

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

Inputs for this part are given in ``modulations``.

Eigenvectors at ``q = (0, 0, 0)`` may be printed to ``qpoints.yaml`` using 

.. code:: shell

    phonopy qpoints.conf

Modulations of the original structure along phonon eigenvectors may be created using:

.. code:: shell

    phonopy modulation.conf

as decribed in the Phonopy documentation. To calculate the amplitudes of modulations, such that the average displacement of the atoms in a modulation is equal to ``avg_displacement`` (in Bohr), use

.. code:: shell

    python calculate_amplitudes.py <avg_displacement> <band indices>

The unit cell vectors in the resulting ``MPOSCAR-*`` files have incorrect units (Phonopy v2.21.2). This is fixed by:

.. code:: shell

    python fix_MPOSCAR.py

The average displacement in ``MPOSCAR-*`` files may be checked by (requires ASE):

.. code:: shell

    python check_displacements.py

The same calculation of the modulation amplitudes as described above may be also performed disregarding hydrogen atoms by using ``calculate_amplitudes_noH.py`` and ``check_displacements_noH.py``.

**Create QE calculations**

Inputs for this part are given in ``calculate_qe``.

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

    bash batch_sub.sh <submission_script_filename>

``batch_sub.sh`` will enter each subdirectory of current directory named ``batch_*`` and run ``sbatch <submission_script_filename>``.

**Postprocess QE calculations**

Inputs for this part are given in ``postprocess_qe`` and ``calculate_qe``.

To plot a band structure, use:

.. code:: shell

    python plot_bands.py

The data required for plotting will be parsed from ``pwscf.out``, ``pp_bands.out``, ``explicit_labels.pkl`` and the ``*dat.gnu`` band structure file generated by QE. The image will be saved to ``bands.png`` and all the data required for replotting will be saved to ``bands.pkl``.

A batch of Python calculations may be run using:

.. code:: shell

    bash batch_python.sh <python_script_filename>

``batch_python.sh`` will enter each subdirectory of current directory named ``batch_*`` and run ``python <python_script_filename>``.

The projected density of states (PDOS) for each of the atomic species defined in the ``ATOMIC_SPECIES`` card in ``pwscf.in`` may be calculated using:

.. code:: shell

    source sumpdos.sh

which may also be run in batch using

.. code:: shell

    source batch_bash.sh <bash_script_filename>
