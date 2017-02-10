'''

'''
import IMP

import os
import sys

import time

import IMP
import HGM
import HGM.energies
import HGM.distances
#import HGM.sampling
#import HGM.display

import HGM.helpers
#import HGM.helpersPlot

from alternate_configs import configs


dataDirSample   = "../../data/ARP"
solutionFileName  = "save-1TYQ-HGM.txt"
solutionFilePath  = os.path.join(dataDirSample,solutionFileName)

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
          
config_name_for_this_run    = "arp_EM_0_2FRET1"


currentRepresentationFileName = configs[config_name_for_this_run][0]
    



#    import the function responsible for modelisation of TFIIH complex
#exec ( "from {0:s} import build_TFIIH_subunits_info".format( tfiihRepresentationFileName ) )
exec ( "from {0:s} import build_subunits_info".format( currentRepresentationFileName ) )


def main():
    m = IMP.Model()
    m.set_log_level(IMP.SILENT)
#    tfiihInfos = build_TFIIH_subunits_info(m)
    cplxInfos = build_subunits_info(m)
    HGM.helpers.mute_all_restraints(m)
    mcs         = HGM.representation.MyConfigurationSet(cplxInfos)
    mcs.read_all_configs_from_file(solutionFilePath)
    mcs.load_configuration(0)
    
    print "model energy",m.evaluate(False)
    
    particles   = mcs.get_particles()
    names       = map (lambda p:p.get_name(),particles )
    pdms = HGM.distances.ParticlesPairDistanceMatrix( map(HGM.helpers.XYZRdecorate,particles) )
    
    for i in range(1,len(particles)) :
        for j in range(i):
            print '&{0:>12s} - {1:>12s}&{2:6.2f}\\\\'.format(names[i],names[j],pdms.get_value(i,j))
    

if __name__ == "__main__" :
    main()
    print "...that's all folks !"
