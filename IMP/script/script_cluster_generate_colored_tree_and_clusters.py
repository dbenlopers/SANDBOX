'''


compute clusters on a sample
in : 
 linkage matrix (attached to linkage method and sample)
 threshold to cut the linkage matrix (or number of clusters)
out :
 colored dendogram
 clusters
'''



import os
import sys
import scipy.cluster.hierarchy as hierarch

import IMP
import HGM.helpers,HGM.cluster

from alternate_configs import configs

from matplotlib import pyplot as plt

#config_name_for_this_run    = "arp_EM_0_2"
#config_name_for_this_run    = "arp_EM_0_2a"

#config_name_for_this_run    = "arp_EM_0_2aLM"
#config_name_for_this_run    = "arp_EM_0_2aL"
#config_name_for_this_run    = "arp_EM_0_2aLA"

config_name_for_this_run    = "arp_EMd_0_2aLM"

#config_name_for_this_run    = "arp_EM_0_2aLAI5"

#cplxRepresentationFileName  = configs[config_name_for_this_run][0]
#def build_subunits_info():
#    print "build_subunits_info function UNDEFINED\n Don't know how to build subunits !!!\n EMERGENCY STOP"
#    sys.exit(1)
#exec ( "from {0:s} import build_subunits_info".format( cplxRepresentationFileName ) )


#ignore_precomputed_matrix = False
#ignore_precomputed_matrix = True

#linkageMethodList=["single","complete","average","weighted","centroid","median"]
#linkageMethodList=["single","complete","average","weighted"]
linkageMethodList=["complete"]
threshold_cuts_for_method = {
    "single" : [30],
#    "complete": [10,20,30,40,50],
#    "complete": [15,20],
    "complete":[15],
#    "complete":[14],
    "average":  [30],
    "weighted": [30],
    
    "centroid": [30],
    "median":   [30]
                             }

dendo_figsize=(16,6)

#NUM_REQUESTED_CLUSTERS          = [10]  # not used
NUM_DISTINCT_COLORS             = 20


runDir                      = os.path.join("results",config_name_for_this_run)
sDir                        = os.path.join(runDir,"samples")
asDir                       = os.path.join(runDir,"samples-alt")
cDir                        = os.path.join(runDir,"clusters")
gDir                        = os.path.join(runDir,"graphics")
gcDir                       = os.path.join(gDir,"clusters")

dendoDir                    = gcDir



#sample_tag



 #
 #    SPECIFIC SAMPLE
 #
tag,nb = ("low",2000)
#tag,nb = ("low",1000)
#tag,nb = ("low",100)
sample_tag          = "-".join([config_name_for_this_run,tag,str(nb)])
lowFileName         = tag + "_energy_subsamples__100__"+str(nb)+".txt"
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


#write_cluster_ids = False
write_cluster_ids = True
## #    default : coloring with random colors
## # change number of colors with NUM_DISTINCT_COLORS defined upper in the file
#cluster_colors  = None
#nb_clusters     = None
## #    specific run
cluster_colors  = { 
    1:"red",
    4:"orange",
    5:"burlywood",
    9:"g",# "green"
    10:"#0fff0f",
    11:"#2fd050"
    }
nb_clusters     = 11


def main():
    for linkage_meth in linkageMethodList :
        print "- linkage method",linkage_meth
        lmPath = HGM.cluster.get_linkage_matrix_file_path(linkage_meth, sample_tag, cDir)
        try:
            lm=HGM.cluster.read_linkage_matrix_from_file(lmPath)
        except:
            print "can't find a linkage matrix\n consider to run script >script_cluster_generate_cluster_tree.py< first\n I stop here !"
            sys.exit()
        
        thresholds = None
#        try:
#            nb_clustl   = NUMBER_OF_REQUESTED_CLUSTERS
#            get_threshold = lambda nb_c: HGM.cluster.get_threshold_for_number_of_clusters(lm,nb_c)
#            thresholds  = map(get_threshold, nb_clustl)
#        except:
        thresholds  = threshold_cuts_for_method[linkage_meth]
            
        
        for t in thresholds :
            print "  -cutting at threshold",t
            
            gccDir = os.path.join(gcDir,HGM.cluster.forge_cluster_dir_name(t,linkage_meth,sample_tag))
            HGM.helpers.check_or_create_dir(gccDir)
        
            dendoFileName   = HGM.cluster.forge_dendo_file_name(linkage_meth, sample_tag, t)            
            dendoFilePath   = os.path.join(gccDir,dendoFileName)
            
            if cluster_colors == None :
                colors = HGM.helpers.get_distinct_colors(NUM_DISTINCT_COLORS)
                colors = HGM.helpers.convert_rgba_colors_to_matplotlib_strings(colors)
            else :
                colors = HGM.cluster.make_cluster_colors_list(cluster_colors,nb_clusters) 
                
            HGM.cluster.plot_dendogram(dendoFilePath,lm,dendo_figsize,color_threshold=t, cluster_colors=colors)
        
        if write_cluster_ids == True :
            print "writing cluster ids to file",
            cfilePath = HGM.cluster.forge_cluster_ids_file_path(cDir,thresholds, linkage_meth, sample_tag)
            print cfilePath 
            HGM.cluster.write_cluster_id_for_thr_to_file( lm , cfilePath , thresholds )
        

if __name__ == "__main__" :
    main()
    print "...that's all folks"




