#aws_mss_prep_step1.sh
#!/bin/bash
# from the /shared
sudo su -
cd /tmp
mkdir imp
cd imp
# get the demo imp job to test a job run
curl -LOk https://github.com/pellst/imp_msstudio_init/archive/master.zip
unzip master.zip
#cd /scratch/imp/imp_msstudio_init-master/driver_imp_mss/imp_model
cd /tmp/imp/imp_msstudio_init-master/mss_out/imp_model
cd /tmp/imp/imp_msstudio_init-master/mss_out/imp_model
chmod 755 /tmp/imp/imp_msstudio_init-master/mss_out/imp_model/aws_mss_prep_step*