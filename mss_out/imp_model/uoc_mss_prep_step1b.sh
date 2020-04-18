#!/bin/bash
#uoc_mss_prep_step1b.sh
# from the /home/username/scratch
nameuser=$USER
echo $nameuser

# todo: add check that $nameuser exists

# following steps are performed by the uoc_mss_prep_step1.sh script and are incl here for INFO only
#mkdir imp
#cd imp
# get the demo imp job to test a job run
#curl -LOk https://github.com/pellst/imp_msstudio_init/archive/master.zip
#unzip master.zip
#cd /home/$nameuser/scratch/imp/imp_msstudio_init-master/mss_out/imp_model
##chmod 777 /home/$nameuser/scratch/imp/imp_msstudio_init-master/mss_out/*
#chmod 755 /home/$nameuser/scratch/imp/imp_msstudio_init-master/mss_out/imp_model/uoc_mss_prep_step*



# anaconda snapshot from ARC
# on arc we put this in $HOME/imp and it adds in $HOME/imp/anaconda
#cd /home/$nameuser/imp


# http only works when this file is made public
##curl -LOk https://pcluster-resource.s3-us-west-2.amazonaws.com/anaconda_arc201907imp12_0.tgz
#aws s3 cp s3://pcluster-resource/anaconda_arc201907imp12_0.tgz .
#tar -xzvf anaconda_arc201907imp12_0.tgz

# on Cedar and Graham we go into /scratch/$USER and therein we add this anaconda snapshot that includes the IMP2.12.0 package.
# anaconda snapshot from Cedar ( works on Graham as well)
##cd /home/$nameuser/scratch
#cd /scratch/$nameuser


# http only works when this file is made public
##curl -LOk https://pcluster-resource.s3-us-west-2.amazonaws.com/cedar_anaconda_imp2_12_0_baselineA.tar.gz
#aws s3 cp s3://pcluster-resource/cedar_anaconda_imp2_12_0_baselineA.tar.gz .
#tar -xzvf cedar_anaconda_imp2_12_0_baselineA.tar.gz








