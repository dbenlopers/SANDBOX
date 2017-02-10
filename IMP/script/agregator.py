
import os
import sys
#import scipy.cluster.hierarchy as hierarch

import IMP
import HGM.helpers
import HGM.representation

import glob

from alternate_configs import configs


config_name_for_this_run    = "3NIG_EM_0_4l_f_20"

cplxRepresentationFileName  = configs[config_name_for_this_run][0]
def build_subunits_info():
    print "build_subunits_info function UNDEFINED\n Don't know how to build subunits !!!\n EMERGENCY STOP"
    sys.exit(1)
exec ( "from {0:s} import build_subunits_info".format( cplxRepresentationFileName ) )


runDir                      = os.path.join("results",config_name_for_this_run)
sDir                        = os.path.join(runDir,"samples")
asDir                       = os.path.join(runDir,"samples-alt")
cDir                        = os.path.join(runDir,"clusters")
gDir                        = os.path.join(runDir,"graphics")
gcDir                       = os.path.join(gDir,"clusters")
c_domDir                    = os.path.join(cDir,'by_domaine')

clustDir = "/home/arnaud/Desktop/TFIIH/src/coarse2/results/3NIG_EM_0_4l_f_20/clusters/cluster_samples_centroid_file-9-meth:centroid low-1000"
clustersFilePath = "/home/arnaud/Desktop/TFIIH/src/coarse2/results/3NIG_EM_0_4l_f_20/clusters/cluster_samples_centroid_file-9-meth:centroid low-1000/all_clusters_representatives.txt"

def init_cplx():
    m = IMP.Model()
    m.set_log_level(IMP.SILENT)
    cplxinfos = build_subunits_info(m)
    return cplxinfos 

def get_cluster_representatives_pathes():
    fps = glob.glob( os.path.join(clustDir,"id_clust_*.txt") )
    return fps
    
def get_clusters_representatives(cplxInfo,files):
    mcs=HGM.representation.MyConfigurationSet(cplxInfo)
    for f in files :
        print "reading from",f
        mcs.read_configs_from_file(f,[1])
    return mcs

def main():
    print "getting cluster representative file pathes...",
    fps = get_cluster_representatives_pathes()
    print "got",len(fps),"pathes" 
    cplxInfo = init_cplx()
    print "loading cluster representatives...",
    mcs = get_clusters_representatives(cplxInfo,fps)
    print "got",mcs.get_number_of_configurations(),"configs"
    print "saving representatives"
    mcs.save_all_configs_to_file(clustersFilePath)
    




if __name__ == "__main__" :
    main()
    print "...that's all folks !"
    
    
    
    
    
