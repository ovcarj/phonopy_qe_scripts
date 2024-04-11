#!/bin/bash
#SBATCH --partition=partition
#SBATCH --job-name=phonopy_calc
##SBATCH --cpus-per-task=1
##SBATCH --mem=100gb
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=8
#SBATCH --output=%x-%j.out
#SBATCH --error=%x-%j.err
#SBATCH --time=10-00:00:00

module purge
module load QE/6.8

export MKL_CBWR="AVX2"
export I_MPI_FABRICS=shm:ofi
ulimit -s unlimited

mpiexec.hydra -bootstrap slurm pp.x -i pp_charge.in > pp_charge.out

