#!/bin/bash
#uoc_mss_prep_step1.sh
# from the /home/username/scratch
nameuser=$1
echo $nameuser
cd /home/$nameuser/scratch
mkdir imp
cd imp
# get the demo imp job to test a job run
curl -LOk https://github.com/pellst/imp_msstudio_init/archive/master.zip
unzip master.zip
cd /home/$nameuser/scratch/imp/imp_msstudio_init-master/mss_out/imp_model
#chmod 777 /home/$nameuser/scratch/imp/imp_msstudio_init-master/mss_out/*
chmod 755 /home/$nameuser/scratch/imp/imp_msstudio_init-master/mss_out/imp_model/uoc_mss_prep_step*





