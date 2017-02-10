'''
Created on 22 avr. 2013

'''


usage       =     """\n %prog [options]
Generation of a pymol script for use with chimera in order to produce png pictures for HGM models

The 

EXEMPLE :
 %prog -r   -c
            --col-map="./Setup/1TYQ-color-mapping.xml"\
            --ms-lvl="complex" --col-lvl="subunit"
            
"""


import time
import sys
import os.path
from optparse import OptionParser

import HGM2, HGM2.files.samples, HGM2.representation, HGM2.display.colors
from models2cmm import models2cmm




def parseOptions():
    """ returns an object with command line options fields set.
    """
    parser = OptionParser(usage=usage)
    #
    
    parser.add_option("-r","--representation-file",           action="store",    type="string",
                      dest="representationFile",
                      help="Representation file explaning HGM representation of the complex")
    parser.add_option("-c","--coordinates-file",              action="store",    type="string",
                      dest="coordinatesFile",
                      help="Path to the file hosting model coordinates for the given representation")
    
    parser.add_option("-P","--path","--png-path",             action="store",    type="string",
                      dest="pngPath",                           default=".",
                      help="Path to a directory where to dump the png files")
    parser.add_option("-p","--prefix","--png-prefix",         action="store",    type="string",
                      dest="pngPrefix",                         default="HGM-model",
                      help="Filename prefix for the png files to output")

    
    parser.add_option("-m","--col-map","--color-map-file",         action="store",    type="string",
                      dest="cplxColorMap",
                      help="Path to a color map file that allows for mapping of subunits or domains to a color")
    
    
    parser.add_option("-o","--out","--chim","--chimera-script",         action="store",    type="string",
                      dest="chimeraScriptFilePath",   default=None,
                      help="the path for the resulting chimera script")
    parser.add_option("-R","--orient","--orientation",         action="store",    type="string",
                      dest="orientationFilePath",   default=None,
                      help="Path to a file that should be used as a reference for the frame orientation priori to shoot pictures")
    parser.add_option("-d","--dpi",                              action="store",    type="int",
                      dest="dpi",   default=None,
                      help="controls the size of produced images")

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


def get_chimera_script_lines(picture_filePathes, filePath_reference=None, dpi=None):
    """ returns python lines for a chimera script loading cmm files and producing png images
    (beware : I cannot have more than one marker in each)
    @param picture_filePathes : a list of pairs (cmmPath,pngPath) to specify where to find each cmm file and where to dump the corresponding image
    @param filePath_reference : a reference file, used to set the point of view, if none provided, pics will be centered automatically 
    @param dpi : controls the size of the picture, defaults to 100
    """
    command_lines = []
    command_lines.extend([
    "from chimera import runCommand       # to be able to run commands :)",
    "from chimera import replyobj         # to emit status message",
    "" ])
    if filePath_reference != None :
        command_lines.extend([                      
        "runCommand(\"open #0 {0:s}\")        # I want to align my pictures on THIS frame".format(filePath_reference),
        "runCommand(\"~modeldisp #0\")        # but I don't want to see it in the pictures)",
        "" ])
    
    for filePath_markerFile,filePath_pngFile in picture_filePathes :
        command_lines.append("runCommand(\"open #1 {0:s}\")".format(filePath_markerFile))
        dpi_string = ("") if (dpi == None) else ("units inches dpi {0:.1f}".format(dpi))
        command_lines.append( "runCommand(\"copy file {0:s} {1:s}\")".format( filePath_pngFile , dpi_string) )        
        command_lines.append("runCommand(\"close #1\")")
        
    return command_lines
    
def main():
    testcasePath            = "/Users/schwarz/DATA/testcases-complexes/3NIG/"
#    filePath_reference      = os.path.join(testcasePath,"viewPointReference-map-3NIG.png")
    filePath_reference      = os.path.join(testcasePath,"viewPointReference-cmm-3NIG-colores-004.py")
    picture_filePathes      = []
    for i in range(1,10) :
        fileName = "HGM_col_best_{0:>03d}".format(i)
        path1 = os.path.join(testcasePath,"ColoresAttempts","3NIG-3FCU-004",fileName+"--0.cmm")
        path2 = os.path.join(testcasePath,"ColoresAttempts","3NIG-3FCU-004",fileName)
        picture_filePathes.append( (path1,path2) )
    print "\n".join(get_chimera_script_lines( picture_filePathes,filePath_reference ))
    
    
    
    
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
    if indices == None :
        indices = range( coodsSet.get_number_of_configurations() )
    
    color_mapping = None
    if options.cplxColorMap != None :
        print "> reading color mapping file"
        color_mapping = HGM2.display.colors.ComplexColors.get_from_xml(options.cplxColorMap)
    
    if options.verbose == True :
        print "v> color mapping"
        print str(color_mapping)
        print "v< color mapping"
    
    topology       = None
    
    cmmPath = os.path.join(options.pngPath,"cmm")
    if options.verbose == True :
        print "producing cmm files"
    if not os.path.exists(cmmPath):
        try :
            if options.verbose == True : 
                print "directory <",cmmPath,"> does not exist, I'll create it"
            os.makedirs(cmmPath)
        except :
            raise
    models2cmm( cplx, coodsSet, cmmPath, options.pngPrefix,
                cplx_color_mapping=color_mapping, cplx_topology=topology, 
                indices=indices, marker_set_level="complex", color_level=options.level_col,verbose=options.verbose )

    if options.verbose == True :
        print "producing chimera script file for rendering images"
    picture_filePathes = [
        ( os.path.join( cmmPath,          options.pngPrefix + "--{0:d}.cmm".format(idx) ) ,
          os.path.join( options.pngPath,  options.pngPrefix + "--{0:d}.png".format(idx) ) )
            for idx in indices 
          ]
    script_lines = get_chimera_script_lines(picture_filePathes, filePath_reference=options.orientationFilePath, dpi=options.dpi)
    f = open(options.chimeraScriptFilePath,"w")
    f.write( "\n".join(script_lines) )
    f.close()
    
    print "> should run something like 'chimera --script {0:s}' maybe with a '--nogui' in front".format(options.chimeraScriptFilePath)

    t_stop = time.time()
    print "...finished (in {0}s)".format( t_stop-t_start )  
