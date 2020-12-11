#===============================================================================
#
#         FILE: prep_hyperp_imp_hx_v2.py
#
#        USAGE: 
#           LINUX: nohup /shared/anaconda/bin/python prep_hyperp_imp_v2ux.py --count=1 --name=DemoImpModel --config=ConfigImp.yaml >/shared/imp/imp_msstudio_init-master/mss_out/imp_model$runnum/trace.log 2>&1 &
# 
#  DESCRIPTION: IMP (integrative modeling platform) driver script configured with ConfigImp.yaml
#                Python Modeling Interface (PMI) ; https://integrativemodeling.org/
#                source for IMP located in github https://github.com/salilab/imp/
#
#      OPTIONS: ---
# REQUIREMENTS: ---
#         BUGS: ---
#        NOTES: supports imp 2.12.0 as at 2019-Dec-06
#
#       AUTHOR: MassSpecStudio Develoment Team, 
# ORGANIZATION: 
#      VERSION: 2.0
#      CREATED: 06/16/2019 12:00:00
#     REVISION: 01/14/2020 12:00:00 --- imp2.12.0 ; https://integrativemodeling.org/2.12.0/doc/manual/changelog.html
#     REVISION: 03/10/2020 12:00:00 --- hx tight/loose classification; sigma in place of Distance value.
#
#       The old IMP::pmi::representation::Representation class has been removed from IMP.pmi. 
#       New applications should use IMP::pmi::topology::System instead.
#
#       The IMP::pmi::restraints::crosslinking::ISDCrossLinkMS class for handling crosslinking has been removed. Use 
#       IMP::pmi::restraints::crosslinking::CrossLinkingMassSpectrometryRestraint instead.
#
#
#
#===============================================================================

import optparse
import logging
import time
import yaml

import IMP
import IMP.core
import IMP.algebra
import IMP.atom
import IMP.container

import IMP.pmi.restraints.crosslinking
import IMP.pmi.restraints.stereochemistry
import IMP.pmi.restraints.em
import IMP.pmi.restraints.basic
import IMP.pmi.tools
import IMP.pmi.samplers
import IMP.pmi.output
import IMP.pmi.macros
#import IMP.pmi.representation
import IMP.pmi.topology

import os
import sys

#import IMP
import IMP.pmi
import IMP.pmi.io
import IMP.pmi.io.crosslink
#import IMP.pmi.topology
#import IMP.pmi.macros
#import IMP.pmi.restraints.stereochemistry
#import IMP.pmi.restraints.em
from IMP.pmi.restraints.crosslinking import CrossLinkingMassSpectrometryRestraint as XLRestraint
#import os



# tutorial starting point
# https://integrativemodeling.org/tutorials/rnapolii_stalk/


#C:\apps\Anaconda3\python.exe prep_hyperp_imp_v2.py --count=1 --name=Demo --config="ConfigImp.yaml"



# Primitive Types
ImpHandle = str ## E.g. subset names
CrossLinkFilename = str ## csv file containing crosslink data
#Email = str ## must be of NAME@DOMAIN form
#Url = str
Directory = str
TopologyFile = str
Target_gmm_file = str






def load_yaml_config(config_file):
    with open(config_file, 'r') as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)




def load_config(config_file,
                title ):
    """
    Parses a project.yaml file and uses the contents to
    set the current execution context.

    Optionally injects additional values
    https://martin-thoma.com/configuration-files-in-python/

    https://github.com/beetbox/confuse
    https://hackersandslackers.com/simplify-your-python-projects-configuration/

    """
 
    logging.info('config filename %s!' % config_file)
    #obj = yaml.safe_load(config_file)
    cfg = load_yaml_config(config_file)
    for section in cfg:
        logging.info(section + ' %s!' % cfg[section])

        if section == "xl_groupB":
            #
            for i in cfg[section]:
                logging.info(i)
                for k, v in i.items():
                    logging.info(k +': %s!' % v)

        if section == "xl_dbA":
            #
            for i in cfg[section]:
                logging.info(i)
                for k, v in i.items():
                    logging.info(k +': %s!' % v)

        if section == "crosslinkdb":
            #
            for i in cfg[section]:
                logging.info(i)
                for k, v in i.items():
                    logging.info(k +': %s!' % v)


        if section == "degree_of_freedom":
            #logging.info( subxl_group + ' %s!' % cfg[section])
            for i in cfg[section]:
                logging.info(i +': %s!' % cfg[section][i])

    #print(cfg['topology_file'])
    #print(cfg['title'])
    logging.info('given topology_file %s!' % cfg['topology_file'])
    logging.info('given title %s!' % cfg['title'])
    


    # perform pipeline setup
    model_pipeline(cfg)

    

def seed(config, title):
    """
    Seeds an imp project
    """

    load_config(config,
                   title=title)


def mkdir(adddirname):
    if not os.path.exists(adddirname):
        os.makedirs(adddirname)


def model_pipeline(project):
    """
    Model pipeline for IMP project
    """

    logging.info('model_pipeline title %s!' % project["title"])

    #---------------------------
    # Define Input Files
    # The first section defines where input files are located. 
    # The topology file defines how the system components are structurally represented. 
    # target_gmm_file stores the EM map for the entire complex, which has already been converted into a Gaussian mixture model.
    #---------------------------
    datadirectory = project["data_directory"] 
    #"C:/dev/project/py_imp/py_imp/pmi_tut/rnapolii/data/"

    # C:/Users/adminL/source/repos/py_imp/py_imp/pmi_tut/rnapolii/data/
    logging.info('config data_directory %s!' % datadirectory)
    print('config data_directory %s!' % datadirectory)




    # Start by getting directory paths
    #this_path = os.path.dirname(os.path.realpath(__file__)) + "/"
    #cwd = os.getcwd()
    this_path = project["data_directory"]
    mkdir(this_path)
    print('config this_path %s!' % this_path)
 
    # these paths are relative to the topology file
    pdb_dir = this_path + "data/xtal"
    fasta_dir = this_path + "data/fasta"
    gmm_dir = this_path + "data/em"
    xl_dir = this_path + "data/xl"
    topo_dir = this_path + "data/topo"

    #pdb_dir = this_path + "../data/xtal"
    #fasta_dir = this_path + "../data/fasta"
    #gmm_dir = this_path + "../data/em"
    #xl_dir = this_path + "../data/xl"
    #topo_dir = this_path + "../data/topo"


    logging.info('this_path %s!' % this_path)
    print('this_path %s!' % this_path)

    logging.info('pdb_dir %s!' % pdb_dir)
    logging.info('fasta_dir %s!' % fasta_dir)
    logging.info('gmm_dir %s!' % gmm_dir)
    print('gmm_dir %s!' % gmm_dir)
    logging.info('xl_dir %s!' % xl_dir)
    logging.info('topo_dir %s!' % topo_dir)

    #if not os.path.exists(pdb_dir):
    #    os.makedirs(pdb_dir)
    #mkdir(pdb_dir)
    #mkdir(fasta_dir)
    #mkdir(gmm_dir)
    #mkdir(xl_dir)
    #mkdir(topo_dir)

    topology_file = topo_dir+'/'+project["topology_file"]
    target_gmm_file = gmm_dir+'/'+project["target_gmm_file"]
    
    #logging.info('data_directory %s!' % datadirectory)

    logging.info('model_pipeline topology_file %s!' % topology_file)
    logging.info('target_gmm_file %s!' % target_gmm_file)

    class MSStudioCrosslinks:
        # Class that converts an MS Studio crosslink file
        # into a csv file and corresponding IMP CrossLinkDataBase object
        def __init__(self, infile):
            self.infile = infile
            self.xldbkc = self.get_xldbkc()
            self.xldb = IMP.pmi.io.crosslink.CrossLinkDataBase(self.xldbkc)
            self.xldb.create_set_from_file(self.infile, self.xldbkc)

        def get_xldbkc(self):
            # Creates the keyword converter database to translate MS Studio column names
            # into IMP XL database keywords
            xldbkc = IMP.pmi.io.crosslink.CrossLinkDataBaseKeywordsConverter(IMP.pmi.io.crosslink.ResiduePairListParser("MSSTUDIO"))
            xldbkc.set_site_pairs_key("Selected Sites")
            xldbkc.set_protein1_key("Protein 1")
            xldbkc.set_protein2_key("Protein 2")
            xldbkc.set_unique_id_key("Peptide ID")
            
            return xldbkc

        def parse_infile(self):
            # Returns a list of each crosslink's attributes as a dictionary.
            import csv
            return csv.DictReader(open(self.infile), delimiter=',', quotechar='"')

        def get_database(self):
            return self.xldb

 





    # Topology file should be in the same directory as this script
    #topology_file = this_path +"../topology/topology.txt"
    logging.info('Initialize model')
    # Initialize model
    mdl = IMP.Model()


    # Build the Model Representation Using a Topology File Using the topology file we define the overall topology: we introduce the molecules with their 
    # sequence and their known structure, and define the movers. Each line in the file is a user-defined molecular Domain, 
    # and each column contains the specifics needed to build the system. See the TopologyReader documentation for a full description of the topology file format.

    #topology file example:
    #|molecule_name  |color     |fasta_fn          |fasta_id|pdb_fn             |chain|residue_range|pdb_offset|bead_size|em_residues_per_gaussian|rigid_body|super_rigid_body|chain_of_super_rigid_bodies|
    #|Rpb1           |blue      |1WCM_new.fasta.txt|1WCM:A  |1WCM_map_fitted.pdb|A    |1,1140       |0         |20       |0                       |1         | 1              |                           |
    #|Rpb1           |blue      |1WCM_new.fasta.txt|1WCM:A  |1WCM_map_fitted.pdb|A    |1141,1274    |0         |20       |0                       |2         | 1              | 

    # https://integrativemodeling.org/2.10.1/doc/ref/classIMP_1_1pmi_1_1topology_1_1TopologyReader.html


    #|molecule_name|color|fasta_fn|fasta_id|pdb_fn|chain|residue_range|pdb_offset|bead_size|em_residues_per_gaussian|rigid_body|super_rigid_body|chain_of_super_rigid_bodies|flags|
    #|Rpb1   |blue   |1WCM.fasta|1WCM:A|1WCM.pdb|A|1,1140   |0|10|0|1|1,3|1||
    #|Rpb1   |blue   |1WCM.fasta|1WCM:A|1WCM.pdb|A|1141,1274|0|10|0|2|1,3|1||
    #|Rpb1   |blue   |1WCM.fasta|1WCM:A|1WCM.pdb|A|1275,END |0|10|0|3|1,3|1||

    # fasta.txt files are what is expected

    # Read in the topology file. We must handle multiple topology files: meaning we need to handle either consolidate as one OR handle multiple sets of XL csv files
    # Specify the directory where the PDB files, fasta files and GMM files are
    logging.info('Specify the directory where the PDB files, fasta files and GMM files are')
    toporeader = IMP.pmi.topology.TopologyReader(topology_file,
                                      pdb_dir=pdb_dir,
                                      fasta_dir=fasta_dir,
                                      gmm_dir=gmm_dir)

    # Use the BuildSystem macro to build states from the topology file
    
    bldsys = IMP.pmi.macros.BuildSystem(mdl)
    

    # Each state can be specified by a topology file.
    logging.info('add_state(toporeader)')
    bldsys.add_state(toporeader)
    

    #Building the System Representation and Degrees of Freedom
    #Here we can set the Degrees of Freedom parameters, which should be optimized according to MC acceptance ratios. There are three kind of movers: Rigid Body, Bead, and Super Rigid Body (super rigid bodies are sets of rigid bodies and beads that will move together in an additional Monte Carlo move).
    #max_rb_trans and max_rb_rot are the maximum translation and rotation of the Rigid Body mover, max_srb_trans and max_srb_rot are the maximum translation and rotation of the Super Rigid Body mover and max_bead_trans is the maximum translation of the Bead Mover.
    #The execution of the macro will return the root hierarchy (root_hier) and the degrees of freedom (dof) objects, both of which are used later on.



    # Build the system representation and degrees of freedom
    """
    root_hier, dof = bldsys.execute_macro(max_rb_trans=project.degree_of_freedom.max_rb_trans,
                                      max_rb_rot=project.degree_of_freedom.max_rb_rot,
                                      max_bead_trans=project.degree_of_freedom.max_bead_trans,
                                      max_srb_trans=project.degree_of_freedom.max_srb_trans,
                                      max_srb_rot=project.degree_of_freedom.max_srb_rot)
    """
    logging.info('bldsys.execute_macro')
    root_hier, dof = bldsys.execute_macro()
    """
    fb = dof.create_flexible_beads(mol.get_non_atomic_residues(),
                           max_trans=bead_max_trans)
    """
    #print(dof.get_rigid_bodies() )

    #print(toporeader.get_rigid_bodies() )


    outputobjects=[]
    
     


    # Stereochemistry restraints
    ev = IMP.pmi.restraints.stereochemistry.ExcludedVolumeSphere(included_objects=bldsys.get_molecules()[0].values(), resolution=20)
    ev.add_to_model()
    outputobjects.append(ev)

    crs = []
    for mol in bldsys.get_molecules()[0].values():
        #dof.create_flexible_beads(mol.get_non_atomic_residues(),
        #                   max_trans=bead_max_trans)
        cr = IMP.pmi.restraints.stereochemistry.ConnectivityRestraint([mol])
        cr.add_to_model()
        crs.append(cr)
        outputobjects.append(cr)
    logging.info('IMP.pmi.tools.shuffle_configuration')
    IMP.pmi.tools.shuffle_configuration(root_hier, 
                                        max_translation=100, # raise for larger systems if shuffling fails at niterations, want it ~1.5x size of system in angstrom
                                        verbose=True, 
                                        cutoff=5.0,
                                        niterations=100)

    logging.info(ev.evaluate());
    dof.optimize_flexible_beads(500) #if beads are not connecting at initial rmf, increase; number of steps to optimize connectivity 
    logging.info(ev.evaluate());
    
 



    # Getting length of list 
    length = len(project["xl_groupB"]) 
    i = 0
    
    xlList=[]
    logging.info('Iterating using while loop')
    # Iterating using while loop 
    while i < length: 
        logging.info(project["xl_groupB"][i])
        #"refid","length","slope","resolution","label","weight","crosslink_distance"

        logging.info(project["xl_groupB"][i]["refid"])
        logging.info(project["xl_groupB"][i]["length"])
        logging.info(project["xl_groupB"][i]["slope"])
        logging.info(project["xl_groupB"][i]["resolution"])
        logging.info(project["xl_groupB"][i]["sigma_kappa"])
        logging.info(project["xl_groupB"][i]["sigma_theta"])
        logging.info(project["xl_groupB"][i]["sigma_init"])
        logging.info(project["xl_groupB"][i]["label"])
        logging.info(project["xl_groupB"][i]["weight"])
        logging.info(project["xl_groupB"][i]["crosslink_distance"])

        
        # Set up crosslinking restraint
        xlB = XLRestraint(root_hier=root_hier, 
                 CrossLinkDataBase=MSStudioCrosslinks(xl_dir + "/" + project["xl_groupB"][i]["refid"]).get_database(),
                 length=project["xl_groupB"][i]["length"], #midpoint? Double check with Daniel and excel function thing
                 resolution=project["xl_groupB"][i]["resolution"], #keep 1, lower limit
                 slope=project["xl_groupB"][i]["slope"], # 0.01 for longer XL and 0.03 for shorter, range - check by making sure midpoint is less than 0.5 e.g 30 * 0.01
                 label=project["xl_groupB"][i]["label"],
                 sigma_form="Gamma",
                 sigma_kappa=project["xl_groupB"][i]["sigma_kappa"],
                 sigma_theta=project["xl_groupB"][i]["sigma_theta"],
                 sigma_init=xproject["xl_groupB"][i]["sigma_init"],              
                 filelabel=project["xl_groupB"][i]["label"],
                 weight=project["xl_groupB"][i]["weight"]) #ignore weight, calculated via IMP
        logging.info(xlB)
		# using slope of -1 to indicate exception ; this was previously 's', but that conflicts with the number field
        if project["xl_groupB"][i]["slope"]!="-1":
            xlB.set_psi_is_sampled(False)
        xlB.set_sigma_is_sampled(True)
        xlList.append(xlB)
        xlB.add_to_model()
        outputobjects.append(xlB)
        #dof.get_nuisances_from_restraint(xlB)
        dof.movers + xlB.get_movers()   
        i += 1     
 
    for i in range(len(xlList) ): 
        logging.info(xlList[i])   
        
        
    
    # xl_files = [(xl_dir + 'PRC2_DSS_BS3_2020_vLoose.csv', 30, 0.01, 1.6, 12), 
    # (xl_dir + 'PRC2_DSS_BS3_2020_loose.csv', 30, 0.01, 1.45, 9), 
    # (xl_dir + 'PRC2_DSS_BS3_2020_mod.csv', 30, 0.01, 1.3, 6), 
    # (xl_dir + 'PRC2_DSS_BS3_2020_tight.csv', 30, 0.01, 1.15, 3), 
    # (xl_dir + 'PRC2_DSS_BS3_2020_vTight.csv', 30, "s", 1.0, 1)]

    # xl_restraints = []

    # for xlf in xl_files:
        # xldb = MSStudioCrosslinks(xlf[0]).get_database()
        # print xlf, xldb.unique_id_key
            # label = xlf[0].split('/')[-1][0:-4]
        # xlr = XLRestraint(root_hier=root_hier,
                     # CrossLinkDataBase=xldb,
                     # length=xlf[1], #midpoint? Double check with Daniel and excel function thing
                     # resolution=1, #keep 1, lower limit
                     # slope=0.01, # 0.01 for longer XL and 0.03 for shorter, range - check by making sure midpoint is less than 0.5 e.g 30 * 0.01
                     # label=label,
                     # sigma_form="Gamma",
                     # sigma_kappa=xlf[3],
                     # sigma_theta=2.0,
                     # sigma_init=xlf[4],
                     # filelabel=label+"_missing",
                     # weight=1.) #ignore weight, calculated via IMP
        # if xlf[2]!="s":
            # xlr.set_psi_is_sampled(False)
        # xlr.set_sigma_is_sampled(True)
        # xl_restraints.append(xlr)
        # xlr.add_to_model()
        # outputobjects.append(xlr)
        # dof.movers + xlr.get_movers()   
    
    
    
    xl_rests = xlList + crs     
    
    
    logging.info('EM Restraint')
    #EM Restraint
    densities = IMP.atom.Selection(root_hier,representation_type=IMP.atom.DENSITIES).get_selected_particles()
    '''
    IMP.isd.gmm_tools.decorate_gmm_from_text(
                    "../data/em/Ciferri_PRC2.50.gmm.txt",
                    target_ps,
                    m,
                    radius_scale=3.0,
                    mass_scale=1.0)
    '''

    #coords=[IMP.core.XYZ(p) for p in target_ps]

    #print coords
    #TODO: add in the EM data file processing logic once we have the em data file
    # https://github.com/salilab/imp/
    # github\imp\modules\isd\pyext\src\create_gmm.py
    # python.exe create_gmm.py ../data/em/Ciferri_CEM_PRC2.map.mrc 50 Ciferri_CEM_PRC2_map.gmm50.txt -m Ciferri_CEM_PRC2_map.gmm50.mrc
    # Ciferri_CEM_PRC2_map.gmm50.txt 
    # "../data/em/Ciferri_CEM_PRC2_map.gmm50.txt",
    # alias is gmm_file_ouput.txt
    # TODO: skip this step if the gmm.txt is absent.
    logging.info('EM filename check for %s!' % project["target_gmm_file"])
    #print('EM filename check for %s!' % project["target_gmm_file"])
    if os.path.isfile(target_gmm_file):
        logging.info('EM file exists %s!' % target_gmm_file)
        #print('EM file exists %s!' % target_gmm_file)
        #print('EM file exists %s!' % project["target_gmm_file"])
        gemt = IMP.pmi.restraints.em.GaussianEMRestraint(densities,                                                     
                                                         #project["target_gmm_file"],
                                                         target_gmm_file,
                                                         scale_target_to_mass=True,
                                                         slope=0,
                                                         weight=200.0)

        gemt.set_label("GaussianEMRestraint")
        gemt.add_to_model()
        outputobjects.append(gemt)
    else:
        logging.info('skip gemt addition: EM file does NOT exist %s!' % target_gmm_file)
        print('skip gemt addition: EM file does NOT exist %s!' % target_gmm_file)
    


    # Gaussian functions are widely used in statistics to describe the normal distributions, in signal processing to define Gaussian filters
    # , in image processing where two-dimensional Gaussians are used for Gaussian blurs, and in mathematics to solve heat equations and diffusion equations 
    # and to define the Weierstrass transform.
    # https://en.wikipedia.org/wiki/Gaussian_function

    # Electron Microscopy Restraint
    #  The GaussianEMRestraint uses a density overlap function to compare model to data
    #   First the EM map is approximated with a Gaussian Mixture Model (done separately)
    #   Second, the components of the model are represented with Gaussians (forming the model GMM)
    #   Other options: scale_to_target_mass ensures the total mass of model and map are identical
    #                  slope: nudge model closer to map when far away
    #                  weight: experimental, needed becaues the EM restraint is quasi-Bayesian
    #
    #em_components = IMP.pmi.tools.get_densities(root_hier)
    # substitute em_components with densities in the call given below
    """ 

    gemt = IMP.pmi.restraints.em.GaussianEMRestraint(densities,
                                                     target_gmm_file,
                                                     scale_target_to_mass=True,
                                                     slope=0.000001,
                                                     weight=200.0)
    #gemt.set_label("Ciferri_PRC2")
    gemt.add_to_model()
    outputobjects.append(gemt)  
    
    """
    #print("Monte-Carlo Sampling:")
    logging.info("Monte-Carlo Sampling:")

    #--------------------------
    # Monte-Carlo Sampling
    #--------------------------

    #--------------------------
    # Set MC Sampling Parameters
    #--------------------------
    #num_frames = 20000
    #num_frames = 50
    num_frames = project["sampling_frame"]
    #if '--test' in sys.argv: num_frames=100
    num_mc_steps = 10

    logging.info('set states %s!' % project["states"])
    logging.info('set sampling_frame %s!' % project["sampling_frame"])
    logging.info('set num_frames %s!' % num_frames)

    logging.info('set output_dir %s!' % project["output_dir"])
    logging.info('set num_mc_steps %s!' % num_mc_steps)



    #TODO: add config setup for these fixed values
    logging.info('set monte_carlo_temperature=1.0')
    logging.info('set simulated_annealing=True')
    logging.info('set simulated_annealing_minimum_temperature=1.0')
    logging.info('set simulated_annealing_maximum_temperature=2.5')
    logging.info('set simulated_annealing_minimum_temperature_nframes=200')
    logging.info('set simulated_annealing_maximum_temperature_nframes=20')
    logging.info('set replica_exchange_minimum_temperature=1.0')
    logging.info('set replica_exchange_maximum_temperature=2.5')
    logging.info('set number_of_best_scoring_models=0')
    logging.info('set monte_carlo_steps %s!' % num_mc_steps)
    logging.info('set number_of_frames %s!' % num_frames)
    logging.info('set global_output_directory %s!' % project["output_dir"])




    # https://integrativemodeling.org/2.10.1/doc/ref/classIMP_1_1pmi_1_1macros_1_1ReplicaExchange0.html#a239c4009cc04c70236730479f9f79744
    # This object defines all components to be sampled as well as the sampling protocol
    mc1=IMP.pmi.macros.ReplicaExchange0(mdl,
                                        root_hier=root_hier,
                                        monte_carlo_sample_objects=dof.get_movers(),
                                        output_objects=outputobjects,
                                        crosslink_restraints=xl_rests,    # allows XLs to be drawn in the RMF files
                                        monte_carlo_temperature=1.0,
                                        simulated_annealing=True,
                                        simulated_annealing_minimum_temperature=1.0,
                                        simulated_annealing_maximum_temperature=2.5,
                                        simulated_annealing_minimum_temperature_nframes=200,
                                        simulated_annealing_maximum_temperature_nframes=20,
                                        replica_exchange_minimum_temperature=1.0,
                                        replica_exchange_maximum_temperature=2.5,
                                        number_of_best_scoring_models=0,
                                        monte_carlo_steps=num_mc_steps, #keep at 10
                                        number_of_frames=num_frames, 
                                        global_output_directory=project["output_dir"],
                                        test_mode=False)

    # start sampling
    mc1.execute_macro()

    #logging.info("GEMT", gemt.evaluate());
    #logging.info("XL1", xl1.evaluate(), xl2.evaluate());
    for i in range(len(xlList) ): 
        logging.info(xlList[i].evaluate())  
    logging.info("EV", ev.evaluate());
    logging.info("CR", cr.evaluate());  



    



    # https://integrativemodeling.org/tutorials/rnapolii_stalk/sampling.html
    #Sampling Output
    #The script generates an output directory containing the following:

    #pdbs: a directory containing the 100 best-scoring models (see the number_of_best_scoring_models variable above) from the run, in PDB format.
    #rmfs: a single RMF file containing all the frames. RMF is a file format specially designed to store coarse-grained, multi-resolution and multi-state models such as those generated by IMP. It is a compact binary format and (as in this case) can also be used to store multiple models or trajectories.
    #Statistics from the sampling, contained in a "statfile", stat.*.out. This file contains information on each restraint, MC acceptance criteria and other things at each step.
    #Gathering Data from statfile

    #Data from the stat file can be parsed and analyzed using two utilities:

    #process_output.py - parses the statfile and returns columns of interest
    #plot_stat.sh - plots one or two columns of data (requires gnuplot)









def prep_hyperparam(count, name, config):
    logging.info('prep_hyperparam %s!' % name)
    seed(config,name)


parser = optparse.OptionParser()
parser.add_option("--anaconda_dir", action="store", dest="anaconda_dir", help="path to the root directory of your Anaconda installation")
parser.add_option("--count", action="store", dest="count", help="count variable for IMP", default="1")
parser.add_option("--name", action="store", dest="name", help="Name of job", default="DemoImpModel")
parser.add_option("--config", action="store", dest="config", help="config file name (within imp_model directory)", default="ConfigImp.yaml")
parser.add_option("--output_file", action="store", dest="output_file", help="file to redirect imp script execution into, rather than stdout", default="trace.txt")

options, args = parser.parse_args()

print('count string:', options.count )
print('name string:', options.name )
print('config string:', options.config )


if __name__ == '__main__':
    timestr = time.strftime("%Y%m%d-%H%M%S")
    #os.path.basename(__file__)
    #logfilename = os.path.splitext(__file__)[0] + timestr + '.log'
    logfilename = os.path.splitext(__file__)[0] + '.log'
    print('log filename: %s!' % logfilename)

    logging.basicConfig(filename=logfilename, filemode='w', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)

    logging.info('log filename: %s!' % logfilename)
    #logging.info(os.path.splitext(__file__)[0])
    #logging.info(os.path.basename(__file__))
    logging.debug('This is a debug message')
    logging.info('This is an info message')
    logging.warning('This is a warning message')
    logging.error('This is an error message')
    logging.critical('This is a critical message')
    prep_hyperparam(options.count, options.name, options.config)

