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


# config_name_for_this_run    = "3NIG_EM_0_2aC"                  
# config_name_for_this_run    = "3NIG_EM_0_2aC_20"     
# config_name_for_this_run    = "3NIG_EM_0_2lmC"
# config_name_for_this_run    = "3NIG_EM_0_2lmC_20"
config_name_for_this_run    = "3NIG_EM_0_2lC"
# config_name_for_this_run    = "3NIG_EM_0_2lC_20" 
# config_name_for_this_run    = "3NIG_EM_0_3ambiC"  
# config_name_for_this_run    = "3NIG_EM_0_3ambiC_20"



# config_name_for_this_run    = "3IAM_EM_0_3a"
# config_name_for_this_run    = "3IAM_EM_0_3lm"
# config_name_for_this_run    = "3IAM_EM_0_3l"

# config_name_for_this_run    = "3IAM_EM_0_4a"
# config_name_for_this_run    = "3IAM_EM_0_4lm"
# config_name_for_this_run    = "3IAM_EM_0_4l"

# config_name_for_this_run    = "3IAM_EM_0_5a"
# config_name_for_this_run    = "3IAM_EM_0_5lm"
# config_name_for_this_run    = "3IAM_EM_0_5l"


# config_name_for_this_run    = "4FXG_EM_0_1a_40"
# config_name_for_this_run    = "4FXG_EM_0_1lm_40"
# config_name_for_this_run    = "4FXG_EM_0_1l_40"
# config_name_for_this_run    = "4FXG_EM_0_1a_30"
# config_name_for_this_run    = "4FXG_EM_0_1lm_30"
# config_name_for_this_run    = "4FXG_EM_0_1l_30"
# config_name_for_this_run    = "4FXG_EM_0_1a_20"
# config_name_for_this_run    = "4FXG_EM_0_1lm_20"
# config_name_for_this_run    = "4FXG_EM_0_1l_20"
#
#    PARAMETERS
#
#
#
sample_tag                 = "low"


cplxRepresentationFileName = configs[config_name_for_this_run][0]
runDir                      = os.path.join("results",config_name_for_this_run)
savePrefix                  = "saves"
saveDirSample               = os.path.join(runDir,"samples")


dDir                        = os.path.join(runDir,"distances-"+sample_tag)
dmDir                       = os.path.join(dDir,"distMatrices")
dhDir                       = os.path.join(dDir,"distHistograms")
dhSubDir                    = "distHistograms/"
ccDir                       = os.path.join(dDir,"crossCorel")
eDir                        = os.path.join(runDir,"energies")



for d in [dDir,dmDir,dhDir,ccDir] :
    HGM.helpers.check_or_create_dir(d)



savePrefix = "saves"
sDir = os.path.join(runDir, "samples")
sample_indexes      =  HGM.helpers.read_all_sample_indices(sDir, savePrefix)



sampleDescription   = config_name_for_this_run + "--range-" +str(sample_tag)+ "--"
distMatrixFileName  = "beads-dist-matrix--"+sampleDescription+".pickle"
htmlFileName        = "beads-dist-histo--"+sampleDescription+".html"
ccFileName          = "beads_crossCorelations_-"+sampleDescription+".txt"
sseFileName         = "subsamples-energies.txt"
eFileName           = "sample-energies.txt"


#eFileName                   = "sample-energies"++".txt"

distMatrixFilePath  = os.path.join(dmDir,distMatrixFileName)
ccFilePath          = os.path.join(ccDir,ccFileName)
htmlFilePath        = os.path.join(dDir,htmlFileName)
energiesFilePath    =    os.path.join(eDir,eFileName)
subsamplesEnergyfilePath    =    os.path.join(eDir,sseFileName)



#    
#    print "-- read samples..."
#    for i in sample_indexes:
#        print i,"..",
#        saveName        = savePrefix+"--"+str(i)+".txt"
#        mcs.read_all_configs_from_file(os.path.join(saveDirSample,saveName))
#    print "   loaded",mcs.get_number_of_configurations(),"configurations"




def readSortedConfigs( indices, sample, saveDirSample ):
    """
    @param indices:  list of configuration indices ("sid:ssidx")
    @param saveDirSample:  where the configuration files are saved
    @return cs:    a cConfigurationSet object in which I I'll store all  
    """
#    subunitsInfos = mcs.get_prot_info_model()
    print "  ... reading specific configurations"
    for cidx in indices:
        (si,isi)=cidx.split(":")
        (si,isi)=(int(si),int(isi))
        filePath          = HGM.helpers.forge_sample_path(saveDirSample, savePrefix, si)
        sample.read_configs_from_file(filePath, [isi])
#    print "sample size:",sample.get_number_of_configurations()
#    return sample

def read_samples(mcs,sid=sample_indexes):
    print "-- read samples..."
    for i in sid:
        if i%15==0: print ""
        print i,"..",
        saveName        = savePrefix+"--"+str(i)+".txt"
        mcs.read_all_configs_from_file(os.path.join(saveDirSample,saveName))
    print "   loaded",mcs.get_number_of_configurations(),"configurations"

def read_sorted_sample(mcs,sample_tag):
    print "-- read sorted samples"
    sse = HGM.energies.SubsamplesEnergies()
        
    print "getting subsamples energies from samples energies"
    sse.read_samples_energies_from_file(energiesFilePath)

#    print "getting subsamples energies from subsample energy file"
#    sse.read_from_file(subsamplesEnergyfilePath)
    
    print "saving subsamples energies"
    sse.write_to_file(subsamplesEnergyfilePath)
    print "ARE",len(sse.get_sorted_subsamples_energies()),"conformations in the sample energies"

    sl = sse.get_sorted_subsamples_energies()
    print "GOT",len(sl),"indices"
    
    readSortedConfigs( map(lambda x:x[0], sl), mcs, saveDirSample )
    
    
    


def compute_domains_dist_matrix(mcs):
    print "-- Computing dist matrix",
    pdms = HGM.distances.ParticlesPairDistanceMatrixSet(mcs)
    print "    (",pdms.get_number_of_configurations(),"configurations)"
    
    return pdms


def compute_and_save_beads_covariance(pdms):
    print "  - Extract distances per edges"
    edge_len=[]
    edges=[]
    names   = map(lambda p:p.get_name(),pdms.get_particles())
#    subunits=sdms.get_subunit_names()
    for i in range(1,len(names)):
        for j in range(i):
            edge_len.append( pdms.get_distances(i,j) )
            edges.append(names[i]+"-"+names[j])
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


def dump_all_beads_histograms(pdms,sampleName,bins=60):
    """ produces histograms for all pairs in the half matrix """
#    names=protein_info_dict.keys()
    names = map(lambda p:p.get_name(),pdms.get_particles())
    print "BEAD NAMES :",names
#    pdms.get_subunit_names()
    img_files=[]
    
    def make_png_name(name1,name2,sn=sampleName):
        return "beads-dist-histo--"+str(sn)+"--"+name1+"-"+name2+".png"
    def make_png_stats_name(name1,name2,sn=sampleName):
        return "beads-dist-histo--"+str(sn)+"--stats--"+name1+"-"+name2+".png"
    
    def create_histograms():
        for i in range(1,len(names)) :
            name1 = names[i]
            for j in range (0,i):
                name2 =  names[j]
                print "output hist for ",name1,name2
                values=pdms.get_distances(i,j)
                
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
        fhtml.write("<html><head><title>Beads pair distances HISTOGRAMS</title><base href='"+ dhSubDir +"'/></head><body>\n")    
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
exec ( "from {0:s} import build_subunits_info".format( cplxRepresentationFileName ) )




def main():

    m = IMP.Model()
    m.set_log_level(IMP.SILENT)
    
    cplxInfos = build_subunits_info(m)
    HGM.helpers.mute_all_restraints(m)
        
    mcs         = HGM.representation.MyConfigurationSet(cplxInfos)
    pdms        = HGM.distances.ParticlesPairDistanceMatrixSet(mcs)
    
    time_start = time()
    try :
        raise ValueError() # force matrix computation
        pdms.load_pickled(distMatrixFilePath)
        print "   loaded domains dist matrix set from existing pickled file {0:s}".format(distMatrixFilePath)
    except :
        print "   pickle file {0:s} does not exist, generating and saving subunits distance matrix".format(distMatrixFilePath)
#        read_samples(mcs,sample_indexes)
#        read_sorted_sample(mcs,sample_tag)
        mcs.read_all_configs_from_file('/home/arnaud/Desktop/TFIIH/src/coarse2/results/' + config_name_for_this_run + '/samples-alt/low_energy_subsamples__0-50__1000.txt')
        pdms = compute_domains_dist_matrix(mcs)
        pdms.save_pickled(distMatrixFilePath)
    time_stop = time()

    print "  -> beads pair distance matrix generated ({0:.1f}s) ({1:d} configs)".format(time_stop-time_start,pdms.get_number_of_configurations())

    time_start = time()
    dump_all_beads_histograms(pdms,sampleDescription)
    time_stop = time()
    print "  -> subunits pair distance histograms generated ({0:.1f}s)".format(time_stop-time_start)

    
    
    time_start = time()
    compute_and_save_beads_covariance(pdms)
    time_stop = time()
    print "  -> covariance studied in ({0:.1f}s)".format(time_stop-time_start)
    
    
    
    
    
    
    
    
    
if __name__ == "__main__" :
    time_start = time()
    main()
    time_stop = time()
    print "All done... (in {0:.1f}s)".format(time_stop-time_start)
    
    
