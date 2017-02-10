'''
Created on 28 mars 2013

'''

usage       =     """\n %prog [options]
Generation of .pym pymol representation of models
 
This script allows one to output .pym files to vizualize models in pymol.
These files are built from a representation and a coordinate file. 

EXEMPLE :
 %prog -r ./Setup/1TYQ-HGM-rep.xml  -c ./Setup/1TYQ-HGM.txt  -P ./Models/ --p 1TYQ-HGM--model\
            --col-map="./Setup/1TYQ-color-mapping.xml"\
            --ms-lvl="complex" --col-lvl="subunit"
            
@todo: allow one to specify specific model indices to produce. For the moment, we output all models in the coordinate file.
@todo: allow one to chose between dumping distinct models in distinct .pym file, or tu dump everything in a "trajectory"
@todo: allow one to chose for the cgo object names, between the element name, a chain ID, or anything else
"""

import time
import sys
import os.path
from optparse import OptionParser

import HGM2.representation.complex
import HGM2.display.colors, HGM2.display.pymol
import HGM2.files.samples

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
    
    parser.add_option("-P","--path","--pym-path",             action="store",    type="string",
                      dest="pymPath",                           default=".",
                      help="path to a directory where to dump the pym files")
    parser.add_option("-p","--prefix","--pym-prefix",         action="store",    type="string",
                      dest="pymPrefix",                         default="HGM-model",
                      help="filename prefix for the pym files to output")
    
    parser.add_option("-m","--col-map","--color-map-file",         action="store",    type="string",
                      dest="cplxColorMap",
                      help="Path to a color map file that allows for mapping of subunits or domains to a color")
#    parser.add_option("-i","--id-models",                     action="store",    type="string",
#                      dest="indices",
#                      help="[optional] specify a coma separated list of indices for specific models to output as pdb files, if not set all models will be processed")
    parser.add_option("-l","--sel-lvl","--selection-level",         action="store",    type="string",
                      dest="level_sel",                         default="subunit",
                      help="controls the 'level' at which distinct pymol selections are produced in the resulting pym files (an object per 'subunit', per 'domain', or for the whole 'complex')")
    parser.add_option("-L","--col-lvl","--color-level",         action="store",    type="string",
                      dest="level_col",                         default="subunit",
                      help="controls the 'level' at which objects colored (use specific color foreach 'domain', or same color for markers in same 'subunit' or whole 'complex')")
    parser.add_option("-i","--indices",                     action="store",    type="string",
                      dest="indices",
                      help="allows one to select a specific subset of indices in the coordinates file (beware, starts with index 0)")
    parser.add_option("-v","--verbose",                     action="store_true", default='False',
                      dest="verbose",                       
                      help="verbose mode")
    options,args      = parser.parse_args(sys.argv[1:])
    #    Mandatory options
    #
    try :
        if options.representationFile  == None :
            errMsg = "Should provide a representation file"
            raise
        if options.coordinatesFile  == None :
            errMsg = "Should provide a coordinates file"
            raise
        
    except :
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
            self.representationFile      = test_dir+"Setup/1TYQ-HGM-rep.xml"

            self.coordinatesFile         = test_dir+"Setup/1TYQ-HGM.txt"
            self.pymPrefix               = "1TYQ-HGM--solution"
            self.pymPath                 = test_dir+"Display/"
            #
#            self.coordinatesFile         = test_dir+"Samples/ARP-EM0_2-saves--0.txt"
#            self.pymPrefix               = "ARP-EM0_2-saves--0-subset6"
#            self.pymPath                 = test_dir+"Display/"
#            _indices                = "10-11,102-104,199"
#            self.indices=HGM2.files.samples.get_indices_from_string( _indices )
            self.indices                = None
            
            self.cplxColorMap            = test_dir+"Setup/1TYQ-HGM-colors.xml"
            self.verbose                 = True
#            self.verbose                = False
            self.level_sel                = "complex"
#            self.level_sel               = "subunit"
#            self.level_sel                = "domain"
#            self.level_col               = "complex"
#            self.level_col               = "subunit"
            self.level_col               = "domain"

    options=pipo()
    return options






__get_pymol_color_CGO_string        = HGM2.display.pymol.get_pymol_color_CGO_string

def __get_pymol_sphere_CGO_string(x,y,z,r):
    return "SPHERE, {0:.4f}, {1:.4f}, {2:.4f}, {3:.4f},".format(x,y,z,r)
    
def __write_CGO_header(f):
    f.write(
"""from pymol.cgo import *
from pymol import cmd
from pymol.vfont import plain
"""
    )
def __write_CGO_lines(f,cgo_entries,frame_index=None):
    f.write("\n# "+(""if(frame_index==None)else str(frame_index))+"\n")
    f.write("data={}\n")
    for k,v in cgo_entries.iteritems() :
        f.write("data[\""+k+"\"]=[\n")
        for cgo_line in v :
            f.write(cgo_line + "\\\n")
        f.write("]\n")
#    for k in cgo_entries.keys() :
#        f.write("cmd.load_cgo(data["+k+"])")
    f.write("\n".join([
      "for k,v in data.items():",
      ("\tcmd.load_cgo(v,k)" if (frame_index == None) else "\tcmd.load_cgo(v,k,"+str(frame_index)+")")         
    ]))


_DEFAULT_SPHERE_COLOR = HGM2.display.colors.Color.get_by_name("purple")
__LEVEL_SUBUNIT, __LEVEL_DOMAIN, __LEVEL_COMPLEX = 0,1,2
def get_pymolCGOlines_for_complex_coordinates( cplx_coordinates,
                                               cplx_color_mapping=None, cplx_topology=None,
                                               selection_level="subunit", color_level="domain",
                                               verbose=False):
    """
    outputs a list of cmm lines for a given complex and coordinates
    @param cplx_coordinates     :   a CoordinatesSet::Coordinates object to transform in pdb
    @param cplx_chain_mapping   :   an optional mapping for the into chainIDs
    @param cplx_topology        :   topology description file for complex
    @param selection_level      :   decomposition level for selection objects {"domain","subunit","complex"} defaults to "subunit"
    @param color_level          :   colouring level {"domain","subunit","complex"} defaults to "domain"
    
    @todo : could spare some octets by placing colors only where needed. For the moment we indicate color for each bead even if only one color is used for the whole complex.
    """
    if (selection_level == "subunit") :
        sel_lvl = __LEVEL_SUBUNIT
    elif (selection_level == "domain"):
        sel_lvl = __LEVEL_DOMAIN
    elif (selection_level == "complex"):
        sel_lvl = __LEVEL_COMPLEX
    else :
        raise KeyError("when set, 'selection_level' keyword argument should be one of {'domain','complex','subunit'}")
    
    if (color_level == "subunit") :
        c_lvl = __LEVEL_SUBUNIT
    elif (color_level == "domain"):
        c_lvl = __LEVEL_DOMAIN
    elif (color_level == "complex"):
        c_lvl = __LEVEL_COMPLEX
    else :
        raise KeyError("when set, 'color_level' keyword argument should be one of {'domain','complex','subunit'}")
    
    
    cplx = cplx_coordinates.get_complex()
#    cplx = HGM2.representation.complex.Complex()
    
    if cplx_color_mapping == None :
        if verbose == True : print 'pym cgo creation> using default color'
        get_domain_color = lambda bead : _DEFAULT_SPHERE_COLOR
        get_subunit_color = get_domain_color
        get_complex_color = lambda : _DEFAULT_SPHERE_COLOR
    else :
        if verbose == True : print 'pym cgo creation> using color mapping'
        get_domain_color  = lambda bead :\
            cplx_color_mapping.get_subunit( bead.get_subunit().get_name() ).get_domain( bead.get_name() ).get_color()
        get_subunit_color = lambda subunit :\
            cplx_color_mapping.get_subunit( subunit.get_name() ).get_color()
        get_complex_color = lambda :\
            cplx_color_mapping.get_color()    
    
    if verbose == True : print "pym cgo creation>  considering complex "+cplx.get_full_name()
    
    cgo_lines={}
    if sel_lvl == __LEVEL_COMPLEX :
        curr_key = cplx.get_name()
        cgo_lines[curr_key] = []
    if c_lvl == __LEVEL_COMPLEX :
        curr_color = get_complex_color()
    for s in cplx.get_subunits():
        if sel_lvl == __LEVEL_SUBUNIT :
            curr_key = s.get_name()
            cgo_lines[curr_key] = []
        if c_lvl == __LEVEL_SUBUNIT :    
            curr_color = get_subunit_color(s)
        for b in s.get_beads():
            if sel_lvl == __LEVEL_DOMAIN :
                curr_key = b.get_full_name()
                cgo_lines[curr_key] = []
            if c_lvl == __LEVEL_DOMAIN :
                curr_color = get_domain_color(b)
            
            x, y, z = cplx_coordinates.get_bead_coordinates(b)
            r       = b.get_radius()
            
            cgo_lines[curr_key].append( __get_pymol_color_CGO_string( curr_color ) )
            cgo_lines[curr_key].append( __get_pymol_sphere_CGO_string(x,y,z,r) )
        
    if verbose == True : print "pym cgo creation> finished"
    
    return cgo_lines
        
        
        




def models2pym ( cplx, coodsSet, pymPath, pymPrefix,
                cplx_color_mapping=None, cplx_topology=None,
                indices=None, selection_level="subunit", color_level="domain",verbose=False ) :
    """  """
    if verbose == True : print ">>> models2pym"
    
    if indices == None :
        indices = range( coodsSet.get_number_of_configurations() )
    
    if verbose == True : print " working on {0:d} model indices".format(len(indices))
    
    
    pymFilePath = os.path.join( pymPath, (pymPrefix+".pym"  ) )
    pyf = open(pymFilePath,'w')
    __write_CGO_header(pyf)
    
#    pcgolfs = []
    fidx = 0
    for idx in indices :
        fidx+=1
        if verbose == True : print " - working on config {0:d}".format(idx)
        cplx_coordinates    = coodsSet.get_configuration(idx)
        
#        pymFilePath = os.path.join( pymPath, (pymPrefix+"--{0:d}.pym".format(idx)  ) )
#        pyf = open(pymFilePath,'w')
        
        pcgol = get_pymolCGOlines_for_complex_coordinates( cplx_coordinates, 
                                                                  cplx_color_mapping=cplx_color_mapping, cplx_topology=cplx_topology,
                                                                  selection_level=selection_level, color_level=color_level,
                                                                  verbose=verbose)
        __write_CGO_lines(pyf, pcgol, fidx)
#        pcgolfs.append(pcgol)
#    for pcgol in pcgolfs
    pyf.close()
    if verbose == True : print "   - saved to",pymFilePath




if __name__ == "__main__" :
    t_start = time.time()
    options = parseOptions()
#    options = get_test_options()
    
#    if options.verbose == True : 
    print "> reading representation file"
    cplx            = HGM2.representation.complex.Complex.get_complex_from_xml_file(options.representationFile)
    print "> reading coordinates file"
    coodsSet        = HGM2.representation.complex.CoordinatesSet(cplx)
    coodsSet.read_all_configs_from_file(options.coordinatesFile)
    print "   - got",coodsSet.get_number_of_configurations(),"configurations"
    
    indices = options.indices
    
    
    color_mapping = None
    if options.cplxColorMap != None :
        print "> reading color mapping file"
        color_mapping = HGM2.display.colors.ComplexColors.get_from_xml(options.cplxColorMap)
    
    if options.verbose == True :
        print "v> color mapping"
        print str(color_mapping)
        print "v< color mapping"
    
    topology       = None
    
    models2pym( cplx, coodsSet, options.pymPath, options.pymPrefix,
                cplx_color_mapping=color_mapping, cplx_topology=topology, 
                indices=indices, selection_level=options.level_sel, color_level=options.level_col,verbose=options.verbose )
  
    
    t_stop = time.time()
    print "...finished (in {0}s)".format( t_stop-t_start )    
