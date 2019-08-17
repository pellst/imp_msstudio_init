#!/bin/bash
#sudo su -
cd /shared
#From the scatch folder on Ceder:
# get latest anaconda and then run install step
curl -O https://repo.anaconda.com/archive/Anaconda3-2019.03-Linux-x86_64.sh
sudo bash Anaconda3-2019.03-Linux-x86_64.sh -b -p /shared/anaconda 
sudo rm -rf /shared/Anaconda3-2019.03-Linux-x86_64.sh
export PYTHONPATH="/shared/anaconda"
export PATH="/shared/anaconda/bin:$PATH"
conda init bash
conda activate
conda --version