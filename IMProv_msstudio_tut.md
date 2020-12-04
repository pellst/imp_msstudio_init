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

[logo]: https://github.com/pellst/imp_msstudio_init/raw/master/uml_diag_IMProv_msstudio.png "msstudio IMProv prep"

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

Using the Add Proteins wizard screen. Select the FASTA or PDB files to add reference sequences. 
This will then show the Name and give the opportunity to customize the Topology by clicking the 
Manage button under the Topology column for the row with a protein name.


Project - Add Proteins Topology: 

![alt text](https://github.com/pellst/imp_msstudio_init/raw/master/xl_imp_images/msst_imp_proj_wizard_step1c_topo.png "Logo Title Text 1")

The Topology record can be edited to set the start and end of the sequence together with the PDB Offset etc. 
Once you click Ok you will be returned to the Add Proteins wizard screen so that you can do the same for each of the Proteins involved. 
The representation can be adjusted e.g. two structures can be assigned to a single sequence and bead size can be adjusted.
Once you have completed all the Proteins that you wish to amend. 
You can click the Next button (at the bottom right hand corner of the screen) which will take you to the Add Link Data wizard screen


Project - Add Link Data [XL, EM ...]:
 
![alt text](https://github.com/pellst/imp_msstudio_init/raw/master/xl_imp_images/msst_imp_proj_wizard_step1d_datafiles.png "Logo Title Text 1")

Add Link Data wizard screen is where you can add additional data files including Cross-Linking, Hydrogen Exchange, Covalent Labeling and Electron Microscopy. 
These files will be included in their respective folders for the final output that is generated. 
Once you have completed your file selections you can click the Next button (at the bottom right hand corner of the screen). 
This will take you to the Configure IMP wizard screen.



Project - Configure IMP sampling frames... : 

![alt text](https://github.com/pellst/imp_msstudio_init/raw/master/xl_imp_images/msst_imp_proj_wizard_step1e_config.png "Logo Title Text 1")

The Configure IMP wizard screen is where we define the Directory path to export the data files and modeling scripts to. 
We also set the Sampling Frames and States here. 
The Ridgid Body and Super Ridgid Body assignments are available through the pick lists provided. 
The final step is to click the Export button (at the bottom right hand corner of the screen). 
This will produce the folder structure containing the Topology and YAML Config file together with the raw data files that you selected in the wizard steps ( data folder ). 
It also adds a folder with the modeling scripts needed (imp_model) to perform the job run using the python driver script provided.


Project - Exported directory - data files : 

![alt text](https://github.com/pellst/imp_msstudio_init/raw/master/xl_imp_images/msst_imp_proj_wizard_step1f_direxport.png "Logo Title Text 1")


Project - Exported directory - python driver script : 

![alt text](https://github.com/pellst/imp_msstudio_init/raw/master/xl_imp_images/msst_imp_proj_wizard_step1g_driverscripts.png "Logo Title Text 1")



Project - Deployment to HPC platform running IMP package : 

![alt text](https://github.com/pellst/imp_msstudio_init/raw/master/xl_imp_images/msst_imp_proj_wizard_step2a_pmi.png "Logo Title Text 1")


We make use of a setup script from github gist in order to provide the commands needed to get the sample project from github. 
This brings with it the example files and scripts that we will be using to complete this demonstrating.

'''
#### get the setup script from github gist and review before running: 
curl -LOk https://gist.githubusercontent.com/pellst/4853822ea5ca74785af61d0ad39cf84d/raw/uoc_mss_prep_step1.sh
chmod 755 uoc_mss_prep_step1.sh
#### run the script uoc_mss_prep_step1.sh in order to get the sample folders and scripts setup ./uoc_mss_prep_step1.sh
#### in the folder /scratch/$USER/imp/imp_msstudio_init-master/mss_out/imp_model, the following shell scripts are now available
uoc_mss_prep_step1.sh
uoc_mss_prep_step2.sh
uoc_mss_prep_step3.sh

'''

## Fast Track:
* login to **Cedar** on Compute Canada and run these scripts in your user account
  * see **Installing** [section](https://github.com/pellst/imp_msstudio_init/blob/master/IMProv_on_Cedar_tut.md)


* alternatively, login to your **AWS** account and from the Management Console perform these steps to launch an EC2 spot instance using the AMI for IMProv MPI jobs
  * steps to setup your own AMI, see **Deployment** [section](https://github.com/pellst/imp_msstudio_init/blob/master/IMProv_on_AWS_tut.md)




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

