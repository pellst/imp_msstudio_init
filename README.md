# IMP ( integrative modeling platform ) config and driver script
# imp_msstudio_init

Python script and example yaml configuration for running IMP modeling job

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. 
See deployment for notes on how to deploy the project on a live system.

From the downloaded and extracted master branch. Run the following to execute the example job:
```
imp_msstudio_init-master\driver_imp_init\imp_model>run_py_impjob.bat
```

For linux platform there is a python script available:
imp_job_run.py


### Prerequisites

The driver script runs with python 3.x and depends on the Python Modeling Interface (PMI)

```
initial setup for PMI
Anaconda3\Library\bin\conda config --add channels salilab
Anaconda3\Library\bin\conda install imp scikit-learn matplotlib

https://integrativemodeling.org/tutorials/rnapolii_stalk/
Anaconda3\Library\bin\conda install numpy scipy


bring up Anaconda Prompt and run : activate base
you can see envs available with: conda info --envs
for example: this shows us that base is c:\apps\Anaconda3




```

```
Give examples
```

### Installing

A step by step series of examples that tell you how to get a development env running

The readme_setup_cedar.txt is a good place to start. This explains how to setup the example on Compute Canada's Cedar cluster.


```
Taken from the readme_setup_cedar.txt:


#### get the setup script and call it with the correct username as the first arg: 
~~~
curl -LOk https://gist.githubusercontent.com/pellst/4853822ea5ca74785af61d0ad39cf84d/raw/uoc_mss_prep_step1.sh
chmod 755 uoc_mss_prep_step1.sh
~~~

#### run the script uoc_mss_prep_step1.sh in order to get the sample folders setup
~~~
uoc_mss_prep_step1.sh tpells
~~~

#### in the folder scratch/imp/imp_msstudio_init-master/mss_out/imp_model, the following shell scripts are now available
~~~
            uoc_mss_prep_step1.sh
            uoc_mss_prep_step2.sh
            uoc_mss_prep_step3.sh
~~~
			
#### we can continue on to step2 to setup anaconda			
uoc_mss_prep_step2.sh


#### once anaconda has been setup we can bring in the imp module and others needed for the job run
uoc_mss_prep_step3.sh

#### the next step is to review the following:
#### located in scratch/imp/imp_msstudio_init-master/mss_out/imp_model
ConfigImp.yaml
mjob_run_cedar.sh

```

#### amend the sampling_frame in ConfigImp.yaml
sampling_frame: 1000
#### the cores is used for the ntasks-per-node=x where x=16 is a good starting point
#### performance expectations are that with a single node and 1 cpu per task and 16 tasks per node we can run 20000 sampling_frame in 9 hours

#### amend the slurm script settings in mjob_run_cedar.sh
#Runbook info.

~~~
#!/bin/bash
# example slurm job script setup to run on for example Cedar
#SBATCH --job-name=SLURM_imp
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=16
#SBATCH --cpus-per-task=1
#SBATCH --mem=32G
#SBATCH --time=0-1:00:00
#SBATCH --account=sponsername 
~~~


#in order to run the job we call this and give a unit number to be used for naming the folder that is setup eg: 12 here
~~~
./mjob_run_cedar.sh 12
~~~

The wrapper script mjob_run_cedar.sh essentially performs a slurm job scheduler call to launch: srun python prep_hyperp_imp_v2ux.py and this in turn runs the 
prep_hyperp_imp_v2ux.py driver script. The configuration of the driver script is accomplished with the ConfigImp.yaml
There are assumptions that have been made and while a basic modeling run has been anticipated. The prep_hyperp_imp_v2ux.py script can
be customised further in order to fit the specific modeling scenario.

```
finished
```

End with an example of getting some data out of the system or using it for a little demo

## Running the tests

Explain how to run the automated tests for this system

### Break down into end to end tests

Explain what these tests test and why

```
Give an example
```

### And coding style tests

Explain what these tests test and why

```
Give an example
```

## Deployment

Add additional notes about how to deploy this on a live system

## Built With

* [Python](https://github.com/pellst/imp_msstudio_init) - The language used
* [IMP](https://integrativemodeling.org/tutorials/rnapolii_stalk/) - The integrated modeling platform 

## Contributing

Please read [CONTRIBUTING.md] for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

## Authors

* **MassSpecStudio Development Team** - *Initial work* - [University of Calgary](https://github.com/pellst/imp_msstudio_init)

See also the list of [contributors](https://github.com/pellst/imp_msstudio_init/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* MassSpecStudio Development Team
* [IMP dataset source] (https://integrativemodeling.org/tutorials/rnapolii_stalk/)
* Inspiration
* etc

