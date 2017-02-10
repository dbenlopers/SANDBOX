'''


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

#config_name_for_this_run    = "arp_EM_0_1"
#config_name_for_this_run    = "arp_EM_0_2"

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

#config_name_for_this_run    = "3IAM_EM_0_1aC"
#config_name_for_this_run    = "3IAM_EM_0_2aC"

#config_name_for_this_run    = "3IAM_EMc_0_1aC"
#config_name_for_this_run    = "3IAM_EMc_0_2aC"

#config_name_for_this_run    = "3NIG_EM_0_2aC"
#config_name_for_this_run    = "3NIG_EM_0_3ambiC"
#config_name_for_this_run    = "3NIG_EM_0_2aC_20"
#config_name_for_this_run    = "3NIG_EM_0_3ambiC_20"
#config_name_for_this_run    = "3NIG_EM_0_2lmC"
#config_name_for_this_run    = "3NIG_EM_0_2lmC_20"
#config_name_for_this_run    = "3NIG_EM_0_2lC"
#config_name_for_this_run    = "3NIG_EM_0_2lC_20"


#config_name_for_this_run    = "3NIG_EM_0_2aC_f"
#config_name_for_this_run    = "3NIG_EM_0_3ambiC_f"
#config_name_for_this_run    = "3NIG_EM_0_2aC_f_20"
#config_name_for_this_run    = "3NIG_EM_0_3ambiC_f_20"
#config_name_for_this_run    = "3NIG_EM_0_2lmC_f"
#config_name_for_this_run    = "3NIG_EM_0_2lmC_f_20"
#config_name_for_this_run    = "3NIG_EM_0_2lC_f"
#config_name_for_this_run    = "3NIG_EM_0_2lC_f_20"

#config_name_for_this_run    = "3NIG_EM_0_4a_f"
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

#config_name_for_this_run    = "4FXG_EM_0_1a_20"
#config_name_for_this_run    = "4FXG_EM_0_1lm_20"
#config_name_for_this_run    = "4FXG_EM_0_1l_20"

#config_name_for_this_run    = "4FXG_EM_0_2a_40"
#config_name_for_this_run    = "4FXG_EM_0_2lm_40"
#config_name_for_this_run    = "4FXG_EM_0_2l_40"
#

#config_name_for_this_run    = "4FXG_EM_0_2a_20"
#config_name_for_this_run    = "4FXG_EM_0_2lm_20"
#config_name_for_this_run    = "4FXG_EM_0_2l_20"

#    PARAMETERS
#
#
#
currentRepresentationFileName = configs[config_name_for_this_run][0]
#runDir                      = os.path.join("Users","schwarz","Dev","TFIIH","src","coarse2","results",config_name_for_this_run)
runDir                      = os.path.join("results",config_name_for_this_run)
saveDirSample               = os.path.join(runDir,"samples")
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

#sample_indexes      = range(100)
#sample_indexes      = range(130)
#sample_indexes      = range(10)
#sample_indexes      = range(3000)
#sample_indexes      = range(1000)
#sample_indexes      = range(1010,1020)
#sample_indexes      = range(310,322)
#sample_indexes      = range(322);sample_indexes.append(1000)
#sample_indexes      = [300]
sample_indexes      = HGM.helpers.read_all_sample_indices(saveDirSample,savePrefix)



#    import the function responsible for modelisation of TFIIH complex
#exec ( "from {0:s} import build_TFIIH_subunits_info".format( tfiihRepresentationFileName ) )
exec ( "from {0:s} import build_subunits_info".format( currentRepresentationFileName ) )





def compute_current_decomposed_energies(cplxInfos):
    results = []
    se   = cplxInfos.get_model().evaluate(False)
    results.append( ("Total",se) )
    sevr = cplxInfos.evr.evaluate(False)
    results.append( ("Clashes",sevr) )
    sstr = sum ( map( ( lambda r:r.evaluate(False)) , cplxInfos.str ) )
    results.append( ("Cohesion",sstr) )
    sscr = sum ( map( ( lambda r:r.evaluate(False)) , cplxInfos.scr ) )
    results.append( ("Contacts",sscr) )
    semr = cplxInfos.emr.evaluate(False)
    results.append( ("EM",semr) )
    try :
        locr = cplxInfos.locr.evaluate(False)
        results.append( ("Location",locr) )
    except :
        pass
    try :
        fdr = cplxInfos.fdr.evaluate(False)
        results.append( ("Fret",fdr) )
    except :
        pass
    return results


def output_energies_decomposition(cplxInfos):
#    se   = tfiihinfo.get_model().evaluate(False)
#    sevr = tfiihinfo.evr.evaluate(False)
#    sstr = sum ( map( ( lambda r:r.evaluate(False)) , tfiihinfo.str ) )
#    sscr = sum ( map( ( lambda r:r.evaluate(False)) , tfiihinfo.scr ) )
#    semr = tfiihinfo.emr.evaluate(False)
##    print "[total-energy:{0:10.2f}] sub-cohes:{1:10.2f} sub-inter:{2:10.2f} excl-vol:{3:10.2f} EM:{4:10.2f}".format(
##           se , sstr, sscr, sevr, semr )
#    fdr = tfiihinfo.fdr.evaluate(False)
#    print "[total-energy:{0:10.2f}] sub-cohes:{1:10.2f} sub-inter:{2:10.2f} excl-vol:{3:10.2f} EM:{4:10.2f} FRET:{5:10.2f}".format(
#           se , sstr, sscr, sevr, semr, fdr )
    el = compute_current_decomposed_energies(cplxInfos)
    print " ".join(map( lambda x:"{0}:{1:10.2f}".format(*x) , el ))
    
    print "  ===== decomposing interaction restraint ( diff subunits ) ====="
    threshold=0.0
    for e in filter ( lambda x:x[1] > threshold, [ (r.get_name(),r.evaluate(False)) for r in cplxInfos.scr ]) :
        print "   {0:>30s} ---> {1:10.2f}".format(*e)

    print "  ===== decomposing cohesion restrain (same subunit) ====="
    threshold=0.0
    for e in filter ( lambda x:x[1] > threshold, [ (r.get_name(),r.evaluate(False)) for r in cplxInfos.str ]) :
        print "   {0:>30s} ---> {1:10.2f}".format(*e)

def main():
        
    m = IMP.Model()
    m.set_log_level(IMP.SILENT)
#    tfiihInfos = build_TFIIH_subunits_info(m)
    cplxInfos = build_subunits_info(m)
    HGM.helpers.mute_all_restraints(m)
    
    dataDirSample   = "/home/arnaud/Desktop/TFIIH/data/3NIG/"
    sampleFileName  = "save-3NIG-HGM.txt"
    sampleFilePath  = os.path.join(dataDirSample,sampleFileName)
    
    mcs         = HGM.representation.MyConfigurationSet(cplxInfos)
    mcs.read_all_configs_from_file(sampleFilePath)
    mcs.load_configuration(0)
    print m.evaluate(False)
    
    output_energies_decomposition(cplxInfos)
    
        
if __name__ == "__main__" :
    main()
    print "...Finished !"
    
