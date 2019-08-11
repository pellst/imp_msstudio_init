# readme - aws deployment of parallelCluster and running aws Batch with MPI

# https://docs.aws.amazon.com/parallelcluster/latest/ug/getting_started.html

# https://docs.aws.amazon.com/parallelcluster/latest/ug/tutorials_03_batch_mpi.html
Running an MPI Job with AWS ParallelCluster and awsbatch Scheduler 
This tutorial walks you through running an MPI job with awsbatch as a scheduler. 
If you haven't yet installed AWS ParallelCluster and configured your CLI, follow the instructions in the getting started guide before continuing with this tutorial. Also, make sure to read through the awsbatch networking setup documentation before moving to the next step. 


# An example configuration file is installed with AWS ParallelCluster in the Python directory at site-packages/aws-parallelcluster/examples/config
# The example configuration file is also available on GitHub, at https://github.com/aws/aws-parallelcluster/blob/release/cli/pcluster/examples/config
#  https://docs.aws.amazon.com/parallelcluster/latest/ug/pluster.create.html
#AWS Batch is used only with AWS Batch clusters.
#For more details, see https://aws.amazon.com/batch/. 
# https://docs.aws.amazon.com/parallelcluster/latest/ug/install-windows.html



# make use of AWS CLI interface - setup key pair for CLI admin
# .pem key file must have permissions restricted to prevent general access by others 
# we can run anaconda prompt on a local machine - at the prompt we can setup pcluster
# setup pip and then use pip to setup aws-parallelcluster
# at anaconda prompt:
python -m pip install --upgrade pip
#pip-19.2.1

pip install aws-parallelcluster
#Successfully built aws-parallelcluster
#Installing collected packages: jmespath, botocore, s3transfer, boto3, aws-parallelcluster
#Successfully installed aws-parallelcluster-2.4.1 boto3-1.9.204 botocore-1.12.204 jmespath-0.9.4 s3transfer-0.2.1

# confirm version of aws-parallelcluster installed
pcluster version

#(base) C:\>where pcluster
#eg: C:\apps\Anaconda3\Scripts\pcluster.exe


# setup config for awsbatch template
aws_config_mpi_awsbatch.txt

#prep awsbatch
pcluster create -c aws_config_mpi_awsbatch.txt -t improvmpibat awsbatch-improvmpibat


#login to cluster:
pcluster ssh awsbatch-improvmpibat -i key-demo-my-awsbatch.pem




#aws_mss_prep_step1.sh
#!/bin/bash
# from the /shared
cd /shared
mkdir imp
cd imp
# get the demo imp job to test a job run
curl -LOk https://github.com/pellst/imp_msstudio_init/archive/master.zip
unzip master.zip
cd /shared/imp/imp_msstudio_init-master/mss_out/imp_model

# setup permissions to run the aws_mss_prep_step*.sh scripts
# to setup anaconda run
aws_mss_prep_step2.sh

# to setup imp modeling run
aws_mss_prep_step3.sh

# to run the mpi imp modeling job on aws
awsbsub -jn impjob3 -n 1 -cf submit_mpi.sh
# monitor the job run
watch awsbstat -d 
# look at the job logs with awsbout -s jobNumber


# shutdown when finished with AMI
#pcluster delete -r us-west-2 -nw awsbatch-improvmpibat