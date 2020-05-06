# on AWS













# get the setup script from github gist and review before running: 
curl -LOk https://gist.githubusercontent.com/pellst/4853822ea5ca74785af61d0ad39cf84d/raw/aws_mss_prep_step1.sh
chmod 755 aws_mss_prep_step1.sh
# run the script aws_mss_prep_step1.sh in order to get the sample folders and scripts setup
./aws_mss_prep_step1.sh


# in the folder scratch/$USER/imp/imp_msstudio_init-master/mss_out/imp_model, the following shell scripts are now available

            aws_mss_prep_step1.sh
            aws_mss_prep_step2.sh
            aws_mss_prep_step3.sh
			
# we can continue on to step2 to setup anaconda			
./aws_mss_prep_step2.sh


# once anaconda has been setup we can bring in the imp module (lastest version) and others needed for the job run
./aws_mss_prep_step3.sh

# the next step is to review the following:
# located in scratch/$USER/imp/imp_msstudio_init-master/mss_out/imp_model
ConfigImp.yaml
aws_run_onenode.sh


# amend the sampling_frame in ConfigImp.yaml
sampling_frame: 1000
# the cores is used for the ntasks-per-node=x where x=16 is a good starting point
# performance expectations are that with a single node and 1 cpu per task and 16 tasks per node we can run 20000 sampling_frame in 9 hours

# amend the script settings in aws_run_onenode.sh


#in order to run the job we call this and give a unit number to be used for naming the folder that is setup eg: 12 here
./aws_run_onenode.sh 12


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
            aws_run_onenode.sh
            param.sh
            prep_hyperp_imp_v2.py
            prep_hyperp_imp_v2ux.py
            readme_setup_cedar.txt
            run_imp.slurm
            aws_mss_prep_step1.sh
            aws_mss_prep_step2.sh
            aws_mss_prep_step3.sh
			


#Individual steps performed by shell scripts to setup env and driver script example per the steps given at the beginning of this document"

From the shared folder on AWS:
# get latest anaconda and then run install step
curl -O https://repo.anaconda.com/archive/Anaconda3-2019.03-Linux-x86_64.sh
bash Anaconda3-2019.03-Linux-x86_64.sh -b -p /shared/anaconda 
rm -rf /home/acc_user_name /Anaconda3-2019.03-Linux-x86_64.sh
export PYTHONPATH="/shared/anaconda"
export PATH="/shared/anaconda/bin:$PATH"
conda init bash
conda activate
conda --version

#logout and then log back into Cedar

export PYTHONPATH="/shared/anaconda"
export PATH="/shared/anaconda/bin:$PATH"
conda activate
conda --version

#conda 4.6.11

# then we can get imp setup
conda config --add channels salilab
conda install imp scikit-learn matplotlib
conda install numpy scipy scikit-learn matplotlib

# from the /shared
# this also includes the scripts to use to perform the installation of IMP and Anaconda on Cedar 
mkdir imp
cd imp
# get the demo imp job to test a job run
curl -LOk https://github.com/pellst/imp_msstudio_init/archive/master.zip
unzip master.zip
cd /shared/imp/imp_msstudio_init-master/driver_imp_mss/imp_model


			