'''


reads given samples, compute RMSD to solution as well as energy, and plot that graph
'''

import os
import math
import re

import IMP
import HGM
import HGM.representation, HGM.helpers, HGM.helpersPlot

from alternate_configs import configs

import matplotlib
from matplotlib import pyplot as plt, numpy as np
import scipy
from matplotlib.ticker import NullFormatter





#config_name_for_this_run    = "3NIG_EM_0_2aC"                  
#config_name_for_this_run    = "3NIG_EM_0_2aC_20"     
#config_name_for_this_run    = "3NIG_EM_0_2lmC"
#config_name_for_this_run    = "3NIG_EM_0_2lmC_20"
#config_name_for_this_run    = "3NIG_EM_0_2lC"
#config_name_for_this_run    = "3NIG_EM_0_2lC_20" 
#config_name_for_this_run    = "3NIG_EM_0_3ambiC"  
#config_name_for_this_run    = "3NIG_EM_0_3ambiC_20"
        
#config_name_for_this_run    = "3IAM_EM_0_1aC"
#config_name_for_this_run    = "3IAM_EMc_0_1aC"
#config_name_for_this_run    = "3IAM_EM_0_2aC"
#config_name_for_this_run    = "3IAM_EMc_0_2aC"

#config_name_for_this_run    = "3IAM_EM_0_3a"
#config_name_for_this_run    = "3IAM_EM_0_3lm"
config_name_for_this_run    = "3IAM_EM_0_3l"

#config_name_for_this_run    = "3IAM_EM_0_4a"
#config_name_for_this_run    = "3IAM_EM_0_4lm"
#config_name_for_this_run    = "3IAM_EM_0_4l"


#config_name_for_this_run        = "arp_EMd_0_2aLM" 
#config_name_for_this_run        = "arp_EM_0_2aLM"
#config_name_for_this_run        = "arp_EMd_0_2aLFc1"
#config_name_for_this_run        = "arp_EM_0_2aL"
#config_name_for_this_run        = "arp_EM_0_2aLMs"
#config_name_for_this_run        = "arp_EM_0_2aLA"



#    AUTO SETTINGS
#
savePrefix                  = "saves"

runDir                      = os.path.join("results",config_name_for_this_run)
sDir                        = os.path.join(runDir,"samples")
asDir                       = os.path.join(runDir,"samples-alt")
#eDir                        = os.path.join(runDir,"energies")
rmsdDir                     = os.path.join(runDir,"rmsd")
gDir                        = os.path.join(runDir,"graphics")
#grmsdDir                    = os.path.join(gDir,"rmsd")

#energiesFilePath    = os.path.join(eDir,eFileName)
#subsampleFilePath   = os.path.join(eDir,sseFileName)

#lowEFilePath        = os.path.join(asDir,lowFileName)
#highEFilePath       = os.path.join(asDir,highFileName)
 

#    SCRIPT PARAMS
#

#solutionFilePath        = "/home/arnaud/Desktop/TFIIH/data/3NIG/save-3NIG-HGM.txt"
#solutionFilePath        = "/home/arnaud/Desktop/TFIIH/data/ARP/save-1TYQ-HGM.txt"
solutionFilePath        = "/home/arnaud/Desktop/TFIIH/data/3IAM/save-3IAM-HGM.txt"
nbBins                  = 100



#sample_indices          = HGM.helpers.read_all_sample_indices(sDir, savePrefix)
#sample_tag = "38001"
##sample_tag = "all"

#sample_indices          = range(50)
#sample_tag = "10000"

sample_indices          = range(0,20)
sample_tag = "1000 best"

dotFilePath             = os.path.join(rmsdDir,"rmsdVSenergy--"+sample_tag+".txt")
plotFilePath            = os.path.join(gDir,"rmsdVSenergy--"+sample_tag+".png")
plotTitle               = "rmsd to solution vs energies ("+sample_tag+" cfg)"
plotFilePath_histormsd  = os.path.join(gDir,"rmsd-histo--"+sample_tag+".png")
plotFilePath_histormsdstats = os.path.join(gDir,"rmsd-histoS--"+sample_tag+".png")
plotTitleRmsdHisto      = "histogram of rmsd to solution ("+sample_tag+" cfg)"
plotFilePath_scatterHist= os.path.join(gDir,"scatter-rmsdVSenergy--"+sample_tag+".png") 
plotFilePath_scatterHist2= os.path.join(gDir,"density-scatter-rmsdVSenergy--"+sample_tag+".png") 

#    === HERE WE GO
#





for d in [rmsdDir,gDir] :
    HGM.helpers.check_or_create_dir(d)
    
subunitsRepresentationFileName = configs[config_name_for_this_run][0]
exec ( "from {0:s} import build_subunits_info".format( subunitsRepresentationFileName ) )













def get_samples_paths(sample_indices):
    samples_paths=[]
    for sample_index in sample_indices :
        samples_paths.append(
                os.path.join(sDir,
                             HGM.helpers.forge_sample_name(savePrefix, sample_index))
                             )
    return samples_paths
        


def gather_coordinates_for_current_config(xyzl):
    """ outputs the concatenated list of partile coordinates for a given model"""
    vect = []
    for X in xyzl :
        vect.extend([X.get_x(),X.get_y(),X.get_z()])
    return vect

def compute_current_energy(m):
    return m.evaluate(False)

def compute_rmsd(coods_current,coods_solution):
    rmsd = HGM.helpers.compute_coods_rmsd(coods_current,coods_solution)
    return rmsd

def read_dots(filePath):
    f=open(filePath)
    dots=[]
    for line in f :
        tokens = re.split("\s+",line.strip())
        dots.append(  map(float,tokens)  )
    return dots

def plot_2D(plotFilePath,dots,title):
#    matplotlib.rcParams['axes.unicode_minus'] = False
    fig = plt.figure()
    ax = fig.add_subplot(111)
#    ax.plot(dots[:][0],dots[:][1], 'o')
    X=[];Y=[]
    for x,y in dots :
        X.append(x);Y.append(y)
#    ax.plot(X,Y, 'o')
    ax.plot(X,Y, '.')
    ax.set_xlim([15000,36000])
    ax.set_ylim([0,250])
#    ax.scatter(X,Y)
#    ax.imshow(array, cmap=cm.hot, origin='lower',clip_on=True,filternorm=1)
#    plt.colorbar()

    ax.set_title(title)

    plt.savefig(plotFilePath)
    plt.clf()

#def plot_2D_color(plotFilePath,dots,title):
#    X=[];Y=[]
#    for x,y in dots :
#        X.append(x);Y.append(y)
#    X=np.array(X)
#    Y=np.array(Y)
#    # histogram the data
#    thresh = 3
#    bins=[100,100]
#    hh, locx, locy = scipy.histogram2d(X, Y, bins=bins)
#    posx = np.digitize(X, locx)
#    posy = np.digitize(Y, locy)
#    
#    #select points within the histogram
#    ind = (posx > 0) & (posx <= bins[0]) & (posy > 0) & (posy <= bins[1])
#    hhsub = hh[posx[ind] - 1, posy[ind] - 1] # values of the histogram where the points are
#    xdat1 = X[ind][hhsub < thresh] # low density points
#    ydat1 = Y[ind][hhsub < thresh]
#    hh[hh < thresh] = np.nan # fill the areas with low density by NaNs
#    
##    xyrange=[[0,40000],[0,300]]
##    plt.imshow(hh.T,cmap='jet', interpolation='none')
##    plt.imshow(hh.T,cmap='jet',extent=np.array(xyrange).flatten(), interpolation='none')
#    plt.imshow(hh.T,cmap='jet',aspect="equal",extent=None)
#    plt.colorbar()   
#    plt.plot(xdat1, ydat1, '.')
#    
#    plt.savefig(plotFilePath)
#    plt.clf()

def plot_2D_and_histos(plotFilePath,dots):
    print "# creating data from dots"
    X=[];Y=[]
    for x,y in dots :
        X.append(x);Y.append(y)

    nullfmt   = NullFormatter()         # no labels
    
    print "# definitions for the axes"
    left, width = 0.1, 0.65
    bottom, height = 0.1, 0.65
    bottom_h = left_h = left+width+0.02
    
    rect_scatter = [left, bottom, width, height]
    rect_histx = [left, bottom_h, width, 0.2]
    rect_histy = [left_h, bottom, 0.2, height]
    
    print "start with a rectangular Figure"
    plt.figure(1, figsize=(8,8))
    
    axScatter = plt.axes(rect_scatter)
    axHistx = plt.axes(rect_histx)
    axHisty = plt.axes(rect_histy)
    
    print "# no labels"
    axHistx.xaxis.set_major_formatter(nullfmt)
    axHisty.yaxis.set_major_formatter(nullfmt)
    
    print "# the scatter plot:"
#    axScatter.scatter(X, Y)
    axScatter.plot(X, Y,'.')
    
    print "# now determine nice limits by hand:"
#    binwidth = 0.25
#    nbBins = 60
    print " -1"
#    xymax = np.max( [np.max(np.fabs(X)), np.max(np.fabs(Y))] )
#    xymin = np.min( [np.min(np.fabs(X)), np.min(np.fabs(Y))] )
    xmax = np.max(X); ymax = np.max(Y)
    xmin = np.min(X); ymin = np.min(Y)
#    taille fixe sur les histo
#    xmin=0;xmax=40000
#    ymin=0;ymax=12
        
        
        
#    print xymax,xymin
    print " -2"
#    lim = ( int(xymax/binwidth) + 1) * binwidth
    print " -3"
#    axScatter.set_xlim( (-lim, lim) )
#    axScatter.set_ylim( (-lim, lim) )
    axScatter.set_xlim( (xmin*.9, xmax*1.1) )
    axScatter.set_ylim( (ymin*.9, ymax*1.1) )
    print " -4"
#    bins = np.arange(-lim, lim + binwidth, binwidth)
    binwidth = (xmax*1.1-xmin*.9) / nbBins
    xBins = np.arange(xmin*.9,xmax*1.1 + binwidth, binwidth)
    binwidth = (ymax*1.1-ymin*.9) / nbBins
    yBins = np.arange(ymin*.9,ymax*1.1 + binwidth, binwidth)
    print " -5"
    axHistx.hist(X, bins=xBins)
    print " -6"
    axHisty.hist(Y, bins=yBins, orientation='horizontal')
    
    print "making histograms"
    axHistx.set_xlim( axScatter.get_xlim() )
    axHisty.set_ylim( axScatter.get_ylim() )

    
    print "# save plot"
    plt.savefig(plotFilePath)
    plt.clf()
    

def plot_scatter_Etotal_vs_RMSD_with_densities(plotFilePath,dots,title):
#    matplotlib.rcParams['axes.unicode_minus'] = False
#    bins    =   [200,200]
#    bins    =   [100,100]
#    bins    =   [50,50]
    bins    =   [35,35]
#    bins    =   [20,20]
#    thresh  =   2
    thresh  =   5
#    thresh  =   15
#    thresh  =   40
    
    fig = plt.figure()
    ax = fig.add_subplot(111)
#    ax.plot(dots[:][0],dots[:][1], 'o')
    X=  [];Y=[]
    for d in dots :
#        x,y
        X.append(d[0]);Y.append(d[-1])
#    ax.plot(X,Y, 'o')
    mX=0.9*min(X);MX=1.1*max(X)
    mY=0.9*min(Y);MY=1.1*max(Y)
    
    X=np.array(X)
    Y=np.array(Y)
    xyrange = [[mX,MX],[mY,MY]]
    hh, locx, locy = scipy.histogram2d(X, Y, range=xyrange, bins=bins)
    posx = np.digitize(X, locx)
    posy = np.digitize(Y, locy)

    #select points within the histogram
    ind = (posx > 0) & (posx <= bins[0]) & (posy > 0) & (posy <= bins[1])
    hhsub = hh[posx[ind] - 1, posy[ind] - 1] # values of the histogram where the points are
    xdat1 = X[ind][hhsub < thresh] # low density points
    ydat1 = Y[ind][hhsub < thresh]
    hh[hh < thresh] = np.nan # fill the areas with low density by NaNs
    
#    ax.imshow(hh.T[::-1],cmap='jet',extent=np.array(xyrange).flatten(), interpolation='none',aspect='auto')
    im=ax.imshow(hh.T[::-1],cmap='jet',extent=np.array(xyrange).flatten(), interpolation='nearest',aspect='auto')
#    ax.imshow(hh.T[::-1],cmap='jet',extent=np.array(xyrange).flatten(), interpolation='gaussian',aspect='auto')
#    ax.plot(xdat1, ydat1, 'wo')
#    ax.plot(xdat1, ydat1, 'k.')
    ax.plot(xdat1, ydat1, 'b,')
    fig.colorbar(im)
#    plt.show()

#    ax.set_xlim([0,100])
#    ax.set_ylim([0,100])
#    ax.plot(X,Y, '.')
#    ax.set_xlim([mX,MX])
#    ax.set_ylim([mY,MY])
#    ax.scatter(X,Y)
#    ax.imshow(array, cmap=cm.hot, origin='lower',clip_on=True,filternorm=1)
#    plt.colorbar()

    ax.set_title(title)
    
    print "  > plotting",plotFilePath
#    plt.show()
    plt.savefig(plotFilePath)
    plt.clf()
 
    
    

def plot_RMSD_histo(plotFilePath,plotFilePath2,dots,plotTitle):
    rmsd = np.array(dots)[:,1]
    xlabel  = None
    ylabel  = None
    
    meanX,stdX = HGM.helpers.compute_list_statistics(rmsd)
    minX = min(rmsd)
    maxX = max(rmsd)
    title   = plotTitle+\
            "range:[{3:.2f},{4:.2f}]\n size:{0:d} E{1:.2f}: s{2:.2f}:".format(len(rmsd),meanX,stdX,minX,maxX)
    HGM.helpersPlot.plot_histogram_with_margins(
                plotFilePath2,
                rmsd, nbBins, xlabel, ylabel, title)
    HGM.helpersPlot.plot_histogram(
                plotFilePath,
                rmsd, nbBins, xlabel, ylabel, title)

def main():


    fp=open(rmsdDir+"/liste"+config_name_for_this_run+"-"+sample_tag+".txt","w")
    
    
    dots=[] # this is where we'll store points (energy,rmsd to solution)
    
    try : # try to load information from file 
        raise Error
        dots = read_dots(dotFilePath)
        print "found existing dotfile (",dotFilePath,") with",len(dots),"dots"
    except : # calculate info and dump it to file
        print "can't find dotfile, revert to computation prior to plot"
        print " -- creating universe"
        m = IMP.Model()
        m.set_log_level(IMP.SILENT)
        print " -- crowding universe"
        subunitsInfos = build_subunits_info(m)
        HGM.helpers.mute_all_restraints(m)
        xyzl = map (HGM.helpers.XYZdecorate, subunitsInfos.get_particles())
    
        print " -- loading the solution",solutionFilePath,
        solution        = HGM.representation.MyConfigurationSet(subunitsInfos)
        solution.read_all_configs_from_file(solutionFilePath)
        print ""
        solution.load_configuration(0)
        coods_solution  = gather_coordinates_for_current_config(xyzl)
        
    
    #    print sample_indices
        print " -- loading sample names...",
        
#        !!!!!!!!!!!! modif pr les 1000 meilleurs
#        sampleFiles=get_samples_paths(sample_indices)
        sampleFiles=[os.path.join(asDir,"low_energy_subsamples__0-50__1000.txt")]
        
        print "found",len(sampleFiles)
        
        print " -- loading samples to compute E and RMSD"
        mcs = HGM.representation.MyConfigurationSet(subunitsInfos)
        loop_index=0
        for samplePath in sampleFiles :
            loop_index+=1
            if loop_index % 15 == 0 : print ""
            print loop_index,"..",
            mcs.read_all_configs_from_file(samplePath)
            for i in range(mcs.get_number_of_configurations()) :
                mcs.load_configuration(i)                               
                coods_current = gather_coordinates_for_current_config(xyzl)
                
                #sauvegarde de l'indice de la config avec l'energie
                e       = compute_current_energy(m)
                rmsd    = compute_rmsd(coods_current,coods_solution)
                fp.write(samplePath+"::"+str(i)+"  "+str(rmsd)+"  "+str(e)+"\n")
                dots.append( (e,rmsd) )
            mcs.delete_all_configs()
           
        fp.close()
            
        #tri du fichier et sauvegarde  
          
        d_list=[line.strip() for line in open(rmsdDir+"/liste"+config_name_for_this_run+"-"+sample_tag+".txt")]
        d_list.sort( key=lambda line: line.split("  ")[-1],reverse=True)
        sorted=open(rmsdDir+"/liste_sorted"+config_name_for_this_run+"-"+sample_tag+".txt","w")
        for line in d_list:
            sorted.write(line+"\n")
        sorted.close()
        
        
        print " -- dumping dots to file",dotFilePath
        f=open(dotFilePath,"w")
        for e,d in dots :
            f.write("{0:.2f} {1:.2f}\n".format(e,d))
        f.close()
        
    
    print "- plotting stuff"
#    plot_2D(plotFilePath,dots,plotTitle)
#    plot_2D_color(plotColorFilePath,dots,plotTitle)
#    plot_RMSD_histo(plotFilePath_histormsd,plotFilePath_histormsdstats,dots,plotTitle)

#    plot_2D_and_histos(plotFilePath_scatterHist, dots)
#    plot_scatter_Etotal_vs_RMSD_with_densities(plotFilePath_scatterHist2, dots,plotFilePath)
    


    
    
    
if __name__ == "__main__":
    main()
    print " ... That's all folks !"
