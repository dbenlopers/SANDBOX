'''
Created on 12 mars 2013

'''

__date__ ="$march. 11 2013$"


import sys
from optparse import OptionParser

import os

import time
import numpy as np

#import numpy as np

import HGM2.pdb.segments
import HGM2.representation.complex
import HGM2.pdb.pdb

usage       =     """\n %prog [options]
This script reads a "domain segments" file, and outputs optionnally one or two amongst :
 - a corresponding "complex representation" file
 - coordinates for the HGM

Input:
 - an XML segment description file for the complex with the subunits and subunit domains definition
 - [optionnally] a PDB (solution) file
Output:
 - an XML representation file for the complex
 - [optionnally] a coordinate file for the HGM representation of the solution

"""

def parseOptions():
    """ returns an object with command line options fields set.
    """
    parser = OptionParser(usage=usage)
    #
    parser.add_option("-i","--segments-file",              action="store",    type="string",
                      dest="segmentfile",
                      help="path to input xml segments file")
    parser.add_option("--pdb",                              action="store",    type="string",
                      dest="pdbfile",
                      help="path to input pdb file")
    parser.add_option("-o","--description-file",            action="store",    type="string",   
                      dest="descriptionfile",
                      help="""path to output xml description file""")
    parser.add_option("-c","--coordinates-file",            action="store",    type="string",   
                      dest="coordinatefile",
                      help="""path to a file where to store coordinates for the HGM representation corresponding to the pdb""")
    parser.add_option("-v","--verbose",                     action="store_true", default='False',
                      dest="verbose",                       
                      help="verbose mode")
    options,args      = parser.parse_args(sys.argv[1:])

    #    
    if options.segmentfile == None :
        sys.stderr.write( "Should provide a segments file path\n\n" )
        parser.print_usage()
        sys.exit(1)
    #
    if (options.descriptionfile == None) and (options.pdbfile == None):
        sys.stderr.write( "If you wan't me to output anything, you should provide at least a representation file path or a coordinate file path\n\n" )
        parser.print_usage()
        sys.exit(1)
    #    
    if (options.pdbfile != None) and (options.coordinatefile == None) :
        sys.stderr.write( "pdb file path provided, but no output coordinate file path provided : I'll ignore pdb\n\n" )
        options.pdbfile = None
    if (options.coordinatefile != None) and (options.pdbfile == None) :
        sys.stderr.write( "output coordinate file path provided, but no pdb file to read : I won't produce an HGM coordinates file\n\n" )
        parser.print_usage()
        sys.exit(1)
    return options


def get_test_options():
    class pipo():
        def __init__(self):
            test_dir = "/Users/schwarz/HGM-testcases/ARP/"
            self.segmentfile        = test_dir+"Setup/1TYQ-domain-mapping.xml"
            self.descriptionfile    = test_dir+"Setup/1TYQ-HGM-rep.xml"
            self.pdbfile            = test_dir+"Structs/1TYQ.pdb"
            self.coordinatefile     = test_dir+"Setup/1TYQ-HGM.txt"
            self.verbose            = True
    options=pipo()
    return options
     
     
def gather_residues_per_domain(m,ccsm):
    """ """
    def is_res_in_one_segment(res,segment_list):
        for s in segment_list:
            if s.is_in(res) :
                return True
        return False
     
    coordinates_per_domain      = {}
    discrepencies_per_domain    = []
    AA_per_domain               = {}
    
    for d in ccsm.get_domains() :
        d_chain                     = d.get_subunit_chain()
        segment_list                = d.get_segments()
        coordinates_per_domain[d]   = []
        AA_per_domain[d]            = set()
        for e in m.get_entries_from_chain( d_chain ) :
            if is_res_in_one_segment( e.get_resNum() , segment_list ):
                AA_per_domain[d].add( e.get_resNum() )
                coordinates_per_domain[d].append( e.get_coordinates() )
                
        discrepency = d.get_size()-len(AA_per_domain[d])
#        print "-->",discrepency,d.get_size(),len(coordinates_per_domain[d])
        if discrepency > 0 :
            discrepencies_per_domain.append( (d,discrepency) )
    
    # check if there are observed discrepencies between segment ranges 
    #       and number of residues in the structure
    if discrepencies_per_domain :
        print " - WARNING, discrepencies observed between sequence length and number of residue in the structure"
        for d,discrepency in discrepencies_per_domain :
            print "    domain {0:<15s} {1:>20s} lacks {2:>4d} AA ({3:>5.1f}%); expected {4:>4d} AA, got {5:>4d}".format(
                            d.get_full_name() ,
                            "["+( d.get_subunit_chain()+":"+(",".join(map(str,d.get_segments()))) )+"]" ,
                            (d.get_size() - len(AA_per_domain[d])),
                            (100*(d.get_size() - len(AA_per_domain[d])) / d.get_size() ) ,
                            d.get_size() ,
                            len(AA_per_domain[d])
                            )
            
    return coordinates_per_domain
     
     

     
def pdb2rep( segmentFilePath,descriptionFilePath,pdbFilePath,coordinateFilePath,verbose=False):
    print "\n> reading segment description file",segmentFilePath
    ccsm        = HGM2.pdb.segments.ComplexChainSegmentMapping.get_from_xml_file(segmentFilePath)
    if verbose == True : 
        print ccsm
    
    print "\n> computing complex representation"
    cplx        = HGM2.representation.complex.Complex.get_from_ComplexChainSegmentMapping(ccsm)
    if verbose == True : 
        print cplx
    
    if descriptionFilePath != None :
        print "\n> writing complex representation to file",descriptionFilePath
        header_lines =["date   : "+time.asctime(),
                       "script : "+os.path.split(__file__)[1]]
        cplx.write_to_xml_file(descriptionFilePath,header_lines)
        
    if pdbFilePath != None :
        print "\n> considering HGM solution coordinate"
        
        print " - reading pdb file", pdbFilePath
        m = HGM2.pdb.pdb.MolecInfos()
        m.read_pdb_file( pdbFilePath )
        m = m.filterAllAtom()
        
        print ' - gathering residues per domain'
        coordinates_per_domain = gather_residues_per_domain(m,ccsm)
        
        print ' - computing mass centers for domains'
        cplx_coods   = HGM2.representation.complex.CoordinatesSet(cplx)
        pdb_coods    = cplx_coods.add_configuration()
        for d,coods in coordinates_per_domain.iteritems():
            d_center = list( np.mean( coods, axis=0 ) )
            s_name = d.get_subunit().get_name()
            d_name = d.get_name()
            b = cplx.get_subunit(s_name).get_bead(d_name)
            pdb_coods.set_bead_coordinates(b,d_center)
        
        print ' - saving coordinates to',coordinateFilePath
        cplx_coods.write_configurations_to_file(coordinateFilePath)
        
     
if __name__ == "__main__":
    t_start = time.time()
    
    options = parseOptions()
#    options = get_test_options()
    
    pdb2rep(options.segmentfile, options.descriptionfile, options.pdbfile, options.coordinatefile, options.verbose)
    
    t_stop = time.time()
    print "...finished (in {0})".format( t_stop-t_start )
    
    
