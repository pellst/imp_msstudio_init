#uoc_mss_prep_step1.sh
#!/bin/bash
# from the /home/tpells/scatch
cd /home/tpells/scatch
mkdir imp
cd imp
# get the demo imp job to test a job run
curl -LOk https://github.com/pellst/imp_msstudio_init/archive/master.zip
unzip master.zip
cd /home/tpells/scatch/imp/imp_msstudio_init-master/mss_out/imp_model
#chmod 777 /home/tpells/scatch/imp/imp_msstudio_init-master/mss_out/*
chmod 755 /home/tpells/scatch/imp/imp_msstudio_init-master/mss_out/imp_model/uoc_mss_prep_step*




