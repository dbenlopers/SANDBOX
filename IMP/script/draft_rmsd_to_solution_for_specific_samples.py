'''
Created on 4 nov. 2012

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




#config_name_for_this_run        = "arp_EM_0_2" 
config_name_for_this_run        = "arp_EM_0_2aLM" 
#config_name_for_this_run        = "arp_EM_0_2aL"



#    AUTO SETTINGS
#
savePrefix                  = "saves"

runDir                      = os.path.join("results",config_name_for_this_run)
#sDir                        = os.path.join(runDir,"samples")
asDir                       = os.path.join(runDir,"samples-alt")
#eDir                        = os.path.join(runDir,"energies")
#rmsdDir                     = os.path.join(runDir,"rmsd")
#gDir                        = os.path.join(runDir,"graphics")
#grmsdDir                    = os.path.join(gDir,"rmsd")


sampleTag                       = "100"  # qualification
nbLow                           =1000

#energiesFilePath    = os.path.join(eDir,eFileName)
#subsampleFilePath   = os.path.join(eDir,sseFileName)
lowFileName         = "low_energy_subsamples__"+sampleTag+"__"+str(nbLow)+".txt"
lowEFilePath        = os.path.join(asDir,lowFileName)
#highEFilePath       = os.path.join(asDir,highFileName)
 

#    SCRIPT PARAMS
#

solutionFilePath        = "../../data/ARP/save-1TYQ-HGM.txt"
nbBins                  = 100


idx_to_compare=[431,144,244,781,37,809,718,611,407]



subunitsRepresentationFileName = configs[config_name_for_this_run][0]
exec ( "from {0:s} import build_subunits_info".format( subunitsRepresentationFileName ) )





#
#def gather_coordinates_for_current_config(xyzl):
#    """ outputs the concatenated list of partile coordinates for a given model"""
#    vect = []
#    for X in xyzl :
#        vect.extend([X.get_x(),X.get_y(),X.get_z()])
#    return vect
#
#def compute_rmsd(coods_current,coods_solution):
#    rmsd2 = 0
#    for i in range(len(coods_current)) :
#        c=coods_current[i]-coods_solution[i]
#        rmsd2 += c*c
#    return math.sqrt(rmsd2)



def main():
    m = IMP.Model()
    m.set_log_level(IMP.SILENT)
    cplxInfos = build_subunits_info(m)
    HGM.helpers.mute_all_restraints(m)
    
    xyzl = map (HGM.helpers.XYZdecorate, cplxInfos.get_particles())
    
    sol = HGM.representation.MyConfigurationSet(cplxInfos)
    sol.read_all_configs_from_file(solutionFilePath)
    sol.load_configuration(0)
    coods_sol  = HGM.helpers.gather_coordinates_for_current_config(xyzl)
    
    mcs = HGM.representation.MyConfigurationSet(cplxInfos)
    mcs.read_all_configs_from_file(lowEFilePath)
    for idx in idx_to_compare:
        mcs.load_configuration(idx)
        coods = HGM.helpers.gather_coordinates_for_current_config(xyzl)
        rmsd = HGM.helpers.compute_rmsd(coods_sol, coods)
        e   = m.evaluate(False)
#        print " idx {0:d}  rmsd {0:.2f}".format(idx,rmsd)
        print  "& {0:.2f}".format(rmsd), #"RMSDS:"+
#        print + "& {0:.2f}".format(e), #"ENERGIES"
if __name__ == "__main__" :
    main()
