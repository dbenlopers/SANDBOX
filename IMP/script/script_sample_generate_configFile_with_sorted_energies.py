'''


Generate configuration save files for lowest energies and highest energies in a complete sample
sample files are dumped in asDir (= samples-alt) by default
'''
import os

import IMP

import HGM
import HGM.energies
from alternate_configs import configs

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


#config_name_for_this_run    = "4FXG_EM_0_1a_40"
#config_name_for_this_run    = "4FXG_EM_0_1lm_40"
#config_name_for_this_run    = "4FXG_EM_0_1l_40"
#config_name_for_this_run    = "4FXG_EM_0_1a_30"
#config_name_for_this_run    = "4FXG_EM_0_1lm_30"
#config_name_for_this_run    = "4FXG_EM_0_1l_30"
#config_name_for_this_run    = "4FXG_EM_0_1a_20"
#config_name_for_this_run    = "4FXG_EM_0_1lm_20"
#config_name_for_this_run    = "4FXG_EM_0_1l_20"

#config_name_for_this_run    = "4FXG_EM_0_2a_40"
#config_name_for_this_run    = "4FXG_EM_0_2lm_40"
#config_name_for_this_run    = "4FXG_EM_0_2l_40"
#config_name_for_this_run    = "4FXG_EM_0_2a_20"
#config_name_for_this_run    = "4FXG_EM_0_2lm_20"

#config_name_for_this_run    = "arp_EM_0_2aLFc1"
#config_name_for_this_run    = "arp_EM_0_2aLFRET1"
#config_name_for_this_run    = "arp_EM_0_2aLFc4"
#config_name_for_this_run    = "arp_EM_0_2aLFc5"
##config_name_for_this_run    = "arp_EM_0_2aLFc3"
##config_name_for_this_run    = "arp_EM_0_2aLFc2"

#config_name_for_this_run    = "arp_EM_0_2Fc1"
#config_name_for_this_run    = "arp_EM_0_2Fc3"
#config_name_for_this_run    = "arp_EM_0_2Fc4"
##config_name_for_this_run    = "arp_EM_0_2F2"
##config_name_for_this_run    = "arp_EM_0_2F3"
          
#config_name_for_this_run    = "arp_EM_0_2FRET1"


sampleTag                       = "0-50"  # qualification of the sample on which the script was launched

#    SCRIPT PARAMS
#
nbLow               = 1000
nbHigh              = 1000

#nbLow               = 100
#nbHigh              = 100


lowFileName         = "low_energy_subsamples__"+sampleTag+"__"+str(nbLow)+".txt"
highFileName        = "high_energy_subsamples__"+sampleTag+"__"+str(nbHigh)+".txt"

eFileName           = "sample-energies.txt"
sseFileName         = "subsamples-energies.txt"

savePrefix                  = "saves"

#    AUTO SETTINGS
#
runDir                      = os.path.join("results",config_name_for_this_run)
sDir                        = os.path.join(runDir,"samples")
asDir                       = os.path.join(runDir,"samples-alt")
eDir                        = os.path.join(runDir,"energies")

energiesFilePath    = os.path.join(eDir,eFileName)
subsampleFilePath   = os.path.join(eDir,sseFileName)

lowEFilePath        = os.path.join(asDir,lowFileName)
highEFilePath       = os.path.join(asDir,highFileName)
 



for d in [asDir] :
    HGM.helpers.check_or_create_dir(d)
    
subunitsRepresentationFileName = configs[config_name_for_this_run][0]
exec ( "from {0:s} import build_subunits_info".format( subunitsRepresentationFileName ) )


def gatherConfigs( indices, subunitsInfos, saveDirSample ):
    """
    @param indices:  list of configuration indices ("sid:ssidx")
    @param saveDirSample:  where the configuration files are saved
    @return cs:    a cConfigurationSet object in which I I'll store all  
    """
    samples = {}
#    print " ... collecting indices and subindices"
#    for i in indices :
#        sampleIdx = sl[i][0]
    print "    > gather subsample idx per sample idx"
    for cidx in indices:
        (si,isi)=cidx.split(":")
        (si,isi)=(int(si),int(isi))
        try :
            samples[si].append(isi)
        except :
            samples[si]=[isi]
#        print samples
    sample  = HGM.representation.MyConfigurationSet( subunitsInfos )
    print "  ... reading specific configurations"
    for si,sisl in samples.iteritems() :
        sampleFileName          = savePrefix+"--"+str(si)+".txt"
        filePath                = os.path.join(saveDirSample,sampleFileName)
        sample.read_configs_from_file(filePath, sisl)
    
    return sample

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
    
        # read subsample energies
    
    print " -- read energies",
    sse = HGM.energies.SubsamplesEnergies()
    try :
        sse.read_from_file(subsampleFilePath)
        print " (from subsample energies save file)"
    except :
        sse.read_samples_energies_from_file(energiesFilePath)
        print " (from samples energies save file)"
    
    ssel = sse.get_sorted_subsamples_energies()
    
    print "    energies range from {",ssel[0],"} to {",ssel[-1],"}"
    
    print " -- saving ",nbLow,"lowest energies to",lowEFilePath
    indices = map( lambda x:x[0], ssel[0:nbLow])
    print indices[0:10]
#    sample = gatherConfigs(indices, subunitsInfos, sDir)
    sample = gatherSortedConfigs(indices, subunitsInfos, sDir)
    print " (",sample.get_number_of_configurations()," configurations)"
    sample.save_all_configs_to_file(lowEFilePath)
    
    print " -- saving ",nbLow,"highst energies to",highEFilePath
    indices = map( lambda x:x[0], ssel[-nbHigh-1:-1])
#    sample = gatherConfigs(indices, subunitsInfos, sDir)
    sample = gatherSortedConfigs(indices, subunitsInfos, sDir)
    print " (",sample.get_number_of_configurations()," configurations)"
    sample.save_all_configs_to_file(highEFilePath)

    
if __name__ == "__main__" :
    main()
    print "\n..that's all folks !"
    
