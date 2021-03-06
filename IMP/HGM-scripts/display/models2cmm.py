'''
Created on 25 mars 2013

read coordinates and output chimera marker cmm files for an HGM complex
'''

__author__="Schwarz.B"
__date__ ="$march. 11 2013$"

usage       =     """\n %prog [options]
Generation of .cmm chimera representation of models
 
This script allows one to output chimera marker set .cmm files for one or several models saved in a sample file

EXEMPLE :
 %prog -r ./Setup/1TYQ-HGM-rep.xml  -c ./Setup/1TYQ-HGM.txt  -P ./Models/ --p 1TYQ-HGM--model\
            --col-map="./Setup/1TYQ-color-mapping.xml"\
            --ms-lvl="complex" --col-lvl="subunit"
"""

import time
import sys
import os.path
from optparse import OptionParser

import HGM2, HGM2.representation, HGM2.representation.complex
import HGM2, HGM2.display, HGM2.display.colors, HGM2.display.chimera
import HGM2.files.samples




_DEFAULT_MARKER_COLOR = HGM2.display.colors.Color.get_by_name("purple")

#import HGM2.pdb,HGM2.pdb.segments





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
    
    parser.add_option("-P","--path","--cmm-path",             action="store",    type="string",
                      dest="cmmPath",                           default=".",
                      help="path to a directory where to dump the cmm files")
    parser.add_option("-p","--prefix","--cmm-prefix",         action="store",    type="string",
                      dest="cmmPrefix",                         default="HGM-model",
                      help="filename prefix for the cmm files to output")
    
    parser.add_option("-m","--col-map","--color-map-file",         action="store",    type="string",
                      dest="cplxColorMap",
                      help="Path to a color map file that allows for mapping of subunits or domains to a color")
#    parser.add_option("-i","--id-models",                     action="store",    type="string",
#                      dest="indices",
#                      help="[optional] specify a coma separated list of indices for specific models to output as pdb files, if not set all models will be processed")
    parser.add_option("-l","--ms-lvl","--marker-set-level",         action="store",    type="string",
                      dest="level_ms",                         default="subunit",
                      help="controls the 'level' at which marker sets are produced in the resulting cmm files (a marker set per 'subunit', per 'domain', or for the whole 'complex')")
    parser.add_option("-L","--col-lvl","--color-level",         action="store",    type="string",
                      dest="level_col",                         default="subunit",
                      help="controls the 'level' at which markers are colored (use specific color foreach 'domain', or same color for markers in same 'subunit' or whole 'complex')")
    parser.add_option("-i","--indices",                     action="store",    type="string",
                      dest="indices",
                      help="allows one to select a specific subset of indices in the coordinates file (beware, starts with index 0)")
    parser.add_option("-v","--verbose",                     action="store_true", default='False',
                      dest="verbose",                       
                      help="verbose mode")
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
#            self.cmmPrefix              = "1TYQ-HGM--solution"
#            self.cmmPath                = test_dir+"Structs/"
#            #
            self.coordinatesFile         = test_dir+"Samples/ARP-EM0_2-saves--0.txt"
            self.cmmPath                = test_dir+"Structs/"
            self.cmmPrefix               = "ARP-mdl-EM0_2--0"

            #
#            _indices                = "0"
#            _indices                = "1"
            _indices                = "10-11,102-104,199"
            self.indices=HGM2.files.samples.get_indices_from_string( _indices )
#            self.indices                = None


            
            self.cplxColorMap           = test_dir+"Setup/1TYQ-HGM-colors.xml"
            self.verbose                = True
#            self.verbose                = False
            self.level_ms                = "complex"
#            self.level_ms                = "subunit"
#            self.level_ms                = "domain"
#            self.level_col               = "complex"
#            self.level_col               = "subunit"
            self.level_col               = "domain"

    options=pipo()
    return options





__LEVEL_SUBUNIT, __LEVEL_DOMAIN, __LEVEL_COMPLEX = 0,1,2 
def get_MarkerSets_for_complex_coordinates( cplx_coordinates,cplx_color_mapping=None, cplx_topology=None,marker_set_level="subunit", color_level="domain",verbose=False):
    """
    outputs a list of cmm lines for a given complex and coordinates
    @param cplx_coordinates     :   a CoordinatesSet::Coordinates object to transform in pdb
    @param cplx_chain_mapping   :   an optional mapping for the into chainIDs
    @param cplx_topology        :   topology description file for complex
    @param marker_set_level     :   Marker set level decomposition {"domain","subunit","complex"} defaults to "subunit"
    @param color_level          :   Marker set colouring level {"domain","subunit","complex"} defaults to "domain"
    """
    if (marker_set_level == "subunit") :
        ms_lvl = __LEVEL_SUBUNIT
    elif (marker_set_level == "domain"):
        ms_lvl = __LEVEL_DOMAIN
    elif (marker_set_level == "complex"):
        ms_lvl = __LEVEL_COMPLEX
    else :
        raise KeyError("when set, 'marker_set_level' keyword argument should be one of {'domain','complex','subunit'}")
    
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
        if verbose == True : print 'marker set creation> using default color'
        get_domain_color = lambda bead : _DEFAULT_MARKER_COLOR
        get_subunit_color = get_domain_color
        get_complex_color = lambda : _DEFAULT_MARKER_COLOR
    else :
        if verbose == True : print 'marker set creation> using color mapping'
        get_domain_color  = lambda bead :\
            cplx_color_mapping.get_subunit( bead.get_subunit().get_name() ).get_domain( bead.get_name() ).get_color()
        get_subunit_color = lambda subunit :\
            cplx_color_mapping.get_subunit( subunit.get_name() ).get_color()
        get_complex_color = lambda :\
            cplx_color_mapping.get_color()
#        def get_domain_color(bead):
#            color = cplx_color_mapping.get_subunit( bead.get_subunit().get_name() ).get_domain( bead.get_name() ).get_color()
#            print bead.get_subunit().get_name(),bead.get_name(),bead.get_full_name(),color
#            return color
    
    
    if verbose == True : print "marker set creation>  considering complex "+cplx.get_full_name()
    mss = HGM2.display.chimera.MarkerSets()
    
    if ms_lvl == __LEVEL_COMPLEX :
        marker_id = 1
        ms = mss.add_markerSet(cplx.get_full_name())
    if c_lvl == __LEVEL_COMPLEX :    
        color = get_complex_color()
    for s in cplx.get_subunits():
        if ms_lvl == __LEVEL_SUBUNIT :
            marker_id = 1
            ms = mss.add_markerSet(s.get_name())
        if c_lvl == __LEVEL_SUBUNIT :    
            color = get_subunit_color(s)
        for b in s.get_beads():
            if ms_lvl == __LEVEL_DOMAIN :
                marker_id = 1
                ms = mss.add_markerSet(b.get_full_name())
            if c_lvl == __LEVEL_DOMAIN :    
                color = get_domain_color(b)
                
            x, y, z = cplx_coordinates.get_bead_coordinates(b)
            r       = b.get_radius()
#            color = get_domain_color(b)
            
            ms.add_marker(id=marker_id, coods=(x,y,z) ,radius=r,color=color)
            marker_id+=1

        
    if verbose == True : print "marker set creation> finished"
    
    return mss
        
        
        
        


def models2cmm( cplx, coodsSet, cmmPath, cmmPrefix, \
                cplx_color_mapping=None, cplx_topology=None, \
                indices=None, marker_set_level="subunit", color_level="domain", verbose=False ) :
    """ 
    @return: the list of the markerset file pathes that were produced
    """
    if verbose == True : print ">>> models2cmm"
    
    cmmFilePath_list = []
    
    if indices == None :
        indices = range( coodsSet.get_number_of_configurations() )
    
    if verbose == True : print " working on {0:d} model indices".format(len(indices))
    
    for idx in indices :
        if verbose == True : print " - working on config {0:d}".format(idx)
        cplx_coordinates    = coodsSet.get_configuration(idx)
        cmmFilePath = os.path.join( cmmPath, (cmmPrefix+"--{0:d}.cmm".format(idx)  ) )
        ms = get_MarkerSets_for_complex_coordinates( cplx_coordinates, 
                                                                  cplx_color_mapping=cplx_color_mapping, cplx_topology=cplx_topology,
                                                                  marker_set_level=marker_set_level, color_level=color_level,
                                                                  verbose=verbose)
        ms.write_to_cmm_file(cmmFilePath)
        if verbose == True : print "   - saved to",cmmFilePath
        cmmFilePath_list.append(cmmFilePath)
    
    return (cmmFilePath_list)



if __name__ == "__main__":
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
    
    models2cmm( cplx, coodsSet, options.cmmPath, options.cmmPrefix,
                cplx_color_mapping=color_mapping, cplx_topology=topology, 
                indices=indices, marker_set_level=options.level_ms, color_level=options.level_col,verbose=options.verbose )

    t_stop = time.time()
    print "...finished (in {0}s)".format( t_stop-t_start )    
    
    
    
