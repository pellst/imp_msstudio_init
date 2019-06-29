import optparse
import logging
import yaml

#C:\apps\Anaconda3\python.exe demo_click_v2.py --count=1 --name=Demo --config="impProjectA.yaml"

"""
 example yaml
title_id: 12345
title: imp config settings
states: 1
sampling_frame: 1000
output_dir: c:\tmp\
crosslink_distance: 10.834
"""


"""
datadirectory = "C:/dev/project/py_imp/py_imp/pmi_tut/rnapolii/data/"
topology_file = datadirectory+"topology.txt"
target_gmm_file = datadirectory+'emd_1883.map.mrc.gmm.50.txt'


# Build the system representation and degrees of freedom
root_hier, dof = bs.execute_macro(max_rb_trans=4.0,
                                  max_rb_rot=0.3,
                                  max_bead_trans=4.0,
                                  max_srb_trans=4.0,
                                  max_srb_rot=0.3)


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




# accommodate multiple crosslink datasets. here is the first one:

# Crosslinks - dataset 1
#  To use this restraint we have to first define the data format
#  Here assuming that it's a CSV file with column names that may need to change
#  Other options include the linker length and the slope (for nudging components together)
xldbkwc = IMP.pmi.io.crosslink.CrossLinkDataBaseKeywordsConverter()
xldbkwc.set_protein1_key("pep1.accession")
xldbkwc.set_protein2_key("pep2.accession")
xldbkwc.set_residue1_key("pep1.xlinked_aa")
xldbkwc.set_residue2_key("pep2.xlinked_aa")

xl1db = IMP.pmi.io.crosslink.CrossLinkDataBase(xldbkwc)
xl1db.create_set_from_file(datadirectory+'polii_xlinks.csv')

xl1 = IMP.pmi.restraints.crosslinking.CrossLinkingMassSpectrometryRestraint(
                                   root_hier=root_hier,
                                   CrossLinkDataBase=xl1db,
                                   length=21.0,
                                   slope=0.01,
                                   resolution=1.0,
                                   label="Trnka",
                                   weight=1.)

xl1.add_to_model()             # crosslink must be added to the model

https://pypi.org/project/dacite/

"""

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

        if section == "xl_groupA":
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
 



    if title:
        #project.title = title
        logging.info('given title %s!' % title)


def seed(config, title):
    """
    Seeds an imp modeling project
    """

    load_config(config,
                   title=title)


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
    logging.basicConfig(filename='app_demo_click.log', filemode='w', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)

    logging.debug('This is a debug message')
    logging.info('This is an info message')
    logging.warning('This is a warning message')
    logging.error('This is an error message')
    logging.critical('This is a critical message')
    prep_hyperparam(options.count, options.name, options.config)


