#!/usr/bin/python
'''

'''


import HGM2.pdb.pdb
import HGM2.pdb.segments

import sys
import time
from optparse import OptionParser


usage       =     """\n %prog [options]
This script allows one to define new chains in a PDB file by expressing chain-segments as new chains.

Input:
 - a PDB file
 - a text file with a mapping :
     chainID:segment(in res) --> new chainId
Output:
 - a PDB file

Example :
 
pdbChainMapper.py -i 3NIG_1.pdb -o 3NIG_2.pdb -s 3NIG-chain-map.txt

segment map file format :
# example :
# remark lines start with '#' sign

# empty lines are authorized
# three ':' separated fields
# first two field identify a pdb segment, and third one map this segment to a new chain ID
C : 1-457            : C
D : 1-55,435-471     : D
D : 107-351          : 1
D : 56-106,352-434   : 2
E : 1-118            : E
E : 119-134,140-219  : 3
F : 1-107            : F
F : 108-214          : 4
"""

def parseOptions():
    """ returns an object with command line options fields set.
    """
    parser = OptionParser(usage=usage)
    #
    parser.add_option("-i","--pdb",                     action="store",    type="string",
                      dest="pdbfile",
                      help="path to input pdb file")
    parser.add_option("-o","--pdb-new",                     action="store",    type="string",   
                      dest="newpdbfile",
                      help="""path to output pdb file""")
    parser.add_option("-s","--segments",                     action="store",    type="string",   
                      dest="segmentfile",
                      help="""path to the file describing the pdb segments and the new chain ID to apply""")
    parser.add_option("-v","--verbose",                     action="store_true", default='False',
                      dest="verbose",                       
                      help="verbose mode")
    options,args      = parser.parse_args(sys.argv[1:])
    
    if options.pdbfile == None :
        sys.stderr.write( "Should provide a pdb file path\n\n" )
        parser.print_usage()
        sys.exit(1)
    if options.newpdbfile == None :
        sys.stderr.write( "Should provide an output pdb file path\n\n" )
        parser.print_usage()
        sys.exit(1)
    if options.segmentfile == None :
        sys.stderr.write( "Should provide a file segments path\n\n" )
        parser.print_usage()
        sys.exit(1)    
    return options


def get_test_options():
    class pipo():
        def __init__(self):
            test_dir = "/Users/schwarz/HGM-testcases/ARP/"
            self.pdbfile     = test_dir+"Structs/1TYQ.pdb"
            self.newpdbfile  = test_dir+"Structs/1TYQ-domains-dp.pdb"
            self.segmentfile = test_dir+"Setup/1TYQ-chain-map.txt"
            self.verbose     = True
    options=pipo()
    return options

def remap_chains(pdb_filePath,segments_map_filePath,newPdb_filePath,verbosity=False):
    
    if verbosity == True :
        print "> reading segment chain mapping file",segments_map_filePath
    sm = HGM2.pdb.segments.ChainSegmentMapping(path=segments_map_filePath)
#    sm.read_map_from_file(segments_map_filePath)
    
    if verbosity == True :
        print "> reading pdb file",pdb_filePath
    m = HGM2.pdb.pdb.MolecInfos()
    m.read_pdb_file(pdb_filePath)
    
    if verbosity == True :
        print "> chains in the Model:"
        print "  ",m.get_chainIDs()
    
    nm=HGM2.pdb.pdb.MolecInfos()
    for seg in sm.iter_segments():
        c,s,nc = seg.get_chain(),(seg.get_range()),sm.get_new_chain(seg)
#        print "> extracting segment",c,s,"and remaping to",nc
        el = m.get_entries_from_chain(c)
        for e in el :
            r= int(e["resSeq"])
            inSegment = ( (r>=s[0]) and (r<=s[1]) )
            if inSegment == True :
                e["chainID"]=nc
                nm.insert_entry(e)
    
    if verbosity == True :            
        print "> chains in the new model:"
        print "  ",nm.get_chainIDs()

        print "> saving new pdb to",newPdb_filePath
    nm.saveCoordinates(newPdb_filePath)
    

if __name__ == "__main__" :
    print "remapping segment chains"
    t_start = time.time()
    
    options = parseOptions()
#    options = get_test_options()
    
    pdb_filePath     = options.pdbfile
    new_pdb_filePath = options.newpdbfile
    map_file_path    = options.segmentfile

    remap_chains( pdb_filePath , map_file_path, new_pdb_filePath, options.verbose )

    t_stop = time.time()
    print "...finished (in {0})".format( t_stop-t_start )
    
