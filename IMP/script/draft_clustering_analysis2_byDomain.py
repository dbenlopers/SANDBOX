'''
@author : kopp

Script qui calcul les stats sur les cluster provenant du draft_cluster_models_by_domain.py
 et de script_energy_plot__E_vs_RSMDtoSolution__dump_file__foreachEtype.py pour les scores
 
 -print stat for all cluster
 -save all models from each cluster and save in specific  file with mcs format
 -save centroid and average models from each cluster and save in specific file
 -create html file for all cluster (or n biggest ) in one html file with all stat

   V2 of script 
'''

import IMP, IMP.algebra, IMP.core, IMP.atom
import HGM, HGM.helpers, HGM.helpersPlot, HGM.representation, HGM.samples
from alternate_configs import configs
import sys
import os
import re
import time
import HGM.times
import getpass
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
config_name_for_this_run    = "3NIG_EM_0_2lC"
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

# config_name_for_this_run    = "4FXG_EM_0_1a_40"
# config_name_for_this_run    = "4FXG_EM_0_1lm_40"
# config_name_for_this_run    = "4FXG_EM_0_1l_40"
# config_name_for_this_run    = "4FXG_EM_0_1a_30"
# config_name_for_this_run    = "4FXG_EM_0_1lm_30"
# config_name_for_this_run    = "4FXG_EM_0_1l_30"
# config_name_for_this_run    = "4FXG_EM_0_1a_20"
# config_name_for_this_run    = "4FXG_EM_0_1lm_20"
# config_name_for_this_run    = "4FXG_EM_0_1l_20"





cplxRepresentationFileName  = configs[config_name_for_this_run][0]
runDir                      = os.path.join("results",config_name_for_this_run)
sDir                        = os.path.join(runDir,"samples")
asDir                        = os.path.join(runDir,"samples-alt")
cDir                        = os.path.join(runDir,"clusters")
rDir                        = os.path.join(runDir,"rmsd")
gDir                        = os.path.join(runDir,"graphics")
htmlDir                     = os.path.join(runDir,"html_cluster")
gcDir                       = os.path.join(gDir,"clusters")
c_domDir                    = os.path.join(cDir,'by_domaine')
gc_domDir                   = os.path.join(gcDir,'by_domaine')

for d in [htmlDir,gcDir] :
    HGM.helpers.check_or_create_dir(d)


#rmsdDir                     = os.path.join(runDir,"rmsd")
#dotFilePath              = os.path.join(rmsdDir,"rmsdVSenergy--"+sample_tag+".txt")


# nbBins                  = 60

cluster_list_3=[] #stock les cluters avec thres=3
cluster_list_6=[] #stock les cluters avec thres=6
cluster_list_9=[] #stock les cluters avec thres=9
cluster_list_15=[] #stock les cluters avec thres=15
cluster_file = []
sample_list=[] #stock les samples
########################################### PARAMETERS ############################

#Sample_indexes
sample_tag                  = "low-1000" 

#Clustering method
methode_clust               = "complete"


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



plt.figure(1, figsize=(8,8))


#######################   HTML PART    ##########################################"


#create template for html file  
def create_html_stat_file(file,c1,c2,c3,c4,c5,domain):
    content='<?xml version="1.0" encoding="UTF-8" ?>\n\
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">\n\
<html xmlns="http://www.w3.org/1999/xhtml">\n\
<head>\n\
<title>Clustering Statistics Summary</title>\n\
<meta http-equiv="content-type" content="text/html; charset=utf-8"/>\n\
<link rel="stylesheet" type="text/css" href="/home/arnaud/Desktop/style.css">\n\
<script type="text/javascript" language="Javascript" \n\
src="http://www.kryogenix.org/code/browser/sorttable/sorttable.js">\n\
</script>\n\
<script type=\'text/javascript\'>\n\
function showhide(divID) {\n\
  var item = document.getElementById(divID);\n\
  if (item) {\n\
    item.className=(item.className==\'hidden\')?\'unhidden\':\'hidden\';\n\
  }\n\
}\n\
function toggle_pile_visibility(divID) {\n\
  var item = document.getElementById(divID);\n\
  if (item) {\n\
    item.className=(item.className==\'pile_unvisible\')?\'pile_visible\':\'pile_unvisible\';\n\
  }\n\
}\n\
function pile_visible(divID) {\n\
  var item = document.getElementById(divID);\n\
  if (item) {\n\
    item.className=\'pile_visible\';\n\
  }\n\
}\n\
function pile_unvisible(divID) {\n\
  var item = document.getElementById(divID);\n\
  if (item) {\n\
    item.className=\'pile_unvisible\';\n\
  }\n\
}\n\
</script>\n\
</head>\n\
<body>\n\
<h1>Clustering Statistics Summary</h1>\n\
<p><i>report created by </i>'+getpass.getuser()+'<i> the </i>'+time.strftime('%d/%m/%y %H:%M:%S',time.localtime())+'\n\
</p>\n\
<pre>\n\
'+config_name_for_this_run+' for subunit '+domain+'\n\
\n\
</pre>\n\
<hr/>\n\
<h2><a href="javascript:showhide(\'thres3\');">Clusters stats thres=3</a></h2>\n\
<div id=\'thres3\' class=\'hidden\'>\n\
<table  class="\sortable\">\n\
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
            <th>Min Clashes</th>\n\
            <th>Max Clashes</th>\n\
            <th>Mean Clashes</th>\n\
            <th>Min Cohesion</th>\n\
            <th>Max Cohesion</th>\n\
            <th>Mean Cohesion</th>\n\
            <th>Min Contacts</th>\n\
            <th>Max Contacts</th>\n\
            <th>mean Contacts</th>\n\
            <th>Min EM</th>\n\
            <th>Max EM</th>\n\
            <th>Mean EM</th>\n\
        </tr>\n\
     </thead> \n\
     <tbody>\n\
'+c1+'\n\
</tbody> \n\
</table>\n\
</div>\n\
<hr/>\n\
<h2><a href="javascript:showhide(\'thres6\');">Clusters stats thres=6</a></h2>\n\
<div id=\'thres6\' class=\'hidden\'>\n\
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
            <th>Min Clashes</th>\n\
            <th>Max Clashes</th>\n\
            <th>Mean Clashes</th>\n\
            <th>Min Cohesion</th>\n\
            <th>Max Cohesion</th>\n\
            <th>Mean Cohesion</th>\n\
            <th>Min Contacts</th>\n\
            <th>Max Contacts</th>\n\
            <th>mean Contacts</th>\n\
            <th>Min EM</th>\n\
            <th>Max EM</th>\n\
            <th>Mean EM</th>\n\
        </tr>\n\
     </thead> \n\
     <tbody>\n\
'+c2+'\n\
</tbody> \n\
</table>\n\
</div>\n\
<hr/>\n\
<h2><a href="javascript:showhide(\'thres9\');">Clusters stats thres=9</a></h2>\n\
<div id=\'thres9\' class=\'hidden\'>\n\
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
            <th>Min Clashes</th>\n\
            <th>Max Clashes</th>\n\
            <th>Mean Clashes</th>\n\
            <th>Min Cohesion</th>\n\
            <th>Max Cohesion</th>\n\
            <th>Mean Cohesion</th>\n\
            <th>Min Contacts</th>\n\
            <th>Max Contacts</th>\n\
            <th>mean Contacts</th>\n\
            <th>Min EM</th>\n\
            <th>Max EM</th>\n\
            <th>Mean EM</th>\n\
        </tr> \n\
     </thead> \n\
     <tbody> \n\
'+c3+'\n\
</tbody> \n\
</table>\n\
</div>\n\
<hr/>\n\
<h2><a href="javascript:showhide(\'thres15\');">Clusters stats thres=15</a></h2>\n\
<div id=\'thres15\' class=\'hidden\'>\n\
<table  class=\"sortable\">\n\
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
            <th>Min Clashes</th>\n\
            <th>Max Clashes</th>\n\
            <th>Mean Clashes</th>\n\
            <th>Min Cohesion</th>\n\
            <th>Max Cohesion</th>\n\
            <th>Mean Cohesion</th>\n\
            <th>Min Contacts</th>\n\
            <th>Max Contacts</th>\n\
            <th>mean Contacts</th>\n\
            <th>Min EM</th>\n\
            <th>Max EM</th>\n\
            <th>Mean EM</th>\n\
        </tr>\n\
     </thead> \n\
     <tbody>\n\
'+c4+'\n\
</tbody> \n\
</table>\n\
</div>\n\
<hr/>\n\
<h2><a href="javascript:showhide(\'other\');">Other</a></h2>\n\
<div id=\'other\' class=\'hidden\'>\n\
'+c5+'\n\
\n\
</div>\n\
<hr/>\n\
</body>\n\
</html>\n'
    
    
    f=open(file,"w")
    f.write(content)
    f.close()


    
################################   CLUSTERING STAT PART   ####################################
#cluster object
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
        for i in range(len(self.liste)):
            self.liste[i].print_sample()


    def compute_stat(self):

        
        score_list={}
        rmsd_list={}
        
        liste_score=[]
        liste_rmsd=[]
        liste_clashes=[]
        liste_cohesion=[]
        liste_contacts=[]
        liste_em=[]
        

        
        for i in range(len(self.liste)):

            sample=load_sample_from_list(self.liste[i])
            
            liste_score.append(float(sample.get_e()))
            liste_rmsd.append(float(sample.get_rmsd()))
            liste_clashes.append(float(sample.get_clashes()))
            liste_cohesion.append(float(sample.get_cohesion()))
            liste_contacts.append(float(sample.get_cohesion()))
            liste_em.append(float(sample.get_em()))
            
            score_list[sample.id]=sample.get_e()
            rmsd_list[sample.id]=sample.get_rmsd()
        
        max_score="{0:.2f}".format(max(liste_score))
        min_score="{0:.2f}".format(min(liste_score))
        id_min_score=min(score_list, key=lambda x: score_list.get(x))
        mean_score="{0:.2f}".format(numpy.mean(liste_score))
        
        max_rmsd="{0:.2f}".format(max(liste_rmsd))
        min_rmsd="{0:.2f}".format(min(liste_rmsd))
        id_min_rmsd=min(rmsd_list, key=lambda x: score_list.get(x))
        mean_rmsd="{0:.2f}".format(numpy.mean(liste_rmsd))
        
        min_clashes="{0:.2f}".format(min(liste_clashes))
        max_clashes="{0:.2f}".format(max(liste_clashes))
        mean_clashes="{0:.2f}".format(numpy.mean(liste_clashes))
        
        min_cohesion="{0:.2f}".format(min(liste_cohesion))
        max_cohesion="{0:.2f}".format(max(liste_cohesion))
        mean_cohesion="{0:.2f}".format(numpy.mean(liste_cohesion))
        
        min_contacts="{0:.2f}".format(min(liste_contacts))
        max_contacts="{0:.2f}".format(max(liste_contacts))
        mean_contacts="{0:.2f}".format(numpy.mean(liste_contacts))
        
        min_em="{0:.2f}".format(min(liste_em))
        max_em="{0:.2f}".format(max(liste_em))
        mean_em="{0:.2f}".format(numpy.mean(liste_em))
        
        
        
        
        liste=[]
        liste.append(max_score)
        liste.append(min_score)
        liste.append(mean_score)
        liste.append(max_rmsd)
        liste.append(min_rmsd)
        liste.append(mean_rmsd)
        liste.append(id_min_score)
        liste.append(id_min_rmsd)
        
        liste.append(min_clashes)
        liste.append(max_clashes)
        liste.append(mean_clashes)
        liste.append(min_cohesion)
        liste.append(max_cohesion)
        liste.append(mean_cohesion)
        liste.append(min_contacts)
        liste.append(max_contacts)
        liste.append(mean_contacts)
        liste.append(min_em)
        liste.append(max_em)
        liste.append(mean_em)
        
        return liste

             
                
#sample object
class sample :
      
    def __init__(self,name):
        self.id=name
        self.e=0
        self.clashes=0
        self.cohesion=0
        self.contacts=0
        self.em=0
        self.rmsd=0
        self.mcs_id=None
    
    def set_e(self,energie):
        self.e=energie
        
    def get_e(self):
        return self.e
    
    def set_clashes(self,clashes):
        self.clashes=clashes
        
    def get_clashes(self):
        return self.clashes
    
    def set_cohesion(self,cohesion):
        self.cohesion=cohesion
        
    def get_cohesion(self):
        return self.cohesion
    
    def set_contact(self,contact):
        self.contacts=contact
        
    def get_contact(self):
        return self.contacts
    
    def set_em(self,em):
        self.em=em
        
    def get_em(self):
        return self.em
        
    def set_rmsd(self,rmsd):
        self.rmsd=rmsd
        
    def get_rmsd(self):
        return self.rmsd

    def set_mcs_id(self,mcs_id):
        self.mcs_id=mcs_id
        
    def print_sample(self):
        print self.id," ",self.e," ",self.rmsd," ",self.clashes," ",self.cohesion," ",self.contacts," ",self.em
        
    def get_name(self):
        return self.id




#return true or false if cluster id is in cluster list
def find_cluster(cluster_list,indexe):
    for i in range(len(cluster_list)):
        if cluster_list[i].get_id()==indexe :
            return True
    else :
        return False

#return cluster from id given in argument
def get_cluster(cluster_list,indexe):
    for i in range(len(cluster_list)) :
        if cluster_list[i].get_id()==indexe :
            return cluster_list[i]

#load and create cluster object from cluster file
def load_cluster(file_path) :
    fp=open(file_path,"r")
    for line in fp :
        if line[0]=="#" :
            continue
        line_splited = line.split()
#        print line_splited
        
        #ajout ds thrs 3
        if find_cluster(cluster_list_3, line_splited[1])==False :
            clust=cluster(line_splited[1])
            cluster_list_3.append(clust)
            clust=get_cluster(cluster_list_3,line_splited[1])
            clust.add_sample(line_splited[0])
        else :
            clust=get_cluster(cluster_list_3,line_splited[1])
            clust.add_sample(line_splited[0])
            
        #ajout ds thrs 6
        if find_cluster(cluster_list_6, line_splited[2])==False :
            clust=cluster(line_splited[2])
            cluster_list_6.append(clust)
            clust=get_cluster(cluster_list_6,line_splited[2])
            clust.add_sample(line_splited[0])
        else :
            clust=get_cluster(cluster_list_6,line_splited[2])
            clust.add_sample(line_splited[0])
            
        #ajout ds thrs 9
        if find_cluster(cluster_list_9, line_splited[3])==False :
            clust=cluster(line_splited[3])
            cluster_list_9.append(clust)
            clust=get_cluster(cluster_list_9,line_splited[3])
            clust.add_sample(line_splited[0])
        else :
            clust=get_cluster(cluster_list_9,line_splited[3])
            clust.add_sample(line_splited[0])
            
        #ajout ds thrs 15
        if find_cluster(cluster_list_15, line_splited[4])==False :
            clust=cluster(line_splited[4])
            cluster_list_15.append(clust)
            clust=get_cluster(cluster_list_15,line_splited[4])
            clust.add_sample(line_splited[0])
        else :
            clust=get_cluster(cluster_list_15,line_splited[4])
            clust.add_sample(line_splited[0])
    
    fp.close()

#return id from sample    
def find_sample(indexe):
    for i in range(len(sample_list)) :
        if sample_list[i].id==indexe :
            return sample_list[i].id

#return sample
def load_sample_from_list(indexe):
    return sample_list[int(indexe)]

#load scoring of sample from scoring file
def load_scoring(file_path) :
    fp=open(file_path,"r")
    id_sample=0
    for line in fp :
        if line[0]=="T":
            continue
        line_splited = line.split()
                
        sample_add=sample(id_sample)
        sample_add.set_e(line_splited[0])
        sample_add.set_clashes(line_splited[1])
        sample_add.set_cohesion(line_splited[2])
        sample_add.set_contact(line_splited[3])
        sample_add.set_em(line_splited[4])
        sample_add.set_rmsd(line_splited[5])
#        sample_add.print_sample()
        sample_list.append(sample_add)
        id_sample+=1
    fp.close()





#not used but compute energy from sample
def compute_current_energy(m):
    return m.evaluate(False)

#compute centroid sample from cluster
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



        
      
#sorted cluster list
def get_sorted_cluster(cluster):
    liste_sorted=[]
    liste_sorted=sorted(cluster,key=lambda x: len(x.liste),reverse=True)
    return liste_sorted

#compute stat for one cluster
def get_stat_from_clust(cluster,thres,domaine):
    res=[]
    res = cluster.compute_stat() 
    


        
    if True==True:
        id=cluster.get_id()
        m = IMP.Model()
        m.set_log_level(IMP.SILENT)
        cplxinfos = build_subunits_info(m)
        mcs         = HGM.representation.MyConfigurationSet(cplxinfos)
        for i in range (len(cluster.liste)):
            sample=load_sample_from_list(cluster.liste[i])
            id =  sample.id

            
#            !!!!!!!!! modif ici si alt sample dir est used !!!!!!!!!! asDir ou sDir
            file_dir=os.path.join(asDir,'low_energy_subsamples__0-50__1000.txt')
            #affiche le fichier et le n de config contenue dans le cluster
#            print file_dir+" "+sample_id[1]    
            mcs.read_configs_from_file(file_dir,[int(id)]) 
               
#        id_clust=id.split("::")
        save_dir_file=os.path.join(c_domDir,domaine+"cluster_samples_file-"+str(thres)+"-meth:"+str(methode_clust)+" "+sample_tag)
        save_dir_centroid_file=os.path.join(c_domDir,domaine+"cluster_samples_centroid_file-"+str(thres)+"-meth:"+str(methode_clust)+" "+sample_tag)
        
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
    
    other="cent conf "+str(id_cen)+" dist "+str(d)+" from centroid"

    if print_stat==True :
        print "--------------------------------------------------------------------------------------------------"
        print  " Cluster id   : "+str(cluster.get_id())+"  threshold : "+str(thres)
        print  " Size         : "+str(len(cluster.liste))
        print  " Max score    : "+str(res[0])
        print  " Min score    : "+str(res[1])
        print  " Min score id : "+str(res[6])
        print  " Mean score   : "+str(res[2])
        print  " Max rmsd     : "+str(res[3])
        print  " Min rmsd     : "+str(res[4])
        print  " Min rmsd id  : "+str(res[7])
        print  " Mean rmsd    : "+str(res[5])
        print  " Min Clashes  : "+str(res[8])
        print  " Max Clashes  : "+str(res[9])
        print  " Mean Clashes : "+str(res[10])
        print  " Min Cohesion : "+str(res[11])
        print  " Max Cohesion : "+str(res[12])
        print  " Mean Cohesion: "+str(res[13])
        print  " Min Contact  : "+str(res[14])
        print  " Max Contact  : "+str(res[15])
        print  " Mean Contact : "+str(res[16])
        print  " Min EM       : "+str(res[17])
        print  " Max EM       : "+str(res[18])
        print  " Mean EM      : "+str(res[19])
        print  " central config is the number ",id_cen," distance ",d," from centroid"
        print "-------------------------------------------------------------------------------------------------"

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
            <td>'+str(res[8])+'</td>\n\
            <td>'+str(res[9])+'</td>\n\
            <td>'+str(res[10])+'</td>\n\
            <td>'+str(res[11])+'</td>\n\
            <td>'+str(res[12])+'</td>\n\
            <td>'+str(res[13])+'</td>\n\
            <td>'+str(res[14])+'</td>\n\
            <td>'+str(res[15])+'</td>\n\
            <td>'+str(res[16])+'</td>\n\
            <td>'+str(res[17])+'</td>\n\
            <td>'+str(res[18])+'</td>\n\
            <td>'+str(res[19])+'</td>\n\
            </tr>\n'
    return add

#compute stat for all cluster
def compute_stat(domaine):  
    

    print "  ---compute for Thres = 3 ----"
    liste_sorted_cluster_3=get_sorted_cluster(cluster_list_3)
    c1=''
    for i in range(len(cluster_list_3)) :
        content=''
        content=get_stat_from_clust(liste_sorted_cluster_3[i],3,domaine) 
        c1+=content


             
    print "  ---compute for Thres = 6 ----"
    liste_sorted_cluster_6=get_sorted_cluster(cluster_list_6)
    c2=''
    for i in range(len(cluster_list_6)) :
        content=''
        content=get_stat_from_clust(liste_sorted_cluster_6[i],6,domaine)
        c2+=content
      
    print "  ---compute for Thres = 9 ----"
    liste_sorted_cluster_9=get_sorted_cluster(cluster_list_9)
    c3=''
    for i in range(len(cluster_list_9)) :
        content=''
        content=get_stat_from_clust(liste_sorted_cluster_9[i],9,domaine)
        c3+=content
        
    print "  ---compute for Thres = 15 ----"
    liste_sorted_cluster_15=get_sorted_cluster(cluster_list_15)
    c4=''
    for i in range(len(cluster_list_15)) :
        content=''
        content=get_stat_from_clust(liste_sorted_cluster_15[i],15,domaine)
        c4+=content
    

    return c1,c2,c3,c4

#main function
def main() :
    
    domaines_list = ['3NIGC-0','3NIGD-0','3NIGD-1','3NIGD-2','3NIGE-0','3NIGE-1','3NIGF-0','3NIGF-1']
    #domaines_list = ['3NIGE-0']
    
    
    energie_file = os.path.join(rDir,"rmsdVSenergies--"+sample_tag+".txt")
    
    print "---Load energie and rmsd from file---"
    try:
        load_scoring(energie_file)
    except IOError as e:
        print "I/O error({0}): {1}".format(e.errno, e.strerror)
        print "No energie file"
        print "Script will be terminated now "
        sys.exit()
    
    
    time_start = time.time()
    
    for domaine in domaines_list:
        cluster_file = os.path.join(cDir,domaine+"_1000_best_models_clusters-ids-per_thr--"+methode_clust+"--0-50-1000.txt")
        #need to reset this list here
        del cluster_list_3[:] 
        del cluster_list_6[:]
        del cluster_list_9[:] 
        del cluster_list_15[:]
        
        print "---Load cluster file from file---"
        try:
            load_cluster(cluster_file)
        except IOError as er:
            print "I/O error({0}): {1}".format(er.errno, er.strerror)
            print "No cluster file"
            print "Script will be terminated now "
            sys.exit()
        
        print "---Computing cluster stat and html file---"
        #html_file=os.path.join(htmlDir,"clusters_stats : "+methode_clust+" "+sample_tag+".html")
        html_file=os.path.join(htmlDir,domaine+"_1000_clusters_stats : "+methode_clust+" "+sample_tag+".html")
        c1,c2,c3,c4=compute_stat(domaine)


        print "---summary cluster stat---"
        print "--nb cluster with thres 3 : "+str(len(cluster_list_3))
        print "--nb cluster avec thres 6 : "+str(len(cluster_list_6))
        print "--nb cluster avec thres 9 : "+str(len(cluster_list_9))
        print "--nb cluster avec thres 15 : "+str(len(cluster_list_15))
    
        c5='<p>--nb cluster with thres 3 : '+str(len(cluster_list_3))+'</p>\n\
        <p>--nb cluster with thres 6 : '+str(len(cluster_list_6))+'</p>\n\
        <p>--nb cluster with thres 9 : '+str(len(cluster_list_9))+'</p>\n\
        <p>--nb cluster with thres 15 : '+str(len(cluster_list_15))+'</p>\n'

    
        create_html_stat_file(html_file, c1, c2, c3, c4,c5,domaine)

    
    time_stop = time.time()
    print "full stat generated in {0:d}s".format( int(time_stop - time_start) )

if __name__ == "__main__" :
    main()
    print "...Finished  \o/  "