#!/bin/bash
sudo su -
cd /tmp
#From the scatch folder on Ceder:
# get latest anaconda and then run install step
curl -O https://repo.anaconda.com/archive/Anaconda3-2019.03-Linux-x86_64.sh
sudo bash Anaconda3-2019.03-Linux-x86_64.sh -b -p /tmp/anaconda 
sudo rm -rf /tmp/Anaconda3-2019.03-Linux-x86_64.sh
export PYTHONPATH="/tmp/anaconda"
export PATH="/tmp/anaconda/bin:$PATH"
conda init bash
conda activate
conda --version