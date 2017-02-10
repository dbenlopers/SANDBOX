'''
generate a sample based on MD sampling

'''

import os

import IMP
#print "IMP version : ",IMP.get_module_version_info().get_version()
import HGM
#import HGM.sampling
#import HGM.display

import HGM.energies
import HGM.helpers
import HGM.helpersPlot

from alternate_configs import configs
#    MY TFIIH REPRESENTATION
#config_name_for_this_run    = "fixedGeom_0"
#config_name_for_this_run    = "fixedGeom_1"
#config_name_for_this_run    = "fixedGeom_EM_1_1"
config_name_for_this_run    = "fixedGeom_EM_1_2"

#config_name_for_this_run    = "arp_EM_0_2"

#
#    PARAMETERS
#
#
#
subunitsRepresentationFileName = configs[config_name_for_this_run][0]
runDir                      = os.path.join("results",config_name_for_this_run)
saveDirSample               = os.path.join(runDir,"samples")
savePrefix                  = "saves"
eDir                        = os.path.join(runDir,"energies")
eFileName                   = "sample-energies.txt"
eFilePath = os.path.join(eDir,eFileName)
graphicsDir                 = os.path.join(runDir,"graphics","energies","histograms")
graphicsFilePrefix          = "energy-histogram--"
htmlDir                     = os.path.join(runDir,"graphics","energies")
htmlSummaryFileName         = "energy-histograms.html"

for d in [
          os.path.join(runDir,"graphics"),
          os.path.join(runDir,"graphics","energies"),
          os.path.join(runDir,"graphics","energies","histograms"),          
          ] :
    HGM.helpers.check_or_create_dir(d)


#
#    Sample configuration
#
#sample_indexes      = range(50)
sample_indexes      = HGM.helpers.read_all_sample_indices(saveDirSample, savePrefix)


nbGraphsPerLine     = 4

#
#    Histogram
#
nbBins              = 100


#    import the function responsible for modelisation of TFIIH complex
exec ( "from {0:s} import build_subunits_info".format( subunitsRepresentationFileName ) )



    
def dump_histo(graphicsFileName,energies,title):
    graphicsFileName
    xlabel  = None
    ylabel  = None
    
    meanX,stdX = HGM.helpers.compute_list_statistics(energies)
    title   = title+savePrefix+"size:{0:d} E{1:.2f}: s{2:.2f}:".format(len(energies),meanX,stdX)
    HGM.helpersPlot.plot_histogram_with_margins(
                os.path.join(graphicsDir,graphicsFileName),
                energies, nbBins, xlabel, ylabel, title)    


def dump_html(graphicsFileName,graphicsFileNames=None):
    print "-- generate HTML summary"
    fhtml = open(os.path.join(htmlDir,htmlSummaryFileName),"w")
    fhtml.write("<html><head><title>"+config_name_for_this_run+"</title></head><body>\n")
    
    fhtml.write("<H1>Global histogram</H1>\n")
    fhtml.write("     <img src=\""+os.path.join("histograms",graphicsFileName)+"\"/>\n\n\n")
    
    fhtml.write("<hr><H1>Sample histograms</H1>\n")
    fhtml.write("<table>\n")
    if graphicsFileNames != None :
        nbGraphs = 0
        newLine  = 1
        for graphicsFileName in graphicsFileNames :
            nbGraphs+=1
            if newLine : fhtml.write("  <tr>\n")
            newLine = (True)if((nbGraphs%nbGraphsPerLine)==0)else(False)
            fhtml.write("     <td><img src=\""+os.path.join("histograms",graphicsFileName)+"\"/></td>\n")
            if newLine : fhtml.write("  </tr>\n")
        if newLine == False : fhtml.write("  </tr>\n")
        fhtml.write("</table>\n")
    fhtml.write("</body></html>")
    fhtml.close()

def main():    
        
    m = IMP.Model()
    m.set_log_level(IMP.SILENT)
    tfiihInfos = build_subunits_info(m)
        
#    mcs         = HGM.representation.MyConfigurationSet(tfiihInfos)
    
    complete_sample_energies = []
    graphicsFileNames = []
    loop_index = 0
    
    print " - read energies file"    
    es=HGM.energies.EnergiesForSampleCollection()
    es.read_from_file(eFilePath)
    print " - generate histograms and filename from energies"
    for i in sample_indexes:
        loop_index+=1
        print i,"..",
        if loop_index % 15 == 0 : print ""
        graphicsFileName=graphicsFilePrefix+"sample--"+str(i)+".png"
        graphicsFileNames.append(graphicsFileName)
        energies =es.get_sample_energy(i)
#        saveName        = savePrefix+"--"+str(i)+".txt"
#        title   = "Energies histogram for sample \n"+saveName[:-4]
#        dump_histo(graphicsFileName,energies,title)
        complete_sample_energies.extend(energies)
#    complete_sample_energies = es.get_all_energies()


#    print " -- read samples, compute energies, and dump histo"
#    for i in sample_indexes:
#        loop_index+=1
#        print i,"..",
#        if loop_index % 15 == 0 : print ""
#        saveName        = savePrefix+"--"+str(i)+".txt"
#        mcs.read_all_configs_from_file(os.path.join(saveDirSample,saveName))
#        
#        energies = HGM.helpers.compute_sample_energies(mcs,m)
#        
#        graphicsFileName=graphicsFilePrefix+"sample--"+str(i)+".png"
#        graphicsFileNames.append(graphicsFileName)
#        title   = "Energies histogram for sample \n"+saveName[:-4]
#        dump_histo(graphicsFileName,energies,title)
#        
#        complete_sample_energies.extend(energies)
#        
#        mcs.delete_all_configs()

    
    graphicsFileName = graphicsFilePrefix+"all-samples.png"
    dump_histo(graphicsFileName,complete_sample_energies,"Energies histogram for all samples\n")
    
    dump_html(graphicsFileName,graphicsFileNames)

        
if __name__ == "__main__" :
    main()
    print "...Finished !"
    
