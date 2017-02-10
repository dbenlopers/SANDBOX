'''

'''


import os
import sys
#import scipy.cluster.hierarchy as hierarch

import IMP
import HGM.helpers,HGM.cluster

from alternate_configs import configs

#from matplotlib import pyplot as plt

#config_name_for_this_run    = "arp_EM_0_2"
#config_name_for_this_run    = "arp_EM_0_2a"

#config_name_for_this_run    = "arp_EM_0_2aLM"
#config_name_for_this_run    = "arp_EM_0_2aL"
#config_name_for_this_run    = "arp_EM_0_2aLA"

#config_name_for_this_run    = "arp_EM_0_2aLA1"
#config_name_for_this_run    = "arp_EM_0_2aLA2"
#config_name_for_this_run    = "arp_EM_0_2aLA3"
#config_name_for_this_run    = "arp_EM_0_2aLA"
#config_name_for_this_run    = "arp_EM_0_2aLA5"
#config_name_for_this_run    = "arp_EM_0_2aLA6"
#config_name_for_this_run    = "arp_EM_0_2aLA7"
#config_name_for_this_run    = "arp_EM_0_2aLA8"

#config_name_for_this_run    = "arp_EM_0_2aLAI2"
#config_name_for_this_run    = "arp_EM_0_2aLAI4"
#config_name_for_this_run    = "arp_EM_0_2aLAI5"

#config_name_for_this_run    = "3NIG_EM_0_2aC"
#config_name_for_this_run    = "3NIG_EM_0_2lC"
#config_name_for_this_run    = "3NIG_EM_0_2lC_20" 
config_name_for_this_run    = "3NIG_EM_0_2lC_f"

cplxRepresentationFileName  = configs[config_name_for_this_run][0]
def build_subunits_info():
    print "build_subunits_info function UNDEFINED\n Don't know how to build subunits !!!\n EMERGENCY STOP"
    sys.exit(1)
exec ( "from {0:s} import build_subunits_info".format( cplxRepresentationFileName ) )


ignore_precomputed_matrix = False
#ignore_precomputed_matrix = True

#linkageMethodList=["single","complete","average","weighted","centroid","median"]
#linkageMethodList=["single","complete","average","weighted"]
#linkageMethodList=["single","complete","average","centroid"]
#linkageMethodList=["complete"]
linkageMethodList=["centroid"]
#linkageMethodList=["single"]

dendo_figsize=(16,6)




runDir                      = os.path.join("results",config_name_for_this_run)
sDir                        = os.path.join(runDir,"samples")
asDir                       = os.path.join(runDir,"samples-alt")
cDir                        = os.path.join(runDir,"clusters")
gDir                        = os.path.join(runDir,"graphics")
gcDir                       = os.path.join(gDir,"clusters")

dendoDir                    = gcDir

for d in [cDir,gDir,gcDir] :
    HGM.helpers.check_or_create_dir(d)

#sample_tag



# #
# #    SPECIFIC SAMPLE
# #
#tag,nb = ("low",2000)
tag,nb = ("low",1000)
#tag,nb = ("low",500)
#tag,nb = ("low",100)
sample_tag          = "-".join([config_name_for_this_run,tag,str(nb)])
#lowFileName         = tag + "_energy_subsamples__100__"+str(nb)+".txt"
lowFileName         = tag + "_energy_subsamples__0-50__"+str(nb)+".txt"
lowEFilePath        = os.path.join(asDir,lowFileName)
#highEFilePath       = os.path.join(asDir,highFileName)
samplePathes=[lowEFilePath]


## #
## #    ALL
## #
#sample_indices          = range(10)
##sample_indices          = range(100)
##
##sample_indices          = HGM.helpers.read_all_sample_indices(sDir, savePrefix)
##sample_indices = sample_indices[:100]
##
#sample_tag      = config_name_for_this_run+"-"+str(len(sample_indices)*200)
#samplePathes    = HGM.helpers.forge_sample_pathes_from_indices( sDir , sample_indices )

    
def generate_observation_matrix_from_configs_domain(mcs,subunit,i):
    #mcss = HGM.representation.MyConfigurationSet()
    modelInfo = mcs.get_prot_info_model()
    
    print subunit


    xyzl = HGM.helpers.get_XYZdecorated_particles([modelInfo.get_subunit_info(subunit).get_bead(i).get_particle()])
    X=[]
    for j in range( mcs.get_number_of_configurations() ):
        mcs.load_configuration(j)
        X.append( HGM.helpers.gather_coordinates_for_current_config(xyzl) )
    return X



def init_model():
    m = IMP.Model()
    m.set_log_level(IMP.SILENT)
    cplxInfos = build_subunits_info(m)
    HGM.helpers.mute_all_restraints(m) 
    mcs         = HGM.representation.MyConfigurationSet(cplxInfos)
    return mcs

    
def forge_dendo_filePath(linkage_meth,tag=sample_tag,basedir=dendoDir):
    dendo_fileName = HGM.cluster.forge_dendo_file_name(linkage_meth, tag)
    return os.path.join(basedir,dendo_fileName)

def main():
    
    observation_matrix = None
    
    for linkage_meth in linkageMethodList:
        print "- linkage method",linkage_meth
        lmPath = HGM.cluster.get_linkage_matrix_file_path(linkage_meth, sample_tag, cDir)
        
        try:
            if ignore_precomputed_matrix :
                raise Exception()
            lm=HGM.cluster.read_linkage_matrix_from_file(lmPath)
            print "  got linkage matrix from file"
        except:
            print "  no linkage matrix found, computing one"
            if observation_matrix == None :
                print "  first of all, gathering observation matrix",
                mcs = init_model()
                HGM.helpers.read_models_from_pathes(mcs, samplePathes)
#                nb_mdls_l = HGM.helpers.read_models_from_pathes(mcs, samplePathes)
#                write_sample_indices_to_file(samplePathes,nb_mdls_l)
#                observation_matrix = HGM.cluster.get_observation_matrix_from_config(mcs, particles)
                observation_matrix = HGM.cluster.compute_observation_matrix_from_config(mcs)
                #observation_matrix = generate_observation_matrix_from_configs_domain(mcs, '3NIGC', 0)
                print "  ...done"
            lm = HGM.cluster.compute_linkage_matrix_from_observations(observation_matrix, linkage_meth)
            HGM.cluster.write_linkage_matrix_to_file(lm, lmPath)
        
        dendoFilePath = forge_dendo_filePath(linkage_meth)
        HGM.cluster.plot_dendogram(dendoFilePath,lm,dendo_figsize)
        print "plotted dendogram at",dendoFilePath
        
            
if __name__ == "__main__" :
    main()
    print "...That's all folks !"
    
    
