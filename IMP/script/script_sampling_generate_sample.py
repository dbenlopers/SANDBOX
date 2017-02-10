
import os
import sys

import time

import IMP
import IMP.em

import HGM
import HGM.sampling
import HGM.display
import HGM.helpers
import HGM.times

from alternate_configs import configs




#
#    PARAMETERS
#
#
#

#config_name_for_this_run    = None
#config_name_for_this_run    = "fixedGeom_0"
#config_name_for_this_run    = "fixedGeom_1_l0"
config_name_for_this_run    = "fixedGeom_1_1"


tfiihRepresentationFileName = configs[config_name_for_this_run][0]
runDir                      = os.path.join("results",config_name_for_this_run)
saveDirSample               = os.path.join(runDir,"samples")
savePrefix                  = "saves"

for d in [runDir,saveDirSample] :
    HGM.helpers.check_or_create_dir(d)

#
#    Models generation
#
BBs             = 200
nb_cg_steps     = 500
#
md_type         = HGM.sampling.BERENDSEN
T               = 300
tau             = 100
sampling_step   = 200
#
#    Sample configuration
#
#number_samples      = 10
#number_samples      = 1
#sample_indexes      = range(number_samples)
sample_indexes      = range(10,100)
#
dryRun_size         = 50
sample_size         = 200

#    import the function responsible for modelisation of TFIIH complex
exec ( "from {0:s} import build_TFIIH_subunits_info".format( tfiihRepresentationFileName ) )


def main():
    
    time_start = time.time()
     
    m = IMP.Model()
    m.set_log_level(IMP.SILENT)
    tfiihInfos = build_TFIIH_subunits_info(m)
    HGM.helpers.mute_all_restraints(m)
    
    times = HGM.times.Times()
        
#    For an unexplained reason, it seems that the MD motor loses speed during the game, I thus will use different motors for each sampling
#    smd = HGM.sampling.SamplerSimpleMD(tfiihInfos,md_type,T,tau,sampling_step)
    
    mcs         = HGM.representation.MyConfigurationSet(tfiihInfos)
    
    print "-- generate sample"
    for i in sample_indexes:
        time_loop_start = time.time()
        
        smd = HGM.sampling.SamplerSimpleMD(tfiihInfos,md_type,T,tau,sampling_step)
        
        smd.do_generate_sample(dryRun_size)               # a dry run before
        cs = smd.do_generate_sample(sample_size,False)    # actually generating the sample
        saveName        = savePrefix+"--"+str(i)+".txt"
        mcs.read_configurationSet(cs)
        mcs.save_all_configs_to_file(os.path.join(saveDirSample,saveName))
        mcs.delete_all_configs()
        time_loop_stop = time.time()
        elapse_time = int(time_loop_stop-time_loop_start)
        times.set_sample_time(i,elapse_time)
        print "{0:d}({1:d}s)..".format( i , elapse_time ),
        sys.stdout.flush()
    
    time_stop = time.time()

    print "full sample generated in {0:d}s".format( int(time_stop - time_start) )
    
if __name__ == "__main__" :
    main()
    print "...Finished !"
    