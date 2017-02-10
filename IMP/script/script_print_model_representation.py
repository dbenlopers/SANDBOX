'''


Outputs the model description of TFIIH (subunits, beads, mass, radii) as a latex table
'''

import os
from time import time

import IMP
import HGM
import HGM.sampling
import HGM.display
import HGM.distances


import HGM.helpers
import HGM.helpersPlot

from alternate_configs import configs
#    MY TFIIH REPRESENTATION
#config_name_for_this_run    = "fixedGeom_1"

config_name_for_this_run    = "arp_EM_0_1"


#
#    PARAMETERS
#
#
#
tfiihRepresentationFileName = configs[config_name_for_this_run][0]
runDir                      = os.path.join("results",config_name_for_this_run)
saveDirSample               = os.path.join(runDir,"samples")
savePrefix                  = "saves"



    

#    import the function responsible for modelisation of TFIIH complex
#exec ( "from {0:s} import build_TFIIH_subunits_info".format( tfiihRepresentationFileName ) )
exec ( "from {0:s} import build_ARP_subunits_info".format( tfiihRepresentationFileName ) )

def main():

    m = IMP.Model()
    m.set_log_level(IMP.SILENT)
#    tfiihInfos = HGM.representation.ModelInfo()
#    tfiihInfos = build_TFIIH_subunits_info(m)
    tfiihInfos = build_ARP_subunits_info(m)
    HGM.helpers.mute_all_restraints(m)
    
    
#    subunitInfos=HGM.representation.SubunitInfo()
#    
#    subunit_names = tfiihInfos.get_subunit_names()

#    subunit_names = [
#                     'p52',
#                     'p8', 
#                     'p44', 
#                     'p34', 
#                     'p62', 
#                     'XPB', 
#                     'XPD', 
#                     'MAT1', 
#                     'CDK7', 
#                     'CyclinH'
#                     ]
    
    subunit_names = [
                     'arp3',
                     'arp2', 
                     'arpc1', 
                     'arpc2', 
                     'arpc3', 
                     'arpc4', 
                     'arpc5'
                     ]    
    
    
    
    
#    print subunit_names
    print r"\begin{table}[htbp!]"
    print r"\begin{centering}"
    print r"\begin{tabular}{|l r|l r r r|}"
    print r"\hline"
    print r"  \multicolumn{2}{|c|}{subunit} & \multicolumn{4}{c|}{beads}\\"
    print r"  name&nb beads&name & size(nb AA) & radius(\AA) & mass(Da)\\"
    print r"\hline"
    
    
    for subunit_name in subunit_names :
        print r"\hline"
        subunitInfos = tfiihInfos.get_subunit_info(subunit_name)
        size=subunitInfos.get_number_of_beads()
        line_head = "{0}&{1}&".format(subunit_name,size)
#        print "     ","name & size(nb AA) & radius & mass \\"
        for bead_index in range(subunitInfos.get_number_of_beads()) :
            bead=subunitInfos.get_bead(bead_index)
#            bead=HGM.representation.SubunitInfo.Bead()
            print line_head,"{0} & {1:4d} & {2:3.1f} & {3:8d}\\\\".format(bead.get_name(),bead.get_size(),bead.get_radius(),bead.get_mass())
            line_head=" & & "
            
    print r"\hline"        
    print r"\end{tabular}"
    print r"\caption{",config_name_for_this_run,"}"
    print r"\label{",config_name_for_this_run,"}"
    print r"\end{centering}"
    print r"\end{table}"
    
    
if __name__ == "__main__" :
    time_start = time()
    main()
    time_stop = time()
    print "All done... (in {0:.1f}s)".format(time_stop-time_start)
    
    
