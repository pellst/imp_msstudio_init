# on CEDAR

# get the setup script and call it with the correct username as the first arg: 
curl -LOk https://gist.githubusercontent.com/pellst/4853822ea5ca74785af61d0ad39cf84d/raw/uoc_mss_prep_step1.sh
chmod 755 uoc_mss_prep_step1.sh
# run the script uoc_mss_prep_step1.sh in order to get the sample folders setup
uoc_mss_prep_step1.sh tpells


# in the folder scratch/imp/imp_msstudio_init-master/mss_out/imp_model, the following shell scripts are now available

            uoc_mss_prep_step1.sh
            uoc_mss_prep_step2.sh
            uoc_mss_prep_step3.sh
			
# we can continue on to step2 to setup anaconda			
uoc_mss_prep_step2.sh


# once anaconda has been setup we can bring in the imp module and others needed for the job run
uoc_mss_prep_step3.sh

# the next step is to review the following:
# located in scratch/imp/imp_msstudio_init-master/mss_out/imp_model
ConfigImp.yaml
mjob_run_cedar.sh


# amend the sampling_frame in ConfigImp.yaml
sampling_frame: 1000
# the cores is used for the ntasks-per-node=x where x=16 is a good starting point
# performance expectations are that with a single node and 1 cpu per task and 16 tasks per node we can run 20000 sampling_frame in 9 hours

# amend the slurm script settings in mjob_run_cedar.sh
#Runbook info.

#!/bin/bash
# example slurm job script setup to run on for example Cedar
#SBATCH --job-name=SLURM_imp
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=16
#SBATCH --cpus-per-task=1
#SBATCH --mem=32G
#SBATCH --time=0-1:00:00
#SBATCH --account=sponsername 



#in order to run the job we call this and give a unit number to be used for naming the folder that is setup eg: 12 here
./mjob_run_cedar.sh 12

# sbatch run_imp.slurm
# see job run status - initially pending scheduling submission
#squeue -u userannie
#upon completion the slurm-nnnnnnn.out file will contain the trace of the job run
# scancel jobID



#Directory listing of sample and scripts:

\---mss_out
    +---data
    |   +---data
    |   |   \---em
    |   |           Ciferri_CEM_PRC2.map.mrc
    |   |           gmm_file_ouput.txt
    |   |           
    |   +---em
    |   |       Ciferri_CEM_PRC2.map.mrc
    |   |       gmm_file_ouput.txt
    |   |       
    |   +---fasta
    |   |       prc2_pentamer.fasta
    |   |       
    |   +---hx
    |   |       HX_PRC2.csv
    |   |       
    |   +---topo
    |   |       Topology.txt
    |   |       
    |   +---xl
    |   |       PRC2_BS3_protected.csv
    |   |       PRC2_BS3_standard.csv
    |   |       PRC2_BS3_unprotected.csv
    |   |       PRC2_DSS_protected.csv
    |   |       PRC2_DSS_standard.csv
    |   |       PRC2_DSS_unprotected.csv
    |   |       
    |   \---xtal
    |           5hyn_ABC.pdb
    |           AEBP2_HMM_A_107-117.pdb
    |           AEBP2_HMM_A_136-146.pdb
    |           AEBP2_HMM_A_166-175.pdb
    |           AEBP2_HMM_A_229-243.pdb
    |           AEBP2_HMM_A_69-79.pdb
    |           RBBP4-threaded2yb8_SUZ12-fragment.pdb
    |           
    \---imp_model
            array_job.sh
            aws_config_mpi_awsbatch.txt
            aws_mpi_setup_readme.txt
            aws_mss_prep_step1.sh
            aws_mss_prep_step2.sh
            aws_mss_prep_step3.sh
            aws_submit_mpi.sh
            ConfigImp.yaml
            create_gmm.py
            imp_job_run.py
            mjob_run.sh
            mjob_run_cedar.sh
            param.sh
            prep_hyperp_imp_v2.py
            prep_hyperp_imp_v2ux.py
            readme_setup_cedar.txt
            run_imp.slurm
            uoc_mss_prep_step1.sh
            uoc_mss_prep_step2.sh
            uoc_mss_prep_step3.sh
			


#Individual steps performed by shell scripts to setup env and driver script example per the steps given at the beginning of this document"

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
cd /home/userannie/scratch/imp/imp_msstudio_init-master/driver_imp_mss/imp_model


			