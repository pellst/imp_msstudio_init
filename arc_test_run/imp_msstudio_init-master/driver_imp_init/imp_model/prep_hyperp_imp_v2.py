#===============================================================================
#
#         FILE: prep_hyperp_imp_v2.py
#
#        USAGE: C:\apps\Anaconda3\python.exe prep_hyperp_imp_v2.py --count=1 --name=DemoImpModel --config="ConfigImp.yaml"   > prep_hyperp_imp_v2_trace.txt 2>&1  
#
#  DESCRIPTION: IMP (integrative modeling platform) driver script configured with ConfigImp.yaml
#                Python Modeling Interface (PMI) ; https://integrativemodeling.org/
#
#      OPTIONS: ---
# REQUIREMENTS: ---
#         BUGS: ---
#        NOTES: ---
#       AUTHOR: MassSpecStudio Develoment Team, 
# ORGANIZATION: 
#      VERSION: 2.0
#      CREATED: 06/14/2019 12:00:00
#     REVISION: ---
#===============================================================================

from typing import Optional, Set, List, Union, Dict, Any
import click
import logging
import time
import yaml
from dataclasses import dataclass, field
from dacite import from_dict

import IMP
import IMP.core
import IMP.algebra
import IMP.atom
import IMP.container

import IMP.pmi.restraints.crosslinking
import IMP.pmi.restraints.stereochemistry
import IMP.pmi.restraints.em
import IMP.pmi.restraints.basic
import IMP.pmi.representation
import IMP.pmi.tools
import IMP.pmi.samplers
import IMP.pmi.output
import IMP.pmi.macros
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


@dataclass
class Degree_of_freedom():
    """
    Degree_of_freedom
    """
    #dof : Optional[List[float]] = None
    """List of Degree_of_freedom"""
    max_rb_trans: Optional[float]
    #4.0
    max_rb_rot: Optional[float]
    #0.3
    max_bead_trans: Optional[float]
    #4.0
    max_srb_trans: Optional[float]
    #4.0
    max_srb_rot: Optional[float]
    #0.3



@dataclass
class XL_db():
    """
    XL_db
    """
    #xldb : Optional[List[str]] = None
    ##"refid","set_protein1_key","set_protein2_key","set_residue1_key","set_residue2_key","set_site_pairs_key","set_unique_id_key"
    
    refid: str
    #polii_xlinks.csv
    set_protein1_key: str
    #pep1.accession
    set_protein2_key: str
    #pep2.accession
    set_residue1_key: Optional[str]
    #pep1.xlinked_aa
    set_residue2_key: Optional[str]
    #pep2.xlinked_aa

    #TODO add
    set_site_pairs_key: Optional[str]
    #("Selected Sites")
    ##set_protein1_key: str
    #("Protein 1")
    ##set_protein2_key: str
    #("Protein 2")
    set_unique_id_key: Optional[str]
    #("Peptide ID")
    
@dataclass
class CrossLink_db():
    """
    CrossLink_db
    """
    
    #xlfiles : Optional[List[CrossLinkFilename]] = None
    #"""List of crosslink filenames"""
    ##"refid","length","slope","resolution","label","weight","crosslink_distance"

    refid: str
    #polii_xlinks.csv
    length: float
    #21.0
    slope: float
    #0.01
    resolution: float
    #1.0
    label: str
    #Trnka
    weight: float
    #1.0
    crosslink_distance : float










@dataclass
class ImpProject():
    """
    A configuration for an ontology project/repository

    This is divided into project-wide settings, plus
    groups of products. Products are grouped into 4
    categories (more may be added)
    """

    #id : OntologyHandle = ""
    #"""OBO id for this ontology. Must be lowecase Examples: uberon, go, cl, envo, chebi"""
    title_id : int = ""
    """proj identifier for this imp project"""

    title : str = ""
    """Concise descriptive text about this imp project"""

    sampling_frame : int = ""
    """Concise descriptive text about this imp project"""

    states : int = ""
    """Concise descriptive text about this imp project"""

    output_dir : str = ""
    """Concise descriptive text about this imp project"""

    #crosslink_distance : float = ""
    #"""Concise descriptive text about this imp project"""

    # provide support for nested content
    # crosslink filename and config settings ; for multiple csv files

    namespaces : Optional[List[str]] = None
    """A list of namespaces that are considered at home in this ontology. Used for certain filter commands."""

    crosslinkdb : Optional[List[CrossLinkFilename]] = None
    """List of crosslink filenames"""


    #data_directory: Optional[List[Directory]] = field(default_factory=lambda: ['C:/dev/project/py_imp/py_imp/pmi_tut/rnapolii/data/', 'C:/dev/project/py_imp/py_imp/data/'])
    data_directory: Optional[Directory] = None

    xl_groupA : Optional[List[CrossLink_db]] = None
    #xl_groupB : Optional[CrossLink_db] = None
    #xl_groupC : Optional[CrossLink_db] = None

    xl_dbA : Optional[List[XL_db]] = None
    #xl_dbB : Optional[XL_db] = None
    #xl_dbC : Optional[XL_db] = None
    #xl_dbB : Optional[List[XL_db]] = None

    topology_file : Optional[TopologyFile] = "Topology.txt"

    target_gmm_file : Optional[Target_gmm_file] = None

    degree_of_freedom : Optional[Degree_of_freedom] = None
    #degree_of_freedom : Optional[float] = None



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

    project = ImpProject()

    if config_file is None:
        logging.info('missing config content !' )
    else:
        #obj = yaml.load(config_file, Loader=yaml.FullLoader)
        obj = yaml.safe_load(config_file)
        
        #obj = load_yaml_config(config_file)
        
        logging.info('config content %s!' % obj)
        project = from_dict(data_class=ImpProject, data=obj)
        logging.info('set title_id %s!' % project.title_id)
        logging.info('set title %s!' % project.title)
        logging.info('set states %s!' % project.states)
        logging.info('set sampling_frame %s!' % project.sampling_frame)
        logging.info('set output_dir %s!' % project.output_dir)
        #logging.info('set crosslink_distance %s!' % project.crosslink_distance)
        logging.info('set namespaces %s!' % project.namespaces)
        # crosslinkdb
        #logging.info('set crosslinkdb %s!' % project.crosslinkdb)
        # export_formats
        # logging.info('set export_fmts %s!' % project.export_formats)
        # data_directory
        logging.info('set data_directory %s!' % project.data_directory)

        logging.info('set xl_groupA %s!' % project.xl_groupA)
       # logging.info('set xl_groupB %s!' % project.xl_groupB)
       # logging.info('set xl_groupC %s!' % project.xl_groupC)

        #topology_file
        logging.info('set topology_file %s!' % project.topology_file)

        #target_gmm_file
        logging.info('set target_gmm_file %s!' % project.target_gmm_file)

        #degree_of_freedom
        logging.info('set degree_of_freedom %s!' % project.degree_of_freedom)
        logging.info('set degree_of_freedom.max_rb_trans %s!' % project.degree_of_freedom.max_rb_trans)

        #xl_db
        #logging.info('set xl_db %s!' % project.xl_db)

        #xl_dbA
        logging.info('set xl_dbA %s!' % project.xl_dbA)
        logging.info('set xl_dbA first %s!' % project.xl_dbA[0].refid)
        logging.info('set xl_dbA second %s!' % project.xl_dbA[1].refid)
        logging.info('set xl_dbA count %s!' % len(project.xl_dbA))

        for i in range(len(project.xl_dbA) ): 
            logging.info(project.xl_dbA[i]) 

        #List[CrossLink_db]
        # Using enumerate()  
        #for i, val in enumerate(project.xl_groupA): 
        #    logging.info(i, ",",val) 

        # Getting length of list 
        length = len(project.xl_groupA) 
        i = 0
   
        # Iterating using while loop 
        while i < length: 
            logging.info(project.xl_groupA[i])
            #"refid","length","slope","resolution","label","weight","crosslink_distance"

            logging.info(project.xl_groupA[i].refid)
            logging.info(project.xl_groupA[i].length)
            logging.info(project.xl_groupA[i].slope)
            logging.info(project.xl_groupA[i].resolution)
            logging.info(project.xl_groupA[i].label)
            logging.info(project.xl_groupA[i].weight)
            logging.info(project.xl_groupA[i].crosslink_distance)
            i += 1

        #dir(project.xl_groupA[i])

        #for i in range(len(project.xl_groupA) ): 
        #    print(project.xl_groupA[i]) 

        # logging.info('set xl_dbB %s!' % project.xl_dbB)
        # logging.info('set xl_dbC %s!' % project.xl_dbC)

        # perform pipeline setup
        model_pipeline(project)



    if title:
        #project.title = title
        logging.info('given title %s!' % title)
    

def seed(config, title):
    """
    Seeds an ontology project
    """

    #mg = Generator()

    #mg.
    load_config(config,
                   title=title)
    #project = mg.context.project

def mkdir(adddirname):
    if not os.path.exists(adddirname):
        os.makedirs(adddirname)


def model_pipeline(project):
    """
    Model pipeline for IMP project
    """

    logging.info('model_pipeline title_id %s!' % project.title_id)

    #---------------------------
    # Define Input Files
    # The first section defines where input files are located. 
    # The topology file defines how the system components are structurally represented. 
    # target_gmm_file stores the EM map for the entire complex, which has already been converted into a Gaussian mixture model.
    #---------------------------
    datadirectory = project.data_directory 
    #"C:/dev/project/py_imp/py_imp/pmi_tut/rnapolii/data/"

    # C:/Users/adminL/source/repos/py_imp/py_imp/pmi_tut/rnapolii/data/
    logging.info('config data_directory %s!' % datadirectory)




    # Start by getting directory paths
    #this_path = os.path.dirname(os.path.realpath(__file__)) + "/"
    #cwd = os.getcwd()
    this_path = project.data_directory
    mkdir(this_path)
 
    # these paths are relative to the topology file
    pdb_dir = this_path + "./data/xtal"
    fasta_dir = this_path + "./data/fasta"
    gmm_dir = this_path + "./data/em"
    xl_dir = this_path + "./data/xl"
    topo_dir = this_path + "./data/topo"

    #pdb_dir = this_path + "../data/xtal"
    #fasta_dir = this_path + "../data/fasta"
    #gmm_dir = this_path + "../data/em"
    #xl_dir = this_path + "../data/xl"
    #topo_dir = this_path + "../data/topo"


    logging.info('this_path %s!' % this_path)

    logging.info('pdb_dir %s!' % pdb_dir)
    logging.info('fasta_dir %s!' % fasta_dir)
    logging.info('gmm_dir %s!' % gmm_dir)
    logging.info('xl_dir %s!' % xl_dir)
    logging.info('topo_dir %s!' % topo_dir)

    #if not os.path.exists(pdb_dir):
    #    os.makedirs(pdb_dir)
    #mkdir(pdb_dir)
    #mkdir(fasta_dir)
    #mkdir(gmm_dir)
    #mkdir(xl_dir)
    #mkdir(topo_dir)

    topology_file = topo_dir+'/'+project.topology_file
    target_gmm_file = gmm_dir+'/'+project.target_gmm_file
    
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

 
    class nonMSStudioCrosslinks:
        # Class that converts an MS Studio crosslink file
        # into a csv file and corresponding IMP CrossLinkDataBase object
        def __init__(self, infile, indbA):
            self.infile = infile
            self.indbA = indbA
            self.xldbkc = self.get_xldbkc()
            self.xldb = IMP.pmi.io.crosslink.CrossLinkDataBase(self.xldbkc)
            self.xldb.create_set_from_file(self.infile, self.xldbkc)

        def get_xldbkc(self):
            # Creates the keyword converter database to translate MS Studio column names
            # into IMP XL database keywords
            xldbkc = IMP.pmi.io.crosslink.CrossLinkDataBaseKeywordsConverter()
            logging.info('set xl_dbA %s!' % self.indbA.refid)
            logging.info('set xl_dbA set_protein1_key %s!' % self.indbA.set_protein1_key)
            logging.info('set xl_dbA set_protein2_key %s!' % self.indbA.set_protein2_key)
            logging.info('set xl_dbA set_residue1_key %s!' % self.indbA.set_residue1_key)
            logging.info('set xl_dbA set_residue2_key %s!' % self.indbA.set_residue2_key)
          
            xldbkc.set_protein1_key(self.indbA.set_protein1_key)
            xldbkc.set_protein2_key(self.indbA.set_protein2_key)
            xldbkc.set_residue1_key(self.indbA.set_residue1_key)
            xldbkc.set_residue2_key(self.indbA.set_residue2_key)
            return xldbkc

        def parse_infile(self):
            # Returns a list of each crosslink's attributes as a dictionary.
            import csv
            return csv.DictReader(open(self.infile), delimiter=',', quotechar='"')

        def get_database(self):
            return self.xldb




    # Topology file should be in the same directory as this script
    #topology_file = this_path +"../topology/topology.txt"

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
    toporeader = IMP.pmi.topology.TopologyReader(topology_file,
                                      pdb_dir=pdb_dir,
                                      fasta_dir=fasta_dir,
                                      gmm_dir=gmm_dir)

    # Use the BuildSystem macro to build states from the topology file
    
    bldsys = IMP.pmi.macros.BuildSystem(mdl)
    

    # Each state can be specified by a topology file.
    
    bldsys.add_state(toporeader)
    

    #Building the System Representation and Degrees of Freedom
    #Here we can set the Degrees of Freedom parameters, which should be optimized according to MC acceptance ratios. There are three kind of movers: Rigid Body, Bead, and Super Rigid Body (super rigid bodies are sets of rigid bodies and beads that will move together in an additional Monte Carlo move).
    #max_rb_trans and max_rb_rot are the maximum translation and rotation of the Rigid Body mover, max_srb_trans and max_srb_rot are the maximum translation and rotation of the Super Rigid Body mover and max_bead_trans is the maximum translation of the Bead Mover.
    #The execution of the macro will return the root hierarchy (root_hier) and the degrees of freedom (dof) objects, both of which are used later on.



    # Build the system representation and degrees of freedom
    
    root_hier, dof = bldsys.execute_macro(max_rb_trans=project.degree_of_freedom.max_rb_trans,
                                      max_rb_rot=project.degree_of_freedom.max_rb_rot,
                                      max_bead_trans=project.degree_of_freedom.max_bead_trans,
                                      max_srb_trans=project.degree_of_freedom.max_srb_trans,
                                      max_srb_rot=project.degree_of_freedom.max_srb_rot)
    

    #root_hier, dof = bldsys.execute_macro()
    """
    fb = dof.create_flexible_beads(mol.get_non_atomic_residues(),
                           max_trans=bead_max_trans)
    """
    print(dof.get_rigid_bodies() )

    print(toporeader.get_rigid_bodies() )


    #outputobjects=[]

    # Fix all rigid bodies but not Rpb4 and Rpb7 (the stalk)
    # First select and gather all particles to fix.
    fixed_particles=[]
    for prot in ["Rpb1","Rpb2","Rpb3","Rpb5","Rpb6","Rpb8","Rpb9","Rpb10","Rpb11","Rpb12"]:
        fixed_particles+=IMP.atom.Selection(root_hier,molecule=prot).get_selected_particles()

    # Fix the Corresponding Rigid movers and Super Rigid Body movers using dof
    # The flexible beads will still be flexible (fixed_beads is an empty list)!
    fixed_beads,fixed_rbs=dof.disable_movers(fixed_particles,
                                             [IMP.core.RigidBodyMover,
                                              IMP.pmi.TransformMover])

    # Randomize the initial configuration before sampling, of only the molecules
    # we are interested in (Rpb4 and Rpb7)
    IMP.pmi.tools.shuffle_configuration(root_hier,
                                        excluded_rigid_bodies=fixed_rbs,
                                        max_translation=50,
                                        verbose=False,
                                        cutoff=5.0,
                                        niterations=100)

    outputobjects = [] # reporter objects (for stat files)

    #-----------------------------------
    # Define Scoring Function Components
    #-----------------------------------

    # Here we are defining a number of restraints on our system.
    #  For all of them we call add_to_model() so they are incorporated into scoring
    #  We also add them to the outputobjects list, so they are reported in stat files

    # Connectivity keeps things connected along the backbone (ignores if inside
    # same rigid body)
    mols = IMP.pmi.tools.get_molecules(root_hier)
    for mol in mols:
        molname=mol.get_name()
        IMP.pmi.tools.display_bonds(mol)
        cr = IMP.pmi.restraints.stereochemistry.ConnectivityRestraint(mol,scale=2.0)
        cr.add_to_model()
        cr.set_label(molname)
        outputobjects.append(cr)

    # Excluded Volume Restraint
    #  To speed up this expensive restraint, we operate it at resolution 20
    ev = IMP.pmi.restraints.stereochemistry.ExcludedVolumeSphere(
                                             included_objects=root_hier,
                                             resolution=10)
    ev.add_to_model()
    outputobjects.append(ev)


    
    
    # Getting length of list 
    length = len(project.xl_groupA) 
    i = 0
    
    xlList=[]

    # Iterating using while loop 
    while i < length: 
        logging.info(project.xl_groupA[i])
        #"refid","length","slope","resolution","label","weight","crosslink_distance"

        logging.info(project.xl_groupA[i].refid)
        logging.info(project.xl_groupA[i].length)
        logging.info(project.xl_groupA[i].slope)
        logging.info(project.xl_groupA[i].resolution)
        logging.info(project.xl_groupA[i].label)
        logging.info(project.xl_groupA[i].weight)
        logging.info(project.xl_groupA[i].crosslink_distance)


    
        # Set up crosslinking restraint
        xlA = XLRestraint(root_hier=root_hier, 
                 CrossLinkDataBase=nonMSStudioCrosslinks(xl_dir + "/" + project.xl_groupA[i].refid, project.xl_dbA[i]).get_database(),
                 length=project.xl_groupA[i].length, #midpoint? Double check with Daniel and excel function thing
                 resolution=project.xl_groupA[i].resolution, #keep 1, lower limit
                 slope=project.xl_groupA[i].slope, # 0.01 for longer XL and 0.03 for shorter, range - check by making sure midpoint is less than 0.5 e.g 30 * 0.01
                 label=project.xl_groupA[i].label,
                 filelabel=project.xl_groupA[i].label,
                 weight=project.xl_groupA[i].weight) #ignore weight, calculated via IMP
        logging.info(xlA)
        xlList.append(xlA)
        xlA.add_to_model()
        outputobjects.append(xlA)
        dof.get_nuisances_from_restraint(xlA)
        i += 1     
 
    for i in range(len(xlList) ): 
        logging.info(xlList[i]) 
        
    xl_rests = xlList

    


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
    em_components = IMP.pmi.tools.get_densities(root_hier)

    gemt = IMP.pmi.restraints.em.GaussianEMRestraint(em_components,
                                                     target_gmm_file,
                                                     scale_target_to_mass=True,
                                                     slope=0.000001,
                                                     weight=80.0)
    gemt.add_to_model()
    outputobjects.append(gemt)

    #--------------------------
    # Monte-Carlo Sampling
    #--------------------------

    #--------------------------
    # Set MC Sampling Parameters
    #--------------------------
    #num_frames = 20000
    num_frames = 50
    #if '--test' in sys.argv: num_frames=100
    num_mc_steps = 10

    logging.info('set states %s!' % project.states)
    logging.info('set sampling_frame %s!' % project.sampling_frame)
    logging.info('set num_frames %s!' % num_frames)

    logging.info('set output_dir %s!' % project.output_dir)
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
    logging.info('set number_of_best_scoring_models=10')
    logging.info('set monte_carlo_steps %s!' % num_mc_steps)
    logging.info('set number_of_frames %s!' % num_frames)
    logging.info('set global_output_directory %s!' % "output")




    # https://integrativemodeling.org/2.10.1/doc/ref/classIMP_1_1pmi_1_1macros_1_1ReplicaExchange0.html#a239c4009cc04c70236730479f9f79744
    # This object defines all components to be sampled as well as the sampling protocol
    mc1=IMP.pmi.macros.ReplicaExchange0(mdl,
                                        root_hier=root_hier,
                                        monte_carlo_sample_objects=dof.get_movers(),
                                        output_objects=outputobjects,
                                        crosslink_restraints=xl_rests, #[xl1,xl2],    # allows XLs to be drawn in the RMF files
                                        monte_carlo_temperature=1.0,
                                        simulated_annealing=True,
                                        simulated_annealing_minimum_temperature=1.0,
                                        simulated_annealing_maximum_temperature=2.5,
                                        simulated_annealing_minimum_temperature_nframes=200,
                                        simulated_annealing_maximum_temperature_nframes=20,
                                        replica_exchange_minimum_temperature=1.0,
                                        replica_exchange_maximum_temperature=2.5,
                                        number_of_best_scoring_models=10,
                                        monte_carlo_steps=num_mc_steps,
                                        number_of_frames=num_frames,
                                        global_output_directory="output")

    # Start Sampling
    mc1.execute_macro()



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








@click.command()
@click.option('--count', default=1, help='Not Used count.')
@click.option('--name', prompt='Experiment name',
              help='Experiment name.')
@click.option('-C', '--config',       type=click.File('r'))
def prep_hyperparam(count, name, config):
    """Simple program that greets NAME for a total of COUNT times."""
    #for x in range(count):
    click.echo('prep_hyperparam %s!' % name)
    logging.info('prep_hyperparam %s!' % name)

    #project = ImpProject()
    seed(config,name)


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
    prep_hyperparam()

