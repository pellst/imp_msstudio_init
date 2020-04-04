#/usr/bin/bash -x
runnum=$1
# pip install awscli --upgrade --user

sudo mkdir /shared/imp/imp_msstudio_init-master/mss_out/imp_model$runnum
cd      /shared/imp/imp_msstudio_init-master/mss_out/imp_model$runnum
sudo cp /shared/imp/imp_msstudio_init-master/mss_out/imp_model/*.* /shared/imp/imp_msstudio_init-master/mss_out/imp_model$runnum
# number of cores on instance determines param for -N 16
nohup /shared/anaconda/bin/mpiexec -N 16 /shared/anaconda/bin/python prep_hyperp_imp_v2ux.py --count=1 --name=DemoImpModel --config=ConfigImp.yaml >/shared/imp/imp_msstudio_init-master/mss_out/imp_model$runnum/trace.log 2>&1 &

# archive
# tar -cvzf imp_model18.tgz /shared/imp/imp_msstudio_init-master/mss_out/imp_model18
# aws s3 cp imp_model18.tgz s3://pcluster-resource
