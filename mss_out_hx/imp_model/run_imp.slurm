#!/bin/bash
# example slurm job script setup to run on for example UoC ARC
#SBATCH --job-name=SLURM_imp
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=16
#SBATCH --cpus-per-task=1
#SBATCH --mem=32G
#SBATCH --time=00:30:00
#SBATCH --partition=cpu2019




# mpiexec python prep_hyperp_imp_v2ux.py --count=1 --name=DemoImpModel --config=ConfigImp.yaml
srun python prep_hyperp_imp_v2ux.py --count=1 --name=DemoImpModel --config=ConfigImp.yaml

echo "Job Finished"