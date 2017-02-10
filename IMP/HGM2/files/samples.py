'''

'''
import re
import sys

#reRemarkLine        = re.compile("^\s*\#")
#reEmptyLine         = re.compile("^\s*$")
# a segment has format x-y
reIndex           = re.compile("^\s*(\d+)$")
reRange           = re.compile("^\s*(\d+)\s*-\s*(\d+)\s*$")



def get_indices_from_string(s,stringent=False):
    """returns a list of indices from a string
    @param s: indices string list, a coma separated list of indices or indices ranges (exemple : "1,4-278,89")
    @param stringent: what shall I do 
    """
    
    indices = []
    tokens  =   s.strip().split(",")
    for token in tokens :
        m = reIndex.match( token )
        if m != None :
            indices.append( int(m.group(0)) )
        else:
            m = reRange.match( token )
            if m != None :
                a,b = map(int,m.groups())
                if b < a :
                    errMsg = 'range bounds scrambeled ? ("{0:d}-{1:d}")'.format(a,b)
                    if stringent == True :
                        raise ValueError(errMsg)
                    else :
                        sys.stderr.write(errMsg + "\n")    
                indices.extend( range( a , b+1 ) )
            else:
                errMsg = 'unknown index range format ("{0:s}")'.format(token)
                if stringent == True :
                    raise ValueError(errMsg)
                else :
                    sys.stderr.write(errMsg + "\n")
    return indices
