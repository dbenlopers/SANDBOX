'''


Compute energies for an ensemble of samples, and save it in three files
    all energies sorted by sample index
    statistics : average and std_dev per smaple index
    statistics sorted

'''

import os
import sys

import time

import IMP
import HGM
import HGM.energies
#import HGM.sampling
#import HGM.display

import HGM.helpers
#import HGM.helpersPlot

from alternate_configs import configs
#    MY TFIIH REPRESENTATION
#config_name_for_this_run    = "fixedGeom_0"
#config_name_for_this_run    = "fixedGeom_1_godzilla"
#config_name_for_this_run    = "fixedGeom_1"
#config_name_for_this_run    = "fixedGeom_1_1"
#config_name_for_this_run    = "test_fixedGeom_1_1"
#config_name_for_this_run    = "test_fixedGeom_1_2"
#config_name_for_this_run    = "test_fixedGeom_1_3"
#config_name_for_this_run    = "fixedGeom_EM_1_0"
#config_name_for_this_run    = "fixedGeom_EM_1_1"
#config_name_for_this_run    = "fixedGeom_EM_1_2"
#config_name_for_this_run    = "arp_EM_0_2aLM"
#config_name_for_this_run    = "arp_EM_0_2aL"
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
##config_name_for_this_run    = "arp_EM_0_1"


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

#
#    PARAMETERS
#
#
#
subunitsRepresentationFileName = configs[config_name_for_this_run][0]
#runDir                      = os.path.join("Users","schwarz","Dev","TFIIH","src","coarse2","results",config_name_for_this_run)
runDir                      = os.path.join("results",config_name_for_this_run)
saveDirSample               = os.path.join(runDir,"samples")
asDir                       = os.path.join(runDir,"samples-alt")
savePrefix                  = "saves"

eDir                        = os.path.join(runDir,"energies")
eFileName                   = "sample-energies.txt"
eStatFileName               = "sample-energy-stats.txt"
eStatsortedFileName         = "sample-energy-stats-sorted.txt"

for d in [eDir] :
    HGM.helpers.check_or_create_dir(d)

#
#    Sample configuration
#
#sample_indexes      = range(25)

#sample_indexes      = range(100,150)
#sample_indexes      = range(100,187)

#sample_indexes      = range(101)
#sample_indexes      = range(130)
#sample_indexes      = range(10)
#sample_indexes      = range(3000)
#sample_indexes      = range(1000)
#sample_indexes      = range(1010,1020)
#sample_indexes      = range(310,322)
#sample_indexes      = range(322);sample_indexes.append(1000)
#sample_indexes      = [300]
#sample_indexes       = range(1000,1400)
sample_indexes      = HGM.helpers.read_all_sample_indices(saveDirSample,savePrefix)
#sample_indexes      = [1]
print "sample_indexes",sample_indexes




#    import the function responsible for modelisation of TFIIH complex
exec ( "from {0:s} import build_subunits_info".format( subunitsRepresentationFileName ) )




def main():
        
    m = IMP.Model()
    m.set_log_level(IMP.SILENT)
    tfiihInfos = build_subunits_info(m)
    HGM.helpers.mute_all_restraints(m)
    
    mcs         = HGM.representation.MyConfigurationSet(tfiihInfos)

    es=HGM.energies.EnergiesForSampleCollection()
    loop_index=0
#    print sample_indexes
    for i in sample_indexes:
        loop_index+=1
        if loop_index % 15 == 0 : print ""
        print i,"..",
        sys.stdout.flush()
        sampleFileName          = savePrefix+"--"+str(i)+".txt"
#        sampleFileName         = os.path.join(asDir,"low_energy_subsamples__0-50__1000.txt")
        size = mcs.read_all_configs_from_file(os.path.join(saveDirSample,sampleFileName))
#        time1=time.time()
        es.set_energies_for_sample(i,mcs)
#        time2=time.time()
#        print "({0:4.2}s)".format(time2-time1),
#        print ">>",mcs.get_model().evaluate(False)
        mcs.delete_all_configs()


    print es.get_number_of_energies(),"energies computed on",\
        es.get_number_of_samples(),"samples"
    
    print "\n-- write energy and statistics"
    eFilePath           = os.path.join(eDir,eFileName)
    statFilePath        = os.path.join(eDir,eStatFileName)
    statsortedFilePath  = os.path.join(eDir,eStatsortedFileName)
    es.write_to_file(eFilePath)
    es.get_statistics().write_to_file(statFilePath)
    es.get_statistics().write_to_file(statsortedFilePath,True)
    
    
        
if __name__ == "__main__" :
    main()
    print "...Finished !"
    
