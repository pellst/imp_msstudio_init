#!/bin/bash
cd /home/$USER/scratch

export PYTHONPATH="/home/$USER/scratch/anaconda"
export PATH="/home/$USER/scratch/anaconda/bin:$PATH"
conda init bash
conda activate
conda --version
# then we can get imp setup
conda config --add channels salilab
#conda install -y imp 
conda install -c salilab imp=2.11.1=py37hf484d3e_1
conda install -y scikit-learn matplotlib
conda install -y numpy scipy 
# avoid this next version with all in one step as it is suspect
#conda install -y imp numpy scipy scikit-learn matplotlib
#scikit-learn matplotlib