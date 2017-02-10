'''
'''

import colors
import xml.dom.minidom

#def get_chimera_color( color ):
#    """ return a chimera color string corresponding to a given Color
#    """



_DEFAULT_MARKER_RADIUS             = 1.0                   # 1AA
_DEFAULT_MARKER_COLOR_CHANNELS      = (0.8,0.8,0.8)
#_DEFAULT_MARKER_COLOR              = colors.Color.get_by_name("gray60")




def get_chimera_color_channels( ben_color ):
    return map( lambda x: x/255. , ben_color.get_channels() )

def get_chimera_color_channels_string( ben_color ):
    return 'r="{0:.3f}" g="{1:.3f}" b="{2:.3f}"'.format( *get_chimera_color_channels( ben_color ) )

def get_color_from_chimera_color_channels( r,g,b ):
    return colors.Color.get_from_rgb( int(r*255), int(g*255), int(b*255) )


#<marker_sets>
#<marker_set name="C">
#<marker id="1" x="-40.355" y="6.8887" z="55.171" r="1" g="0" b="1" radius="22"/>
def _get_marker_sets_from_xml_file( filePath ):
    
    def treat_marker_tag(markerSet,mt):
        
        if not mt.hasAttribute("id") :
            raise Exception("marker should have an ID")
        mid=int(mt.getAttribute("id"))
        if not ( mt.hasAttribute("x") and mt.hasAttribute("y") and mt.hasAttribute("z") ) :
            raise Exception("marker should have x,y,z coordinates")
        x,y,z=map( lambda v:float(mt.getAttribute(v)),["x","y","z"])
        
        radius=_DEFAULT_MARKER_RADIUS
        if mt.hasAttribute("radius"):
            radius=float(mt.getAttribute("radius"))
        
        r,g,b=_DEFAULT_MARKER_COLOR_CHANNELS
        if mt.hasAttribute("r") :
            r         = float(mt.getAttribute("r"))
        if mt.hasAttribute("g") :
            g         = float(mt.getAttribute("g"))
        if mt.hasAttribute("b") :
            b         = float(mt.getAttribute("b"))
        
        markerSet.add_marker( mid, (x,y,z), radius, get_color_from_chimera_color_channels( r,g,b ) )
        
            
    def treat_markerSet_tag(markerSets,mst):
        if not mst.hasAttribute("name") :
            raise Exception("MarkerSet should have a name")
        name          = mst.getAttribute("name")
        
        markerSet = markerSets.add_markerSet(name)
        ml = mst.getElementsByTagName("marker")
        for mt in ml :
            treat_marker_tag(markerSet,mt)

    def treat_markerSets_tag( doc ):
        mssl       = doc.getElementsByTagName("marker_sets")
        
        if len(mssl) > 1 :
            raise Exception("cannot handle more than one marker_sets in a file")
        elif len(mssl) == 0 :
            raise Exception("file doesn't contain a marker_sets")
        mss        = mssl[0]
        
        markerSets = MarkerSets()
        
        msl        = mss.getElementsByTagName("marker_set")
        for mst in msl :
            treat_markerSet_tag(markerSets,mst)
        
        return markerSets
    
    doc = xml.dom.minidom.parse( filePath )
    markerSets =treat_markerSets_tag( doc )
    
    return markerSets



class MarkerSets:
    """ A class to read/write/handle Chimera marker sets """
    
    @staticmethod
    def get_from_chimera_cmm_file(filePath):
        """returns a MarkerSet object from a chimera file"""
        return _get_marker_sets_from_xml_file(filePath)
            
    class Marker():
        """ a chimera marker 
        @param mid:       a marker id (these are maintained for each marker set in chimera with increasing indices starting from 1)
        @param coods:    a triplet of coods
        @param radius:   (optional) a floating point number
        @param color:    (optional) a colors.Color instance
        
        @todo: I should maintain ID coherence; 
        for the moment this is left to the user two markers of a same marker set can have the same ID
        """
        def __init__(self, marker_set, mid, coods, radius=_DEFAULT_MARKER_RADIUS ,color=None ):
            """ """
            self.__marker_set               = marker_set
            self.__id                       = mid
            self.__x,self.__y,self.__z      = coods
            self.__radius                   = radius
            self.__color                    = color         # should be a Color as defined in 'colors' module
            
        def __str__(self):
            return '<marker id="{0:d}" x="{1:.3f}" y="{2:.3f}" z="{3:.3f}" radius="{4:.3f}" {5:s}/>'.format(
                                        self.__id,self.__x,self.__y,self.__z,self.__radius,
                                        ("" if (not self.has_color()) else get_chimera_color_channels_string( self.get_color() ) )
                                        )
            
        def get_id(self):
            return self.__id
        def get_x(self):
            return self.__x
        def get_y(self):
            return self.__y
        def get_z(self):
            return self.__z
        def get_coordinates(self):
            return (self.__x, self.__y, self.__z)
        def get_radius(self):
            return self.__radius
        def has_color(self):
            return self.__color != None
        def get_color(self):
            return self.__color
    
    
    class MarkerSet:
        def __init__(self,container,name):
            self.__container    = container
            self.__name         = name
            self.__markers      = []
#            self.__idx_to_marker= {}
#            self.__last_idx_used= 1

        def __str__(self):
            ret_lines  = []
            ret_lines.append('<marker_set name="{0:s}">'.format(self.get_name()))
            ret_lines.extend([str(m) for m in self.__markers])
            ret_lines.append('</marker_set>')
            return "\n".join(ret_lines)
    
        def get_name(self):
            return self.__name
        
        def get_markers(self):
            return self.__markers
        
        def add_marker(self,id,coods,radius=_DEFAULT_MARKER_RADIUS,color=None):
            marker = MarkerSets.Marker(self, id, coods, radius, color)
            self.__markers.append( marker )
            return marker
    
    
    def __init__(self):
        self.__markerSets=[]
        self.__name_to_markerSets={}
        
    def __str__(self):
        ret_lines = ['<marker_sets>']
        ret_lines.extend([str(ms) for ms in self.__markerSets])
        ret_lines.append('</marker_sets>')
        return "\n".join(ret_lines) 
        
    def add_markerSet(self,name):
        try :
            ms = self.__name_to_markerSets.get[name]
            print "there is alreay a MarkerSet named "+name+" in the MarkerSets container"
        except :
            ms = MarkerSets.MarkerSet(self,name)
            self.__markerSets.append(ms)
            self.__name_to_markerSets[name]=ms
        return ms
            
    def get_markerSet(self,mid):
        """@param mid: MarkerSet identifier; either an index or a name"""
        if isinstance(mid, basestring) :
            return self.__name_to_markerSets[mid]
        else :
            return self.__markerSets[mid]
        
    def get_markerSets(self):
        return self.__markerSets
    
    def write_to_cmm_file(self,cmmFilePath):
        f = open(cmmFilePath,'w')
        f.write(str(self))
        f.close()
    
        
