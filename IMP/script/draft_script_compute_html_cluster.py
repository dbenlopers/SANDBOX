'''
@author : kopp

Script qui calcul les stats sur les cluster provenant du draft_cluster_models.py
 et de script_energy_plot__E_vs_RSMDtoSolution__dump_file.py
 et cherche  le scatter-plot deja calculer pour les n plus gros (ou tous) cluster pour chaque threshold dans un fichier HTML
  et affiche les stat si on veut

'''
import IMP, IMP.algebra, IMP.core, IMP.atom
import HGM, HGM.helpers, HGM.helpersPlot, HGM.representation
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
config_name_for_this_run        = "arp_EMd_0_2aLM"
cplxRepresentationFileName  = configs[config_name_for_this_run][0]
runDir                      = os.path.join("results",config_name_for_this_run)
sDir                        = os.path.join(runDir,"samples")
cDir                        = os.path.join(runDir,"clusters")
rDir                        = os.path.join(runDir,"rmsd")
gDir                        = os.path.join(runDir,"graphics")
htmlDir                     = os.path.join(runDir,"html_cluster")

for d in [htmlDir] :
    HGM.helpers.check_or_create_dir(d)

#rmsdDir                     = os.path.join(runDir,"rmsd")
#dotFilePath              = os.path.join(rmsdDir,"rmsdVSenergy--"+sample_tag+".txt")

#correspond au sample_indexes
sample_tag                  = "0-20" 
#methode de clustering 
methode_clust               = "centroid"

nbBins                  = 60


###PARAMETERS #####

#print stat
#print_stat=True
print_stat=False

#Nombre de cluster a afficher pour chaque threshold or 0 for all cluster in html file !!firefox don't love that
#nbClust = 0
nbClust = range(10)


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

        
        liste_score=[]
        liste_rmsd=[]
        
        for i in range(len(self.liste)):
            sample=find_load_sample(sample_list,self.liste[i])
            score=sample.get_e()
            rmsd=sample.get_rmsd()
            liste_score.append(float(score))
            liste_rmsd.append(float(rmsd))
        
        
        max_score=max(liste_score)
        min_score=min(liste_score)
        max_rmsd=max(liste_rmsd)
        min_rmsd=min(liste_rmsd)    
        mean_score=numpy.mean(liste_score)
        mean_rmsd=numpy.mean(liste_rmsd)
        
        list=[]
        list.append(max_score)
        list.append(min_score)
        list.append(mean_score)
        list.append(max_rmsd)
        list.append(min_rmsd)
        list.append(mean_rmsd)
        return list

             
                

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
    

def find_load_sample(sample_list,indexe):
    for i in range(len(sample_list)) :
        if sample_list[i].get_name()==indexe :
            return sample_list[i]


def load_ener_rmsd(file_path) :
    fp=open(file_path,"r")
    for line in fp :
        if line[0]=="#":
            continue
        line_splited = line.split()
        re_splited = line_splited[0].split("/samples/")
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
#    xmax = np.max(X); ymax = np.max(Y)
#    xmin = np.min(X); ymin = np.min(Y)
#    taille fixe sur les histo
    xmin=0;xmax=40000
    ymin=0;ymax=100
             
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
        
#    print "# save plot"
    plt.savefig(plotFilePath)
    plt.clf()




def draw_single_cluster(cluster,thres,plotFilePath):
    dots=[]
    for i in range(len(cluster.liste)):
        sample=find_load_sample(sample_list,cluster.liste[i])
        score=sample.get_e()
        rmsd=sample.get_rmsd()
        dots.append((score,rmsd))
    draw_single_cluster_plot(plotFilePath, dots)

def get_stat_from_clust(cluster,thres,html_file):
    res=[]
    res = cluster.compute_stat()
    if print_stat==True :
        print "-----------------------------------------"
        print  " Cluster id : "+str(cluster.get_id())+"  threshold : "+str(thres)
        print  " Size       : "+str(len(cluster.liste))
        print  " Max score  : "+str(res[0])
        print  " Min score  : "+str(res[1])
        print  " Mean score : "+str(res[2])
        print  " Max rmsd   : "+str(res[3])
        print  " Min rmsd   : "+str(res[4])
        print  " Mean rmsd  : "+str(res[5])
        print "-----------------------------------------"
    
    
    gclustDir = os.path.join(gDir,"cluster_with_threshold="+str(thres))
    if not os.path.isdir(gclustDir):
        os.makedirs(gclustDir)
    plotFilePath  =   os.path.join(gclustDir,"rmsdVSenergy_cluster_id-:"+str(cluster.get_id())+"-:-thres-:"+str(thres)+"-"+sample_tag+".png")
#    draw_single_cluster(cluster,thres,plotFilePath) 
        
    #ajout ds le fichier html 
    add='<tr>\n\
            <td>'+str(cluster.get_id())+'</td>\n\
            <td>'+str(len(cluster.liste))+'</td>\n\
            <td>'+str(res[1])+'</td>\n\
            <td>'+str(res[0])+'</td>\n\
            <td>'+str(res[2])+'</td>\n\
            <td>id config min score</td>\n\
            <td>'+str(res[4])+'</td>\n\
            <td>'+str(res[3])+'</td>\n\
            <td>'+str(res[5])+'</td>\n\
            <td>id config min rmsd</td>\n\
            <td>other</td>\n\
        </tr>\n'
    
       
    add='<section> <h2>Scatter-plot du Cluster : '+str(cluster.get_id())+"  threshold : "+str(thres)+' </h2>\n\
                 <img src="/home/arnaud/Desktop/TFIIH/src/coarse2/'+plotFilePath+'" width="400" height="350" alt="cluster scatter-plot" />\n\
                 <aside>\n\
                     <h2>Statistique du Cluster :</h2>\n\
                     <p>Size = '+str(len(cluster.liste))+'</p>\n\
                     <p>Mean score = '+str(res[2])+'</p>\n\
                     <p>Min score  = '+str(res[1])+'</p>\n\
                     <p>Max score  = '+str(res[0])+'</p>\n\
                     <p>Mean rmsd  = '+str(res[5])+' &Aring;</p>\n\
                     <p>Min rmsd   = '+str(res[4])+' &Aring;</p>\n\
                     <p>Max rmsd   = '+str(res[3])+' &Aring;</p>\n\
                 </aside>\n\
            </section>\n'
    add_content_html_file(html_file,add)


def get_sorted_cluster(cluster):
    liste_sorted=[]
    liste_sorted=sorted(cluster,key=lambda x: len(x.liste),reverse=True)
    return liste_sorted


def compute_stat():
    
    print "  ---compute for Thres = 3 ----"
    html_file=os.path.join(htmlDir,"res : "+methode_clust+" thres_3.html")
    print "---init html file---"
    init_html_file(html_file)
    liste_sorted_cluster_3=get_sorted_cluster(cluster_list_3)
    
    if nbClust==0 :
        for i in range(len(liste_sorted_cluster_3)):
            get_stat_from_clust(liste_sorted_cluster_3[i],3,html_file)
    else :
        for i in nbClust:
            get_stat_from_clust(liste_sorted_cluster_3[i],3,html_file)
             
    close_html_file(html_file)
    print "---close html file---"
              
    print "  ---compute for Thres = 6 ----"
    html_file=os.path.join(htmlDir,"res : "+methode_clust+" thres_6.html")
    print "---init html file---"
    init_html_file(html_file)
    liste_sorted_cluster_6=get_sorted_cluster(cluster_list_6)
    
    if nbClust==0 :
        for i in range(len(liste_sorted_cluster_6)):
            get_stat_from_clust(liste_sorted_cluster_6[i],6,html_file)
    else :
        for i in nbClust:
            get_stat_from_clust(liste_sorted_cluster_6[i],6,html_file)
             
    close_html_file(html_file)
    print "---close html file---"
        
    print "  ---compute for Thres = 9 ----"
    html_file=os.path.join(htmlDir,"res : "+methode_clust+" thres_9.html")
    print "---init html file---"
    init_html_file(html_file)
    liste_sorted_cluster_9=get_sorted_cluster(cluster_list_9)
    
    if nbClust==0 :
        for i in range(len(liste_sorted_cluster_9)):
            get_stat_from_clust(liste_sorted_cluster_9[i],9,html_file)
    else :
        for i in nbClust:
            get_stat_from_clust(liste_sorted_cluster_9[i],9,html_file)
             
    close_html_file(html_file)
    print "---close html file---"
        
    print "  ---compute for Thres = 15 ----"
    html_file=os.path.join(htmlDir,"res : "+methode_clust+" thres_15.html")
    print "---init html file---"
    init_html_file(html_file)
    liste_sorted_cluster_15=get_sorted_cluster(cluster_list_15)
    
    if nbClust==0 :
        for i in range(len(liste_sorted_cluster_15)):
            get_stat_from_clust(liste_sorted_cluster_15[i],15,html_file)
    else :
        for i in nbClust:
            get_stat_from_clust(liste_sorted_cluster_15[i],15,html_file)
             
    close_html_file(html_file)
    print "---close html file---"
        



def main() :
    time_start = time.time()
    energie_file = os.path.join(rDir,"liste"+config_name_for_this_run+"-"+sample_tag+".txt")
    cluster_file = os.path.join(cDir,"clusters-ids-per_thr--"+methode_clust+"--"+sample_tag+"--.txt")
    
    
    print "---Load energie and rmsd from file---"
    load_ener_rmsd(energie_file)
    
    print "---Load cluster file from file---"
    load_cluster(cluster_file)

    print "---Compute stat---"
    compute_stat()

    print "---summary cluster stat---"
    # faire des stats sommaire
    print "  ---nb cluster avec thres 3 : "+str(len(cluster_list_3))
    print "  ---nb cluster avec thres 6 : "+str(len(cluster_list_6))
    print "  ---nb cluster avec thres 9 : "+str(len(cluster_list_9))
    print "  ---nb cluster avec thres 15 : "+str(len(cluster_list_15))

    
    
    
    time_stop = time.time()
    print "full stat generated in {0:d}s".format( int(time_stop - time_start) )

if __name__ == "__main__" :
    main()
    print "...Finished  \o/  "