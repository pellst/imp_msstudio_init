# IMProv ( integrative modeling platform ) - MassSpecStudio Wizard Workflow (0.1)

This tutorial presents the msstudio wizard to gather the data files 
and driver scripts needed to perform a MPI based IMP modeling job run. We cover how this can be prepared 
using the IMProv wizard in [MassSpecStudio](https://www.msstudio.ca/mss-improv/). 



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

We are able to prepare the data files and driver scripts given above using MassSpecStudio's IMProv wizard.
The activity diagram that follows illustrates the various steps involved in running the modeling pipeline. 
This is provided here in order to set the context for the pre-requisite steps that we need to perform prior to deployment for this modeling job run. 


MassSpecStudio is used to configure the artifacts that are subsequently involved in the following activity diagram: 
![alt text][logo]

[logo]: https://github.com/pellst/imp_msstudio_init/raw/master/uml_diag_improv_msstudio.png "msstudio IMProv prep"

### Prepare a new IMProv modeling project with **MassSpecStudio**

In order to pull together the various data files and prepare the artifacts of a IMProv modeling bundle.
The **MassSpecStudio** application provides a wizard that guides the user through the selection
of the data files and setup of the various configuration settings required by the IMP modeling run.
We need to have installed, on a windows o/s, the **MassSpecStudio** application.  
todo: link to the msstudio IMProv Guide so that users can prepare their own IMProv project 


IMProv configuration Wizard: 

Project - Init: 

![alt text](https://github.com/pellst/imp_msstudio_init/raw/master/xl_imp_images/msst_imp_proj_wizard_step1a.png "Logo Title Text 1")


Project - Add Proteins:
 
![alt text](https://github.com/pellst/imp_msstudio_init/raw/master/xl_imp_images/msst_imp_proj_wizard_step1b_topo.png "Logo Title Text 1")


Project - Add Proteins Topology: 

![alt text](https://github.com/pellst/imp_msstudio_init/raw/master/xl_imp_images/msst_imp_proj_wizard_step1c_topo.png "Logo Title Text 1")


Project - Add Link Data [XL, EM ...]:
 
![alt text](https://github.com/pellst/imp_msstudio_init/raw/master/xl_imp_images/msst_imp_proj_wizard_step1d_datafiles.png "Logo Title Text 1")


Project - Configure IMP sampling frames... : 

![alt text](https://github.com/pellst/imp_msstudio_init/raw/master/xl_imp_images/msst_imp_proj_wizard_step1e_config.png "Logo Title Text 1")


Project - Exported directory - data files : 

![alt text](https://github.com/pellst/imp_msstudio_init/raw/master/xl_imp_images/msst_imp_proj_wizard_step1f_direxport.png "Logo Title Text 1")


Project - Exported directory - python driver script : 

![alt text](https://github.com/pellst/imp_msstudio_init/raw/master/xl_imp_images/msst_imp_proj_wizard_step1g_driverscripts.png "Logo Title Text 1")



Project - Deployment to HPC platform running IMP package : 

![alt text](https://github.com/pellst/imp_msstudio_init/raw/master/xl_imp_images/msst_imp_proj_wizard_step2a_pmi.png "Logo Title Text 1")





## Fast Track:
* login to **Cedar** on Compute Canada and run these scripts in your user account
  * steps ...
  * see **Installing** [section](https://github.com/pellst/imp_msstudio_init/blob/master/IMProv_on_Cedar_tut.md)


* alternatively, login to your **AWS** account and from the Management Console perform these steps to launch an EC2 spot instance using the AMI for IMProv MPI jobs
  * steps ...
  * steps to setup your own AMI, see **Deployment** [section](https://github.com/pellst/imp_msstudio_init/blob/master/IMProv_on_Cedar_tut.md)

  * steps to launch existing AMI, follow ...



```
code block 



```










## Prerequisites
* Installation of MassSpecStudio
* Obtain the various data files required by the modeling job.




## Deployment

Additional notes about how to deploy this on a live system.
We can deploy on any of the following:
* Cedar ( Compute Canada cluster ) 
* AWS
* 






## Built With

* [Python](https://github.com/pellst/imp_msstudio_init) - The language used
* [IMP](https://integrativemodeling.org/tutorials/rnapolii_stalk/) - The integrated modeling platform 


## Authors

* **MassSpecStudio Development Team** - *Initial work* - [University of Calgary](https://github.com/pellst/imp_msstudio_init)

See also the list of [contributors](https://github.com/pellst/imp_msstudio_init/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* [MassSpecStudio Development Team](https://www.msstudio.ca/mss-improv/)
* [IMP dataset source](https://integrativemodeling.org/tutorials/rnapolii_stalk/)
* Inspiration
* etc

