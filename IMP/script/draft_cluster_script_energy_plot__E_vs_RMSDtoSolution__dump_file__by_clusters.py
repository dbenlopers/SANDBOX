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




config_name_for_this_run    = "3NIG_EM_0_3ambi"

##config_name_for_this_run    = "arp_EM_0_1"

#config_name_for_this_run    = "arp_EM_0_2"
#config_name_for_this_run    = "arp_EM_0_2a"

#config_name_for_this_run    = "arp_EM_0_2aLM"
#config_name_for_this_run    = "arp_EM_0_2aL"
#config_name_for_this_run    = "arp_EM_0_2aLA"

#config_name_for_this_run    = "arp_EM_0_2aLFc1"
#config_name_for_this_run    = "arp_EM_0_2aLFRET1"
#config_name_for_this_run    = "arp_EM_0_2aLFc4"
#config_name_for_this_run    = "arp_EM_0_2aLFc5"
#config_name_for_this_run    = "arp_EM_0_2aLFc3"
##config_name_for_this_run    = "arp_EM_0_2aLFc2"
#config_name_for_this_run    = "arp_EM_0_2aLFc1Fc3"

#config_name_for_this_run    = "arp_EM_0_2Fc1"
#config_name_for_this_run    = "arp_EM_0_2Fc3"
#config_name_for_this_run    = "arp_EM_0_2Fc4"
#config_name_for_this_run    = "arp_EM_0_2F2"
#config_name_for_this_run    = "arp_EM_0_2F3"
          
#config_name_for_this_run    = "arp_EM_0_2FRET1"

#config_name_for_this_run    = "arp_EMd_0_2aLM"
#config_name_for_this_run    = "arp_EMd_0_2aL"
#config_name_for_this_run    = "arp_EMd_0_2a"


#config_name_for_this_run    = "arp_EMd_0_2aLFc1Fc3"

#config_name_for_this_run    = "arp_EMd_0_2aLFc5"
#config_name_for_this_run    = "arp_EMd_0_2aLFc4"

#    AUTO SETTINGS
#
savePrefix                  = "saves"

runDir                      = os.path.join("results",config_name_for_this_run)
sDir                        = os.path.join(runDir,"samples")
#asDir                       = os.path.join(runDir,"samples-alt")
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

solutionFilePath        = "/home/arnaud/Desktop/TFIIH/data/3NIG/3NIG-cover-fst.cmm"
nbBins                  = 100


#sample_indices          = range(5)
#sample_tag = "1000"

#sample_indices          = range(50)
#sample_indices          = range(99)
sample_indices          = range(0,10)
#sample_indices          = range(150)
#sample_indices          = range(200)

#print HGM.helpers.get_sample_indices_gaps(sDir, savePrefix)
#sample_indices          = HGM.helpers.read_all_sample_indices(sDir, savePrefix)
#sample_indices = sample_indices[:100]

sample_tag = config_name_for_this_run+"-"+str(len(sample_indices)*200)
#sample_tag = config_name_for_this_run+"-38001"
##sample_tag = config_name_for_this_run+"-all"

#sample_indices          = range(5)
#sample_tag = config_name_for_this_run+"-1000"

#sample_indices          = range(50)
#sample_tag = config_name_for_this_run+"-10000"

#sample_indices          = range(101)
#sample_tag = config_name_for_this_run+"-20000"

#dotFilePath             = os.path.join(rmsdDir,"rmsdVSenergies--"+sample_tag+".txt")

plotFilePath            = os.path.join(gDir,"rmsdVSenergy--"+sample_tag+".png")
#plotTitle               = "rmsd to solution vs energies ("+sample_tag+" cfg)"

plotFilePath_histormsd      = os.path.join(gDir,"rmsd-histo--"+sample_tag+".png")
plotFilePath_histormsdstats = os.path.join(gDir,"rmsd-histoS--"+sample_tag+".png")
plotTitleRmsdHisto          = "histogram of rmsd to solution ("+sample_tag+" cfg)"

plotFilePath_histoE         = os.path.join(gDir,"E-histo--"+sample_tag+".png")
plotFilePath_histoEstats    = os.path.join(gDir,"E-histoS--"+sample_tag+".png")
plotTitleRmsdE              = "histogram of energies to solution ("+sample_tag+" cfg)"

#plotFilePath_scatterHist= os.path.join(gDir,"scatter-rmsdVSenergy--"+sample_tag+".png") 
plotFilePrefix_scatterHist= "scatter-rmsdVSenergy--"+sample_tag+"--"








sampleTag                   = 100
#nbLow                       = 2000
nbLow                       = 1000
asDir                       = os.path.join(runDir,"samples-alt")
lowFileName                 = "low_energy_subsamples__"+str(sampleTag)+"__"+str(nbLow)+".txt"
lowEFilePath                = os.path.join(asDir,lowFileName)

dotFilePath             = os.path.join(rmsdDir,"low_energy_rmsdVSenergies--"+str(sampleTag)+"__"+str(nbLow)+".txt")

cDir                        = os.path.join(runDir,"clusters")
gDir                        = os.path.join(runDir,"graphics")
gcDir                       = os.path.join(gDir,"clusters")

def get_clusterFilePath(meth):
    cfileName   = "clusters-ids--"+meth+"--"+str(sampleTag)+"__"+str(nbLow)+".txt"
    cfilePath = os.path.join(cDir,cfileName)
    return cfilePath

def get_clusterFilePath_per_threshold(meth):
    cfileName   = "clusters-ids-per_thr--"+meth+"--"+str(sampleTag)+"__"+str(nbLow)+".txt"
    cfilePath = os.path.join(cDir,cfileName)
    return cfilePath

#clust_methods=["complete"]
#clust_methods=["single"]
#clust_methods=["average"]
#clust_methods=["weighted"]
#clust_methods=["single","complete","average","weighted"]
#clust_methods=["complete","average","weighted"]
#clust_methods=["complete","weighted"]

clust_methods=["centroid","median"]

#nb_clusts                   = range(2,20)
nb_clusts                   = [15]


def get_plotFilePath_with_clusters(meth,nb_clust):
    return os.path.join(gcDir,"rmsdVSenergy--"+meth+"--"+str(sampleTag)+"__"+str(nbLow)+"--c"+str(nb_clust)+".png")

def get_plotTitle_with_clusters(meth, nb_clust):
    return "rmsd to solution vs energies, lowE, "+str(sampleTag)+"__"+str(nbLow)+"\n clustering "+meth+" nb clust:"+str(nb_clust)



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
        
def get_samples_path_lowE():
    return [lowEFilePath ]


#def gather_coordinates_for_current_config(xyzl):
#    """ outputs the concatenated list of partile coordinates for a given model"""
#    vect = []
#    for X in xyzl :
#        vect.extend([X.get_x(),X.get_y(),X.get_z()])
#    return vect

def compute_current_energy(m):
    return m.evaluate(False)

def compute_current_energies(cplxInfos):
#    m.evaluate(False)
#    cplxInfos.
#    print "[total-energy:{0:10.2f}] sub-cohes:{1:10.2f} sub-inter:{2:10.2f} excl-vol:{3:10.2f} EM:{4:10.2f}".format(
#           se , sstr, sscr, sevr, semr )
    results = []
    se   = cplxInfos.get_model().evaluate(False)
#    results.append("Total",se)
    results.append(se)
    sevr = cplxInfos.evr.evaluate(False)
#    results.append("Clashes",sevr)
    results.append(sevr)
    sstr = sum ( map( ( lambda r:r.evaluate(False)) , cplxInfos.str ) )
#    results.append("Cohesion",sstr)
    results.append(sstr)
    sscr = sum ( map( ( lambda r:r.evaluate(False)) , cplxInfos.scr ) )
#    results.append("Contacts",sscr)
    results.append(sscr)
    semr = cplxInfos.emr.evaluate(False)
#    results.append("EM",semr)
    results.append(semr)
    try :
        locr = cplxInfos.locr.evaluate(False)
#        results.append("Location",locr)
        results.append(locr)
    except :
        pass
    try :
        fdr = cplxInfos.fdr.evaluate(False)
#        results.append("Fret",fdr)
        results.append(fdr)
    except :
        pass
    return results

def get_energy_tags(cplxInfos):
    results=[]
    results.append("Total")
    results.append("Clashes")
    results.append("Cohesion")
    results.append("Contacts")
    results.append("EM")
    try :
        locr = cplxInfos.locr
        results.append("Location")
    except :
        pass
    try :
        fdr = cplxInfos.fdr
        results.append("Fret")
    except : pass
    
    
    return results

def getTagIndex(tag):
    tagIdxs={
    "Total":0,
    "Clashes":1,
    "Cohesion":2,
    "Contacts":3,
    "EM":4,
    "Location":5,
    "Fret":5}
    return tagIdxs[tag]
def getTagColor(tag):
    tagColors={
    "Total":"blue",
    "Clashes":"red",
    "Cohesion":"cyan",
    "Contacts":"orange",
    "EM":"magenta",
    "Location":"green",
    "Fret":"chartreuse"}
    return tagColors[tag]

#def compute_rmsd(coods_current,coods_solution,length=None):
#    rmsd2 = 0
#    for i in range(len(coods_current)) :
#        c=coods_current[i]-coods_solution[i]
#        rmsd2 += c*c
#    if length == None :
#        length = len(coods_solution)    
#    return ( math.sqrt(rmsd2) / length )

def savedots(dots,dotFilePath,tags):
    f=open(dotFilePath,"w")
    f.write( " ".join(tags)+"\n" )
    for d in dots :
#        print dots
        for c in d :
            f.write("{0:.2f} ".format(c))
        f.write("\n")
    f.close()

def read_dots(filePath):
    f=open(filePath)
    dots=[]
    line = f.readline().strip()
    tags = line.split(" ")
    for line in f :
        dots.append( map(float,re.split("\s+",line.strip()) ) )
    return tags,dots

def plot_scatter_Etotal_vs_RMSD(plotFilePath,dots,title):
#    matplotlib.rcParams['axes.unicode_minus'] = False
    fig = plt.figure()
    ax = fig.add_subplot(111)
#    ax.plot(dots[:][0],dots[:][1], 'o')
    X=[];Y=[]
    for d in dots :
#        x,y
        X.append(d[0]);Y.append(d[-1])
#    ax.plot(X,Y, 'o')
    ax.plot(X,Y, '.')
    mY=0.9*min(Y);MY=1.1*max(Y)
    mY=0.9*min(Y);MY=1.1*max(Y)
    ax.set_xlim()
    ax.set_ylim()
#    ax.scatter(X,Y)
#    ax.imshow(array, cmap=cm.hot, origin='lower',clip_on=True,filternorm=1)
#    plt.colorbar()

    ax.set_title(title)
    
    print "  > plotting",plotFilePath
    plt.savefig(plotFilePath)
    plt.clf()



def get_dot_style(c):
    styles = [('blue','o'),
              ('green','o'),
              ('red','o'),
              ('#FFFF00','o'),
              ('#FF9999','o'),
              ('#6666FF','o'),
              ('#CCCC99','o'),
              ('#33FFFF','o'),
              ('#336633','o'),
              ('#336633','o'),
              ('#FF9900','o'),
              ('blue','s'),
              ('green','s'),
              ('red','s'),
              ('#FFFF00','s'),
              ('#FF9999','s'),
              ('#6666FF','s'),
              ('#CCCC99','s'),
              ('#33FFFF','s'),
              ('#336633','s'),
              ('#336633','s'),
              ('#FF9900','s'),
     ]
    return styles[c%len(styles)]



def plot_scatter_Etotal_vs_RMSD_with_clusters(plotFilePath,cdots,plotTitle):
#    matplotlib.rcParams['axes.unicode_minus'] = False
    fig = plt.figure()
    ax = fig.add_subplot(111)
#    ax.plot(dots[:][0],dots[:][1], 'o')
    X={};Y={}
    for d in cdots :
        x=d[0];y=d[1];c=d[2]
        try :
            X[c].append(x);Y[c].append(y)
        except :
            X[c]=[x];Y[c]=[y]
#    ax.plot(X,Y, 'o')
#    ax.plot(X,Y, '.')
    mX=X[X.keys()[0]][0];MX=mX
    mY=Y[Y.keys()[0]][0];MY=mY
    for c in X.keys():
        col,sty = get_dot_style(c)
        print len(X[c]),"...",
        ax.plot(X[c],Y[c], linestyle='None',marker=sty,color=col)
        mX=min( mX, min(X[c]));MX=max( MX, max(X[c]))
        mY=min( mY, min(Y[c]));MY=max( MY, max(Y[c]))
    print ""
    mY=0.9*min(Y);MY=1.1*max(Y)
    mY=0.9*min(Y);MY=1.1*max(Y)
    ax.set_xlim()
    ax.set_ylim()
#    ax.scatter(X,Y)
#    ax.imshow(array, cmap=cm.hot, origin='lower',clip_on=True,filternorm=1)
#    plt.colorbar()

    ax.set_title(plotTitle)
    
    print "  > plotting",plotFilePath
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

def plot_2D_and_histos(plotFilePath,dots,tag):
    idx=getTagIndex(tag)
    color=getTagColor(tag)
    print "# creating data from dots"
    X=[];Y=[]
    for d in dots :
        X.append(d[idx]);Y.append(d[-1])

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
    axScatter.plot(X, Y,'.',color=color)
    
    print "# now determine nice limits by hand:"
#    binwidth = 0.25
#    nbBins = 60
#    print " -1"
#    xymax = np.max( [np.max(np.fabs(X)), np.max(np.fabs(Y))] )
#    xymin = np.min( [np.min(np.fabs(X)), np.min(np.fabs(Y))] )
    xmax = np.max(X); ymax = np.max(Y)
    xmin = np.min(X); ymin = np.min(Y)
        
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
    axHistx.hist(X, bins=xBins, color = color)
#    print " -6"
    axHisty.hist(Y, bins=yBins, orientation='horizontal')
    
    print "making histograms"
    axHistx.set_xlim( axScatter.get_xlim() )
    axHisty.set_ylim( axScatter.get_ylim() )
    
    print "# save plot"
    plt.savefig(plotFilePath)
    plt.clf()
    
def plot_E_histo(plotFilePath,plotFilePath2,dots,plotTitle):
    rmsd = np.array(dots)[:,0]
    xlabel  = None
    ylabel  = None
    
    meanX,stdX = HGM.helpers.compute_list_statistics(rmsd)
    minX = min(rmsd)
    maxX = max(rmsd)
    title   = plotTitle+\
            "\nrange:[{3:.2f},{4:.2f}] size:{0:d} E{1:.2f}: s{2:.2f}:".format(len(rmsd),meanX,stdX,minX,maxX)
    HGM.helpersPlot.plot_histogram_with_margins(
                plotFilePath2,
                rmsd, nbBins, xlabel, ylabel, title)
    HGM.helpersPlot.plot_histogram(
                plotFilePath,
                rmsd, nbBins, xlabel, ylabel, title)

def plot_RMSD_histo(plotFilePath,plotFilePath2,dots,plotTitle):
    rmsd = np.array(dots)[:,-1]
    xlabel  = None
    ylabel  = None
    
    meanX,stdX = HGM.helpers.compute_list_statistics(rmsd)
    minX = min(rmsd)
    maxX = max(rmsd)
    title   = plotTitle+\
            "\nrange:[{3:.2f},{4:.2f}] size:{0:d} E{1:.2f}: s{2:.2f}:".format(len(rmsd),meanX,stdX,minX,maxX)
    HGM.helpersPlot.plot_histogram_with_margins(
                plotFilePath2,
                rmsd, nbBins, xlabel, ylabel, title)
    HGM.helpersPlot.plot_histogram(
                plotFilePath,
                rmsd, nbBins, xlabel, ylabel, title)


def read_cluster_idx_from_file(cFilePath):
        fp = open(cFilePath)
        line = fp.readline().strip()
#        get the number of clusters
        line = line[len("# idx_config   clust-nb :"):]
        nbClusts=map(int,line.split(" "))
        clustIdxs=[]
        for line in fp :
            clustIdxs.append( map(int,re.split("\s+",line.strip())[1:]) )
        return nbClusts,clustIdxs 

def read_cluster_idx_per_thr_from_file(cFilePath):
        fp = open(cFilePath)
        line = fp.readline().strip()
#        get the number of clusters
        line = line[len("# idx_config   thr :"):]
        nbClusts=map(int,line.split(" "))
        clustIdxs=[]
        for line in fp :
            clustIdxs.append( map(int,re.split("\s+",line.strip())[1:]) )
        return nbClusts,clustIdxs

def main():
    dots=[] # this is where we'll store points (energy,rmsd to solution)
    
    print "- getting plot info (E and RMSD) "
    try : # try to load information from file
#        raise ValueError()  # force regeneration of values 
        tags,dots = read_dots(dotFilePath)
        print " - found existing dotfile (",dotFilePath,") with",len(dots),"dots"
    except : # calculate info and dump it to file
        print " - can't find dotfile, revert to computation prior to plot"
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
        coods_solution  = HGM.helpers.gather_coordinates_for_current_config(xyzl)
        
    
    #    print sample_indices
        print " -- loading sample names...",
#        sampleFiles=get_samples_paths(sample_indices)
        sampleFiles=get_samples_path_lowE()
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
                coods_current = HGM.helpers.gather_coordinates_for_current_config(xyzl)
#                e        = compute_current_energy(m)
                es       = compute_current_energies(subunitsInfos)
#                rmsd    = HGM.helpers.compute_rmsd(coods_current,coods_solution)
                rmsd    = HGM.helpers.compute_coods_rmsd(coods_current,coods_solution)
                es.append(rmsd)
                dots.append( es )
            mcs.delete_all_configs()
        
        print " -- dumping dots to file",dotFilePath
        tags =get_energy_tags(subunitsInfos)
        tags.append("rmsds")
        savedots(dots,dotFilePath,tags)

    
    print "- plotting stuff"
#    for tag in tags[:-1] :
#        specific_plotFilePath = os.path.join(gDir,plotFilePrefix_scatterHist+tag+".png")
#        plot_2D_and_histos(specific_plotFilePath, dots, tag)
    for meth in clust_methods :
#        cFilePath=get_clusterFilePath(meth)
        cFilePath=get_clusterFilePath_per_threshold(meth)
        print " -- reading clusters from",cFilePath
#        nbClusts,clustIdxs = read_cluster_idx_from_file(cFilePath)
        nbClusts,clustIdxs = read_cluster_idx_per_thr_from_file(cFilePath)
        for i in range(len(nbClusts)) :
            nb_clust = nbClusts[i]
            cdots = [(dots[k][0],dots[k][-1],clustIdxs[k][i]) for k in range(len(dots))]
            plotFilePath            = get_plotFilePath_with_clusters(meth, nb_clust)
            plotTitle               = get_plotTitle_with_clusters(meth, nb_clust)
            print " -- plotting",plotFilePath
            plot_scatter_Etotal_vs_RMSD_with_clusters(plotFilePath,cdots,plotTitle)
#    plot_2D_color(plotColorFilePath,dots,plotTitle)
#    plot_RMSD_histo(plotFilePath_histormsd,plotFilePath_histormsdstats,dots,plotTitleRmsdHisto)
#    plot_E_histo(plotFilePath_histoE,plotFilePath_histoEstats,dots,plotTitleRmsdE)
    

#    cFilePath=get_clusterThrFilePath(meth)
#    nbClusts,clustIdxs = read_cluster_idx_per_thr_from_file(cFilePath)
    
    
if __name__ == "__main__":
    main()
    print " ... That's all folks !"
