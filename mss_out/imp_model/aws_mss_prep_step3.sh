#!/bin/bash
#sudo su -
cd /shared

export PYTHONPATH="/shared/anaconda"
export PATH="/shared/anaconda/bin:$PATH"
conda init bash
conda activate
conda --version
# then we can get imp setup
conda config --add channels salilab
conda install -y imp scikit-learn matplotlib
conda install -y numpy scipy 
#scikit-learn matplotlib