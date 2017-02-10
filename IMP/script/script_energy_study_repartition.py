'''


'''

import os,sys

import IMP
#print "IMP version : ",IMP.get_module_version_info().get_version()
import HGM
import HGM.sampling
import HGM.energies
import HGM.display

import HGM.helpers
import HGM.helpersPlot

from alternate_configs import configs
#    MY TFIIH REPRESENTATION
#config_name_for_this_run    = "fixedGeom_0"
#config_name_for_this_run    = "fixedGeom_1"
#config_name_for_this_run    = "fixedGeom_1_1"
config_name_for_this_run    = "fixedGeom_EM_1_1"
#
#    PARAMETERS
#
#
#
tfiihRepresentationFileName = configs[config_name_for_this_run][0]
runDir                      = os.path.join("results",config_name_for_this_run)
saveDirSample               = os.path.join(runDir,"samples")
savePrefix                  = "saves"
eDir                        = os.path.join(runDir,"energies")
eFileName                   = "sample-energies.txt"
graphicsDir                 = os.path.join(runDir,"graphics","energies","traces")
graphicsFilePrefix          = "energy-trace--sample"
htmlDir                     = os.path.join(runDir,"graphics","energies")
htmlSummaryFileName         = "energy-traces.html"

for d in [os.path.join(runDir,"graphics"),
          os.path.join(runDir,"graphics","energies"),
          os.path.join(runDir,"graphics","energies","traces")
          ] :
    HGM.helpers.check_or_create_dir(d)

#
#    Sample configuration
#
#sample_indexes  = range(130)
#sample_indexes  = range(500)
#sample_indexes  = range(1000)
sample_indexes  = HGM.helpers.read_all_sample_indices(saveDirSample, savePrefix)
#nbGraphsPerLine     = 4

#    import the function responsible for modelisation of TFIIH complex
exec ( "from {0:s} import build_TFIIH_subunits_info".format( tfiihRepresentationFileName ) )




def output_score_repartition_table(energiesFilePath) :
    def output_score_table( scores ):
        print "scores range from", scores[0], "to", scores[-1]
        #
        minus10    = 0
        minus100   = 0
        minus1000  = 0
        minus10000 = 0
        large      = 0
        for i in scores :
            if   i < 10 :
                minus10     +=1
            elif i < 100 :
                minus100    +=1
            elif i < 1000 :
                minus1000   +=1
            elif i < 10000 :
                minus10000   +=1
            else :
                large += 1
        print "score <    10",minus10
        print "score <   100",minus100
        print "score <  1000",minus1000
        print "score <  1000",minus10000
        print "score >=10000",large
#        print "total sample size :",(minus10+minus100+minus1000+large)," or ",len(scores)
    
    e           = HGM.energies.EnergiesForSampleCollection()
    e.read_from_file(energiesFilePath)

    scores  = []
    scoresE = []
    for sample_index in e.get_sample_indices() :
        scores.extend( e.get_sample_energy(sample_index) )
        scoresE.append( e.get_statistics_for_sample(sample_index)[0] )
    #    
    scores.sort()
    scoresE.sort()
    #
    print "table for complete list of scores"
    output_score_table(scores)
    print "table for list of average scores"
    output_score_table(scoresE)

def main():
    output_score_repartition_table(os.path.join(eDir,eFileName))

    
        
if __name__ == "__main__" :
    main()
    print "...Finished !"
    
