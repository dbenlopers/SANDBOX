'''

read a cluster id file and a dot file, then plot a scatter-plot for each cluster
'''
import HGM.cluster
import HGM.helpers
import HGM.plots.dotPlot
import script_energy_plot__E_vs_RMSDtoSolution__dump_file__foreachEtype as se
import sys
import os
import itertools

#config_name_for_this_run    = "arp_EM_0_2"
#config_name_for_this_run    = "arp_EM_0_2aL"
#config_name_for_this_run    = "arp_EM_0_2aLM"
#config_name_for_this_run    = "arp_EM_0_2aLAI5"

#config_name_for_this_run    = "arp_EMd_0_2aLM"


#config_name_for_this_run    = "3NIG_EM_0_2aC"
#config_name_for_this_run    = "3NIG_EM_0_2lC"
#config_name_for_this_run    = "3NIG_EM_0_2lC_20" 
config_name_for_this_run    = "3NIG_EM_0_2lC_f"

runDir                      = os.path.join("results",config_name_for_this_run)
sDir                        = os.path.join(runDir,"samples")
asDir                       = os.path.join(runDir,"samples-alt")
cDir                        = os.path.join(runDir,"clusters")
gDir                        = os.path.join(runDir,"graphics")
gcDir                       = os.path.join(gDir,"clusters")
rmsdDir                     = os.path.join(runDir,"rmsd")




NUM_DISTINCT_COLORS = 30

#SCATTERPLOT_DOT_TYPE = "."
SCATTERPLOT_DOT_TYPE = "o"

linkage_meth    = "centroid" 
#thresholds      = [5,10,20] 
#thresholds = [15,20]
thresholds = [15]

# #
# #    SPECIFIC SAMPLE
# #
tag,nb = ("low",1000)
sample_tag          = "-".join([config_name_for_this_run,tag,str(nb)])

cfilePath                   = HGM.cluster.forge_cluster_ids_file_path(cDir,thresholds, linkage_meth, sample_tag)
dotfilePath             = os.path.join(rmsdDir,"rmsdVSenergies--"+("-".join([tag,str(nb)]))+".txt")
#rmsdVSenergies--low-2000.txt
 
#plotFileDir                 = 

## #    default : coloring with random colors
## # change number of colors with NUM_DISTINCT_COLORS defined upper in the file
#output_all_clusters = True
#cluster_colors  = True
#nb_clusters     = None
##
## #    specific run
## WARNING : in this list cluster ids start at 1 instead of 0 (damn dendogram !)
#output_all_clusters = False
output_all_clusters = False

cluster_colors  = { 
    1:"red",
    2:"green",
    3:"blue",
    4:"orange",
    5:"burlywood",
    6:"yellow",
    7:"#FF00FF",
    8:"#663300",
    9:"#99FF99",# "green"
     10:"#0fff0f",
     11:"#2fd050",
     12:"cyan"
    }
nb_clusters     = 12

def main():
    print "Reading cluster id file",cfilePath
    try :
        thresholds,fcs = HGM.cluster.read_cluster_id_from_file(cfilePath)
    except :
        print "can't read",cfilePath
        sys.exit(-1)
        
    print "Reading dot file",dotfilePath
    try:
        tags,dots = se.read_dots(dotfilePath)
    except:
        print "can't read",dotfilePath
        sys.exit(-1)
        
    dots = [ (d[0],d[-1]) for d in dots ]
    
#    clusters={}
    x_range = ( min(dots,key=lambda x:x[0])[0],max(dots,key=lambda x:x[0])[0] )
    y_range = ( min(dots,key=lambda x:x[-1])[-1],max(dots,key=lambda x:x[-1])[-1] )
    x_range = se.rescale_range_croped(x_range, .1)
    y_range = se.rescale_range_croped(y_range, .1)
    
    for i,t in enumerate(thresholds) :
#        plot_superimposed_title = "clusters scatterplot linkage "+linkage_meth+" at threshold "+str(t)
#        fig_superimposed = HGM.plots.dotPlot.DotPlot(title = plot_superimposed_title, xRange=x_range, yRange=y_range,has_hist_x=True,has_hist_y=True,xLabel="score",yLabel='rmsd to solution')
#        fig_superimposed = HGM.plots.dotPlot.DotPlot(title = plot_superimposed_title, xRange=x_range, yRange=y_range,xLabel="score",yLabel='rmsd to solution')
        fig_superimposed = HGM.plots.dotPlot.DotPlot( xRange=x_range, yRange=y_range,xLabel="score",yLabel='rmsd to solution')
        fig_superimposed.plot_dots( dots , color="blue" , histo_x=True , histo_y=True , marker="," )
#        clusters[t]=HGM.cluster.extract_clusters(fcs[i])
        clusters=HGM.cluster.extract_clusters(fcs[i]).values()
        colors=([])
        if cluster_colors == None :
            cols = HGM.helpers.get_distinct_colors(NUM_DISTINCT_COLORS)
#            cols = HGM.helpers.convert_rgba_colors_to_matplotlib_strings(colors)
            colors = itertools.cycle( cols )
        else :
            if output_all_clusters == True:
                colors = iter( HGM.cluster.make_cluster_colors_list(cluster_colors,nb_clusters) )
            else :
                colors = iter([ cluster_colors[i] for i in sorted( cluster_colors.keys())])
                
        
         
# # Beware : if you sort, you should attribute colors first ! otherwise colors won't match the ones from the dendogram        
#        clusters.sort(key=lambda x:len(x),reverse=True)
        cluster_dots=[]
        print map(len,clusters)
        
        if (output_all_clusters == True) and (cluster_colors != None) :
            cluster_ids=clusters.keys()
        else  :
            cluster_ids=sorted( map(lambda x: x-1,cluster_colors.keys()) )
            
            
#        for i,cids in enumerate(clusters):
        for i in cluster_ids:
            print " working on cluster",i
            cids = clusters[i]
            cluster_dots=[dots[j] for j in cids]
            gccDir = os.path.join(gcDir,HGM.cluster.forge_cluster_dir_name(t,linkage_meth,sample_tag))
            plotFilePath = os.path.join(gccDir,"cluster-"+str(i)+".png")
            # !!! BEWARE : scipy dendogram skip colors when dealing with singleton clusters !!!
            if len(cluster_dots) > 1 :
                cluster_color = colors.next()
            else :
                cluster_color ="black" 
            se.plot_scatter_Etotal_vs_RMSD(plotFilePath,cluster_dots,"cluster "+str(i),xRange=x_range,yRange=y_range,color=cluster_color,dot_type="o")
#            fig_superimposed.plot_dots( cluster_dots , color=cluster_color , histo_x=True , histo_y=True , marker="." )
            fig_superimposed.plot_dots( cluster_dots , color=cluster_color , histo_x=True , histo_y=True , marker="o" )
        
        fig_superimposed_filePath = os.path.join(gccDir,linkage_meth+"-t"+str(t)+"--superimposed-clusters.png")
        fig_superimposed.save_to_file(fig_superimposed_filePath)

    
if __name__ == "__main__" :
    main()
    print " ...that's all folks !"
    print " ...that's all folks !"
