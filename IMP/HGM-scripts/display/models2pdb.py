'''
Created on march 21 2013
read coordinates and output pdb files for an HGM complex
'''


import sys
import os.path
from optparse import OptionParser

import time

#import itertools

import HGM2,HGM2.representation,HGM2.representation.complex
import HGM2.pdb,HGM2.pdb.segments
import HGM2.files.samples



usage       =     """\n %prog [options]
This script allows one to output PDB files for one or several models saved in a sample file

EXEMPLE :
 %prog -r ./Setup/1TYQ-HGM-rep.xml  -c ./Setup/1TYQ-HGM.txt  -P ./Models/ --p 1TYQ-HGM--solution\
            --chain-map-file="./Setup/1TYQ-domain-mapping.xml"\
            --chain-level="domain"
            
@todo: allow one to specify specific model indices to produce. For the moment, we output all models in the coordinate file.
"""
#pdb files do not allow to specify atom radii nor colors; hence, when opening 



def parseOptions():
    """ returns an object with command line options fields set.
    """
    parser = OptionParser(usage=usage)
    #
    
    parser.add_option("-r","--representation-file",           action="store",    type="string",
                      dest="representationFile",
                      help="representation file explaning HGM representation of the complex")
    parser.add_option("-c","--coordinates-file",              action="store",    type="string",
                      dest="coordinatesFile",
                      help="path to the file hosting model coordinates for the given representation")
    
    parser.add_option("-P","--path","--pdb-path",             action="store",    type="string",
                      dest="pdbPath",                           default=".",
                      help="path to a directory where to dump the pdb files")
    parser.add_option("-p","--prefix","--pdb-prefix",         action="store",    type="string",
                      dest="pdbPrefix",                         default="HGM-model",
                      help="filename prefix for the pdb files to output")
    
    parser.add_option("-m","--map","--chain-map-file",         action="store",    type="string",
                      dest="cplxChainMapFile",
                      help="Path to a chain map file that allows for mapping of subunits or domains to a chain ID")
#    parser.add_option("-i","--id-models",                     action="store",    type="string",
#                      dest="indices",
#                      help="[optional] specify a coma separated list of indices for specific models to output as pdb files, if not set all models will be processed")
#    parser.add_option("-d","--display-file",                  action="store",    type="string",
#                      dest="displayFile",
#                      help="[optional] an xml file controling the colors for the representation of the various beads")
#    parser.add_option("--chimera-script",                     action="store",    type="string",
#                      dest="chimera",
#                      help="[optional] contains chimera code for coloring and setting radii in chimera")
    parser.add_option("-v","--verbose",                     action="store_true", default='False',
                      dest="verbose",                       
                      help="verbose mode")
    parser.add_option("-l","--level","--chain-level",       action="store",    type="string",
                      dest="level",                         default="subunit",
                      help="control the chain 'level' in the produced pdb file (a chain per 'subunit', per 'domain', or for the whole 'complex')")
    parser.add_option("-i","--indices",                     action="store",    type="string",
                      dest="indices",
                      help="allows one to select a specific subset of indices in the coordinates file (beware, starts with index 0)")
#    parser.add_option("-n","--no-idx","--no-index",         action="store_true",
#                      dest="no_idx",                        default=False,
#                      help="when only one model is considered, this option allows one to remove mention of the index from the resulting file name")    
    options,args      = parser.parse_args(sys.argv[1:])
    #    Mandatory options
    #
    class MandatoryOptionException(Exception):
        def __init__(self,message):
            Exception.__init__(self,message)
    try :
        if options.representationFile  == None :
            errMsg = "Should provide a representation file"
            raise MandatoryOptionException(errMsg)
        if options.coordinatesFile  == None :
            errMsg = "Should provide a coordinates file"
            raise MandatoryOptionException(errMsg)
#        if options.pdbPath  == None :
#            errMsg = "Should provide a Path to a directory for the pdb files"
#            raise
        
#        if options.indices != None:
#            indices = misc.get_index_list_from_string(options.indices)
#        if options.displayFile == None and options.chimera
        
    except MandatoryOptionException as e :
        errMsg = e.message
        sys.stderr.write( errMsg + "\n\n" )
        parser.print_usage()
        sys.exit(1)
    
    # let's replace the nasty index specification string with a list of integers
    if options.indices != None :
        options.indices = HGM2.files.samples.get_indices_from_string( options.indices )

    
    return options



def get_test_options():
    class pipo():
        def __init__(self):
            
            test_dir = "/Users/schwarz/HGM-testcases/ARP/"
            
            self.representationFile     = test_dir+"Setup/1TYQ-HGM-rep.xml"
            
#            self.coordinatesFile        = test_dir+"Setup/1TYQ-HGM.txt"
#            self.pdbPath                = test_dir+"Structs/"
#            self.pdbPrefix              = "1TYQ-HGM--solution"
            #
            self.coordinatesFile         = test_dir+"Samples/ARP-EM0_2-saves--0.txt"
            self.pdbPath                = test_dir+"Structs/"
            self.pdbPrefix               = "ARP-mdl-EM0_2--0"
#            _indices                = "0"
#            _indices                = "1"
#            _indices                = "10-11,102-3"
#            self.indices=HGM2.files.samples.get_indices_from_string( _indices )
            self.indices                = None

#            self.cplxChainMapFile       = None
            self.cplxChainMapFile       = test_dir+"Setup/1TYQ-domain-mapping.xml"

            self.verbose                = True
#            self.level                  = "complex"
#            self.level                  = "subunit"
            self.level                  = "domain"


    options=pipo()
    return options



#    Just a few convenient "variables" for this script
#
__LEVEL_DOMAIN, __LEVEL_SUBUNIT, __LEVEL_COMPLEX = 0,1,2



def make_atom_pdb_line( atom_index, res_index, x, y, z, r, chainID ):
    return "ATOM  {0:>5d}  CA  ARG {6:1s}{1:>4d}    {2:>8.3f}{3:>8.3f}{4:>8.3f} 00.00 {5:>5.2f}           C  ".format(atom_index,res_index,x,y,z,r,chainID)

def make_ter_pdb_line(atom_index,res_index,chainID):
    "TER    4726      ARG B 350                                                      "
    return "TER   {0:>5d}      ARG {2:1s}{1:>4d}".format(atom_index,res_index,chainID)



def get_pdb_lines_for_complex_coordinates( cplx_coordinates, cplx_chain_mapping=None, cplx_topology=None,verbose = False, level="subunit"):
        """
        outputs a list of pdb lines for a given complex and coordinates
        @param cplx_coordinates     :   a CoordinatesSet::Coordinates object to transform in pdb
        @param cplx_chain_mapping   :   an optional mapping for the into chainIDs
        @param cplx_topology        :   topology description file for complex
        @param level                :   chain indexing level in {"domain","subunit","complex"} defaults to "subunit" 
        """
        if (level == "subunit") :
            lvl = __LEVEL_SUBUNIT
        elif (level == "domain"):
            lvl = __LEVEL_DOMAIN
        elif (level == "complex"):
            lvl = __LEVEL_COMPLEX
        else :
            raise KeyError("when set, 'level' keyword argument should be one of {'domain','complex','subunit'}")
        
        header_lines        = []
#        atom_lines          = {}
#        connect_lines       = {}    # if cplx_topology != None :
        
        
        if verbose == True : print ": init - computing pdb chainId for each bead"
        cplx = cplx_coordinates.get_complex()
#        cplx = HGM2.representation.complex.Complex()
        get_chain_ID = lambda x:"A"
        if lvl == __LEVEL_COMPLEX:
            pass
        else :
            chain_ID={}
            if cplx_chain_mapping == None :
                chainIDs = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890"
                s_idx = 0
                b_idx = 0
                for s in cplx.get_subunits():
                    for b in s.get_beads():
                        if lvl == __LEVEL_SUBUNIT :
                            chain_ID[b]=chainIDs[s_idx]
                        else :
                            chain_ID[b]=chainIDs[b_idx]
                        b_idx+=1
                    s_idx += 1
            else :
                for s in cplx.get_subunits():
                    for b in s.get_beads():
                        if lvl == __LEVEL_SUBUNIT :
                            chain_ID[b] = cplx_chain_mapping.get_subunit( b.get_subunit().get_name() ).get_chain()
                        else :
                            chain_ID[b] = cplx_chain_mapping.get_subunit( b.get_subunit().get_name() ).get_domain( b.get_name() ).get_domain_chain()
            get_chain_ID = lambda b:chain_ID[b]
        
        if verbose == True : print ": forging pdb REMARK header"
        header_lines.extend( [
            "REMARK 950 Fake PDB file",
            "REMARK 950 complex - {0:s}".format( cplx.get_name() + ( (" v"+cplx.get_version()) if cplx.has_version() else "") )
#            "REMARK 950 model   - {0:s}".format( title )
             ]
            )
        #
        #header_lines.extend( map (lambda s: "REMARK 951    "+s, str(cplx).split("\n") ) )
        #
        if lvl == __LEVEL_DOMAIN :
            header_lines.append("REMARK 952 a chain per domain")
            for b in cplx.get_beads():
                header_lines.append("REMARK 953 chain {0:s}: domain {1:s}".format( get_chain_ID(b), b.get_full_name() ))
        elif lvl == __LEVEL_SUBUNIT :
            header_lines.append("REMARK 952 a chain per subunit")
            for s in cplx.get_subunits():
                header_lines.append("REMARK 953 chain {0:s}: subunit {1:s}".format( get_chain_ID(s.get_bead(0)), s.get_name() ))
        else :
            header_lines.append("REMARK 952 a single chain for the whole complex")
            header_lines.append("REMARK 953 chain {0:s} : complex {1:s}".format( get_chain_ID(cplx.get_subunit(0).get_bead(0)),cplx.get_name()))
        
        atom_lines = []
        if verbose == True : print ": forging pdb ATOM lines"
        atom_index = 1
        res_index  = 1
        for s in cplx.get_subunits():
            for b in s.get_beads():
                x, y, z = cplx_coordinates.get_bead_coordinates(b)
                r       = b.get_radius()
                chainID = get_chain_ID(b)
                atom_lines.append( make_atom_pdb_line( atom_index, res_index, x, y, z, r, chainID ) )
                
                atom_index += 1
                res_index += 1
                if lvl == __LEVEL_DOMAIN:
                    atom_lines.append( make_ter_pdb_line( atom_index,res_index,chainID ) )
                    atom_index += 1
                    res_index += 1
                
            if lvl == __LEVEL_SUBUNIT:
                atom_lines.append( make_ter_pdb_line( atom_index,res_index,chainID ) )
                atom_index += 1
                res_index = 1
                
        if lvl == __LEVEL_COMPLEX:
            atom_lines.append( make_ter_pdb_line( atom_index,res_index,chainID ) )
            
        if verbose == True : print ": END"
        
        return_lines=[]
        return_lines.extend(header_lines)
        return_lines.extend(atom_lines)
        return_lines.append("END                                                                             ")
        return return_lines
        


def models2pdb( cplx, coodsSet, pdbPath, pdbPrefix, 
                cplx_chain_mapping=None, cplx_topology=None,
                indices=None, level="subunit", verbose=True ):
    """
    @param cplx:
    @param coodsSet:
    @param pdbPath:
    @param pdbPrefix:
    @param indices:
    @param level:
    @param verbose:
    """
    
    if verbose == True : print "> models2pdb"
    
    if indices == None :
        indices = range( coodsSet.get_number_of_configurations() )
    
    if verbose == True : print " - working on {0:d} indices".format(len(indices))
    
    for idx in indices :
        if verbose == True : print "  - working on config {0:d}".format(idx)
        cplx_coordinates    = coodsSet.get_configuration(idx)
        pdbFilePath = os.path.join( pdbPath, (pdbPrefix+"--{0:d}.pdb".format(idx)  ) )
        if verbose == True : print "  - saving coods to file",pdbFilePath
        f=open(pdbFilePath,'w')
#        print get_pdb_lines_for_complex_coordinates( cplx_coordinates, cplx_chain_mapping, cplx_topology, verbose)
        f.write("\n".join( get_pdb_lines_for_complex_coordinates( cplx_coordinates, 
                                                                  cplx_chain_mapping=cplx_chain_mapping, cplx_topology=cplx_topology,
                                                                  level=level, verbose=verbose) ) )
        f.close()
        






#
#
#                MAIN
#
#
if __name__ == "__main__":
    t_start = time.time()
    options = parseOptions()
#    options = get_test_options()
    
#    if options.verbose == True : 
    print "> reading representation file"
    cplx            = HGM2.representation.complex.Complex.get_complex_from_xml_file(options.representationFile)
    print "> reading coordinates file"
    coodsSet        = HGM2.representation.complex.CoordinatesSet(cplx)
#    coodsSet.read_all_configs_from_file(options.coordinatesFile)
    coodsSet.read_configs_from_file(options.coordinatesFile)

#    indices = None
#    indices = options.indices
#    if indices == None :
#        coodsSet.read_configs_from_file(options.coordinatesFile,indices=indices)
#    else :
#        coodsSet.read_configs_from_file(options.coordinatesFile,indices=indices)
        
    
    chain_mapping = None
    if options.cplxChainMapFile != None :
        print "> reading chain mapping file"
        chain_mapping = HGM2.pdb.segments.ComplexChainSegmentMapping.get_from_xml_file(options.cplxChainMapFile)
    
    topology       = None
    
    models2pdb( cplx, coodsSet, options.pdbPath, options.pdbPrefix,
                cplx_chain_mapping=chain_mapping, cplx_topology=topology, 
                indices=options.indices, level=options.level, verbose=options.verbose )

    t_stop = time.time()
    print "...finished (in {0})".format( t_stop-t_start )    
    
