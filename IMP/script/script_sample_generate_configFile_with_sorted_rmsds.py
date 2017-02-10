'''


Generate configuration save files for lowest energies and highest energies in a complete sample
sample files are dumped in asDir (= samples-alt) by default
'''
import os

import IMP

import HGM
import HGM.sampleEvaluation
from alternate_configs import configs



#config_name_for_this_run        = "arp_EM_0_2" 
#config_name_for_this_run    = "3NIG_EM_0_1a"
#config_name_for_this_run    = "3NIG_EM_0_2a"
#config_name_for_this_run    = "3NIG_EM_0_3ambi"
#config_name_for_this_run    = "arp_EM_0_2aLA"
#config_name_for_this_run    = "3IAM_EM_0_1a"

#config_name_for_this_run    = "3NIG_EM_0_3ambiC_f"  
config_name_for_this_run    = "3NIG_EM_0_3ambiC_f_20"

#    SCRIPT PARAMS
#
nbLow               = 1000
nbHigh              = 1000

#nbLow               = 100
#nbHigh              = 100





#    AUTO SETTINGS
#
runDir                      = os.path.join("results",config_name_for_this_run)
sDir                        = os.path.join(runDir,"samples")
asDir                       = os.path.join(runDir,"samples-alt")
#eDir                        = os.path.join(runDir,"energies")
evDir                       = os.path.join(runDir,"evaluations")
rDir                        = os.path.join(evDir,"rmsdToSolution")

solutionFilePath        = "/home/arnaud/Desktop/TFIIH/data/3NIG/save-3NIG-HGM.txt"
#solutionFilePath        = "/home/arnaud/Desktop/TFIIH/data/3IAM/save-3IAM-HGM.txt"
savePrefix                  = "saves"
sample_indexes      = HGM.helpers.read_all_sample_indices(sDir, savePrefix)
sampleTag           = "0-50"
#sample_indexes      = [0]
#sample_indexes      = range(10)
#sampleTag                       = str(len(sample_indexes))  # qualification of the sample on which the script was launched


lowFileName         = "low_rmsd_subsamples__"+sampleTag+"__"+str(nbLow)+".txt"
highFileName        = "high_rmsd_subsamples__"+sampleTag+"__"+str(nbHigh)+".txt"

#eFileName           = "sample-energies.txt"
ssrFileName         = "subsamples-rmsds--"+sampleTag+".txt"




#rmsdFilePath    = os.path.join(rDir,rFileName)
subsamplermsdFilePath   = os.path.join(rDir,ssrFileName) # where I will store the rmsd values

lowRFilePath        = os.path.join(asDir,lowFileName)    # where I will store de conform-files
highRFilePath       = os.path.join(asDir,highFileName)   # where I will store de conform-files
 



for d in [asDir,evDir,rDir] :
    HGM.helpers.check_or_create_dir(d)
    
subunitsRepresentationFileName = configs[config_name_for_this_run][0]
exec ( "from {0:s} import build_subunits_info".format( subunitsRepresentationFileName ) )


#def gatherConfigs( indices, subunitsInfos, saveDirSample ):
#    """
#    @param indices:  list of configuration indices ("sid:ssidx")
#    @param saveDirSample:  where the configuration files are saved
#    @return cs:    a cConfigurationSet object in which I I'll store all  
#    """
#    samples = {}
##    print " ... collecting indices and subindices"
##    for i in indices :
##        sampleIdx = sl[i][0]
#    print "    > gather subsample idx per sample idx"
#    for cidx in indices:
#        (si,isi)=cidx.split(":")
#        (si,isi)=(int(si),int(isi))
#        try :
#            samples[si].append(isi)
#        except :
#            samples[si]=[isi]
##        print samples
#    sample  = HGM.representation.MyConfigurationSet( subunitsInfos )
#    print "  ... reading specific configurations"
#    for si,sisl in samples.iteritems() :
#        sampleFileName          = savePrefix+"--"+str(si)+".txt"
#        filePath                = os.path.join(saveDirSample,sampleFileName)
#        sample.read_configs_from_file(filePath, sisl)
#    
#    return sample
#
def gatherSortedConfigs( indices, subunitsInfos, saveDirSample ):
    """
    @param indices:  list of configuration indices ("sid:ssidx")
    @param saveDirSample:  where the configuration files are saved
    @return cs:    a cConfigurationSet object in which I I'll store all  
    """
    sample  = HGM.representation.MyConfigurationSet( subunitsInfos )
    print "  ... reading specific configurations"
    for cidx in indices:
        (si,isi)=cidx.split(":")
        (si,isi)=(int(si),int(isi))
        sampleFileName          = savePrefix+"--"+str(si)+".txt"
        filePath                = os.path.join(saveDirSample,sampleFileName)
        sample.read_configs_from_file(filePath, [isi])
    
    return sample

def main():
    m = IMP.Model()
    m.set_log_level(IMP.SILENT)
    subunitsInfos = build_subunits_info(m)
    HGM.helpers.mute_all_restraints(m)
    
    print " -- subsamples rmsd to solution : evaluation"
    # compute subsamples RMSD
    rsss = HGM.sampleEvaluation.RMSDsToSolutionForSubsamples(subunitsInfos)
    #
    #    let's evaluate samples
    #
#    rsss.read_from_file(subsamplermsdFilePath)
    try :
        rsss.read_from_file(subsamplermsdFilePath)
        print "  - found computed values in file(",subsamplermsdFilePath ,")"
    except :
        print "  - no save file, let's compute"
        print "    loading solution config"
        solution        = HGM.representation.MyConfigurationSet(subunitsInfos)
        solution.read_all_configs_from_file(solutionFilePath)
        solution.load_configuration(0)
        rsss.set_solution()
        print "    loading samples and computing rmsd to solution"
        mcs = HGM.representation.MyConfigurationSet(subunitsInfos)
        loopindex=0
        for i in sample_indexes :
            loopindex+=1; 
            if loopindex%15==0:print ""
            print i,
            mcs.read_all_configs_from_file(
                                           HGM.helpers.forge_sample_path(sDir,savePrefix, i)
                                           )
            rsss.add_sample(i, mcs)
            mcs.delete_all_configs()
        print "    saving values to",subsamplermsdFilePath
        rsss.write_to_file(subsamplermsdFilePath)
    
    print " -- sort subsamples by rmsd to solution"
    ssrmsdl = rsss.get_sorted_subsamples_rmsds_to_solution()
    print len(ssrmsdl)
    
    print "    rmsds range from {",ssrmsdl[0],"} to {",ssrmsdl[-1],"}"
    
    print " -- extracting the first",nbLow,"subsamples"
    indices = map( lambda x:x[0], ssrmsdl[0:nbLow])
    print indices[0:10]
#    sample = gatherConfigs(indices, subunitsInfos, sDir)
    sample = gatherSortedConfigs(indices, subunitsInfos, sDir)
    print " (",sample.get_number_of_configurations()," configurations)"
    sample.save_all_configs_to_file(lowRFilePath)
    
    print " -- extracting the last",nbHigh,"subsamples"
    indices = map( lambda x:x[0], ssrmsdl[-nbHigh:])
    print indices[-10:]
#    sample = gatherConfigs(indices, subunitsInfos, sDir)
    sample = gatherSortedConfigs(indices, subunitsInfos, sDir)
    print " (",sample.get_number_of_configurations()," configurations)"
    sample.save_all_configs_to_file(highRFilePath)

    
    
    
if __name__ == "__main__" :
    main()
    
    
