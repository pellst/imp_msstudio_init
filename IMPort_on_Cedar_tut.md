# IMPort ( integrative modeling platform ) - Workflow (0.1)

This tutorial presents the step by step instructions to gather the data files 
and driver scripts needed to perform a MPI based IMP modeling job run. We demonstrate
these steps using the [PRC2 example project](https://integrativemodeling.org/) and explain how this was prepared 
using [MassSpecStudio](https://www.msstudio.ca/mss-improv/). The instructions cover running the job on two platforms:

* AWS: EC2 spot instance
* Compute Canada: Cedar cluster


#### PRC2 example project:  
* view imp_msstudio_init [on github, here.](https://github.com/pellst/imp_msstudio_init/tree/master/mss_out)
* then, download PRC2 example project, [here.](https://github.com/pellst/imp_msstudio_init/archive/master.zip)

Folders and files included in this project:
* **data**
   * em
   * fasta
   * hx
   * topo
   * xl
   * xtal  
* **imp_model**
   * readme_setup_cedar.txt
   * ConfigImp.yaml
   * mjob_run_cedar.sh
   * prep_hyper_imp_v2ux.py
   * ... and others 

The **data** folder contains various artifacts used to inform the integrative modeling.
The **imp_model** folder contains the driver python script and example yaml configuration for running the IMP modeling job.



AWS environment 3D: 
![alt text](https://github.com/pellst/imp_msstudio_init/raw/master/IMPort_MPI_IAAS_Arch_v1.png "Logo Title Text 1")

AWS environment 2D: 
![alt text](https://github.com/pellst/imp_msstudio_init/raw/master/IMPort_MPI_IaaS_Archit2d_v1.png "Logo Title Text 1")

IMPort Job Run: 
![alt text](https://github.com/pellst/imp_msstudio_init/raw/master/IMPort_uml_diag.png "Logo Title Text 1")

MassSpecStudio: 
![alt text][logo]

[logo]: https://github.com/pellst/imp_msstudio_init/raw/master/uml_diag_IMPort_msstudio.png "msstudio IMPort prep"


## Fast Track:
* login to **Cedar** on Compute Canada and run these scripts in your user account
  * steps ...
  * see **Installing** section

* alternatively, login to your **AWS** account and from the Management Console perform these steps to launch an EC2 spot instance using the AMI for IMPort MPI jobs
  * steps ...
  * steps to setup your own AMI, see **Deployment** section
  * steps to launch existing AMI, follow ...

```
Notes:
. figure: flow diagram to illustrate deployment options and environment setup

. code: aws cloudformation yaml and steps to launch

. code: github gist for cli-input-json. Configuration changes needed for security group and based on golden image ami
```

The json file needed to configure the **cli-input-json** typically has the following elements:
(NetworkInterfaces section is optional and may be required when not launching into default VPC )
```
{
    "ImageId": "ami-nnnn your custom ami with anaconda and IMP already installed",
    "InstanceType": "m5.2xlarge",
    "KeyName": "your_security_key",
    "SecurityGroupIds": [
        "sg-nnnn your security group"
    ],
    "SubnetId": "subnet-nnnn your default subnet in US-West2a for example",
    "DisableApiTermination": false,
    "DryRun": false,
    "EbsOptimized": true,
    "IamInstanceProfile": {
        "Name": "s3_imp_rw_only your IAM role with RW access to s3 bucket"
     },
	"NetworkInterfaces": [
        {
            "AssociatePublicIpAddress": true,
            "DeleteOnTermination": true,
            "DeviceIndex": 0			
        }
    ],	
    "InstanceMarketOptions": {
        "MarketType": "spot",
        "SpotOptions": {
            "MaxPrice": "0.70",
            "SpotInstanceType": "one-time",
            "BlockDurationMinutes": 120,
            "InstanceInterruptionBehavior": "terminate"
        }
    }
}



```





```
# aws cli command with the aws cli already configured using aws configure
# launch spot instance and pre-configured AMI via aws CLI:
aws ec2 run-instances --cli-input-json file://C:/dev/aws/aws_parallelcluster/mpi_launch_instance_config_v3b.json

# lookup the public IP address of the launched instance for the EC2 Dashboard
# use putty or MobaXterm to connect via ssh [private key setup required ]

#pre-configured AMI already has the sample project folders
sudo su -
cd /shared/imp/imp_msstudio_init-master/mss_out/imp_model

# pull the driver script from github gist; we also have this in s3
curl -LOk https://gist.githubusercontent.com/pellst/d12ad92371757ec8c873aa11a7d8f1a2/raw/aws_run_onenode.sh

# alt. get the driver script from s3
aws s3 cp s3://pcluster-resource/aws_run_onenode.sh .


# setup to run 200 frames
(base) [root@ip-172-31-25-238 imp_model]# vi ConfigImp.yaml

# add execute permissions to driver script
(base) [root@ip-172-31-25-238 imp_model]# chmod 755 aws_run_onenode.sh

# setup run as run num22
(base) [root@ip-172-31-25-238 imp_model]# ./aws_run_onenode.sh 22

# change to the imp_model22 folder and monitor the trace.log. For 200 frames this should complete in under 10minutes.

# in order to perform a custom modeling run we need only change from the sample location here:
/shared/imp/imp_msstudio_init-master/mss_out/imp_model
# to the folder which contains another modeling run bundle. 
# We can setup the ConfigImp.yaml to run 200 frames and test again with aws_run_onenode.sh

```

**Content of aws_run_onenode.sh**
```
#/usr/bin/bash -x
runnum=$1
# pip install awscli --upgrade --user

sudo mkdir /shared/imp/imp_msstudio_init-master/mss_out/imp_model$runnum
cd      /shared/imp/imp_msstudio_init-master/mss_out/imp_model$runnum
sudo cp /shared/imp/imp_msstudio_init-master/mss_out/imp_model/*.* /shared/imp/imp_msstudio_init-master/mss_out/imp_model$runnum
nohup /shared/anaconda/bin/python prep_hyperp_imp_v2ux.py --count=1 --name=DemoImpModel --config=ConfigImp.yaml >/shared/imp/imp_msstudio_init-master/mss_out/imp_model$runnum/trace.log 2>&1 &

# archive
# tar -cvzf imp_model18.tgz /shared/imp/imp_msstudio_init-master/mss_out/imp_model18
# aws s3 cp imp_model18.tgz s3://pcluster-resource
```



## Getting Started

These instructions will get you a copy of the example project up and running for testing purposes. 
* how to setup new instance with python (3.x) and imp packages, together with sample project for PRC2.
  * initial run for modeling 200 frames ( approx. run duration is 10min ).
  * how to deploy the project on a live system for a short run. 
    * **runbook** for steps to setup software and data/driver scripts.
    * **playbook** for troubleshooting issues.
* clear distinction between platforms used ( Cedar vs AWS ) and steps to follow in each case.
  * for Cedar provide info on job scheduling with slurm and submitting multiple jobs ( clones ) for comparison.
  * for AWS the running of multiple jobs in parallel, requires launching separate instances.
* See **Deployment section** and additional considerations/details for running at scale.
  * in the deployment section provide guidance on running at scale, using the prepared AMI, incl. launching AMI with cloudformation or aws cli or via aws management console.
  * full job run for modeling 20,000 frames ( approx. run duration 10hrs )
  * for AWS, mention parallel-cluster and aws cli launch. Proof of Concept for use of the NFS folder /shared and symbolic link to python and imp
* 

**Cedar job run**

* links to Cedar preparation docs, account setup, login and run setup scripts 
* [Cedar HPC intro, on Compute Canada](https://www.westgrid.ca//support/quickstart/new_users)
* [Cedar login steps](https://docs.computecanada.ca/wiki/Connecting_with_MobaXTerm#Using_a_Key_Pair)
	* On Windows, various options:
	  * [MobaXTerm](https://docs.computecanada.ca/wiki/Connecting_with_MobaXTerm)
	  * [PuTTY](https://docs.computecanada.ca/wiki/Connecting_with_PuTTY)
* see **Installing** section



**AWS job run**

* this requires running EC2 instances that are not eligible for the AWS Free Tier. While pricing varies, the typical cost for a 32cpu machine is under USD1.00 per hour.
* links to AWS account setup, default VPC launch of EC2 instance using either on-demand or spot instance.
* cloudcraft diagram of VPC, subnet, EC2 instance ( 16, 32 cpu options) , pricing ( on-demand, spot )
* cloudformation script
* prep AMI based on parallel-cluster image ( give version num ) - snapshot for golden image
* Amendment of cloudcraft script ( json or yaml style ) add AMI golden image to use
* IAM role for s3 upload of modeling results. 
  * TODO: add scripted copy of modeling output data to s3.
* option to upload a project content to s3 to store the project bundle generated by msstudio.
* 


In order to work with MPI ( message passing interface ) jobs such as this IMP example on AWS, we need to lay the groundwork. 
Use your existing AWS account or [sign up for AWS](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/get-set-up-for-amazon-ec2.html). 
Read the [EC2 Getting Started Guide](http://docs.amazonwebservices.com/AWSEC2/latest/UserGuide/EC2_GetStarted.html?r=1874). 
Familiarize yourself with how to start, access, and terminate different machine instances. 
We make use of on-demand instances for convenience in the preparation of the initial machine image 
as we explain the installation of the pre-requisite software ( on a t2.micro EC2 instance, in the AWS Free Tier).
Running EC2 spot instances is important, thereafter, in order to minimize costs for the testing of the MPI jobs.
AWS has a [research cloud program](https://pages.awscloud.com/rs/112-TZM-766/images/AWS_Research_Cloud_Program_Letter.pdf) which you may consider joining, [here](https://aws.amazon.com/government-education/research-and-technical-computing/research-cloud-program/). 

We make use of a number of shortcuts via scripted steps to facilitate the initial setup and accelerate the deployment processs.
At a later point we expand our explanation and provide further information or links to help fill in the knowledge gaps.

Initial setup assistance provided by the prep_step* shell scripts ( aws ):
```
# make use of this gist to get the prep_step* shell scripts located here
# /shared/imp/imp_msstudio_init-master/mss_out/imp_model
curl -LOk https://gist.githubusercontent.com/pellst/9f7ad519133dae87f8f813b506b45aac/raw/aws_mss_prep_step1.sh 
chmod 755 aws_mss_prep_step1.sh 
./aws_mss_prep_step1.sh

# prepare anaconda install
#/shared/imp/imp_msstudio_init-master/mss_out/imp_model/aws_mss_prep_step2.sh
#/shared/imp/imp_msstudio_init-master/mss_out/imp_model/aws_mss_prep_step3.sh
```






### Prerequisites

The PRC2 sample project was prepared using the MassSpecStudio application.
The IMP job driver script runs with python 3.x and has a dependency on the Python Modeling Interface (PMI)

The initial software installation of python with Anaconda and python packages for imp 
are included in the setup script. The individual steps are highlighted once again, hereafter.
```
#initial setup for PMI using anaconda
Anaconda3\Library\bin\conda config --add channels salilab
Anaconda3\Library\bin\conda install imp scikit-learn matplotlib

#https://integrativemodeling.org/tutorials/rnapolii_stalk/
Anaconda3\Library\bin\conda install numpy scipy


#bring up Anaconda Prompt and run : activate base
#you can see envs available with: conda info --envs
#for example: this shows us that base is c:\apps\Anaconda3

```

Performance Expectations:
On a 16cpu instance we have observed up to 50 frames per minute throughput, although 30 frames per minute is typical.
We expect 20000 frames to complete in 10 hours ( based on PRC2 example ).




### Installing

The readme_setup_cedar.txt is a good place to start. This explains how to setup the example project on Compute Canada's Cedar cluster.

**Taken from the readme_setup_cedar.txt:**

```
#### get the setup script and call it with the correct username as the first arg: 
~~~
curl -LOk https://gist.githubusercontent.com/pellst/4853822ea5ca74785af61d0ad39cf84d/raw/uoc_mss_prep_step1.sh
chmod 755 uoc_mss_prep_step1.sh
~~~

#### run the script uoc_mss_prep_step1.sh in order to get the sample folders setup
~~~
./uoc_mss_prep_step1.sh your_user_name
~~~

#### in the folder /scratch/username/imp/imp_msstudio_init-master/mss_out/imp_model, the following shell scripts are now available
~~~
            uoc_mss_prep_step1.sh
            uoc_mss_prep_step2.sh
            uoc_mss_prep_step3.sh
~~~
			
#### we can continue on to step2 to setup anaconda			
./uoc_mss_prep_step2.sh
conda --version
python --version

#### once anaconda has been setup we can bring in the imp module and others needed for the job run
./uoc_mss_prep_step3.sh

#### the next step is to review the following:
#### located in /scratch/username/imp/imp_msstudio_init-master/mss_out/imp_model
ConfigImp.yaml
mjob_run_cedar.sh

```

#### amend the sampling_frame in ConfigImp.yaml
sampling_frame: 100
* the cores is used for the ntasks-per-node=x where x=16 is a good starting point
* performance expectations are that with a single node and 1 cpu per task and 16 tasks per node we can run 20000 sampling_frame in 9 hours

#### amend the slurm script settings in mjob_run_cedar.sh

~~~
#!/bin/bash
# example slurm job script setup to run on for example Cedar
#SBATCH --job-name=SLURM_imp
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=16
#SBATCH --cpus-per-task=1
#SBATCH --mem=32G
#SBATCH --time=0-01:00:00
#SBATCH --account=sponsername 
~~~


#in order to run the job we call this and give a unit number to be used for naming the folder that is setup eg: 12 here
~~~
chmod 755 mjob_run_cedar.sh
./mjob_run_cedar.sh 12
#monitor the job run
squeue -u username
~~~

#once the job has finished, look in the imp_model_12 folder and inspect the logs
~~~
tail -100 prep_hyperp_imp_v2ux.log
#do the same for the slurm-nnnnn.out
~~~

#a successful run will include the output folders from the job. Copy the entire imp_model_12 to local machine ( optionally tar the folder in order to archive) 

#in order to run multiple jobs in parallel. From the imp_model folder amend the configuration as needed and call mjob_run_cedar.sh nn once again.


The wrapper script mjob_run_cedar.sh essentially performs a slurm job scheduler call to launch: srun python prep_hyperp_imp_v2ux.py and this in turn runs the 
prep_hyperp_imp_v2ux.py driver script. The configuration of the driver script is accomplished with the ConfigImp.yaml
There are assumptions that have been made and while a basic modeling run has been anticipated. The prep_hyperp_imp_v2ux.py script can
be customised further in order to fit the specific modeling scenario.

```
finished
```

#compute canada will purge files older than 60days in the /scratch area. 
#purge and re-deploy as required

todo: End with an example of getting some data out of the system or using it for analysis


## Deployment

Additional notes about how to deploy this on a live system.
We can deploy on any of the following:
* Cedar ( Compute Canada cluster ) 
* AWS
* 



* **Cedar** ( Compute Canada cluster )
The **installing** section, above, provides the steps to follow in order to prepare your user account on Cedar
with the required software together with the PRC2 sample project.
We have selected Cedar for our example. There are other clusters on Compute Canada that are available, such as **Graham**.


* **AWS**
How to prepare a golden image with the required software together with the PRC2 sample project.

```
Notes:
todo: add aws EC2 launch configuration steps, incl.  ami name, size t2.micro, subnet, route table, ebs size, security, iam user and .pem key-pair

todo: Cloudformation script and aws CLI script options

todo:  /shared/anaconda as install location

The base ami was setup using a aws parallel-cluster image ( linux )
alinux:
us-west-2: ami-09b457d5cba24514a

t2.micro is in the Free Tier. Slower deployment.
t3a.xlarge is a 4cpu 16Gb machine with good network bandwidth for faster deployment.

storage size 30Gb
security group : SSH TCP port 22 for myip 



```



Once we have the aws EC2 instance up and running. We can login via ssh to the new instance and perform the software setup steps:
```
# in a single vm we can create /shared folder
# sudo mkdir /shared 
# sudo chmod 777 /shared

# make use of this gist to get the prep_step* shell scripts located here
# /shared/imp/imp_msstudio_init-master/mss_out/imp_model
curl -LOk https://gist.githubusercontent.com/pellst/9f7ad519133dae87f8f813b506b45aac/raw/aws_mss_prep_step1.sh 
chmod 755 aws_mss_prep_step1.sh 
./aws_mss_prep_step1.sh

# prepare anaconda install
#/shared/imp/imp_msstudio_init-master/mss_out/imp_model/aws_mss_prep_step2.sh
cd /shared/imp/imp_msstudio_init-master/mss_out/imp_model
./aws_mss_prep_step2.sh



# prepare python package install
#/shared/imp/imp_msstudio_init-master/mss_out/imp_model/aws_mss_prep_step3.sh
cd /shared/imp/imp_msstudio_init-master/mss_out/imp_model
./aws_mss_prep_step3.sh


``` 
Upon completion of the software install. We take a snapshot of the aws AMI so that we can use
this configured ami to launch new EC2 instances with suitable CPU and memory capacity for the 
MPI job run for the IMPort PRC2 sample project or your own IMP project.

From here you can follow the **FastTrack** section and use the newly minted ami to run the
PRC2 sample project as an IMP MPI job on aws.


```
Notes:
todo: The current version of IMP 2.11.1 has changes in how it processes the decorate_gmm_from_text. 

todo: The PRC2 sample project configuration needs to be amended to work with the later version.
imp2.12.0 ; amend the call to prep_hyperp_imp_v2ux.py to prep_hyperp_imp_v2_12_0ux.py 
as this has the problem import commented : #import IMP.pmi.representation


```




The base ami was setup using an aws parallel-cluster image ( linux ), namely:
```
alinux:
us-west-2: ami-09b457d5cba24514a
```

The EC2 instance used to prepare the base ami does not need to be xlarge. We can accomplish the software
installation on t2.micro, although selecting a t3a.large instance that has higher network speeds does help. 

The EC2 instance used to perform a job run needs to be xlarge. For example:
```
c4.4xlarge
```

The EBS storage sizing considerations

```
30Gb
```

### Prepare a new IMPort modeling project with **MassSpecStudio**

In order to pull together the various data files and prepare the artifacts of a IMPort modeling bundle.
The **MassSpecStudio** application provides a wizard that guides the user through the selection
of the data files and setup of the various configuration settings required by the IMP modeling run.
We need to have installed, on a windows o/s, the **MassSpecStudio** application.  
todo: link to the msstudio IMPort Guide so that users can prepare their own IMPort project 


## Built With

* [Python](https://github.com/pellst/imp_msstudio_init) - The language used
* [IMP](https://integrativemodeling.org/tutorials/rnapolii_stalk/) - The integrated modeling platform 


## Authors

* **MassSpecStudio Development Team** - *Initial work* - [University of Calgary](https://github.com/pellst/imp_msstudio_init)

See also the list of [contributors](https://github.com/pellst/imp_msstudio_init/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* [MassSpecStudio Development Team](https://www.msstudio.ca/mss-IMPort/)
* [IMP dataset source](https://integrativemodeling.org/tutorials/rnapolii_stalk/)
* Inspiration
* etc

