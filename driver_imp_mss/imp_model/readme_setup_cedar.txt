# on CEDAR

From the scatch folder on Ceder:
# get latest anaconda and then run install step
curl -O https://repo.anaconda.com/archive/Anaconda3-2019.03-Linux-x86_64.sh
bash Anaconda3-2019.03-Linux-x86_64.sh -b -p /home/userannie/scratch/anaconda 
rm -rf /home/userannie/Anaconda3-2019.03-Linux-x86_64.sh
export PYTHONPATH="/home/userannie/scratch/anaconda"
export PATH="/home/userannie/scratch/anaconda/bin:$PATH"
conda init bash
conda activate
conda --version

#logout and then log back into Cedar

export PYTHONPATH="/home/userannie/scratch/anaconda"
export PATH="/home/userannie/scratch/anaconda/bin:$PATH"
conda activate
conda --version

#conda 4.6.11

# then we can get imp setup
conda config --add channels salilab
conda install imp scikit-learn matplotlib
conda install numpy scipy scikit-learn matplotlib

# from the /home/userannie/scatch
mkdir imp
cd imp
# get the demo imp job to test a job run
curl -LOk https://github.com/pellst/imp_msstudio_init/archive/master.zip
unzip master.zip
cd /home/userannie/scatch/imp/imp_msstudio_init-master/driver_imp_mss/imp_model

sbatch run_imp.slurm
# see job run status - initially pending scheduling submission
squeue -u userannie
#upon completion the slurm-nnnnnnn.out file will contain the trace of the job run