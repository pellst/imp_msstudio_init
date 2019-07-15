#!/bin/bash
#SBATCH --time=0-0:5
#SBATCH --array=1-3
./mjob_run.sh $SLURM_ARRAY_TASK_ID

