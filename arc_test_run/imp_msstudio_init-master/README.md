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
Anaconda3\Library\bin\conda install numpy scipy scikit-learn matplotlib

Anaconda3\Library\bin\conda install -c conda-forge dataclasses


bring up Anaconda Prompt and run : activate base
you can see envs available with: conda info --envs
this shows us that base is c:\apps\Anaconda3

pip install dacite==1.0.0
pip install dataclasses-json
pip install dataclasses-jsonschema


```

```
Give examples
```

### Installing

A step by step series of examples that tell you how to get a development env running

Say what the step will be

```
Give the example
```

And repeat

```
until finished
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

