#!/bin/bash
cd /home/$USER/scratch

export PYTHONPATH="/home/$USER/scratch/anaconda"
export PATH="/home/$USER/scratch/anaconda/bin:$PATH"
conda init bash
conda activate
conda --version
# then we can get imp setup
conda config --add channels salilab
conda install -y imp scikit-learn matplotlib
conda install -y numpy scipy 
#scikit-learn matplotlib