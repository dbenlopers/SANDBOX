'''

'''


import os
import re
import numpy
from matplotlib import pyplot as plt


from alternate_configs import configs
#    MY TFIIH REPRESENTATION
#config_name_for_this_run    = "fixedGeom_0"
#config_name_for_this_run    = "fixedGeom_1_1"
#config_name_for_this_run    = "fixedGeom_EM_1_1"
config_name_for_this_run    = "fixedGeom_EM_1_2"

runDir                      = os.path.join("results",config_name_for_this_run)
saveDirSample               = os.path.join(runDir,"samples")
savePrefix                  = "saves"

dDir                        = os.path.join(runDir,"distances")
ccDir                       = os.path.join(dDir,"crossCorel")
#ccMatFilePrefix             = "subunits-distances-crossCorelMatrix"
#ccFileName                  = "crossCorelations-1000.txt"
#ccTag                       = "1000"

#ccMatFilePrefix             = "subunits-distances-crossCorelMatrix-963"
#ccFileName                  = "crossCorelations-963.txt"
#ccTag                       = "963"

#ccMatFilePrefix             = "subunits-distances-crossCorelMatrix-87"
#ccFileName                  = "crossCorelations-EM1.1-87.txt"
#ccTag                       = "87"

#ccMatFilePrefix             = "subunits-distances-crossCorelMatrix-223"
#ccFileName                  = "crossCorelations-EM1.1i-223.txt"
#ccTag                       = "223"

#ccMatFilePrefix             = "subunits-distances-crossCorelMatrix-112"
ccMatFilePrefix             = "subunits-distances-crossCorelMatrix"
ccFileName                  = "crossCorelations-EM1.2-112.txt"
ccTag                       = "112"

ccFilePath          = os.path.join(ccDir,ccFileName)


e_custom = [
     # inter CORE
 'p52-p8',
 #
 'p34-p62',
 'p44-p62',
 'p44-p34',
 #
 'p44-p8',
 'p52-p34',
 'p34-p8',
 'p8-p62',
 'p52-p62',
 'p52-p44',
     
     # CORE to linkers
 'p52-XPD',
 'p52-XPB',
 'XPD-p8',
 'p8-XPB',
 #
 'XPB-p62',
 'p34-XPB',
 'p44-XPB',
 'p44-XPD',
 'XPD-p62',
 'p34-XPD',
 #
 'XPD-XPB',
    # CAK to linkers 
 'XPB-MAT1',
 'CyclinH-XPB',
 'CDK7-XPB',
 'CDK7-XPD',
 'XPD-CyclinH',
 'XPD-MAT1',

    # CAK
 'CDK7-MAT1', 
 'CDK7-CyclinH',
 'CyclinH-MAT1',
 
    # CAK to CORE
 'p52-MAT1',
 'p52-CDK7',
 'p52-CyclinH',
 'p8-MAT1',
 'CyclinH-p8',
 'CDK7-p8',
 #
 'p44-MAT1',
 'p44-CDK7',
 'p44-CyclinH',
 'MAT1-p62',
 'CDK7-p62',
 'CyclinH-p62',
 'CDK7-p34',
 'p34-CyclinH',
 'p34-MAT1'
 ]


#    Filtering out known connected subunits 
#
domains_dict = [
     # inter CORE
 'p34-p62',
 #
 'p44-p8',
 'p52-p34',
 'p34-p8',
 'p8-p62',
 'p52-p62',
 'p52-p44',
     
     # CORE to linkers
 'p52-XPD',
 'XPD-p8',
 'p8-XPB',
 #
 'XPB-p62',
 'p34-XPB',
 'p44-XPB',
 'XPD-p62',
 'p34-XPD',
 #
 'XPD-XPB',
    # CAK to linkers ,
 'CyclinH-XPB',
 'CDK7-XPB',
 'CDK7-XPD',
 'XPD-CyclinH',

    # CAK to CORE
 'p52-MAT1',
 'p52-CDK7',
 'p52-CyclinH',
 'p8-MAT1',
 'CyclinH-p8',
 'CDK7-p8',
 #
 'p44-MAT1',
 'p44-CDK7',
 'p44-CyclinH',
 'MAT1-p62',
 'CDK7-p62',
 'CyclinH-p62',
 'CDK7-p34',
 'p34-CyclinH',
 'p34-MAT1'
 ]

def read_ccDict( fileName ):
    ccf = open(fileName)
    ccd = {}
    for line in ccf :
        try :
            cct,cc = re.split( "\s+" , line.strip() )
            e1,e2 = cct.split(":")
            try :
                ccd[e1][e2]=cc
            except :
                ccd[e1]={e2:cc}
                
        except :
            print "cc read, problem with line (",line," )"
            pass
    
    return ccd


def plot_ccMatrix_custom_restraint(e,ccd,eTag):
    #
    #    Fill cccmatrix
    #
    nbe = len(e)
    ccMatFileName       = "-".join([ccMatFilePrefix,ccTag,eTag]) + ".png"
    ccMatFilePath       = os.path.join(ccDir,ccMatFileName)
    
    cccm = numpy.zeros((nbe,nbe))
    for i in range(len (e)) :
        for j in range (len (e) ) :
            print i,j,
            if i==j :
                cc = 1.0
            else :
            # WARN : matrix indices 
            #    (0,0) ... (0,n)
            #    (1,0) ... (1,n)
            #
            #    (n,0) ... (n,n)
                e1=e[i];e2=e[j]
                print e1,e2,
                try :
                    cc = ccd[e1][e2]
                except :
                    cc = ccd[e2][e1]
            print cc
            cccm[i][len(e)-j-1]=cc
    #
    #    Draw
    #
    plt.clf()
    #plt.yticks(numpy.arange(45)+.5,e,size=10)
    plt.yticks(numpy.arange(nbe)*(float(nbe-2)/(nbe-1))+.5,e,size=10)
    #plt.xticks(numpy.arange(45),e,size=10,orientation=45)
    plt.xticks(numpy.arange(nbe)*(float(nbe-2)/(nbe-1))+1,e,size=8,color="black",rotation=75)
    #plt.xticks(numpy.arange(45)*(43./44)+.6,e,size=8,color="black",rotation=90)
    plt.tick_params(length=0)
    #plt.axhline(y=3+.5,color="black",linewidth=1)
    #plt.axhline(y=3+2.5,color="black",linewidth=1)    
    #plt.axhline(y=10+.5,color="black",linewidth=2)  # Linker
    #plt.axhline(y=10+9+.5,color="black",linewidth=1)  #
    #plt.axhline(y=10+9+1.5,color="black",linewidth=1)  #
    #plt.axhline(y=10+9+1+6.5,color="black",linewidth=2)         # CAK
    #plt.axhline(y=10+9+1+6+3.5,color="black",linewidth=2)       # MIX right
    #plt.axhline(y=10+9+1+6+3+9.5,color="black",linewidth=1)     # MIX left
    plt.imshow(cccm,interpolation='nearest',extent=(nbe-1,0,nbe-1,0))
    plt.colorbar()
    plt.savefig( ccMatFilePath )




cc = read_ccDict( ccFilePath )
plot_ccMatrix_custom_restraint( e_custom,cc,"complete" )
plot_ccMatrix_custom_restraint( domains_dict,cc,"restricted" )


