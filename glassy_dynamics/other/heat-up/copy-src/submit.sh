#!/bin/bash
#SBATCH -A e20560          ## account 
#SBATCH -p short
#SBATCH -N 1                ## number of nodes
#SBATCH -n 40                ## number of cores
#SBATCH -t 3:59:00           ## walltime
#SBATCH	--job-name="glassy"    ## name of job
#SBATCH --mem-per-cpu=2G
#SBATCH --constraint="[quest11|quest12|quest13]"

##### These are shell commands. Note that all PBS commands come first.
cd $SLURM_SUBMIT_DIR
module load intel/2011.3
module load mpi/openmpi-1.6.3-gcc-4.6.3
module load lammps
ulimit -s unlimited

mpirun -np 40 /projects/e20560/bin/lmp_mpi -i input.lammps > output.txt
