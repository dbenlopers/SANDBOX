'''

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

#config_name_for_this_run    = "arp_EM_0_2aLM"
#config_name_for_this_run    = "arp_EM_0_2aL"

#config_name_for_this_run    = "arp_EM_0_2aLFc1"
#config_name_for_this_run    = "arp_EM_0_2aLFRET1"
#config_name_for_this_run    = "arp_EM_0_2aLFc4"
#config_name_for_this_run    = "arp_EM_0_2aLFc5"
##config_name_for_this_run    = "arp_EM_0_2aLFc3"
##config_name_for_this_run    = "arp_EM_0_2aLFc2"

#config_name_for_this_run    = "arp_EM_0_2Fc1"
#config_name_for_this_run    = "arp_EM_0_2Fc3"
#config_name_for_this_run    = "arp_EM_0_2Fc4"
##config_name_for_this_run    = "arp_EM_0_2F2"
##config_name_for_this_run    = "arp_EM_0_2F3"
          
#config_name_for_this_run    = "arp_EM_0_2FRET1"




solutionFilePath        = os.path.join(HGM.helpers.get_datadir(),"ARP","save-1TYQ-HGM.txt")

#    AUTO SETTINGS
#
savePrefix                  = "saves"

runDir                      = os.path.join("results",config_name_for_this_run)
#sDir                        = os.path.join(runDir,"samples")
asDir                       = os.path.join(runDir,"samples-alt")
#eDir                        = os.path.join(runDir,"energies")
rmsdDir                     = os.path.join(runDir,"rmsd")
gDir                        = os.path.join(runDir,"graphics")
#grmsdDir                    = os.path.join(gDir,"rmsd")


sampleTag                       = "100"  # qualification
nbLow                           =1000
#energiesFilePath    = os.path.join(eDir,eFileName)
#subsampleFilePath   = os.path.join(eDir,sseFileName)
lowFileName         = "low_energy_subsamples__"+sampleTag+"__"+str(nbLow)+".txt"
lowEFilePath        = os.path.join(asDir,lowFileName)
#highEFilePath       = os.path.join(asDir,highFileName)
plotFilePath        = os.path.join(gDir,
    "EnergyDecomposition--"+config_name_for_this_run+"--in-increasing-total-E--"+sampleTag+"--low-"+str(nbLow)+".png") 
plotFilePath2       = os.path.join(gDir,
    "EnergyDecomposition-and-rmsd--"+config_name_for_this_run+"--in-increasing-total-E--"+sampleTag+"--low-"+str(nbLow)+".png")

#    SCRIPT PARAMS
#

#solutionFilePath        = "../../data/ARP/save-1TYQ-HGM.txt"
#nbBins                  = 100


#sample_indices          = range(5)
#sample_tag = "1000"


#sample_indices          = HGM.helpers.read_all_sample_indices(sDir, savePrefix)
#sample_tag = config_name_for_this_run+"-"+str(len(sample_indices)*200)
#sample_tag = config_name_for_this_run+"-38001"
##sample_tag = config_name_for_this_run+"-all"

#sample_indices          = range(5)
#sample_tag = config_name_for_this_run+"-1000"

#sample_indices          = range(50)
#sample_tag = config_name_for_this_run+"-10000"

#sample_indices          = range(101)
#sample_tag = config_name_for_this_run+"-20000"

#dotFilePath             = os.path.join(rmsdDir,"rmsdVSenergies--"+sample_tag+".txt")
#
#plotFilePath            = os.path.join(gDir,"rmsdVSenergy--"+sample_tag+".png")
#plotTitle               = "rmsd to solution vs energies ("+sample_tag+" cfg)"
#
#plotFilePath_histormsd      = os.path.join(gDir,"rmsd-histo--"+sample_tag+".png")
#plotFilePath_histormsdstats = os.path.join(gDir,"rmsd-histoS--"+sample_tag+".png")
#plotTitleRmsdHisto          = "histogram of rmsd to solution ("+sample_tag+" cfg)"
#
#plotFilePath_histoE         = os.path.join(gDir,"E-histo--"+sample_tag+".png")
#plotFilePath_histoEstats    = os.path.join(gDir,"E-histoS--"+sample_tag+".png")
#plotTitleRmsdE              = "histogram of energies to solution ("+sample_tag+" cfg)"
#
##plotFilePath_scatterHist= os.path.join(gDir,"scatter-rmsdVSenergy--"+sample_tag+".png") 
#plotFilePrefix_scatterHist= "scatter-rmsdVSenergy--"+sample_tag+"--"






#    === HERE WE GO
#





for d in [rmsdDir,gDir] :
    HGM.helpers.check_or_create_dir(d)
    
subunitsRepresentationFileName = configs[config_name_for_this_run][0]
exec ( "from {0:s} import build_subunits_info".format( subunitsRepresentationFileName ) )












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

def plot_energies(filePath,energies,tags):
    energies = scipy.array( energies )
    plt.clf()
    for tag in tags :
        print "trace",tag
        tE = energies[:,getTagIndex(tag)]
#        print tE[0:4]
        c  = getTagColor(tag)
        plt.plot(tE,'-',color=c)
#        plt.plot(tE,'-',color=c,label=tag)
#    plt.legend()
    print "  > plotting",filePath
    plt.savefig(filePath)
    plt.clf()
    
def plot_energies_and_rmsd(filePath,energies,tags,rmsd):
    energies = scipy.array( energies )
#    plt.clf()
    fig = plt.figure()
    ax1=fig.add_subplot(111)
    for tag in tags :
        print "trace",tag
        tE = energies[:,getTagIndex(tag)]
#        print tE[0:4]
        c  = getTagColor(tag)
#        plt.plot(tE,'-',color=c)
        ax1.plot(tE,'-',color=c)
#        plt.plot(tE,'-',color=c,label=tag)
#    plt.legend()
#    print rmsd
    ax2=ax1.twinx()
#    plt.plot(rmsd,'--',color="black")
    ax2.plot(rmsd,'-',color="black")
    print "  > plotting",filePath
    fig.savefig(filePath)
#    plt.savefig(filePath)
#    plt.clf()
    
#    "Total"
#    "Clashes":1,
#    "Cohesion":2,
#    "Contacts":3,
#    "EM":4,
#    "Location":5,
#    "Fret":5

def main():
    m = IMP.Model()
    m.set_log_level(IMP.SILENT)
    cplxInfos = build_subunits_info(m)
    HGM.helpers.mute_all_restraints(m)
    
    xyzl = map (HGM.helpers.XYZdecorate, cplxInfos.get_particles())

    print " -- loading the solution",solutionFilePath,
    solution        = HGM.representation.MyConfigurationSet(cplxInfos)
    solution.read_all_configs_from_file(solutionFilePath)
    print ""
    solution.load_configuration(0)
    coods_solution  = HGM.helpers.gather_coordinates_for_current_config(xyzl)
    
    mcs = HGM.representation.MyConfigurationSet(cplxInfos)
    mcs.read_all_configs_from_file(lowEFilePath)
    energies=[]
    rmsds   =[]
    print " -- loading configs",
    for idx in range(mcs.get_number_of_configurations()):
        print idx,
        if idx %15 == 0 : print ""
        mcs.load_configuration(idx)
        coods_current = HGM.helpers.gather_coordinates_for_current_config(xyzl)
        rmsd    = HGM.helpers.compute_rmsd(coods_current,coods_solution)
        print rmsd,
        es       = compute_current_energies(cplxInfos)
        energies.append(es)
        rmsds.append(rmsd)
    print " -- plotting data"
    plot_energies(plotFilePath,energies,get_energy_tags(cplxInfos))
    plot_energies_and_rmsd(plotFilePath2,energies,get_energy_tags(cplxInfos),rmsds)
    
    
    

    

    

    

        
if __name__ == "__main__" :
    main()
    print " ...That's all folks !"
