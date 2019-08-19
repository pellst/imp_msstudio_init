#!/bin/bash
cd /home/tpells/scratch
#From the scratch folder on Cedar:
# get latest anaconda and then run install step
curl -O https://repo.anaconda.com/archive/Anaconda3-2019.03-Linux-x86_64.sh
sudo bash Anaconda3-2019.03-Linux-x86_64.sh -b -p /home/tpells/scratch/anaconda 
sudo rm -rf /home/tpells/scratch/Anaconda3-2019.03-Linux-x86_64.sh
export PYTHONPATH="/home/tpells/scratch/anaconda"
export PATH="/home/tpells/scratch/anaconda/bin:$PATH"
conda init bash
conda activate
conda --version