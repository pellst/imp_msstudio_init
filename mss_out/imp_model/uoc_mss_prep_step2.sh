#!/bin/bash
cd /home/tpells/scatch
#From the scatch folder on Cedar:
# get latest anaconda and then run install step
curl -O https://repo.anaconda.com/archive/Anaconda3-2019.03-Linux-x86_64.sh
sudo bash Anaconda3-2019.03-Linux-x86_64.sh -b -p /home/tpells/scatch/anaconda 
sudo rm -rf /home/tpells/scatch/Anaconda3-2019.03-Linux-x86_64.sh
export PYTHONPATH="/home/tpells/scatch/anaconda"
export PATH="/home/tpells/scatch/anaconda/bin:$PATH"
conda init bash
conda activate
conda --version