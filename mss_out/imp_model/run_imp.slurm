#!/bin/bash
# example slurm job script setup to run on for example Cedar
#SBATCH --job-name=SLURM_imp
#SBATCH --nodes=1
#SBATCH --ntasks=4  #number of MPI processes
#SBATCH --mem-per-cpu=1024M
#SBATCH --time=0-00:10:00
#SBATCH --partition=lattice




srun python prep_hyperp_imp_v2ux.py --count=1 --name=DemoImpModel --config=ConfigImp.yaml

echo "Job Finished"
