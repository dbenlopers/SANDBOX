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





##config_name_for_this_run    = "arp_EM_0_1"

#config_name_for_this_run    = "arp_EM_0_2"
#config_name_for_this_run    = "arp_EM_0_2a"

#config_name_for_this_run    = "arp_EM_0_2aLM"
#config_name_for_this_run    = "arp_EM_0_2aL"

#config_name_for_this_run    = "arp_EM_0_2aLA1"
#config_name_for_this_run    = "arp_EM_0_2aLA2"
#config_name_for_this_run    = "arp_EM_0_2aLA3"
#config_name_for_this_run    = "arp_EM_0_2aLA"
#config_name_for_this_run    = "arp_EM_0_2aLA5"
#config_name_for_this_run    = "arp_EM_0_2aLA6"
#config_name_for_this_run    = "arp_EM_0_2aLA7"
#config_name_for_this_run    = "arp_EM_0_2aLA8"

#config_name_for_this_run    = "arp_EM_0_2aLAI2"

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


#config_name_for_this_run    = "3NIG_EM_0_2lCF_1"
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
config_name_for_this_run    = "3NIG_EM_0_2lCF_16"


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


#config_name_for_this_run    = "4FXG_EM_0_1a_40"
#config_name_for_this_run    = "4FXG_EM_0_1lm_40"
#config_name_for_this_run    = "4FXG_EM_0_1l_40"
#config_name_for_this_run    = "4FXG_EM_0_1a_30"
#config_name_for_this_run    = "4FXG_EM_0_1lm_30"
#config_name_for_this_run    = "4FXG_EM_0_1l_30"
#config_name_for_this_run    = "4FXG_EM_0_1a_20"
#config_name_for_this_run    = "4FXG_EM_0_1lm_20"
#config_name_for_this_run    = "4FXG_EM_0_1l_20"

#config_name_for_this_run    = "4FXG_EM_0_2a_40"
#config_name_for_this_run    = "4FXG_EM_0_2lm_40"
#config_name_for_this_run    = "4FXG_EM_0_2l_40"
#config_name_for_this_run    = "4FXG_EM_0_2a_20"
#config_name_for_this_run    = "4FXG_EM_0_2lm_20"




#config_name_for_this_run    = "3IAM_EM_0_6a"
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

for d in [rmsdDir,gDir,asDir] :
    HGM.helpers.check_or_create_dir(d)

#    SCRIPT PARAMS
#
#solutionFilePath        = "/home/arnaud/Desktop/TFIIH/data/4FXG/save-4FXG-HGM.txt"
#solutionFilePath        = "/home/arnaud/Desktop/TFIIH/data/3IAM/save-3IAM-HGM.txt"
solutionFilePath        = "/home/arnaud/Desktop/TFIIH/data/3NIG/save-3NIG-HGM.txt"
#solutionFilePath        = "../../data/ARP/save-1TYQ-HGM.txt"
nbBins                  = 100





def get_samples_paths(sample_indices):
    samples_paths=[]
    for sample_index in sample_indices :
        filePath = os.path.join(sDir,
             HGM.helpers.forge_sample_name(savePrefix, sample_index))
        try:
            with open(filePath) as f: pass
            samples_paths.append( filePath )
        except IOError as e :
#            print "file path does not exist",filePath
            pass
            
    return samples_paths



# #
# #    SPECIFIC SAMPLE
# #
#tag,nb = ("low",100)
#tag,nb = ("low",500)
#tag,nb = ("low",1000)
#tag,nb = ("low",1000)
##tag,nb = ("low",5000)
#sample_tag              = tag +"-"+str(nb)
##distMatrixFileName      = "dist_matrix--"+sampleDescription+".pickle"
#sampleFiles             = [os.path.join(asDir, tag + "_energy_subsamples__0-50__"+str(nb)+".txt")]

##lowFileName         = 
##lowEFilePath        = os.path.join(asDir,lowFileName)
##highEFilePath       = os.path.join(asDir,highFileName)
##sampleFiles=[lowEFilePath]
#__DENSITY_THRESHOLD__ = max(2,nb/1300)

## #
## #    ALL
## #
##sample_indices          = range(5)
sample_tag = "0-50"
##
##sample_indices          = range(20,30)
##
##print HGM.helpers.get_sample_indices_gaps(sDir, savePrefix)
sample_indices          = HGM.helpers.read_all_sample_indices(sDir, savePrefix)
##sample_indices = sample_indices[:100]
##
##sample_tag = config_name_for_this_run+"-"+str(len(sample_indices)*200)
##sample_tag = config_name_for_this_run+"-38001"
###sample_tag = config_name_for_this_run+"-all"
##
sampleFiles=get_samples_paths(sample_indices)
__DENSITY_THRESHOLD__ = 4




dotFilePath             = os.path.join(rmsdDir,"rmsdVSenergies--"+sample_tag+".txt")


plotFilePath            = os.path.join(gDir,"rmsdVSenergy--"+sample_tag+".png")
bplotFilePath           = os.path.join(gDir,"rmsdVSenergy-b--"+sample_tag+".png")
dplotFilePath           = os.path.join(gDir,"rmsdVSenergy-d--"+sample_tag+".png")
dbplotFilePath          = os.path.join(gDir,"rmsdVSenergy-db--"+sample_tag+".png")
plotTitle               = "rmsd to solution vs energies ("+sample_tag+" cfg)"

plotFilePath_histormsd      = os.path.join(gDir,"rmsd-histo--"+sample_tag+".png")
plotFilePath_histormsdstats = os.path.join(gDir,"rmsd-histoS--"+sample_tag+".png")
plotTitleRmsdHisto          = "histogram of rmsd to solution ("+sample_tag+" cfg)"

plotFilePath_histoE         = os.path.join(gDir,"E-histo--"+sample_tag+".png")
plotFilePath_histoEstats    = os.path.join(gDir,"E-histoS--"+sample_tag+".png")
plotTitleRmsdE              = "histogram of energies to solution ("+sample_tag+" cfg)"

#plotFilePath_scatterHist= os.path.join(gDir,"scatter-rmsdVSenergy--"+sample_tag+".png") 
plotFilePrefix_scatterHist= "scatter-rmsdVSenergy--"+sample_tag+"--"
plotFilePrefix_scatterHist_vsS= "scatter-rmsdVSenergy-vT--"+sample_tag+"--"






#    === HERE WE GO
#





for d in [rmsdDir,gDir] :
    HGM.helpers.check_or_create_dir(d)
    
subunitsRepresentationFileName = configs[config_name_for_this_run][0]
exec ( "from {0:s} import build_subunits_info".format( subunitsRepresentationFileName ) )














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

def _plot_scatter_Etotal_vs_RMSD(plotFilePath,dots,title,**kwargs):
#    matplotlib.rcParams['axes.unicode_minus'] = False

    bars = []
    if kwargs.get("bars") != None :
        bars=kwargs.get("bars")
        
    bar_colors = ['r']*len(bars)
    if kwargs.get("bar_colors") != None :
        bar_colors=kwargs.get("bar_colors")

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

    s_X=sorted(X)
    v_bars=[]
    for i,bar in enumerate(bars) :
        color = bar_colors[i]
        idx   = int( (bar*len(X)) / 100.)
        val   = s_X[idx]
        v_bars.append([bar,val])
        ax.axvline(x=val, color=color)
    
    print "-- Energy threshold for vertical bars :"
    for bar,val in v_bars :
        print " {0:>05.2f}% under score {1:>10.2f}".format(bar,val)

    ax.set_title(title)
    
    print "  > plotting",plotFilePath
    plt.savefig(plotFilePath)
    plt.clf()

def plot_scatter_Etotal_vs_RMSD(plotFilePath,dots,title,**kwargs):
#    matplotlib.rcParams['axes.unicode_minus'] = False

    bars = []
    if kwargs.get("bars") != None :
        bars=kwargs.get("bars")
        
    bar_colors = ['r']*len(bars)
    if kwargs.get("bar_colors") != None :
        bar_colors=kwargs.get("bar_colors")
        
    xRange = None
    if kwargs.get("xRange") != None :
        xRange=kwargs.get("xRange")

    yRange = None
    if kwargs.get("yRange") != None :
        yRange=kwargs.get("yRange")
        
    col ='b'
    if kwargs.get("color") != None :
        col=kwargs.get("color")

    dot_type ='.'
    if kwargs.get("dot_type") != None :
        dot_type=kwargs.get("dot_type")

    fig = plt.figure()
    ax = fig.add_subplot(111)
#    ax.plot(dots[:][0],dots[:][1], 'o')
    X=[];Y=[]
    for d in dots :
#        x,y
        X.append(d[0]);Y.append(d[-1])
#    ax.plot(X,Y, 'o')
    ax.plot(X,Y, '.',color = col,marker=dot_type)
#    ax.plot(X,Y, 'o',color = col)

    if xRange == None :
        xRange = rescale_range_croped([min(X),max(X)],0.1)
    if yRange == None :
        yRange = rescale_range_croped([min(Y),max(Y)],0.1)
#    xyrange     = 

    ax.set_xlim(xRange)
    ax.set_ylim(yRange)
#    ax.scatter(X,Y)
#    ax.imshow(array, cmap=cm.hot, origin='lower',clip_on=True,filternorm=1)
#    plt.colorbar()

    s_X=sorted(X)
    v_bars=[]
    for i,bar in enumerate(bars) :
        color = bar_colors[i]
        idx   = int( (bar*len(X)) / 100.)
        val   = s_X[idx]
        v_bars.append([bar,val])
        ax.axvline(x=val, color=color)
    
    print "-- Energy threshold for vertical bars :"
    for bar,val in v_bars :
        print " {0:>05.2f}% under score {1:>10.2f}".format(bar,val)

    ax.set_title(title)
    
    print "  > plotting",plotFilePath
    plt.savefig(plotFilePath)
    plt.clf()



def plot_scatter_Etotal_vs_RMSD_with_densities(plotFilePath,dots,title,**kwargs):
    """
    
    @keyword threshold: threshold for the minimum number of dots to replace the dots by a 
            colored pixel in the density map (default to 15)
    @keyword bars: if not none, this is a list of percentage values [v1,...,vn] (between 0 and 100).
            For each such value 'vi', a vertical line will be drawn at the score level for which there is 'vi%' 
            of the dots on the left part of the plot.
    @keyword bar_colors: a list of colors to draw the various bars, should have same size as the 'bars' kwarg
    @keyword bins: number of bins to consider on eac axe of the 2D density histogram (defaults to [35,35])  
    """
#    matplotlib.rcParams['axes.unicode_minus'] = False
#    bins    =   [200,200]
#    bins    =   [100,100]
#    bins    =   [50,50]
#    bins    =   [20,20]
    bins    =   [35,35]
    if kwargs.get("bins") != None :
        bins    = kwargs.get("bins")  
    
    thresh  =   __DENSITY_THRESHOLD__
    if kwargs.get("threshold") != None :
        thresh = kwargs.get("threshold")
    
    bars = []
    if kwargs.get("bars") != None :
        bars=kwargs.get("bars")
        
    bar_colors = ['r']*len(bars)
    if kwargs.get("bar_colors") != None :
        bar_colors=kwargs.get("bar_colors")
    
    
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
    
    s_X=sorted(X)
    v_bars=[]
    for i,bar in enumerate(bars) :
        color = bar_colors[i]
        idx   = int( (bar*X.size) / 100.)
        val   = s_X[idx]
        v_bars.append([bar,val])
        ax.axvline(x=val, color=color)
    
    print "-- Energy threshold for vertical bars :"
    for bar,val in v_bars :
        print " {0:>05.2f}% under score {1:>10.2f}".format(bar,val)
    
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

def plot_2D_and_histos_EvsT(plotFilePath,dots,tag):
    idx=getTagIndex(tag)
    color=getTagColor(tag)
    print "# creating data from dots"
    X=[];Y=[]
    for d in dots :
        X.append(d[0]);Y.append(d[idx])

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

def rescale_range_croped(range,cropfactor):
    """ rescale a range of values so that it remains centered but the size is changed by removing/adding a scale factor of the range extent
    a scale factor of 0.1 will for instance add 20% of the range extent, 10% to the right, and 10% to the left"""
    a,b = range
    margin=(b-a)*cropfactor
#    print "--> rescaling",range,"to",(a-margin,b+margin),"with margin",margin
    return (a-margin,b+margin)



def main():


    dots=[] # this is where we'll store points (energy,rmsd to solution)
    
    try : # try to load information from file
#        raise ValueError()  # force regeneration of values 
        tags,dots = read_dots(dotFilePath)
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
        coods_solution  = HGM.helpers.gather_coordinates_for_current_config(xyzl)
        
    
    #    print sample_indices
        print " -- loading sample names...",
        print "I have",len(sampleFiles),"sample files to load"
        
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
    
    for tag in tags[:-1] :
        specific_plotFilePath = os.path.join(gDir,plotFilePrefix_scatterHist+tag+".png")
        plot_2D_and_histos(specific_plotFilePath, dots, tag)
#        specific_plotFilePath_vsS = os.path.join(gDir,plotFilePrefix_scatterHist_vsS+tag+".png")
#        plot_2D_and_histos_EvsT(specific_plotFilePath_vsS, dots, tag)
        
    plot_scatter_Etotal_vs_RMSD(plotFilePath,dots,plotTitle)
    plot_scatter_Etotal_vs_RMSD(bplotFilePath,dots,plotTitle,bars=[5,10,20],bar_colors=['r','orange',"g"])
    plot_scatter_Etotal_vs_RMSD_with_densities(dplotFilePath,dots,plotTitle)
    plot_scatter_Etotal_vs_RMSD_with_densities(dbplotFilePath,dots,plotTitle,bars=[5,10,20],bar_colors=['r','orange',"g"])
# #    plot_2D_color(plotColorFilePath,dots,plotTitle)

    plot_RMSD_histo(plotFilePath_histormsd,plotFilePath_histormsdstats,dots,plotTitleRmsdHisto)
    plot_E_histo(plotFilePath_histoE,plotFilePath_histoEstats,dots,plotTitleRmsdE)
    


    
    
    
if __name__ == "__main__":
    main()
    print " ... That's all folks !"
