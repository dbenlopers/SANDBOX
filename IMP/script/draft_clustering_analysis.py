'''
@author : kopp

Script qui calcul les stats sur les cluster provenant du draft_cluster_models.py
 et de script_energy_plot__E_vs_RSMDtoSolution__dump_file.py
 
 -print stat for all cluster
 -create scatter-plot for each cluster in different threshold
 -save all models from each cluster and save in specific  file with mcs format
 -save centroid and average models from each cluster and save in specific file
 -create html file for all cluster (or n biggest ) in specific file by threshold  !!!!! not yet


'''

import IMP, IMP.algebra, IMP.core, IMP.atom
import HGM, HGM.helpers, HGM.helpersPlot, HGM.representation, HGM.samples
from alternate_configs import configs
import sys
import os
import re
import time
import HGM.times
import numpy ;
import scipy;
from matplotlib.ticker import NullFormatter
from matplotlib import pyplot as plt, numpy as np
import matplotlib.cm as cm




#config_name_for_this_run    = "arp_EM_0_2aLMs"
#config_name_for_this_run    = "arp_EM_0_2aLA1"
#config_name_for_this_run        = "arp_EMd_0_2aLM"

#config_name_for_this_run    = "3NIG_EM_0_2aC"                  
#config_name_for_this_run    = "3NIG_EM_0_2aC_20"     
#config_name_for_this_run    = "3NIG_EM_0_2lmC"
#config_name_for_this_run    = "3NIG_EM_0_2lmC_20"
#config_name_for_this_run    = "3NIG_EM_0_2lC"
#config_name_for_this_run    = "3NIG_EM_0_2lC_20" 
#config_name_for_this_run    = "3NIG_EM_0_3ambiC"  
config_name_for_this_run    = "3NIG_EM_0_3ambiC_20"
        
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

cplxRepresentationFileName  = configs[config_name_for_this_run][0]
runDir                      = os.path.join("results",config_name_for_this_run)
sDir                        = os.path.join(runDir,"samples")
asDir                        = os.path.join(runDir,"samples-alt")
cDir                        = os.path.join(runDir,"clusters")
rDir                        = os.path.join(runDir,"rmsd")
gDir                        = os.path.join(runDir,"graphics")
htmlDir                     = os.path.join(runDir,"html_cluster")

for d in [htmlDir] :
    HGM.helpers.check_or_create_dir(d)


#rmsdDir                     = os.path.join(runDir,"rmsd")
#dotFilePath              = os.path.join(rmsdDir,"rmsdVSenergy--"+sample_tag+".txt")


nbBins                  = 60



########################################### PARAMETERS ############################

#Sample_indexes
sample_tag                  = "1000 best" 

#Clustering method
methode_clust               = "centroid"

#Save scatter-plot for all cluster
save_all_cluster_scatter=True
#save_all_cluster_scatter=False

#print stat for cluster 
print_stat=True
#print_stat=False

#seuil_html for html
seuil_html=0

#save all model of cluster in mcs file
save_models_clust=True
#save_models_clust=False

#parameters for scatter-plot size
score_max=40000
rmsd_max=100



########################################### PARAMETERS ############################


exec ( "from {0:s} import build_subunits_info".format( cplxRepresentationFileName ) )


energie_rmsd_file = []
cluster_file = []
sample_list=[] #stock les samples


cluster_list_3=[] #stock les cluters avec thres=3
cluster_list_6=[] #stock les cluters avec thres=6
cluster_list_9=[] #stock les cluters avec thres=9
cluster_list_15=[] #stock les cluters avec thres=15


plt.figure(1, figsize=(8,8))


#partie html

def init_html_file(file):
    init='<!DOCTYPE html>\n\
<html>\n\
    <head>\n\
        <meta charset="utf-8" />\n\
        <title>Clustering Results</title>\n\
        <p>'+config_name_for_this_run+'</p>\n\
        <link rel="stylesheet" type="text/css" href="cluster.css">\n\
        <script type="text/javascript" language="Javascript" \n\
        src="http://www.kryogenix.org/code/browser/sorttable/sorttable.js">\n\
        </script>\n\
    </head>\n\
    <body>\n\
     <h1>Cluster Statistique</h1>\n\
     <table  class="sortable">\n\
     <thead>\n\
        <tr>\n\
            <th>Cluster id </th>\n\
            <th>Size</th>\n\
            <th>Min score</th>\n\
            <th>Max score</th>\n\
            <th>Mean score</th>\n\
            <th>id config min score</th>\n\
            <th>Min rmsd</th>\n\
            <th>Max rmsd</th>\n\
            <th>Mean rmsd</th>\n\
            <th>id config min rmsd</th>\n\
            <th>Other</th>\n\
        </tr>\n\
     </thead> \n\
     <tbody>\n'
    
    
    f=open(file,"w")
    f.write(init)
    f.close()

def add_content_html_file(file,content):    
    f=open(file,"a")
    f.write(content)
    f.close()


def close_html_file(file):
    end='     </tbody> \n\
     </table>\n\
    </body>\n\
</html>\n'
    
    
    f=open(file,"a")
    f.write(end)
    f.close()



    
#partie stat clustering
class cluster :
    

    def __init__(self,name):
        self.id=name
        self.liste=[]
   
    def get_id(self):
        return self.id
        
    def add_sample(self,sample):
        self.liste.append(sample)
        
    def get_size(self):    
        return len(self.liste())
    
    def printing(self):
        print self.id+"   size : "+str(len(self.liste))

    def compute_stat(self):
        max_score=-sys.maxint
        min_score=+sys.maxint
        mean_score=0
        max_rmsd=-sys.maxint
        min_rmsd=+sys.maxint
        mean_rmsd=0
        id_min_score=0
        id_min_rmsd=0
        
        score_list={}
        rmsd_list={}
        
        liste_score=[]
        liste_rmsd=[]
        
        for i in range(len(self.liste)):
            sample=load_sample_from_list(sample_list,self.liste[i])
            score=sample.get_e()
            rmsd=sample.get_rmsd()
            liste_score.append(float(score))
            liste_rmsd.append(float(rmsd))
            
            score_list[sample.id]=score
            rmsd_list[sample.id]=rmsd
        
        max_score="{0:.2f}".format(max(liste_score))
        min_score="{0:.2f}".format(min(liste_score))
        id_min_score=min(score_list, key=lambda x: score_list.get(x))
        
        max_rmsd="{0:.2f}".format(max(liste_rmsd))
        min_rmsd="{0:.2f}".format(min(liste_rmsd))
        id_min_rmsd=min(rmsd_list, key=lambda x: score_list.get(x))
        
        mean_score="{0:.2f}".format(numpy.mean(liste_score))
        mean_rmsd="{0:.2f}".format(numpy.mean(liste_rmsd))
        
        liste=[]
        liste.append(max_score)
        liste.append(min_score)
        liste.append(mean_score)
        liste.append(max_rmsd)
        liste.append(min_rmsd)
        liste.append(mean_rmsd)
        liste.append(id_min_score)
        liste.append(id_min_rmsd)
        return liste

             
                

class sample :
      
    def __init__(self,name):
        self.id=name
        self.e=0
        self.rmsd=0
        self.mcs_id=None
    
    def set_e(self,energie):
        self.e=energie
        
    def get_e(self):
        return self.e
        
    def set_rmsd(self,rmsd):
        self.rmsd=rmsd
        
    def get_rmsd(self):
        return self.rmsd

    def set_mcs_id(self,id):
        self.mcs_id=id
        
    def printing(self):
        print self.id+" "+self.e+" "+self.rmsd
        
    def get_name(self):
        return self.id




#return true or false if cluster id is in cluster list
def find_cluster(cluster_list,indexe):
    for i in range(len(cluster_list)):
        if cluster_list[i].get_id()==indexe :
            return True
    else :
        return False


def get_cluster(cluster_list,indexe):
    for i in range(len(cluster_list)) :
        if cluster_list[i].get_id()==indexe :
            return cluster_list[i]

#return cluster from id given in argument
def load_cluster(file_path) :
    fp=open(file_path,"r")
    for line in fp :
        if line[0]=="#" :
            continue
        line_splited = line.split()
#        print line_splited
        #ajout ds thrs 3
        if find_cluster(cluster_list_3, line_splited[2])==False :
            clust=cluster(line_splited[2])
            cluster_list_3.append(clust)
            clust=get_cluster(cluster_list_3,line_splited[2])
            sample_add=find_sample(sample_list, line_splited[0])
            clust.add_sample(sample_add)
        else :
            clust=get_cluster(cluster_list_3,line_splited[2])
            sample_add=find_sample(sample_list, line_splited[0])
            clust.add_sample(sample_add)
        #ajout ds thrs 6
        if find_cluster(cluster_list_6, line_splited[3])==False :
            clust=cluster(line_splited[3])
            cluster_list_6.append(clust)
            clust=get_cluster(cluster_list_6,line_splited[3])
            sample_add=find_sample(sample_list, line_splited[0])
            clust.add_sample(sample_add)
        else :
            clust=get_cluster(cluster_list_6,line_splited[3])
            sample_add=find_sample(sample_list, line_splited[0])
            clust.add_sample(sample_add)
        #ajout ds thrs 9
        if find_cluster(cluster_list_9, line_splited[4])==False :
            clust=cluster(line_splited[4])
            cluster_list_9.append(clust)
            clust=get_cluster(cluster_list_9,line_splited[4])
            sample_add=find_sample(sample_list, line_splited[0])
            clust.add_sample(sample_add)
        else :
            clust=get_cluster(cluster_list_9,line_splited[4])
            sample_add=find_sample(sample_list, line_splited[0])
            clust.add_sample(sample_add)
        #ajout ds thrs 15
        if find_cluster(cluster_list_15, line_splited[5])==False :
            clust=cluster(line_splited[5])
            cluster_list_15.append(clust)
            clust=get_cluster(cluster_list_15,line_splited[5])
            sample_add=find_sample(sample_list, line_splited[0])
            clust.add_sample(sample_add)
        else :
            clust=get_cluster(cluster_list_15,line_splited[5])
            sample_add=find_sample(sample_list, line_splited[0])
            clust.add_sample(sample_add)

        
        
        
    fp.close()


def load_sample_from_file(sample_file_path,idx_sample) :
    fp =open(sample_file_path,"r")
    fp.close()


def find_sample(sample_list,indexe):
    for i in range(len(sample_list)) :
        if sample_list[i].get_name()==indexe :
            return sample_list[i].id
    

def load_sample_from_list(sample_list,indexe):
    for i in range(len(sample_list)) :
        if sample_list[i].get_name()==indexe :
            return sample_list[i]


def load_scoring(file_path) :
    fp=open(file_path,"r")
    for line in fp :
        if line[0]=="#":
            continue
        line_splited = line.split()
        
#        !!!!!!!!!!!!!!! modif ici !!!!!!!!!!!
#        re_splited = line_splited[0].split("/samples/")
        re_splited = line_splited[0].split("/samples-alt/")
        
        id_config=re_splited[1]
        id_config= sample(id_config)
        id_config.set_e(line_splited[2])
        id_config.set_rmsd(line_splited[1])
#        id_config.printing()
        sample_list.append(id_config)
    fp.close()




def draw_single_cluster_plot(plotFilePath,dots):
#    print "# creating data from dots"
    X=[];Y=[]
    for x,y in dots :
        X.append(float(x));Y.append(float(y))

    nullfmt   = NullFormatter()         # no labels
    
    
    
#    print "# definitions for the axes"
    left, width = 0.1, 0.65
    bottom, height = 0.1, 0.65
    bottom_h = left_h = left+width+0.02
    
    rect_scatter = [left, bottom, width, height]
    rect_histx = [left, bottom_h, width, 0.2]
    rect_histy = [left_h, bottom, 0.2, height]
    
#    print "start with a rectangular Figure"
    plt.figure(1, figsize=(8,8))
    
    axScatter = plt.axes(rect_scatter)
    axHistx = plt.axes(rect_histx)
    axHisty = plt.axes(rect_histy)
    
#    print "# no labels"
    axHistx.xaxis.set_major_formatter(nullfmt)
    axHisty.yaxis.set_major_formatter(nullfmt)
    
#    print "# the scatter plot:"
#    axScatter.scatter(X, Y)

    axScatter.plot(X, Y,'.')
    
#    print "# now determine nice limits by hand:"
#    binwidth = 0.25
#    nbBins = 60
#    print " -1"
#    xymax = np.max( [np.max(np.fabs(X)), np.max(np.fabs(Y))] )
#    xymin = np.min( [np.min(np.fabs(X)), np.min(np.fabs(Y))] )
    xmax = np.max(X); ymax = np.max(Y)
    xmin = np.min(X); ymin = np.min(Y)
#    taille fixe sur les histo
#    xmin=0;xmax=score_max
#    ymin=0;ymax=rmsd_max
             
#    print xymax,xymin
#    print " -2"
#    lim = ( int(xymax/binwidth) + 1) * binwidth
#    print " -3"
#    axScatter.set_xlim( (-lim, lim) )
#    axScatter.set_ylim( (-lim, lim) )
    axScatter.set_xlim( (xmin*.9, xmax*1.1) )
    axScatter.set_ylim( (ymin*.9, ymax*1.1) )
#    print " -4"
#    bins = np.arange(-lim, lim + binwidth, binwidth)
    binwidth = (xmax*1.1-xmin*.9) / nbBins
    xBins = np.arange(xmin*.9,xmax*1.1 + binwidth, binwidth)
    binwidth = (ymax*1.1-ymin*.9) / nbBins
    yBins = np.arange(ymin*.9,ymax*1.1 + binwidth, binwidth)
#    print " -5"
    axHistx.hist(X, bins=xBins)
#    print " -6"
    axHisty.hist(Y, bins=yBins, orientation='horizontal')
    
#    print "making histograms"
    axHistx.set_xlim( axScatter.get_xlim() )
    axHisty.set_ylim( axScatter.get_ylim() )
        
    print "# save plot"
    plt.savefig(plotFilePath)
    plt.clf()

def compute_current_energy(m):
    return m.evaluate(False)


def compute_centroid(models_filePath,centroids_filePath):

    
    m = IMP.Model()
    m.set_log_level(IMP.SILENT)

    cplxInfos = build_subunits_info(m)
    HGM.helpers.mute_all_restraints(m)

    mcs     = HGM.representation.MyConfigurationSet( cplxInfos )
    mcs.read_all_configs_from_file(models_filePath)


    c   = HGM.samples.compute_centroid_for_models( mcs, update_model = True )
    # a configuration set
    mcs_centers = HGM.representation.MyConfigurationSet( mcs.get_prot_info_model() )
    mcs_centers.save_current_config()
    
    i,d = HGM.samples.compute_index_of_central_model_for_models( mcs, centroid=c )
#    print "central config is the number",i,"with a distance",d,"from centroid"
    mcs.load_configuration(i)
    mcs_centers.save_current_config()
    
#    e_centroid=compute_current_energy(m)
#    e_centroid_mean=compute_current_energy(m)

    mcs_centers.save_all_configs_to_file(centroids_filePath)
    
    return i,d



def draw_single_cluster(cluster,thres,plotFilePath):
    dots=[]
    for i in range(len(cluster.liste)):
        sample=load_sample_from_list(sample_list,cluster.liste[i])
        score=sample.get_e()
        rmsd=sample.get_rmsd()
        dots.append((score,rmsd))
    if save_all_cluster_scatter==True :
        draw_single_cluster_plot(plotFilePath, dots)
        
        
        
      
        
        

def get_sorted_cluster(cluster):
    liste_sorted=[]
    liste_sorted=sorted(cluster,key=lambda x: len(x.liste),reverse=True)
    return liste_sorted


def get_stat_from_clust(cluster,thres,html_file):
    res=[]
    res = cluster.compute_stat()  
    
    gclustDir = os.path.join(gDir,"cluster_with_threshold="+str(thres)+"-meth"+str(methode_clust)+" "+sample_tag)
    if not os.path.isdir(gclustDir):
        os.makedirs(gclustDir)
    plotFilePath  =   os.path.join(gclustDir,"rmsdVSenergy_cluster_id-:"+str(cluster.get_id())+"-:-thres-:"+str(thres)+"-"+sample_tag+".png")
    
        
    if save_all_cluster_scatter==True:
        draw_single_cluster(cluster,thres,plotFilePath) 
        
    if True==True:
        id=cluster.get_id()
        m = IMP.Model()
        m.set_log_level(IMP.SILENT)
        cplxinfos = build_subunits_info(m)
        mcs         = HGM.representation.MyConfigurationSet(cplxinfos)
        for i in range (len(cluster.liste)):
            sample=load_sample_from_list(sample_list,cluster.liste[i])
            id =  sample.id
            sample_id = id.split("::")
            
#            !!!!!!!!! modif ici si alt sample dir est used !!!!!!!!!! asDir ou sDir
            file_dir=os.path.join(asDir,sample_id[0])
            
            print file_dir+" "+sample_id[1]    
            mcs.read_configs_from_file(file_dir,[int(sample_id[1])]) 
               
        id_clust=id.split("::")
        save_dir_file=os.path.join(cDir,"cluster_samples_file-"+str(thres)+"-meth:"+str(methode_clust)+" "+sample_tag)
        save_dir_centroid_file=os.path.join(cDir,"cluster_samples_centroid_file-"+str(thres)+"-meth:"+str(methode_clust)+" "+sample_tag)
        
        if not os.path.isdir(save_dir_file):
            os.makedirs(save_dir_file)
        if not os.path.isdir(save_dir_centroid_file):
            os.makedirs(save_dir_centroid_file)
#        print save_dir_file             
        save_file_name="id_clust_"+str(cluster.get_id())+".txt"
#        print save_file_name 
        
        file_save = os.path.join(save_dir_file,save_file_name)
        centroid_file_save = os.path.join(save_dir_centroid_file,save_file_name)

        print mcs.get_number_of_configurations()
#        print file_save
        if save_models_clust==True:
            mcs.save_all_configs_to_file(file_save)
        mcs.delete_all_configs()

        id_cen,d=compute_centroid(file_save,centroid_file_save)
    
    other="central config is the number "+str(id_cen)+" with a distance "+str(d)+" from centroid"

    if print_stat==True :
        print "-----------------------------------------"
        print  " Cluster id : "+str(cluster.get_id())+"  threshold : "+str(thres)
        print  " Size       : "+str(len(cluster.liste))
        print  " Max score  : "+str(res[0])
        print  " Min score  : "+str(res[1])
        print  " Min score id : "+str(res[6])
        print  " Mean score : "+str(res[2])
        print  " Max rmsd   : "+str(res[3])
        print  " Min rmsd   : "+str(res[4])
        print  " Min rmsd id  : "+str(res[7])
        print  " Mean rmsd  : "+str(res[5])
        print  " central config is the number ",id_cen," distance ",d," from centroid"
        print "-----------------------------------------"

        
    #ajout ds le fichier html
    if len(cluster.liste)>seuil_html:
        add='<tr>\n\
            <td>'+str(cluster.get_id())+'</td>\n\
            <td>'+str(len(cluster.liste))+'</td>\n\
            <td>'+str(res[1])+'</td>\n\
            <td>'+str(res[0])+'</td>\n\
            <td>'+str(res[2])+'</td>\n\
            <td>'+str(res[6])+'</td>\n\
            <td>'+str(res[4])+'</td>\n\
            <td>'+str(res[3])+'</td>\n\
            <td>'+str(res[5])+'</td>\n\
            <td>'+str(res[7])+'</td>\n\
            <td>'+other+'</td>\n\
            </tr>\n'

        add_content_html_file(html_file,add)


def get_sorted_cluster(cluster):
    liste_sorted=[]
    liste_sorted=sorted(cluster,key=lambda x: len(x.liste),reverse=True)
    return liste_sorted


def compute_stat():
    print "  ---compute for Thres = 3 ----"
    html_file=os.path.join(htmlDir,"res : "+methode_clust+" "+sample_tag+" thres_3.html")
    print "---init html file---"
    init_html_file(html_file)
    liste_sorted_cluster_3=get_sorted_cluster(cluster_list_3)
    for i in range(len(cluster_list_3)) :
        get_stat_from_clust(liste_sorted_cluster_3[i],3,html_file) 
    close_html_file(html_file)
    print "---close html file---"
             
    print "  ---compute for Thres = 6 ----"
    html_file=os.path.join(htmlDir,"res : "+methode_clust+" "+sample_tag+" thres_6.html")
    print "---init html file---"
    init_html_file(html_file)
    liste_sorted_cluster_6=get_sorted_cluster(cluster_list_6)
    for i in range(len(cluster_list_6)) :
        get_stat_from_clust(liste_sorted_cluster_6[i],6,html_file)
    close_html_file(html_file)
    print "---close html file---"
        
    print "  ---compute for Thres = 9 ----"
    html_file=os.path.join(htmlDir,"res : "+methode_clust+" "+sample_tag+" thres_9.html")
    print "---init html file---"
    init_html_file(html_file)
    liste_sorted_cluster_9=get_sorted_cluster(cluster_list_9)
    for i in range(len(cluster_list_9)) :
        get_stat_from_clust(liste_sorted_cluster_9[i],9,html_file)
    close_html_file(html_file)
    print "---close html file---"
        
    print "  ---compute for Thres = 15 ----"
    html_file=os.path.join(htmlDir,"res : "+methode_clust+" "+sample_tag+" thres_15.html")
    print "---init html file---"
    init_html_file(html_file)
    liste_sorted_cluster_15=get_sorted_cluster(cluster_list_15)
    for i in range(len(cluster_list_15)) :
        get_stat_from_clust(liste_sorted_cluster_15[i],15,html_file)
    close_html_file(html_file)
    print "---close html file---"




def main() :
    time_start = time.time()
#    energie_file = os.path.join(rDir,"rmsdVSenergie--"+sample_tag+".txt")
    energie_file = os.path.join(rDir,"liste"+config_name_for_this_run+"-"+sample_tag+".txt")
    
#    !!!!! modif pour les 1000 meilleurs !!!!!!
#    cluster_file = os.path.join(cDir,"clusters-ids-per_thr--"+methode_clust+"--"+sample_tag+"--.txt")
    cluster_file = os.path.join(cDir,"1000_best_models_clusters-ids-per_thr--centroid--0-50-1000.txt")
    

    print "---Load energie and rmsd from file---"
    try:
        load_scoring(energie_file)
    except IOError as e:
        print "I/O error({0}): {1}".format(e.errno, e.strerror)
        print "Script will be terminated now "
        sys.exit()
    
    print "---Load cluster file from file---"
    try:
        load_cluster(cluster_file)
    except IOError as er:
        print "I/O error({0}): {1}".format(er.errno, er.strerror)
        print "Script will be terminated now "
        sys.exit()
        
    print "---Computing cluster stat---"
    compute_stat()

    print "---summary cluster stat---"
    # faire des stats sommaire
    print "--nb cluster avec thres 3 : "+str(len(cluster_list_3))
    print "--nb cluster avec thres 6 : "+str(len(cluster_list_6))
    print "--nb cluster avec thres 9 : "+str(len(cluster_list_9))
    print "--nb cluster avec thres 15 : "+str(len(cluster_list_15))

    

    
    time_stop = time.time()
    print "full stat generated in {0:d}s".format( int(time_stop - time_start) )

if __name__ == "__main__" :
    main()
    print "...Finished  \o/  "
