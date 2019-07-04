#!/bin/bash
# example slurm job script setup to run on for example Cedar
#SBATCH --job-name=SLURM_imp
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --time=0-00:12:00
#SBATCH --mem=10gb
#SBATCH --account=tbd




python prep_hyperp_imp_v2.py --count=1 --name=DemoImpModel --config=ConfigImp.yaml

echo "Job Finished"