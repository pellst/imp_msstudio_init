#!/bin/bash
cd /shared

export PYTHONPATH="/shared/anaconda"
export PATH="/shared/anaconda/bin:$PATH"
conda init bash
conda activate
conda --version
# then we can get imp setup
conda config --add channels salilab
#conda install -y imp scikit-learn matplotlib
conda install -c salilab imp=2.11.1=py37hf484d3e_1
conda install -y scikit-learn matplotlib
conda install -y numpy scipy 
#scikit-learn matplotlib