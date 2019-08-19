#!/bin/bash
cd /home/tpells/scatch

export PYTHONPATH="/home/tpells/scatch/anaconda"
export PATH="/home/tpells/scatch/anaconda/bin:$PATH"
conda init bash
conda activate
conda --version
# then we can get imp setup
conda config --add channels salilab
conda install -y imp scikit-learn matplotlib
conda install -y numpy scipy 
#scikit-learn matplotlib