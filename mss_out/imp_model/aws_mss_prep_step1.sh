#aws_mss_prep_step1.sh
#!/bin/bash
# from the /shared
#sudo su -
cd /shared
mkdir imp
cd imp
# get the demo imp job to test a job run
curl -LOk https://github.com/pellst/imp_msstudio_init/archive/master.zip
unzip master.zip
#cd /scratch/imp/imp_msstudio_init-master/driver_imp_mss/imp_model
cd /shared/imp/imp_msstudio_init-master/mss_out/imp_model
cd /shared/imp/imp_msstudio_init-master/mss_out/imp_model
#chmod 755 /shared/imp/imp_msstudio_init-master/mss_out/imp_model/aws_mss_prep_step*
chmod 777 /shared/imp/imp_msstudio_init-master/mss_out/*