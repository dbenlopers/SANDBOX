'''
Created on 24 avr. 2013

'''



import sys
from optparse import OptionParser

import os

import time
import numpy as np

#import numpy as np

import HGM2.representation.complex
import HGM2.representation.positionning
import HGM2.display.chimera


usage       =     """\n %prog [options]
This script outputs a chimera cmm marker file corresponding to bead positions
Typically, the produced cmm file is used to defins positionning restraints based on observed positions, 
or simply to visualize such positions.

As a default, markers radii in the produced cmm file reflect the positions 'threshold' fields.
If a representation file is also provided on the command line, the bead radius is added to the threshold for that bead markers.
If a color map file is provided on the command line, the bead color is used for the corresponding markers. 
"""

def parseOptions():
    """ returns an object with command line options fields set.
    """
    parser = OptionParser(usage=usage)
    #
    parser.add_option("-p","--pos","--pos-file","--positions",         action="store",    type="string",
                      dest="posPath",
                      help="the xml bead positions file")
    parser.add_option("-o","--out","--cmm",         action="store",    type="string",
                      dest="cmmPath",
                      help="where shall I write the output cmm file")
#    parser.add_option("-t","--threshold",
#                      help="a threshold constant to override positions"  )
    parser.add_option("-r","--representation-file",           action="store",    type="string",
                      dest="repPath",
                      help="representation file explaning HGM representation of the complex")
    parser.add_option("-m","--col-map","--color-map-file",         action="store",    type="string",
                      dest="cplxColorMap",
                      help="Path to a color map file that allows for mapping of subunits or domains to a color")
    parser.add_option("-l","--ms-lvl","--marker-set-level",         action="store",    type="string",
                      dest="level_ms",                         default="position",
                      help="controls the 'level' at which marker sets are produced in the resulting cmm files (a marker set per 'position', or per 'bead')")    

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
        if options.posPath  == None :
            errMsg = "Should provide a bead position file"
            raise MandatoryOptionException(errMsg)
        if options.cmmPath  == None :
            errMsg = "Should provide an output cmm file path"
            raise MandatoryOptionException(errMsg)
    except MandatoryOptionException as e :
        errMsg = e.message
        sys.stderr.write( errMsg + "\n\n" )
        parser.print_usage()
        sys.exit(1)
    
    
    return options

__DEFAULT_MARKER_COLOR          = HGM2.display.colors.Color.get_by_name("burlywood3")
__LEVEL_POSITION, __LEVEL_BEAD  = 0, 1
def get_cmm_from_positions(pos, cplx=None, colors=None ,marker_set_level="position", verbose=False) :
    if (marker_set_level == "position") :
        ms_lvl = __LEVEL_POSITION
    elif (marker_set_level == "bead"):
        ms_lvl = __LEVEL_BEAD
    else :
        raise KeyError("when set, 'marker_set_level' keyword argument should be one of {'position','bead'}")
    
    if colors != None :
        get_domain_color = lambda b: colors.get_subunit( b.get_subunit_name() ).get_domain( b.get_bead_name() ).get_color()
    else :
        get_domain_color = lambda b: __DEFAULT_MARKER_COLOR

    if cplx != None :
        get_bead_radius = lambda b: cplx.get_subunit(b.get_subunit_name()).get_bead(b.get_bead_name()).get_radius()
    else :
        get_bead_radius = lambda b: 0

    if verbose == True : print "creating MarkerSet"
    mss = HGM2.display.chimera.MarkerSets()
    
    for b in pos.get_beads() :
        if verbose == True : print "treating bead s( {0:s} ) b({1:s})".format(b.get_subunit_name(),b.get_bead_name())
        if ms_lvl == __LEVEL_BEAD :
            marker_id = 1
            ms=mss.add_markerSet( b.get_full_name() )
        beadRadius = get_bead_radius(b)
        b_color = get_domain_color(b)
        for p in b.get_positions() :
            if ms_lvl == __LEVEL_POSITION :
                marker_id = 1
                ms=mss.add_markerSet( p.get_name() )
            x,y,z   = p.get_coordinates()
            r       = p.get_threshold() + beadRadius
            ms.add_marker(id=marker_id, coods=(x,y,z) ,radius=r,color=b_color)
            marker_id += 1
            
    return mss
    
    
if __name__ == "__main__" :
    options = parseOptions()
    #
    pos = HGM2.representation.positionning.BeadPositions.get_from_xml_file( options.posPath )
    cplxRep = None
    if options.repPath != None :
        cplxRep = HGM2.representation.complex.Complex.get_complex_from_xml_file(options.repPath)
    cplxCol = None
    if options.cplxColorMap != None :
        cplxCol = HGM2.display.colors.ComplexColors.get_from_xml(options.cplxColorMap)
    
    cmm = get_cmm_from_positions(pos, cplx=cplxRep, colors=cplxCol ,marker_set_level=options.level_ms, verbose=options.verbose)
    
    if options.verbose == True : print "   - markers saved to",options.cmmPath
    cmm.write_to_cmm_file(options.cmmPath)
    
    
    
    
