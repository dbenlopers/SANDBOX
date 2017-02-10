'''
Created on 17 oct. 2012

'''

import IMP, IMP.algebra, IMP.core, IMP.atom

import HGM, HGM.helpers, HGM.helpersPlot, HGM.representation, HGM.cluster

import scipy
import scipy.cluster.hierarchy as hierarch
import time
import sys
import os

from alternate_configs import configs

import matplotlib
from matplotlib import pyplot as plt

import pickle
import math



config_name_for_this_run    = "3NIG_EM_0_2aC"                  
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

##config_name_for_this_run    = "3IAM_EM_0_1aC"
##config_name_for_this_run    = "3IAM_EMc_0_1aC"
##config_name_for_this_run    = "3IAM_EM_0_2aC"
##config_name_for_this_run    = "3IAM_EMc_0_2aC"


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

cplxRepresentationFileName  = configs[config_name_for_this_run][0]
runDir                      = os.path.join("results",config_name_for_this_run)
sDir                        = os.path.join(runDir,"samples")
savePrefix                  = "saves"
cDir                        = os.path.join(runDir,"clusters")
lmDir                       = os.path.join(cDir,"linkage_matrix")
gDir                        = os.path.join(runDir,"graphics")
gcDir                       = os.path.join(gDir,"clusters")
html_dir                    = os.path.join(runDir,"html_cluster")

for d in [html_dir,gcDir,gDir,cDir,lmDir] :
    HGM.helpers.check_or_create_dir(d)




#default_kmeans_number_of_clusters   = 10
#default_kmeans_number_of_iterations = 10000

#sample_indexes      = [0]
#sampleTag           = "200"

#sample_indexes      = range(5)
#sampleTag           = "1000"
sampleFileNameList=[]
sample_indexes      = range(1,21)
sampleTag           = "0-50"
#nbLow               = "-"
nbLow               = "1000"
#sample_indexes      = range(50)
#sampleTag           = "10000"

distmatrixFileName          = "conformations-distmatrix--"+sampleTag+".pickle"
distmatrixFilePath          = os.path.join(cDir,distmatrixFileName)



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


def generate_observation_matrix_from_configs(mcs):
#    mcss = HGM.representation.MyConfigurationSet()
    modelInfo = mcs.get_prot_info_model()
    
    xyzl = HGM.helpers.get_XYZdecorated_particles(modelInfo.get_particles())
    X=[]
    for i in range( mcs.get_number_of_configurations() ):
        mcs.load_configuration(i)
        X.append( HGM.helpers.gather_coordinates_for_current_config(xyzl) )
    return X
    
    
    
def get_observation_matrix(sampleTag,nbLow,sample_indexes,subunit,i):

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
    

    print "Gathering coordinates"
    return generate_observation_matrix_from_configs_domain(mcs,subunit,i)

def get_observation_matrix_alt(sampleTag,nbLow,subunit,i):
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
    sampleFileNameList.append(sampleFileName)
    size = mcs.read_all_configs_from_file(os.path.join(asDir,sampleFileName))
    print "\nloaded",mcs.get_number_of_configurations(),"configurations"


     
#    print "  - Reading",lowFileName
#        size = mcs.read_all_configs_from_file(lowEFilePath)
#    size = mcs.read_configs_from_file(lowEFilePath,range(0,nbLow))
#    print "\nloaded",mcs.get_number_of_configurations(),"configurations"
    
    print "Gathering coordinates for subunit",subunit
    return generate_observation_matrix_from_configs_domain(mcs,subunit,i)







def main():
    time_start = time.time()
#    sampleTag           = 0

#    sample_indexes      = range(20)
    
#    linkageMethodList=["complete"]
#    linkageMethodList=["single"]
#    linkageMethodList=["average"]
#    linkageMethodList=["weighted"]
    linkageMethodList=["complete"]


    m = IMP.Model()
    m.set_log_level(IMP.SILENT)
    cplxInfos = build_subunits_info(m)
    HGM.helpers.mute_all_restraints(m) 
    mcs         = HGM.representation.MyConfigurationSet(cplxInfos)
    subunit_name=mcs.get_subunit_names()
    

    html_file = os.path.join(html_dir,"Clustering_by_subunit")
    print "-- generate HTML summary at",html_file
    fhtml = f=open(html_file,"w")
    fhtml.write("<html><head><title>Clustering by Domain</title></head><body>\n")    
    fhtml.write("<hr><H1>Cluster dendogram</H1>\n")
    fhtml.write("<table>\n")
    fhtml.write(" <tr>\n")
    fhtml.write("   <td></td>\n")
    threshold=threshold_cuts_for_method[linkageMethodList[0]]
    for seuil in threshold:
        fhtml.write("   <td><b>"+linkageMethodList[0]+" Thres "+str(seuil)+"</b></td>\n")
    fhtml.write(" </tr>\n")
    #clustering par domaine
    
    
    for subunit in subunit_name:
        
        nb_beads=mcs.get_number_of_beads(subunit)
        if nb_beads>1:
            name_doma = mcs.get_subunit_particles(subunit)
            for i in range(len(name_doma)):
                fhtml.write(" <tr>\n")
                fhtml.write("<td>"+subunit+"-"+str(i)+"</td>\n")
                #X=get_observation_matrix(sampleTag,nbLow,sample_indexes)
                X=get_observation_matrix_alt(sampleTag,nbLow,subunit,i)
                hdm = X
                for meth in linkageMethodList:
                    print " - initating method",meth
                    lm = get_linkage_matrix_from_observations(hdm,meth)
                    lmPath=os.path.join(lmDir,"Linkage_matrix:"+subunit+"meth:"+meth+".pickle")
                    HGM.cluster.write_linkage_matrix_to_file(lm, lmPath)
#                    !!!!!!!!!!!! modif pr les 1000 meilleurs
#                    ctfileName   = "clusters-ids-per_thr--"+meth+"--"+str(sampleTag)+"-"+str(nbLow)+".txt"
                    ctfileName   = ""+subunit+"-"+str(i)+"_1000_best_models_clusters-ids-per_thr--"+meth+"--"+str(sampleTag)+"-"+str(nbLow)+".txt"
                    
                    ctfilePath = os.path.join(cDir,ctfileName)
                    cutting_thresholds = threshold_cuts_for_method[meth]
                    for thresh in cutting_thresholds:
                        print "  -cutting at threshold",thresh
                        fhtml.write(" <td>\n")
                        
#                       !!!!!!!!!!!! modif pr les 1000 meilleurs
#                        dendoFileName   = "clusters-ids-per-thr--"+meth+"--"+str(sampleTag)+"--"+str(nbLow)+"--thr"+str(thresh)+".png"
                        dendoFileName   = ""+subunit+"-"+str(i)+"_1000_best_models_clusters-ids-per-thr--"+meth+"--"+str(sampleTag)+"--"+str(nbLow)+"--thr"+str(thresh)+".png"
                        
                        dendoFilePath   = os.path.join(gcDir,dendoFileName)
                        print dendoFilePath
                        plot_dendogram(dendoFilePath,lm,color_threshold=thresh)
                        fhtml.write("   <img src='"+os.path.dirname(__file__)+"/"+dendoFilePath +"'/>\n")
                        fhtml.write(" </td>\n")
                    dump_cluster_id_for_thr_to_file(lm,ctfilePath,cutting_thresholds)
                fhtml.write(" </tr>\n")
        else:   #if subunit is composed of only one domain
            #X=get_observation_matrix(sampleTag,nbLow,sample_indexes)
            domaine=mcs.get_subunit_particles(subunit)
            X=get_observation_matrix_alt(sampleTag,nbLow,subunit,0)
            hdm = X
            fhtml.write(" <tr>\n")
            fhtml.write("<td>"+subunit+"-0"+"</td>\n")
            for meth in linkageMethodList:
                print " - initating method",meth
                lm = get_linkage_matrix_from_observations(hdm,meth)
                lmPath=os.path.join(lmDir,"Linkage_matrix:"+subunit+"meth:"+meth+".pickle")
                HGM.cluster.write_linkage_matrix_to_file(lm, lmPath)
#                !!!!!!!!!!!! modif pr les 1000 meilleurs
#                ctfileName   = "clusters-ids-per_thr--"+meth+"--"+str(sampleTag)+"-"+str(nbLow)+".txt"
                ctfileName   = ""+subunit+"-0_1000_best_models_clusters-ids-per_thr--"+meth+"--"+str(sampleTag)+"-"+str(nbLow)+".txt"
                
                ctfilePath = os.path.join(cDir,ctfileName)
                cutting_thresholds = threshold_cuts_for_method[meth]
                for thresh in cutting_thresholds:
                    print "  -cutting at threshold",thresh
                    fhtml.write(" <td>\n")
                    
#                   !!!!!!!!!!!! modif pr les 1000 meilleurs
#                    dendoFileName   = "clusters-ids-per-thr--"+meth+"--"+str(sampleTag)+"--"+str(nbLow)+"--thr"+str(thresh)+".png"
                    dendoFileName   = ""+subunit+"-0_1000_best_models_clusters-ids-per-thr--"+meth+"--"+str(sampleTag)+"--"+str(nbLow)+"--thr"+str(thresh)+".png"
                    
                    dendoFilePath   = os.path.join(gcDir,dendoFileName)
                    print dendoFilePath
                    plot_dendogram(dendoFilePath,lm,color_threshold=thresh)
                    fhtml.write("   <img src='"+os.path.dirname(__file__)+"/"+dendoFilePath +"'/>\n")
                    fhtml.write(" </td>\n")
                dump_cluster_id_for_thr_to_file(lm,ctfilePath,cutting_thresholds)
            fhtml.write(" </tr>\n")
    fhtml.write("</table>\n")
    fhtml.write("</body></html>\n")
    fhtml.close()

    time_stop = time.time()
    print "clustering generated in {0:d}s".format( int(time_stop - time_start) )

       
if __name__ == "__main__" :
    main()
    print "...Finished !"
    

