'''

reads a dotfile, then graph the plots of percentage of good solutions depending on the score.
i.e. we assess the effect of being restrictive for selective a low score threshold on the percentage of good models generated 
'''


import os
import operator
import matplotlib.pyplot as plt


#config_name_for_this_run    = "arp_EM_0_2"
#config_name_for_this_run    = "arp_EM_0_2a"

#config_name_for_this_run    = "arp_EM_0_2aLM"
#config_name_for_this_run    = "arp_EM_0_2aL"

#config_name_for_this_run    = "3NIG_EM_0_2aC"                  
#config_name_for_this_run    = "3NIG_EM_0_2aC_20"     
#config_name_for_this_run    = "3NIG_EM_0_2lmC"
#config_name_for_this_run    = "3NIG_EM_0_2lmC_20"
#config_name_for_this_run    = "3NIG_EM_0_2lC"
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

#config_name_for_this_run    =  "3NIG_EM_0_4a_f"
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
#config_name_for_this_run    = "3NIG_EM_0_5l_f_20"

config_name_for_this_run    = "3NIG_EM_0_2lCF_1"
#config_name_for_this_run    = "3NIG_EM_0_2lCF_2"
#config_name_for_this_run    = "3NIG_EM_0_2lCF_3"
#config_name_for_this_run    = "3NIG_EM_0_2lCF_4"
#config_name_for_this_run    = "3NIG_EM_0_2lCF_5"
#config_name_for_this_run    = "3NIG_EM_0_2lCF_6"
#config_name_for_this_run    = "3NIG_EM_0_2lCF_7"
#config_name_for_this_run    = "3NIG_EM_0_2lCF_8"
#config_name_for_this_run    = "3NIG_EM_0_2lCF_9"
#config_name_for_this_run    = "3NIG_EM_0_2lCF_10"
#config_name_for_this_run    = "3NIG_EM_0_2lCF_11"
#config_name_for_this_run    = "3NIG_EM_0_2lCF_12"
#config_name_for_this_run    = "3NIG_EM_0_2lCF_13"
#config_name_for_this_run    = "3NIG_EM_0_2lCF_14"
#config_name_for_this_run    = "3NIG_EM_0_2lCF_15"
#config_name_for_this_run    = "3NIG_EM_0_2lCF_16"


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
#config_name_for_this_run    = "4FXG_EM_0_1l_20"

runDir                      = os.path.join("results",config_name_for_this_run)
sDir                        = os.path.join(runDir,"samples")
asDir                       = os.path.join(runDir,"samples-alt")
#eDir                        = os.path.join(runDir,"energies")
rmsdDir                     = os.path.join(runDir,"rmsd")
gDir                        = os.path.join(runDir,"graphics")


#    I'll plot everything in same file,
#    but shall I also save every single plot in a separate file ? 
plot_also_single_files       = True
#plot_also_single_files       = False


###    SPECIFIC LOW ENERGY SAMPLE
###
##tag,nb = ("low",2000)
#tag,nb = ("low",1000)
#sample_tag              = tag +"-"+str(nb)
#sample_tag= "1000 best"

#    ALL SAMPLES
#
#sample_tag = config_name_for_this_run+"-"+str(20000)
sample_tag = "0-50"


dotFilePath             = os.path.join(rmsdDir,"rmsdVSenergies--"+sample_tag+".txt")
#threshold_colors=['magenta']
#thresholds=[50]
threshold_colors=['yellow','blue', 'green', 'orange', 'DarkOrange', 'r']
thresholds=[40,30,20,15,12,9]
#threshold_colors=["r","DarkOrange","orange","green","blue"]
#thresholds=[6,9,12,15,30]
#thresholds=[15]
#thresholds=[6,9,15]


from script_energy_plot__E_vs_RMSDtoSolution__dump_file__foreachEtype import read_dots

def main ():
    print "- reading dotfile",dotFilePath
    try :
        tags,dots = read_dots(dotFilePath)
        print "  found existing dotfile (",dotFilePath,") with",len(dots),"dots"
    except :
        print "sorry, I need a dotfile\n you should run script_energy_plot__E_vs_RMSDtoSolution__dump_file__foreachEtype first\n I won't do anything"
        return 
    
    score_vs_rmsd=[]
    for d in dots :
        score_vs_rmsd.append( (d[0],d[-1]) )
#    score_vs_rmsd.sort(key=operator.getitem(1), reverse=False)
#    score_vs_rmsd.sort(key=lambda x :x[1])
    
    
    f1=plt.figure()
    fig1=f1.add_subplot(1,1,1)
    f2=plt.figure()
    fig2=f2.add_subplot(1,1,1)
    
    if plot_also_single_files :
        f3=plt.figure()
        fig3=f3.add_subplot(1,1,1)
    
    print "- starting plot generation"
    for i,t in enumerate(thresholds):
        print "  working with threshold",t
        score_vs_good={}
        for s,r in score_vs_rmsd :
            #    compute a map    score -> (nb models for that score; nb "good" models for that score)
            try :
                nb_tot,nb_good = score_vs_good[s]
                score_vs_good[s]= (nb_tot+1 , nb_good + (1 if (r<=t) else 0))
            except :
                score_vs_good[s]=(1,(1 if (r<=t) else 0))
        x=[];y=[];xp=[]
        # x  is the table of sorted scores (without repetition)
        # y  is the table of percentages of good models depedning on a given score (sorted on score)
        # xp is the table of percentage of models with a score bellow a threshold (sorted on that score threshold)
        nb_mdl = len(score_vs_good.keys())

        nb_tot = 0
        nb_good = 0
        for score in sorted(score_vs_good.keys()):
            x.append(score)
            nb_tot  += score_vs_good[score][0]
            nb_good += score_vs_good[score][1]
            y.append(100*nb_good/float(nb_tot))
            xp.append(100*nb_tot/float(nb_mdl))


#        if plot_all_in_same_file :

        col = threshold_colors[i]
        fig1.plot(x,y, color=col)
        fig2.plot(xp,y, color=col)

        if plot_also_single_files :
            col = threshold_colors[i]
#            col = "b"
            title       ="Percentage of models under "+str(t)+\
                  " RMSD from solution"
            xLabel      ="Score"
            yLabel      ="Percentage of good models"
#            "percentage of good models"    
            fileName    = os.path.join(gDir,"Solution-enrichment--"+sample_tag+"--t-"+str(t)+".png")
            
            fig3.set_title(title)
            fig3.set_xlabel(xLabel)
            fig3.set_ylabel(yLabel)
            fig3.set_ylim([0,100])
            fig3.plot(x,y, color=col)
            f3.savefig(fileName)
            fig3.clear()
            
            xLabel      ="Percentage of models"
            fileName    = os.path.join(gDir,"Solution-enrichment--"+sample_tag+"-p--t-"+str(t)+".png")
            fig3.set_title(title)
            fig3.set_xlabel(xLabel)
            fig3.set_ylabel("Percentage of good models")
            fig3.set_xlim([0,100])
            fig3.set_ylim([0,100])
            fig3.plot(xp,y, color=col)
            fig3.legend([str(t)])
            f3.savefig(fileName)
            fig3.clear()
            
    t_tag = ",".join(map(str,thresholds))
    title       ="Percentage of models under given RMSD to solution "
    xLabel      ="score"
    fig1.set_title(title)
    fileName    = os.path.join(gDir,"Solution-enrichment--"+sample_tag+"---"+t_tag+".png")
    fig1.set_xlabel("Score") 
    fig1.set_ylabel("Percentage of good models")
    fig1.set_ylim([0,100])
    fig1.legend(['40','30','20','15','12','9'])
    f1.savefig(fileName)
    
    title       ="Percentage of models under given RMSD to solution"
    fig2.set_title(title)   
    fileName    = os.path.join(gDir,"Solution-enrichment--"+sample_tag+"-p---"+t_tag+".png")
    fig2.set_xlabel("Percentage of models used")
    fig2.set_ylabel("Percentage of good models")
    fig2.set_xlim([0,100])
    fig2.set_ylim([0,100])
    fig2.legend(['40','30','20','15','12','9'])
    f2.savefig(fileName)
#        f2.clf()
        
        
if __name__ == "__main__" :
    main()
    print "...that's all folks"
