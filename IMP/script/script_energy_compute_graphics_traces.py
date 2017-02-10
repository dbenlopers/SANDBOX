'''

'''

import os,sys

import IMP
print "IMP version : ",IMP.get_module_version_info().get_version()
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
config_name_for_this_run    = "fixedGeom_1_1"

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
sample_indexes  = range(1000)
nbGraphsPerLine     = 4

#    import the function responsible for modelisation of TFIIH complex
exec ( "from {0:s} import build_TFIIH_subunits_info".format( tfiihRepresentationFileName ) )



def compute_energies_and_make_graph():
    m = IMP.Model()
    m.set_log_level(IMP.SILENT)
    tfiihInfos = build_TFIIH_subunits_info(m)
    mcs         = HGM.representation.MyConfigurationSet(tfiihInfos)
    
    graphicsFileNames=[]
    print "-- read samples and write energy graph"
    loop_index = 0
    for i in sample_indexes:
        loop_index+=1
        print i,"..",
        if loop_index % 15 == 0 : print ""; sys.stdout.flush()
        saveName        = savePrefix+"--"+str(i)+".txt"
        mcs.read_all_configs_from_file(os.path.join(saveDirSample,saveName))
        
        energies = HGM.helpers.compute_sample_energies(mcs,m)
        
        graphicsFileName   = graphicsFilePrefix+"--"+str(i)+".png"
        HGM.helpersPlot.plot_simple_function_as_list(
                       os.path.join(graphicsDir,graphicsFileName),
                       energies ,
                       "frame index" ,
                       "energy graph for sample\n"+saveName )
        
        graphicsFileNames.append(graphicsFileName)
        
        mcs.delete_all_configs()
    return graphicsFileNames


def read_energies_and_make_graph(energiesFilePath):
    e           = HGM.energies.EnergiesForSampleCollection()
    e.read_from_file(energiesFilePath)
    
    graphicsFileNames=[]
    print "-- write energy graphs from energies file"
    loop_index = 0
    for i in sample_indexes:
        loop_index+=1
        print i,"..",
        if loop_index % 15 == 0 : print ""; sys.stdout.flush()
        saveName        = savePrefix+"--"+str(i)+".txt"
        
        energies = e.get_sample_energy(i)
        
        graphicsFileName   = graphicsFilePrefix+"--"+str(i)+".png"
        HGM.helpersPlot.plot_simple_function_as_list(
                       os.path.join(graphicsDir,graphicsFileName),
                       energies ,
                       "frame index" ,
                       "energy graph for sample\n"+saveName )
        
        graphicsFileNames.append(graphicsFileName)
        
    return graphicsFileNames


def output_summary_html(htmlFilePath,graphicsFileNames):
    print "-- generate HTML summary"
    fhtml = open(htmlFilePath,"w")
    fhtml.write("<html><head><title>"+config_name_for_this_run+"</title></head><body>\n<table>\n")
    nbGraphs = 0
    newLine  = 1
    for graphicsFileName in graphicsFileNames :
        nbGraphs+=1
        if newLine : fhtml.write("  <tr>\n")
        newLine = (True)if((nbGraphs%nbGraphsPerLine)==0)else(False)
        fhtml.write("     <td><img src=\""+os.path.join("traces",graphicsFileName)+"\"/></td>\n")
        if newLine : fhtml.write("  </tr>\n")
    if newLine == False : fhtml.write("  </tr>\n")
    fhtml.write("</table></body></html>")
    fhtml.close()

def main():
#    graphicsFileNames = compute_energies_and_make_graph()
    print "read_energies_and_make_graph"
    graphicsFileNames = read_energies_and_make_graph(os.path.join(eDir,eFileName))
    
#    print "output_summary_html" 
#    output_summary_html(os.path.join(htmlDir,htmlSummaryFileName),graphicsFileNames)
    
        
if __name__ == "__main__" :
    main()
    print "...Finished !"
    
