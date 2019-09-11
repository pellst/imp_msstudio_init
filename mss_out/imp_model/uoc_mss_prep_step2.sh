#!/bin/bash
cd /home/$USER/scratch
#From the scratch folder on Cedar:
# get latest anaconda and then run install step
#curl -O https://repo.anaconda.com/archive/Anaconda3-2019.03-Linux-x86_64.sh
curl -O https://repo.anaconda.com/archive/Anaconda3-2019.07-Linux-x86_64.sh
bash Anaconda3-2019.03-Linux-x86_64.sh -b -p /home/$USER/scratch/anaconda 
rm -rf /home/$USER/scratch/Anaconda3-2019.03-Linux-x86_64.sh
export PYTHONPATH="/home/$USER/scratch/anaconda"
export PATH="/home/$USER/scratch/anaconda/bin:$PATH"
conda init bash
conda activate
conda --version