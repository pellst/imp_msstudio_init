#/usr/bin/bash -x
runnum=$1
# pip install awscli --upgrade --user


sudo mkdir /shared/imp/imp_msstudio_init-master/mss_out/imp_model$runnum
sudo chmod 777 /shared/imp/imp_msstudio_init-master/mss_out/imp_model$runnum
cd      /shared/imp/imp_msstudio_init-master/mss_out/imp_model$runnum
sudo cp /shared/imp/imp_msstudio_init-master/mss_out/imp_model/*.* /shared/imp/imp_msstudio_init-master/mss_out/imp_model$runnum

#sudo /shared/anaconda/bin/mpiexec -n 8 /shared/anaconda/bin/python prep_hyperp_imp_v2_14_0ux.py --count=1 --name=DemoImpModel --config=ConfigImp.yaml >/shared/imp/imp_msstudio_init-master/mss_out/imp_model$runnum/trace.log 2>&1

# run imp mpi 
sudo /shared/anaconda/bin/mpiexec -n 8 /shared/anaconda/bin/python prep_hyperp_imp_v2_16_0ux.py --count=1 --name=DemoImpModel --config=ConfigImp.yaml --testing --skipmcrun >/shared/imp/imp_msstudio_init-master/mss_out/imp_model$runnum/trace.log 2>&1

#sudo /home/ec2-user/imp214/imp_release/setup_environment.sh /shared/anaconda/bin/mpiexec -n 4 /shared/anaconda/bin/python prep_hyperp_imp_v2_14_0ux.py --count=1 --name=DemoImpModel --config=ConfigImp.yaml --testing >/shared/imp/imp_msstudio_init-master/mss_out/imp_model$runnum/trace.log 2>&1

# run imp no mpi from source build on rhel8
#sudo /home/ec2-user/imp214/imp_release/setup_environment.sh /shared/anaconda/bin/python prep_hyperp_imp_v2_14_0ux_v2a.py --count=1 --name=DemoImpModel --config=ConfigImp.yaml --testing >/shared/imp/imp_msstudio_init-master/mss_out/imp_model$runnum/trace.log 2>&1


# archive
# tar -cvzf imp_model18.tgz /shared/imp/imp_msstudio_init-master/mss_out/imp_model18
# aws s3 cp imp_model18.tgz s3://pcluster-resource