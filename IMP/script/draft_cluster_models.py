'''
Created on 17 oct. 2012

'''

import IMP, IMP.algebra, IMP.core, IMP.atom

import HGM, HGM.helpers, HGM.helpersPlot, HGM.representation

import scipy
import scipy.cluster.hierarchy as hierarch

import sys
import os

from alternate_configs import configs

import matplotlib
from matplotlib import pyplot as plt

import pickle
import math



#config_name_for_this_run    = "3NIG_EM_0_2aC"                  
#config_name_for_this_run    = "3NIG_EM_0_2aC_20"     
#config_name_for_this_run    = "3NIG_EM_0_2lmC"
#config_name_for_this_run    = "3NIG_EM_0_2lmC_20"
#config_name_for_this_run    = "3NIG_EM_0_2lC"
#config_name_for_this_run    = "3NIG_EM_0_2lC_20" 
#config_name_for_this_run    = "3NIG_EM_0_3ambiC"  
#config_name_for_this_run    = "3NIG_EM_0_3ambiC_20"

#config_name_for_this_run    = "3NIG_EM_0_2aC_f"                  
#config_name_for_this_run    = "3NIG_EM_0_2aC_f_20"     
#config_name_for_this_run    = "3NIG_EM_0_2lmC_f"
#config_name_for_this_run    = "3NIG_EM_0_2lmC_f_20"
#config_name_for_this_run    = "3NIG_EM_0_2lC_f"
#config_name_for_this_run    = "3NIG_EM_0_2lC_f_20" 
#config_name_for_this_run    = "3NIG_EM_0_3ambiC_f"  
#config_name_for_this_run    = "3NIG_EM_0_3ambiC_f_20"

#config_name_for_this_run    =  "3NIG_EM_0_4a_f"
#config_name_for_this_run    = "3NIG_EM_0_4a_f_20"
#config_name_for_this_run    = "3NIG_EM_0_4lm_f"
#config_name_for_this_run    = "3NIG_EM_0_4lm_f_20"
#config_name_for_this_run    = "3NIG_EM_0_4l_f"
#config_name_for_this_run    = "3NIG_EM_0_4l_f_20"
          
#config_name_for_this_run    = "3NIG_EM_0_5a_f"
#config_name_for_this_run    = "3NIG_EM_0_5a_f_20"
#config_name_for_this_run    = "3NIG_EM_0_5lm_f"
#config_name_for_this_run    = "3NIG_EM_0_5lm_f_20"
#config_name_for_this_run    = "3NIG_EM_0_5l_f"
config_name_for_this_run    = "3NIG_EM_0_5l_f_20"

#config_name_for_this_run    = "3IAM_EM_0_1aC"
#config_name_for_this_run    = "3IAM_EMc_0_1aC"
#config_name_for_this_run    = "3IAM_EM_0_2aC"
#config_name_for_this_run    = "3IAM_EMc_0_2aC"


#config_name_for_this_run    = "3IAM_EM_0_3a"
#config_name_for_this_run    = "3IAM_EM_0_3lm"
#config_name_for_this_run    = "3IAM_EM_0_3l"

#config_name_for_this_run    = "3IAM_EM_0_4a"
#config_name_for_this_run    = "3IAM_EM_0_4lm"
#config_name_for_this_run    = "3IAM_EM_0_4l"

#config_name_for_this_run    = "3IAM_EM_0_5a"
#config_name_for_this_run    = "3IAM_EM_0_5lm"
#config_name_for_this_run    = "3IAM_EM_0_5l"

# config_name_for_this_run    = "4FXG_EM_0_1a_40"
# config_name_for_this_run    = "4FXG_EM_0_1lm_40"
# config_name_for_this_run    = "4FXG_EM_0_1l_40"
# config_name_for_this_run    = "4FXG_EM_0_1a_30"
# config_name_for_this_run    = "4FXG_EM_0_1lm_30"
# config_name_for_this_run    = "4FXG_EM_0_1l_30"
# config_name_for_this_run    = "4FXG_EM_0_1a_20"
# config_name_for_this_run    = "4FXG_EM_0_1lm_20"
# config_name_for_this_run    = "4FXG_EM_0_1l_20"

#config_name_for_this_run    = "4FXG_EM_0_2a_40"
#config_name_for_this_run    = "4FXG_EM_0_2lm_40"
#config_name_for_this_run    = "4FXG_EM_0_2l_40"
#config_name_for_this_run    = "4FXG_EM_0_2a_20"
#config_name_for_this_run    = "4FXG_EM_0_2lm_20"

cplxRepresentationFileName  = configs[config_name_for_this_run][0]
runDir                      = os.path.join("results",config_name_for_this_run)
sDir                        = os.path.join(runDir,"samples")
savePrefix                  = "saves"
cDir                        = os.path.join(runDir,"clusters")
gDir                        = os.path.join(runDir,"graphics")
gcDir                       = os.path.join(gDir,"clusters")

#default_kmeans_number_of_clusters   = 10
#default_kmeans_number_of_iterations = 10000

#sample_indexes      = [0]
#sampleTag           = "200"

#sample_indexes      = range(5)
#sampleTag           = "1000"
sampleFileNameList=[]
sample_indexes      = range(1,21)
#sampleTag           = "0-50"
sampleTag           = "0-50"
#nbLow               = "-"
nbLow               = "1000"
#sample_indexes      = range(50)
#sampleTag           = "10000"

distmatrixFileName          = "conformations-distmatrix--"+sampleTag+".pickle"
distmatrixFilePath          = os.path.join(cDir,distmatrixFileName)

#clustThresholds = None
#clustThresholds = {
#    "single" : 60,
#    "complete":60,
#    "average":60,
#    "weighted":60
#                   }

#threshold_cuts_for_method = {
##    "single" : [],
#    "complete": [10,15,20,25],
#    "average":  [10,15,20,25],
#    "weighted": [10,15,20,25],
#    
#    "centroid": [5,10,15,20,25],
#    "median": [5,10,15,20,25]
#                             }


# euclidian = 3*RMSD
#    [9,15,21,30,45] = [3,5,7,10,15]
#threshold_cuts_for_method = {
#    "single" : [9,15,21,30,45],
#    "complete": [9,15,21,30,45],
#    "average":  [9,15,21,30,45],
#    "weighted": [9,15,21,30,45],  
#    "centroid": [9,15,21,30,45],
#    "median":   [9,15,21,30,45]
#                             }
threshold_cuts_for_method = {
    "single" : [3,6,9,15],
    "complete": [3,6,9,15],
    "average":  [3,6,9,15],
    "weighted": [3,6,9,15],  
    "centroid": [3,6,9,15],
    "median":   [3,6,9,15]
                             }

#"dendogram-test--"+sampleTag+"--"+clustMethod+"-linkage.png"

for d in [cDir,gDir,gcDir] :
    HGM.helpers.check_or_create_dir(d)

exec ( "from {0:s} import build_subunits_info".format( cplxRepresentationFileName ) )








# ==================================================
# ==================================================
# ==================================================

def extract_clusters( flat_clusters ):
    """ Extract clusters from a fcluster output
    @param flat_cluster_numbers : a ndarray as output by scipy.cluster.hierarchy.fcluster
    @return: a dict of arrays, each array contains indices of observations that belong to the same cluster
    """
#    nb_observations = len(flat_clusters)
    clusters={}
    observation_index=0 
    for cluster_num in flat_clusters:
        try :
            clusters[cluster_num].append(observation_index)
        except KeyError :
            clusters[cluster_num] = [observation_index]
        observation_index+=1
    return clusters

def extract_clusters_as_sets( flat_clusters ):
    """ Extract clusters from a fcluster output
    @param flat_cluster_numbers : a ndarray as output by scipy.cluster.hierarchy.fcluster
    @return: a dict of sets, each set contains indices of observations that belong to the same cluster
    """
#    nb_observations = len(flat_clusters)
    clusters={}
    observation_index=0 
    for cluster_num in flat_clusters:
        try :
            clusters[cluster_num].add(observation_index)
        except KeyError :
            clusters[cluster_num] = set([observation_index])
        observation_index+=1
    return clusters

def get_score_for_fix_number_of_clusters( linkage_matrix , nb_clusters ):
    """ returns a score that can be used as a threshold to cut the linkage matrix if one desire to create a given number of clusters. 
    Such a threshold can be used e.g. with scipy.fcluster()
    @param linkage_matrix : 
    @param nb_clusters : 
    @return: a floating point number that can be used as a threshol to extract nb_clusters from linkage_matrix
    """
    retval=0.0
    if nb_clusters == 0 :
        retval=linkage_matrix[-nb_clusters][2] + 1.0
    else :
        a=linkage_matrix[1-nb_clusters][2]
        b=linkage_matrix[ -nb_clusters][2]
        retval=b+(a-b)/2
    return retval

def get_flat_clusters_for_fix_number_of_clusters( linkage_matrix , nb_clusters ):
    """ returns the flat cluster array corresponding to the linkage matrix (see scipy.linkage) for a chosen number of clusters
    @param linkage_matrix: a linkage matrix
    @param nb_clusters: how many clusters are desired
    @return : a flat cluster array, that is a list of cluster indices such that return[i] is the cluster index of observed element i
    """
#    print "lm",linkage_matrix
    t=get_score_for_fix_number_of_clusters( linkage_matrix , nb_clusters )
#    print "t",t
    flat_cluster=scipy.cluster.hierarchy.fcluster(linkage_matrix , t, criterion='distance')
#    print "fc",flat_cluster
    return flat_cluster

def extract_n_clusters_as_sets( linkage_matrix , nb_clusters ):
    """ Extract a fixed number of clusters from a linkage matrix
    @param linkage_matrix: a linkage matrix
    @param nb_clusters: how many clusters are desired
    @return: a dict of sets, each set contains indices of observations that belong to the same cluster
    """
    flat_clusters = get_flat_clusters_for_fix_number_of_clusters(linkage_matrix, nb_clusters )
    clusters=[]
    for i in range(nb_clusters) :
        clusters.append( set() )
    observation_index=0 
#    print "fc",len(flat_clusters),flat_clusters
    for cluster_num in flat_clusters:
        cluster_num -= 1
        try :
#            print cluster_num,"-",
#            print cluster_num,observation_index,"::"
            clusters[cluster_num].add(observation_index)
        except KeyError :
            print "erroneous cluster_num found ",cluster_num,"when expecting at max",nb_clusters
            raise
        observation_index+=1
#    print "cll",clusters
    return clusters

# ==================================================
# ==================================================
# ==================================================

def gather_coordinates_for_current_config(xyzl):
    """ outputs the concatenated list of partile coordinates for a given model"""
    vect = []
    for X in xyzl :
        vect.extend([X.get_x(),X.get_y(),X.get_z()])
    return vect

def compute_rmsd(coods_1,coods_2):
    rmsd2 = 0
    for i in range(len(coods_1)) :
        c=coods_1[i]-coods_2[i]
        rmsd2 += c*c
    return math.sqrt(rmsd2)

#class ClustIdx():
#    def __init__(self):
#    

def dump_cluster_id_to_file(linkMatrix,filePath,nbClusts=None):
    """uses a linkage matrix to define clusters, and print those in a csv file
    @param linkMatrix: a linkage matrix
    @param filePath: where to dump the csv file
    @param nbClusts: should be a list containing number of clusters desired
    
    The format of the csv file is in column, as follows :
    idx_config    clust_id_1    clust_id_2    clust_id_3...
    
    idx_config contains the index of a given conformation
    clust_id_i contains the cluster index for the current conformation, when considering n_i clusters
    """
    fcs = []    # I will store my flat clusters in there
    for nb in nbClusts :
        print "  - extracting",nb,"clusters"
        fcs.append ( get_flat_clusters_for_fix_number_of_clusters( linkMatrix , nb ) )

    fp = open(filePath,"w")
    fp.write("# idx_config   clust-nb :"+" ".join(map(str,nbClusts))+"\n")
    
    nb_confo = len(linkMatrix)+1
#    print "NB CONFOS",nb_confo
    
    for i in range (nb_confo) :
        clustIdxs = [ "{0:>4d}".format(int(fcs[k][i])) for k in (range(len(nbClusts))) ]
        fp.write("{0:<5d}".format(i) + " ".join(clustIdxs) + "\n")
        
    fp.close()
    
    
def dump_cluster_id_for_thr_to_file(lm,cfilePath,cutting_thresholds) :
    fcs = []    # I will store my flat clusters in there
    for thr in cutting_thresholds :
        print "  - extracting clusters for threshold",thr
        fcs.append ( scipy.cluster.hierarchy.fcluster( lm , thr, criterion='distance') )
        
    fp = open(cfilePath,"w")
    fp.write("# id_conf_file   idx_config   thr :"+" ".join(map(str,cutting_thresholds))+"\n")
    
    nb_confo = len(lm)+1
#    print "NB CONFOS",nb_confo
    
    for i in range (nb_confo) :
        clustIdxs = [ "{0:>4d}".format(int(fcs[k][i])) for k in (range(len(cutting_thresholds))) ]
        fp.write("{0:<5d}".format(i) + " ".join(clustIdxs) + "\n")
        
    fp.close()
    
    
class ConformationsDistMatrix():
    """ A class to compute and store distances between a set of configurations
        Beware, this matrix will scale as nbConfigs^2, it most probably be hell
    """
    def __eq__(self,cdm):
        """ equality check"""
        returnVal = False
        if self.get_number_of_conformations() == cdm.get_number_of_conformations():
            returnVal = True
            for i in range(0,self._nb_configs-1):
                if self._distances[i] != cdm._distances[i]:
                    returnVal = False
                    break
        return returnVal
        
    def __init__(self):
        self._distances = []
        self._nb_configs = 0
        
#    def compute (self,cs,particles):
#        """ 
#        @param cs: a configuration set object 
#        @param particles: the list of particles to consider for the alignment and the rmsd computation """
#        self._distances = []
#        self._nb_configs = cs.get_number_of_configurations()
#        
#        #
#        print "  > computing inter configuration distances"
#        for i in range(1,self._nb_configs):
#            _temp_row_distances = []
#            cs.load_configuration(i)
#            vects_i=[ IMP.algebra.Vector3D( IMP.core.XYZ_decorate_particle(p).get_coordinates() ) for p in particles ]
#            if i%15 == 0 : print ""
#            print i,".. ",
#            for j in range(0,i):
#                cs.load_configuration(j)
#                vects_j = [ IMP.algebra.Vector3D( IMP.core.XYZ_decorate_particle(p).get_coordinates() ) for p in particles ]
#                rms     = IMP.atom.get_rmsd(vects_j, vects_i)
#                _temp_row_distances.append(rms)
##                print i,j,rms
#            self._distances.append(_temp_row_distances)
#        print ""
        
        
    def compute (self,cs,particles):
        """ 
        @param cs: a configuration set object 
        @param particles: the list of particles to consider for the alignment and the rmsd computation """
        self._distances = []
        self._nb_configs = cs.get_number_of_configurations()
        
        xyzl=[ IMP.core.XYZ_decorate_particle(p) for p in particles ]
        #
        print "  > computing inter configuration distances"
        for i in range(0,self._nb_configs-1):
            _temp_row_distances = []
            cs.load_configuration(i)
#            coods1=gather_coordinates_for_current_config(xyzl)
            vects_i = [ IMP.algebra.Vector3D( IMP.core.XYZ_decorate_particle(p).get_coordinates() ) for p in particles ]
            if i%15 == 0 : print ""
            print i,".. ",
#            for j in range(0,i):
            for j in range(i+1,self._nb_configs):
                cs.load_configuration(j)
                vects_j = [ IMP.algebra.Vector3D( IMP.core.XYZ_decorate_particle(p).get_coordinates() ) for p in particles ]
#                coods2=gather_coordinates_for_current_config(xyzl)
                rms     = IMP.atom.get_rmsd(vects_j, vects_i)
#                rms = compute_rmsd(coods1, coods2)
                _temp_row_distances.append(rms)
#                print i,j,rms
            self._distances.append(_temp_row_distances)
        print ""
        
    def get_number_of_conformations(self):
        return self._nb_configs
    
    def get_conformations_distance(self,config_index_1,config_index_2):
        if config_index_1 == config_index_2 :
            return 0.
        else:
            c2,c1 = sorted([config_index_1,config_index_2])
            return self._distances[c1-1][c2]
        
    def get_half_matrix_as_vector(self):
        vect = []
        for line in self._distances :
            vect.extend(line)
        return vect
    
    def dump_as_MCL_label_input(self,fileName):
        f=open(fileName,'w')
        for i in range(1,self._nb_configs):
            for j in range(0,i):
#                f.write("{0:d} {1:d} {2:f}\n".format(i,j,self._distances[i][j]))
                f.write("{0:d} {1:d} {2:f}\n".format(i,j,self.get_conformations_distance(i,j)))
                
                
    def save_pickeled(self,filePath):
        """save a pickeled version of the matrix"""
        f=open(filePath,"w")
        pickle.dump(self._distances,f,protocol=2)
        f.close()
        
    def read_pickeled(self,filePath):
        f=open(filePath)
        self._distances = pickle.load(f)
        self._nb_configs=len(self._distances)+1
        f.close()





#def test_scy_py_clustering_methods():
#    
#    nb_clusters=5
##    nb_clusters=10
#    def create_distance_matrix(configuRationFileName):
#        print "Initialize system information"
#        protein_info_dict = build_TFIIH_subunits_info()
#        print "Create model"
#        m = IMP.Model()
#        m.set_log_level(IMP.SILENT)
#        print "Create subunits in model, along with intra subunit connectivity"
#        all = create_TFIIH_representation(m,protein_info_dict)
#        #
#        mcs = MyConfigurationSet(protein_info_dict)
#        print "Load configurations ",
##        mcs.load_all_configs_from_file("configs-save-500.txt")
##        mcs.load_all_configs_from_file(path.join(dir_configs,"configs-save-100-0.txt"))
#        mcs.load_all_configs_from_file(configurationFileName)
#        print "loaded",mcs.get_number_of_configurations(),"configurations"
#        #
#        print "Computing all against all distances"
#        particles_to_align  = IMP.core.get_le#    linkageMethodList=["centroid"]aves(all)
#        cdm                 = ConformationsDistMatrix(mcs,particles_to_align)
#        return cdm
#    def savePickleLM(fileName,linkage_matrix):
#        print "saving linkage matrix to", fileName
#        f=open(fileName,"w")
#        pickle.dump(linkage_matrix,f,protocol=2)
#        f.close()
#    def loadPickleLM(fileName):
#        print "loading linkage matrix from",fileName
#        f=open(fileName)
#        linkage_matrix = pickle.load(f)
#        f.close()
#        return linkage_matrix
#    def save_dendogram(fileName,linkage_matrix):
#        print "creating dendogram"
#        plt.figure(figsize=(16,6))
#        dendo               = hierarch.dendrogram(linkage_matrix)
#        print "saving dendogram"
#        plt.savefig(fileName,figsize=(16,6))
#        plt.clf()
##    def save_clusters(fileName,linkage_matrix,nb_clusters):
##        print "saving clusters to", fileName
##        f=open(fileName,"w")
##        pickle.dump(linkage_matrix,f,protocol=2)
##        f.close()
##    def load_clusters(fileName,linkage_matrix):
#    def print_clusters_size(linkageMethodList,clusters):
#        for meth in linkageMethodList:
#            print "*** METHOD ",meth
#            print "cluster size (",len(clusters[meth]),"):",
#            i=0
#            
#            for c in clusters[meth] :
#    #            print "c",c
#                print i,":",len(c),"..",
#                i+=1
#            print ""
#    def savePickleDistMatrix(fileName,cdm):
#        print "saving linkage matrix to", fileName
#        f=open(fileName,"w")
#        pickle.dump(cdm,f,protocol=2)
#        f.close()
#    def loadPickleDistMatrix(fileName):
#        print "loading linkage matrix from",fileName
#        f=open(fileName)
#        cdm = pickle.load(f)
#        f.close()
#        return cdm
#
#    
#    print "test_scy_py_clustering_methods START"
##    #    This part is needed to compute the link matrices, if they are loaded, you don't need that
##    configurationFileName=path.join(dir_configs,"configs-save-100-0.txt")
##    configurationFileName=path.join(dir_configs,"configs-save-1000-0.txt")
##    cdmPickleFileName=path.join(dir_clusters,"pickle-configsDistMatrix-100-0.sav")
##    cdmPickleFileName=path.join(dir_clusters,"configsDistMatrix-save-1000-0.txt")
#    cdmPickleFileName=path.join(dir_clusters,"pickelDistMatrix-aligned-1000-0.sav")
##    cdm = create_distance_matrix(configurationFileName)
##    savePickleDistMatrix(cdmPickleFileName,cdm)
##    cdm=loadPickleDistMatrix(cdmPickleFileName)
##    cdm2=loadPickleDistMatrix(cdmPickleFileName)
##    print cdm == cdm2
##    print cdm.get_conformations_distance(1, 2),cdm2.get_conformations_distance(1, 2)
##    print cdm.get_conformations_distance(10, 2),cdm2.get_conformations_distance(10, 2)
##    print cdm.get_conformations_distance(98, 6),cdm2.get_conformations_distance(98, 6)
#    
##
##    MCL CLUSTERING
##
##    print "dump mcl input file"
###    mclInputMatrixPickleFileName    =   path.join(dir_clusters,"mcl-label-input-100-0.txt")
##    mclInputMatrixPickleFileName    =   path.join(dir_mcl,"mcl-label-input-aligned-1000-0.txt")
##    cdm.dump_as_MCL_label_input(mclInputMatrixPickleFileName)
#    #
#    #    this input file is used by MCL, see script
#    #
#    
##
##    SCIPY CLUSTERING
##
##    hdm = cdm.get_half_matrix_as_vector()
##    del(cdm)   
#    clusters={}
##    linkageMethodList=["single","complete","average","weighted","centroid","median","ward"]:
#    linkageMethodList=["single","complete","average","weighted"]                
#    for meth in linkageMethodList:
#        #
##        lmPickleFileName    = path.join(dir_clusters,"pickle-test-1000-0--"+meth+"-linkMatrix.sav")
#        lmPickleFileName    = path.join(dir_clusters,"pickle-test-aligned-1000-0--"+meth+"-linkMatrix.sav")
##        print "performing",meth,"linkage"
##        lm                  = hierarch.linkage(hdm,method=meth)
##        savePickleLM(lmPickleFileName,lm)
#        print "reading",meth,"linkage" 
#        lm                  = loadPickleLM(lmPickleFileName)
#        #
###        dendoFileName       = path.join(dir_clusters, "dendogram-test-1000-0--"+meth+"-linkage.png")
##        dendoFileName       = path.join(dir_clusters, "dendogram-test-aligned-1000-0--"+meth+"-linkage.png")
##        save_dendogram(dendoFileName,lm)
##        #
#        print "decompose in",nb_clusters,"clusters"
#        
#        clusters[meth] = extract_n_clusters_as_sets( lm , nb_clusters ) 
#        
#    print ""
#    print_clusters_size(linkageMethodList,clusters)

def printDistMatrixExtremas( cdm ):
    m = cdm._distances[0][0]
    M = m
    for row in cdm._distances :
        mm,MM = min(row),max(row)
        if mm<m : m = mm
        if MM>M : M = MM
    print "distance matrix values range between",mm,"and",MM


def get_conformations_by_id(mcs):
    loop_index=0
    print "  - Reading configurations"
    for i in sample_indexes:
        loop_index+=1
        if loop_index % 15 == 0 : print ""
        print i,"..",
        sys.stdout.flush()
        sampleFilePath          = HGM.helpers.forge_sample_path(sDir, i)
        size                    = mcs.read_all_configs_from_file(sampleFilePath)
    print "\nloaded",size,"configurations"
    return size

def get_conformation_by_pathes(mcs,filePathes):
    loop_index=0
    print "  - Reading configurations"
    size =0
    for fp in filePathes :
        loop_index+=1
        if loop_index % 15 == 0 : print ""
        print loop_index,"..",
        sys.stdout.flush()
        try :
            size                    += mcs.read_all_configs_from_file(fp)
        except :
            print "can't find conformation file",fp
            raise
    print "\nloaded",size,"configurations"
    return size

def compute_conformation_dist_matrix(mcs,particles=None):
    """ Compute distance matrix between a set of configurations 
    @param mcs: configurations between which we want distances to be computed
    @param particles: the set of particles that will be used to compute the distance between configurations, if None provided, all particles will be used
    @return: a distance matrix"""
    cdm = ConformationsDistMatrix()
    if particles==None:
        particles = mcs.get_prot_info_model().get_particles()
    print "  - computing conformations dist matrix"
    cdm.compute( mcs , particles )

def read_conformation_dist_matrix_from_path(dfp):
    print " - reading distance matrix from",dfp
    cdm = ConformationsDistMatrix()
    cdm.read_pickeled(distmatrixFilePath)
    return cdm

def save_conformation_dist_matrix_to_path(cdm,dfp):    
    print "  - saving distance matrix to path",dfp
    cdm.save_pickeled(distmatrixFilePath)


#def get_distMatrix():
#    dfp
#    mcs 
#    try :
#        cdm = read_conformation_dist_matrix_from_path(dfp)
#    except :
#        mcs = 
#        cdm = compute_conformation_dist_matrix(mcs)
#        save_conformation_dist_matrix_to_path(cdm, dfp)

def get_configDistMatrix(sampleTag,nbLow):
    
    #
    #
    asDir                           = os.path.join(runDir,"samples-alt")
    lowFileName         = "low_energy_subsamples__"+str(sampleTag)+"__"+str(nbLow)+".txt"
    lowEDistMatrixFileName          = "low_energy_subsamples--dist_matrix2--"+str(sampleTag)+"__"+str(nbLow)+".txt"
    lowEFilePath        = os.path.join(asDir,lowFileName)
    #
    distmatrixFilePath              = os.path.join(cDir, lowEDistMatrixFileName)
    #
    
    cdm = ConformationsDistMatrix()
    try :
        raise Exception()
        cdm.read_pickeled(distmatrixFilePath)
        print "  - found distmatrix",distmatrixFilePath
    except :
        m = IMP.Model()
        m.set_log_level(IMP.SILENT)
        cplxInfos = build_subunits_info(m)
        HGM.helpers.mute_all_restraints(m) 
        print "  - didn't find distance matrix, computing it"
        mcs         = HGM.representation.MyConfigurationSet(cplxInfos)
        loop_index=0
#        print "  - Reading configurations"
#        for i in sample_indexes:
#            loop_index+=1
#            if loop_index % 15 == 0 : print ""
#            print i,"..",
#            sys.stdout.flush()
#            sampleFileName          = savePrefix+"--"+str(i)+".txt"
#            size = mcs.read_all_configs_from_file(os.path.join(sDir,sampleFileName))
#        print "\nloaded",mcs.get_number_of_configurations(),"configurations"
        print "  - Reading",lowFileName
#        size = mcs.read_all_configs_from_file(lowEFilePath)
        size = mcs.read_configs_from_file(lowEFilePath,range(0,nbLow))
        print "\nloaded",mcs.get_number_of_configurations(),"configurations"        
        
        
    #    particles = cplxInfos["XPB"].get_particles()
        particles = cplxInfos.get_particles()
        
        print "  - computing conformations dist matrix"
        cdm.compute( mcs , particles )
        
        print "  - saving to",distmatrixFilePath
        cdm.save_pickeled(distmatrixFilePath)
        
    return cdm


def plot_dendogram(fileName,linkage_matrix,color_threshold=None):
    print "  > creating dendogram"
    plt.figure(figsize=(16,6))
    if color_threshold==None :
        dendo               = hierarch.dendrogram(linkage_matrix)
    else:
        dendo               = hierarch.dendrogram(linkage_matrix,color_threshold=color_threshold)
    print "  > saving dendogram"
    plt.savefig(fileName,figsize=(16,6))
    plt.clf()
    
def plot_dendograms(linkageMethodList,cdm,color_thresholds=None):
    hdm = cdm.get_half_matrix_as_vector()
    del(cdm)
    for clustMethod in linkageMethodList :
        print "performing",clustMethod,"linkage"
        lm                  = hierarch.linkage(hdm,method=clustMethod)
        clusTag = ""
        color_threshold = None
        try :
            color_threshold = color_thresholds[clustMethod]
            clusTag = "--"+str(color_threshold[clustMethod])
        except : 
            pass
#        dendoFileName       = os.path.join(gcDir, "dendogram-test--"+sampleTag+"--"+clustMethod+"-linkage.png")
        dendoFileName       = os.path.join(gcDir, "dendogram-test--"+sampleTag+"--"+clustMethod+clusTag+"-linkage.png")
        plot_dendogram(dendoFileName,lm,color_threshold)

def get_linkage_matrix_from_hdm(hdm,clustMethod):
    """ """
    print "performing",clustMethod,"linkage"
    lm                  = hierarch.linkage(hdm,method=clustMethod)
    return lm

def get_linkage_matrix_from_observations(X,clustMethod):
    """ """
    print "performing",clustMethod,"linkage"
    corr                = math.sqrt(len(X[0])/3.)
    lm                  = hierarch.linkage(X,method=clustMethod)
    lm = map(lambda x:(x[0],x[1],x[2]/corr,x[3]),lm)
    return lm

def get_statClusters(lm,thresh):
    fc=scipy.cluster.hierarchy.fcluster(lm , thresh, criterion='distance')
    cs=extract_clusters_as_sets(fc)
    lens=[]
    for s in cs.keys():
        lens.append(len(cs[s]))
    lens.sort(reverse=True)
    return len(cs.keys()),lens


def generate_observation_matrix_from_configs(mcs):
#    mcss = HGM.representation.MyConfigurationSet()
    modelInfo = mcs.get_prot_info_model()
    xyzl = HGM.helpers.get_XYZdecorated_particles(modelInfo.get_particles())
    X=[]
    for i in range( mcs.get_number_of_configurations() ):
        mcs.load_configuration(i)
        X.append( HGM.helpers.gather_coordinates_for_current_config(xyzl) )
    return X
    
def get_observation_matrix(sampleTag,nbLow,sample_indexes):
#    asDir                           = os.path.join(runDir,"samples-alt")
#    FileName         = "saves--"+str(sampleTag)+str(nbLow)+".txt"
#    DistMatrixFileName          = "saves--dist_matrix--"+str(sampleTag)+str(nbLow)+".txt"
#    FilePath        = os.path.join(asDir,lowFileName) 
    m = IMP.Model()
    m.set_log_level(IMP.SILENT)
    cplxInfos = build_subunits_info(m)
    HGM.helpers.mute_all_restraints(m) 
    print "  - didn't find distance matrix, computing it"
    mcs         = HGM.representation.MyConfigurationSet(cplxInfos)
    loop_index=0
    
#    fp.close()
    print "  - Reading configurations"
    for i in sample_indexes:
        loop_index+=1
#        if loop_index % 15 == 0 : print ""
#        print i,"..",
#        sys.stdout.flush()
        sampleFileName          = savePrefix+"--"+str(i)+".txt"
        sampleFileNameList.append(sampleFileName) #creation de la liste sampleFileName
        size = mcs.read_all_configs_from_file(os.path.join(sDir,sampleFileName))
        print "\nloaded",mcs.get_number_of_configurations(),"configurations"
    

     
#    print "  - Reading",lowFileName
#        size = mcs.read_all_configs_from_file(lowEFilePath)
#    size = mcs.read_configs_from_file(lowEFilePath,range(0,nbLow))
#    print "\nloaded",mcs.get_number_of_configurations(),"configurations"
    
    print "Gathering coordinates"
    return generate_observation_matrix_from_configs(mcs)

def get_observation_matrix_alt(sampleTag,nbLow):
    asDir                           = os.path.join(runDir,"samples-alt")
#    FileName         = "saves--"+str(sampleTag)+str(nbLow)+".txt"
#    DistMatrixFileName          = "saves--dist_matrix--"+str(sampleTag)+str(nbLow)+".txt"
#    FilePath        = os.path.join(asDir,lowFileName) 
    m = IMP.Model()
    m.set_log_level(IMP.SILENT)
    cplxInfos = build_subunits_info(m)
    HGM.helpers.mute_all_restraints(m) 
    print "  - didn't find distance matrix, computing it"
    mcs         = HGM.representation.MyConfigurationSet(cplxInfos)
    loop_index=0

    print "  - Reading configurations"

    loop_index+=1

    sampleFileName="low_energy_subsamples__"+sampleTag+"__"+str(nbLow)+".txt"
    #sampleFileName="low_rmsd_subsamples__0-50__"+str(nbLow)+".txt"
    sampleFileNameList.append(sampleFileName)
    size = mcs.read_all_configs_from_file(os.path.join(asDir,sampleFileName))
    print "\nloaded",mcs.get_number_of_configurations(),"configurations"
    

     
#    print "  - Reading",lowFileName
#        size = mcs.read_all_configs_from_file(lowEFilePath)
#    size = mcs.read_configs_from_file(lowEFilePath,range(0,nbLow))
#    print "\nloaded",mcs.get_number_of_configurations(),"configurations"
    
    print "Gathering coordinates"
    return generate_observation_matrix_from_configs(mcs)



def main():
#    sampleTag           = 0

#    sample_indexes      = range(20)
    
#    linkageMethodList=["complete"]
#    linkageMethodList=["single"]
#    linkageMethodList=["average"]
#    linkageMethodList=["weighted"]
    linkageMethodList=["complete","centroid"]
#    linkageMethodList=["complete","average","weighted"]
#    linkageMethodList=["complete","weighted"]

#    cdm = get_configDistMatrix(sampleTag,nbLow)
#    printDistMatrixExtremas( cdm )
#    hdm = cdm.get_half_matrix_as_vector()

#    linkageMethodList=["median"]
#    linkageMethodList=["centroid"]

#           !!!!!!!!!!!! modif pr les 1000 meilleurs
#    X=get_observation_matrix(sampleTag,nbLow,sample_indexes)
    X=get_observation_matrix_alt(sampleTag,nbLow)
    
    print len(X),"observations of size",len(X[0])
    hdm = X


#    clustThresholds = {
##        "single" : 60,
#        "complete":65,
#        "average":40,
#        "weighted":45
#                       }
#    plot_dendograms(linkageMethodList,cdm,clustThresholds)
    
    

    
    for meth in linkageMethodList:
        print " - initating method",meth
        lm = get_linkage_matrix_from_observations(hdm,meth)
#        sampleTag           = 100
#        nbLow               = 2000 
#        nbLow               = 1000 
        
#        cfileName   = "clusters-ids--"+meth+"--"+str(sampleTag)+"__"+str(nbLow)+".txt"
#        cfilePath = os.path.join(cDir,cfileName)
#        min_nb_clust = 2
#        max_nb_clust = 20
#        for nb_clust in range(min_nb_clust,max_nb_clust):
###            nb_clust        = 9
#            thresh          = get_score_for_fix_number_of_clusters(lm,nb_clust)
#            print "  -",nb_clust,"requires threshold",thresh
#            dendoFileName   = "clusters-ids--"+meth+"--"+str(sampleTag)+"--"+str(nbLow)+"--"+str(nb_clust)+".png"
#            dendoFilePath   = os.path.join(gcDir,dendoFileName)
#            plot_dendogram(dendoFilePath,lm,color_threshold=thresh)
#        dump_cluster_id_to_file(lm,cfilePath,nbClusts=range(min_nb_clust,max_nb_clust))

#        !!!!!!!!!!!! modif pr les 1000 meilleurs
#        ctfileName   = "clusters-ids-per_thr--"+meth+"--"+str(sampleTag)+"-"+str(nbLow)+".txt"
        ctfileName   = "1000_best_models_clusters-ids-per_thr--"+meth+"--"+str(sampleTag)+"-"+str(nbLow)+".txt"
        
        ctfilePath = os.path.join(cDir,ctfileName)
        cutting_thresholds = threshold_cuts_for_method[meth]
        for thresh in cutting_thresholds:
            print "  -cutting at threshold",thresh
            
#           !!!!!!!!!!!! modif pr les 1000 meilleurs
#            dendoFileName   = "clusters-ids-per-thr--"+meth+"--"+str(sampleTag)+"--"+str(nbLow)+"--thr"+str(thresh)+".png"
            dendoFileName   = "1000_best_models_clusters-ids-per-thr--"+meth+"--"+str(sampleTag)+"--"+str(nbLow)+"--thr"+str(thresh)+".png"
            
            dendoFilePath   = os.path.join(gcDir,dendoFileName)
            plot_dendogram(dendoFilePath,lm,color_threshold=thresh)
        dump_cluster_id_for_thr_to_file(lm,ctfilePath,cutting_thresholds)


##        bientot deprecated
#        print "  -- CLUSTERS STATISTICS FOR METH",meth
#        cutting_thresholds = threshold_cuts_for_method[meth]
#        for thresh in cutting_thresholds:
##            nbClust,sizes = get_statClusters(lm,thresh)
##            print "    thr",thresh,":",nbClust,"clusts :",sizes
#            save_stat_cluster(lm,thresh)
       
#def main2():
#    linkageMethodList=["single","complete","average","weighted","median","centroid"]
#    X=get_observation_matrix(sampleTag,nbLow)
#    print len(X),"observations of size",len(X[0])
#    hdm = X
#    for meth in linkageMethodList:
#        print " - initating method",meth
#        lm = get_linkage_matrix(hdm,meth)


       
if __name__ == "__main__" :
    main()
    print "...Finished !"
    

