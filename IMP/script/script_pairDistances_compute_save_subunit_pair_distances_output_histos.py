'''

'''

import os
from time import time

import IMP
#print "IMP version : ",IMP.get_module_version_info().get_version()
import HGM
import HGM.sampling
import HGM.display
import HGM.distances
import HGM.energies


import HGM.helpers
import HGM.helpersPlot

from numpy import corrcoef

from alternate_configs import configs
#    MY TFIIH REPRESENTATION
#config_name_for_this_run    = "fixedGeom_0"
#config_name_for_this_run    = "fixedGeom_1_1"
#config_name_for_this_run    = "fixedGeom_EM_1_1"
config_name_for_this_run    = "fixedGeom_EM_1_2"

#
#    PARAMETERS
#
#
#
tfiihRepresentationFileName = configs[config_name_for_this_run][0]
runDir                      = os.path.join("results",config_name_for_this_run)
saveDirSample               = os.path.join(runDir,"samples")
savePrefix                  = "saves"


dDir                        = os.path.join(runDir,"distances")
dmDir                       = os.path.join(dDir,"distMatrices")
dhDir                       = os.path.join(dDir,"distHistograms")
#dhSubDir                    = "./distHistograms/"
dhSubDir                    = "distHistograms/"
ccDir                       = os.path.join(dDir,"crossCorel")

eDir                        = os.path.join(runDir,"energies")
eFileName                   = "sample-energies-1000.txt"

for d in [dDir,dmDir,dhDir,ccDir] :
    HGM.helpers.check_or_create_dir(d)

#
#    Sample configuration
#

def get_sample_indices_under_energy_threshold(threshold=10):
    print "read energies"
    e           = HGM.energies.EnergiesForSampleCollection()
    e.read_from_file(os.path.join(eDir,eFileName))
    sample_indexes         = e.get_sample_indices_below_threshold(threshold) 
    print "got",len(sample_indexes),"seeded samples above threshold",threshold
    return sample_indexes 

#sample_indexes      = range(10)
#sampleDescription   = "10"
#distMatrixFileName  = "dist_matrix_test_10.pickle"
#htmlFileName        = "subunits_dist_histo_test_10.html"
#ccFileName          = "crossCorelations-10.txt"

#sample_indexes      = range(1000)
#sampleDescription   = "1000"
#distMatrixFileName  = "dist_matrix_test_1000.pickle"
#htmlFileName        = "subunits_dist_histo_test_1000.html"
#ccFileName          = "crossCorelations-1000.txt"


#sample_indexes = get_sample_indices_under_energy_threshold(10)
#sampleDescription   = str(len(sample_indexes))
#distMatrixFileName  = "dist_matrix_test_"+sampleDescription+".pickle"
#htmlFileName        = "subunits_dist_histo_test_"+sampleDescription+".html"
#ccFileName          = "crossCorelations-"+sampleDescription+".txt"

########################

#sample_indexes = range(100,187)
#sampleDescription   = "EM1.1-"+str(len(sample_indexes))
#distMatrixFileName  = "dist_matrix_test_"+sampleDescription+".pickle"
#htmlFileName        = "subunits_dist_histo_test_"+sampleDescription+".html"
#ccFileName          = "crossCorelations-"+sampleDescription+".txt"

sample_indexes = HGM.helpers.read_all_sample_indices(saveDirSample, savePrefix)
#sampleDescription   = "EM1.1i-"+str(len(sample_indexes))
#sampleDescription   = "EM1.2-"+str(len(sample_indexes))
sampleDescription   = "EM1_2-"+str(len(sample_indexes))
distMatrixFileName  = "dist_matrix_test_"+sampleDescription+".pickle"
htmlFileName        = "subunits_dist_histo_test_"+sampleDescription+".html"
ccFileName          = "crossCorelations-"+sampleDescription+".txt"


distMatrixFilePath  = os.path.join(dmDir,distMatrixFileName)
ccFilePath          = os.path.join(ccDir,ccFileName)
htmlFilePath        = os.path.join(dDir,htmlFileName)






#    
#    print "-- read samples..."
#    for i in sample_indexes:
#        print i,"..",
#        saveName        = savePrefix+"--"+str(i)+".txt"
#        mcs.read_all_configs_from_file(os.path.join(saveDirSample,saveName))
#    print "   loaded",mcs.get_number_of_configurations(),"configurations"



def read_samples(mcs,sid=sample_indexes):
    print "-- read samples..."
    for i in sid:
        print i,"..",
        saveName        = savePrefix+"--"+str(i)+".txt"
        mcs.read_all_configs_from_file(os.path.join(saveDirSample,saveName))
    print "   loaded",mcs.get_number_of_configurations(),"configurations"

def compute_subunits_dist_matrix(mcs,tfiihInfos):
    print "-- Computing dist matrix",
    pdms = HGM.distances.ParticlesPairDistanceMatrixSet(mcs)
    print "    (",pdms.get_number_of_configurations(),"configurations)"
    
    print "-- Computing subunits dist matrix",
    sdms = HGM.distances.SubunitsPairDistanceMatrixSet(tfiihInfos,pdms)
    print "    (",sdms.get_number_of_configurations(), "configurations)"
    
    del pdms
    
    return sdms


def compute_and_save_covariance(sdms):
    print "  - Extract distances per edges"
    edge_len=[]
    edges=[]
    subunits=sdms.get_subunit_names()
    for i in range(1,len(subunits)):
        for j in range(i):
            edge_len.append( sdms.get_distances(subunits[i],subunits[j]) )
            edges.append(subunits[i]+"-"+subunits[j])
    print "  - Compute correlation matrix"
    corr=corrcoef(edge_len)
    print "  - Compiling, sorting cross correlations scores"
    correl=[]
    for i in range(1,len(edges)):
        for j in range(i):
            correl.append( ("{0:>15s}:{1:<15s} {2:4.2f}".format(edges[i],edges[j],corr[i][j]),corr[i][j]) )
    correl.sort(key=lambda x:x[1])
    print "  - saving cross correlations scores to",ccFilePath
    ccf = open(ccFilePath,"w")
    for i in range(len(correl)):
        ccf.write( correl[i][0] + "\n" )


def dump_all_subunits_histograms(sdms,sampleName,bins=60):
    """ produces histograms for all pairs in the half matrix """
#    names=protein_info_dict.keys()
    names = sdms.get_subunit_names()
    img_files=[]
    
    def make_png_name(name1,name2,sn=sampleName):
        return "subunits-dist-histo--"+str(sn)+"--"+name1+"-"+name2+".png"
    def make_png_stats_name(name1,name2,sn=sampleName):    
        return "subunits-dist-histo--"+str(sn)+"--stats--"+name1+"-"+name2+".png"
    
    def create_histograms():
        for i in range(1,len(names)) :
            name1 = names[i]
            for j in range (0,i):
                name2 =  names[j]
                print "output hist for ",name1,name2
                values=sdms.get_distances(name1,name2)
                
                xlabel      = "distance (A)"
                ylabel      = "number of models"
                title       = "Distance histograms for subunits\n"+name1+" and "+name2
                imgFileName = make_png_name(name1, name2)
                imgFileName2= make_png_stats_name(name1, name2)
                imgFilePath = os.path.join(dhDir,imgFileName)
                imgFilePath2= os.path.join(dhDir,imgFileName2)
                
                HGM.helpersPlot.plot_histogram(imgFilePath, values, bins, xlabel, ylabel, title)
                HGM.helpersPlot.plot_histogram_with_margins(imgFilePath2, values, bins, xlabel, ylabel, title)
            
#            img_files.append(imgFileName)
    
#    f=open(htmlFilePath,"w")
#    f.write("""<HTML><HEAD>
#        <TITLE>Subunits pair distances HISTOGRAMS</TITLE>
#        <base href='"""+ dhSubDir +"""'/>
#        </HEAD><BODY>""")
#    count = 1
#    for img_file in img_files :
#        if (count%4)==0 :
#            f.write("<BR>\n")
#        f.write("<img src=\""+img_file+"\">\n")
#        count += 1 
#    f.write('</BODY></HTML>\n')
#    f.close()

    def create_html_document(htmlFilePath,png_function):
        print "-- generate HTML summary at",htmlFilePath
        fhtml = f=open(htmlFilePath,"w")
        fhtml.write("<html><head><title>Subunits pair distances HISTOGRAMS</title><base href='"+ dhSubDir +"'/></head><body>\n")    
        fhtml.write("<hr><H1>Sample histograms</H1>\n")
        
        fhtml.write("<table>\n")
        
        fhtml.write(" <tr>\n")
        fhtml.write("   <td></td>\n")
        for i in range( len(names) ) :
            fhtml.write("   <td><b>"+names[i]+"</b></td>\n")
        fhtml.write(" </tr>\n")
        for i in range( len(names) ) :
            fhtml.write(" <tr>\n")
            fhtml.write("   <td><b>"+names[i]+"</b></td>\n")
            for j in range(i) :
                fhtml.write("   <td><img src='"+png_function(names[i],names[j])+"'/></td>\n")
            fhtml.write("   <td></td>\n")
            for j in range(i+1,len(names)) :
                fhtml.write("   <td><img src='"+png_function(names[j],names[i])+"'/></td>\n")
            fhtml.write(" </tr>\n")
        fhtml.write("</table>\n")
        fhtml.write("</body></html>\n")
        fhtml.close()
    
    
    
    create_histograms()
    create_html_document(htmlFilePath,make_png_name)
#    create_html_document(htmlStatsFilePath,make_png_stats_name)



#    import the function responsible for modelisation of TFIIH complex
exec ( "from {0:s} import build_TFIIH_subunits_info".format( tfiihRepresentationFileName ) )




def main():

    m = IMP.Model()
    m.set_log_level(IMP.SILENT)
    
    tfiihInfos = build_TFIIH_subunits_info(m)
    HGM.helpers.mute_all_restraints(m)
        
    mcs         = HGM.representation.MyConfigurationSet(tfiihInfos)
    
    time_start = time()
    try :
        sdms = HGM.helpers.loadPickleDistMatrix(distMatrixFilePath,tfiihInfos)
        print "   loaded subunit dist matrix set from existing pickled file {0:s}".format(distMatrixFilePath)
    except :
        print "   pickle file {0:s} does not exist, generating and saving subunits distance matrix".format(distMatrixFilePath)
        read_samples(mcs,sample_indexes)
        sdms = compute_subunits_dist_matrix(mcs,tfiihInfos)
        HGM.helpers.savePickleDistMatrix(distMatrixFilePath, sdms)
    time_stop = time()

    print "  -> subunits pair distance matrix generated ({0:.1f}s) ({1:d} configs)".format(time_stop-time_start,sdms.get_number_of_configurations())
    

    time_start = time()
    dump_all_subunits_histograms(sdms,sampleDescription)
    time_stop = time()
    print "  -> subunits pair distance histograms generated ({0:.1f}s)".format(time_stop-time_start)

    
    
    time_start = time()
    compute_and_save_covariance(sdms)
    time_stop = time()
    print "  -> covariance studied in ({0:.1f}s)".format(time_stop-time_start)
    
    
    
    
    
    
    
    
    
if __name__ == "__main__" :
    time_start = time()
    main()
    time_stop = time()
    print "All done... (in {0:.1f}s)".format(time_stop-time_start)
    
    
