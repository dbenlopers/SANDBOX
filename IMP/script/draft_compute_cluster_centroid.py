'''
'''

import numpy as np
import scipy, scipy.spatial, scipy.spatial.distance
import operator

import HGM
import HGM.samples
import HGM.helpers
from alternate_configs import configs

import IMP
import IMP.algebra

import os

runDir                      = os.path.join("results","tests")
models_filePath             = os.path.join(runDir,"id_clust_17.txt")
centroids_filePath          = os.path.join(runDir,"id_clust_17__centers.txt")



for d in [runDir] :
    HGM.helpers.check_or_create_dir(d)
    
    
config_name_for_this_run    = "arp_EM_0_2aLM"
subunitsRepresentationFileName = configs[config_name_for_this_run][0]
exec ( "from {0:s} import build_subunits_info".format( subunitsRepresentationFileName ) )
    
    
def test():
    print "setup "
    
    m = IMP.Model()
    m.set_log_level(IMP.SILENT)
    print " -- crowding universe"
    cplxInfos = build_subunits_info(m)
    HGM.helpers.mute_all_restraints(m)
    
    print "read models"
    mcs     = HGM.representation.MyConfigurationSet( cplxInfos )
    mcs.read_all_configs_from_file(models_filePath)

    print "centroid computation"
    c   = HGM.samples.compute_centroid_for_models( mcs, update_model = True )
    # a configuration se
    mcs_centers = HGM.representation.MyConfigurationSet( mcs.get_prot_info_model() )
    mcs_centers.save_current_config()
    
    i,d = HGM.samples.compute_index_of_central_model_for_models( mcs, centroid=c )
    print "central config is the number",i,"with a distance",d,"from centroid"
    mcs.load_configuration(i)
    mcs_centers.save_current_config()
    
    print "saving all configs to file",centroids_filePath
    mcs_centers.save_all_configs_to_file(centroids_filePath)
    
if __name__ == "__main__" :
    print "running test"
    test()
    print "...that's all folks ?"
