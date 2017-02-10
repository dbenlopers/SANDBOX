'''

'''
import os

import IMP
import HGM
import HGM.distances, HGM.helpers
from time import time

from alternate_configs import configs
#    MY TFIIH REPRESENTATION
# config_name_for_this_run    = "3NIG_EM_0_2aC"                  
# config_name_for_this_run    = "3NIG_EM_0_2aC_20"     
# config_name_for_this_run    = "3NIG_EM_0_2lmC"
# config_name_for_this_run    = "3NIG_EM_0_2lmC_20"
# config_name_for_this_run    = "3NIG_EM_0_2lC"
# config_name_for_this_run    = "3NIG_EM_0_2lC_20" 
# config_name_for_this_run    = "3NIG_EM_0_3ambiC"  
# config_name_for_this_run    = "3NIG_EM_0_3ambiC_20"
        

# config_name_for_this_run        = "arp_EM_0_2aLA"

# config_name_for_this_run    = "3IAM_EM_0_3a"
# config_name_for_this_run    = "3IAM_EM_0_3lm"
# config_name_for_this_run    = "3IAM_EM_0_3l"

config_name_for_this_run    = "3IAM_EM_0_4a"
# config_name_for_this_run    = "3IAM_EM_0_4lm"
# config_name_for_this_run    = "3IAM_EM_0_4l"

# config_name_for_this_run    = "3IAM_EM_0_5a"
# config_name_for_this_run    = "3IAM_EM_0_5lm"
# config_name_for_this_run    = "3IAM_EM_0_5l"


#
#    PARAMETERS
#
#
#
representationFileName      = configs[config_name_for_this_run][0]
runDir                      = os.path.join("results",config_name_for_this_run)
saveDirSample               = os.path.join(runDir,"samples")
savePrefix                  = "saves"


dDir                        = os.path.join(runDir,"distances")
dmDir                       = os.path.join(dDir,"distMatrices")
asDir                       = os.path.join(runDir,"samples-alt")

#distMatrixFileName  = "dist_matrix_test_1000.pickle"
#distMatrixFileName  = "dist_matrix_test_963.pickle"
#distMatrixFileName  = "dist_matrix_test_EM1.1-87.pickle"
#distMatrixFileName  = "dist_matrix_test_EM1.1i-223.pickle"
distMatrixFileName  = "dist_matrix_test_EM1.2-112.pickle"
distMatrixFilePath  = os.path.join(dmDir,distMatrixFileName)

# When computing not directly on the dist-matrix, but on a sampleFile
#altConfigDir                = os.path.join(runDir,"altConfigs")
#lowEconfigsFilePath         = os.path.join(altConfigDir,"lowE-configs-112.txt")
#mediumEconfigsFilePath      = os.path.join(altConfigDir,"mediumE-configs-112.txt")
#highEconfigsFilePath        = os.path.join(altConfigDir,"highE-configs-112.txt") 

#sampleFilePath              = lowEconfigsFilePath



#sample_indexes          = range(0,100)
sample_indexes          = range(0,99)
sampleDescription       = config_name_for_this_run + "-" +str(len(sample_indexes))
beadDistMatrixFileName  = "beads-dist-matrix--"+sampleDescription+".pickle"
#distMatrixFileName      = "dist_matrix_test_arp_EM_0_2-100.pickle"
distMatrixFileName  = "dist_matrix_test_"+sampleDescription+".pickle"

#lowEconfigsFileName     = "low_energy_subsamples__100__1000.txt"
#highEconfigsFileName    = "high_energy_subsamples__100__1000.txt"
lowEconfigsFileName     = "low_energy_subsamples__100__2000.txt"
highEconfigsFileName    = "high_energy_subsamples__100__2000.txt"

distMatrixFilePath          = os.path.join(dmDir,distMatrixFileName)
beadDistMatrixFilePath      = os.path.join(dmDir,beadDistMatrixFileName)

lowEconfigsFilePath         = os.path.join(asDir,lowEconfigsFileName)
highEconfigsFilePath        = os.path.join(asDir,highEconfigsFileName) 


exec ( "from {0:s} import build_subunits_info".format( representationFileName ) )


def dump_table(EOA) :
    print "-- Edges repartitions --"
    ts = sorted(EOA.keys())
    
    nbts = len(ts)
    print "edge &"+"&".join(map(lambda x:str(x),ts))
    edges = EOA[ts[0]].get_sorted_edges()
    for (node1,node2,nb) in edges :
        print " {0:>10s} - {1:<10s}".format(node1,node2),
        for t in ts :
            eoa = EOA[t]
            norm_coef = 100./eoa.get_number_of_configurations()
            nb=eoa.get_edge_count(node1,node2)
#            print "&{0:>5d} ({1:3.2f}%)".format (nb,nb*norm_coef),
            print "&{0:3.2f} ".format (nb*norm_coef),
        print r"\\"

def dump_domains_table(EOA,pdms):
    
    def get_edge_tag(s):
#        print "get_tag(",s,")"
        tags= {
     "arp2-d1(0) - arpc5-d1(0)":"A",
     "arp2-d1(0) - arpc1-d1(0)":"A",
     "arp2-d1(0) - arpc4-d1(0)":"L",
    "arpc4-d1(0) - arpc2-d2(1)":"L",
    "arpc4-d1(0) - arpc1-d1(0)":"L",
    "arpc4-d1(0) - arpc5-d1(0)":"L",
     "arp3-d2(1) - arpc3-d1(0)":"L",
     "arp3-d1(0) - arpc2-d1(0)":"L",
     "arp3-d1(0) - arpc2-d2(1)":"M",
      "arp2-d1(0) - arp3-d2(1)":"M",
     "arp3-d1(0) - arpc4-d1(0)":"M",
    "arpc5-d1(0) - arpc1-d1(0)":"M",
    "arp3-d1(0) - arp3-d2(1)":"O",
    "arpc2-d1(0) - arpc2-d2(1)":"O",
     "arpc5-d1(0) - arp2-d1(0)":"A",
     "arpc1-d1(0) - arp2-d1(0)":"A",
     "arpc4-d1(0) - arp2-d1(0)":"L",
    "arpc2-d2(1) - arpc4-d1(0)":"L",
    "arpc1-d1(0) - arpc4-d1(0)":"L",
    "arpc5-d1(0) - arpc4-d1(0)":"L",
     "arpc3-d1(0) - arp3-d2(1)":"L",
     "arpc2-d1(0) - arp3-d1(0)":"L",
     "arpc2-d2(1) - arp3-d1(0)":"M",
      "arp3-d2(1) - arp2-d1(0)":"M",
     "arpc4-d1(0) - arp3-d1(0)":"M",
    "arpc1-d1(0) - arpc5-d1(0)":"M",
    "arp3-d2(1) - arp3-d1(0)":"O",
    "arpc2-d2(1) - arpc2-d1(0)":"O",
    }
        tag = " "
        try :
            tag = tags[s]
        except :
            pass
        return tag
    
    print "-- Edges repartitions --"
    ts = sorted(EOA.keys())
    print "ts",ts
#    p = HGM.distances.ParticlesPairDistanceMatrixSet()
    p_names = map(lambda p:p.get_name(), pdms.get_particles())
#    print "EOA",EOA
        
    edges      = EOA[ts[0]].get_sorted_edges()
    
    print r"\begin{table}[htbp!]"
    print r"\centering"
    print r"{\footnotesize"
    print r"\begin{tabular}{|c|l"+("|r"*len(ts))+"|}"
    print r"\cline{2-"+str(len(ts)+2)+"}"
    print "\multicolumn{1}{c|}{} & edge &"+"&".join(map(lambda x:str(x),ts))+r"\\"
    print r"\hline"
    
    for (node1,node2,nb) in edges :
#        print " {0:>10s} - {1:<10s}".format(p_names[node1],p_names[node2]),
#        print " &{0:>10s} - {1:<10s}".format(p_names[node1],p_names[node2]),
        tag = get_edge_tag("{0:>10s} - {1:<10s}".format(p_names[node1],p_names[node2]))
        print "{2:s}&{0:>10s} - {1:<10s}".format(p_names[node1],p_names[node2],tag),
        for t in ts :
            eoa = EOA[t]
            norm_coef = 100./eoa.get_number_of_configurations()
            nb=eoa.get_edge_count(node1,node2)
#            print "&{0:>5d} ({1:3.2f}%)".format (nb,nb*norm_coef),
            print "&{0:3.2f} ".format (nb*norm_coef),
        print r"\\"
    
    print r"\hline" 
    print r"\end{tabular}"
    print r"}"
    print "%"
    print r"%\caption{}"
    print r"%\label{}"
    print r"\end{table}"
        
#def _dump_edge_histo(edge_counts,nb_configs):
##    edge_counts
##    nb_configs
#    nbe=len(edge_counts)
#    y=arange(nbe)
#    
#    labels = [a+"-"+b for (a,b,c) in edge_counts]
#    normalization = 100./nb_configs
#    values = [c*normalization for (a,b,c) in edge_counts]
#    plt.title("subunits contact propensities observed in "+str(nb_configs)+" configurations")
##    plt.title("subunits contact propensities observed in 49899 configurations")
##    plt.barh (labels,values)
#    plt.barh (y,values)
#    plt.yticks(y,labels)
#    plt.axvline(x=30,color='red')
#    plt.axvline(x=20,color='orange')
#    plt.axvline(x=10,color='lime')
#    plt.axvline(x=5 ,color='green')
#    plt.axvline(x=1 ,color='blue')
#    plt.savefig("HIST-EDGES-PROPENSITIES-"+str(nb_configs)+".png")
#    plt.clf()

    
def load_dist_matrix(tfiihInfos):
    time_start = time()
    try :
        sdms = HGM.helpers.loadPickleDistMatrix(distMatrixFilePath)
        print "   loaded subunit dist matrix set from existing pickled file {0:s}".format(distMatrixFilePath)
    except :
        print " can't load dist matrix",distMatrixFilePath
        raise 
    time_stop = time()
    print "  -> dist-matrix loaded in ({0:.1f}s)".format(time_stop-time_start)
    return sdms

def compute_dist_matrix_for_sample_in_file( sampleFilePath, tfiihInfo ):
    mcs         = HGM.representation.MyConfigurationSet(tfiihInfo)
    mcs.read_all_configs_from_file(sampleFilePath)
    print "-- Computing dist matrix",
    pdms = HGM.distances.ParticlesPairDistanceMatrixSet(mcs)
    print "    (",pdms.get_number_of_configurations(),"configurations)"
    print "-- Computing subunits dist matrix",
    sdms = HGM.distances.SubunitsPairDistanceMatrixSet(tfiihInfo,pdms)
    print "    (",sdms.get_number_of_configurations(), "configurations)"
    return sdms


def main():
    m = IMP.Model()
    m.set_log_level(IMP.SILENT)
    cplxInfos = build_subunits_info(m)
    HGM.helpers.mute_all_restraints(m)
    
    
    
#    print "loading pair distance matrix",
#    sdms = HGM.helpers.loadPickleDistMatrix(distMatrixFilePath,tfiihInfos)
#    print "...done"

    # SUBUNITS
#    sdms = load_dist_matrix(cplxInfos)
#    sdms = compute_dist_matrix_for_sample_in_file(sampleFilePath, cplxInfos)
    
    # DOMAINS
#    mcs = HGM.representation.MyConfigurationSet(cplxInfos)
#    pdms = HGM.distances.ParticlesPairDistanceMatrixSet(mcs)
#    pdms.load_pickled(beadDistMatrixFilePath)
    mcs = HGM.representation.MyConfigurationSet(cplxInfos)
    mcs.read_all_configs_from_file(lowEconfigsFilePath)
    print "Read low configurations file, got",mcs.get_number_of_configurations(),"models"
    pdms = HGM.distances.ParticlesPairDistanceMatrixSet(mcs)
        
#    print pdms.get_number_of_configurations(),len(pdms.get_particles()),pdms.get_distance(0, 1, 2)
    
    EOA = {}


    # DOMAINS
    nodes = range(len(pdms.get_particles()))

#    thresholds = [1,2,3,4,5,6,7,8,9,10]
    thresholds = [5,10,15,20]
#    thresholds = [1]
    print "computing connectivity graph edge-accumulator"
    for t in thresholds :
        print "computing distance graph for threshold",t
        # SUBUNITS
#        eoa = HGM.distances.EdgeOccurenceAccumulator(sdms,t)
        # DOMAINS
        eoa = HGM.distances.EdgeOccurenceAccumulator(pdms,t,nodes)
        EOA[t] = eoa
    # SUBUNITS
#    dump_table(EOA)
    # DOMAINS
    dump_domains_table(EOA,pdms)
    
    
#    dump_plots(EOA)

if __name__ == "__main__" :
    main()
