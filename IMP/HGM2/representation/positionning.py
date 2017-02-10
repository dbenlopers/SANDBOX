'''

'''


import xml.dom.minidom

_DEFAULT_THRESHOLD_VALUE = 0.0


#<bead_positions name="pipo">
#   <bead subunit_name="arpc3" bead_name="d">
#      <position name="first" x="29.005" y="-13.081" z="10.371" threshold="5"/>
#      <position name="second" x="29.005" y="-13.081" z="0" threshold="9"/>
#   </bead>
#   <bead subunit_name="arpc1" bead_name="d">
#      <position name="unique" x="-41.744" y="4.104" z="53.703" threshold="1"/>
#   </bead>
#</bead_positions>

def _get_bead_positions_from_xml_file( filePath ):

    def treat_position_tag(bead,pt):
        if not ( pt.hasAttribute("x") and pt.hasAttribute("y") and pt.hasAttribute("z") ) :
            raise Exception("position should have x,y,z coordinates")
        x,y,z=map( lambda v:float(pt.getAttribute(v)),["x","y","z"])
        
        threshold = _DEFAULT_THRESHOLD_VALUE
        if pt.hasAttribute("threshold") :
            threshold = float(pt.getAttribute("threshold"))
        name = None
        if pt.hasAttribute("name") :
            name = pt.getAttribute("name")
                
        bead.add_position( x,y,z,threshold,name  )
            
    def treat_bead_tag(beadPositions,bt):
        if not bt.hasAttribute("bead_name") :
            raise Exception("bead should have a bead name")
        if not bt.hasAttribute("subunit_name") :
            raise Exception("bead should have a subunit name")
        name          = bt.getAttribute("bead_name")
        sname         = bt.getAttribute("subunit_name")
        
        bead = beadPositions.add_bead(sname,name)
        
        pl = bt.getElementsByTagName("position")
        for pt in pl :
            treat_position_tag(bead,pt)

    def treat_beadPositions_tag( doc ):
        bpl       = doc.getElementsByTagName("bead_positions")
        
        if len(bpl) > 1 :
            raise Exception("cannot handle more than one bead_positions in a file")
        elif len(bpl) == 0 :
            raise Exception("file doesn't contain a bead_positions")
        bps        = bpl[0]
        
        name = bps.getAttribute('name')
        
        beadPositions = BeadPositions(name)
        
        bl        = bps.getElementsByTagName("bead")
        for bt in bl :
            treat_bead_tag(beadPositions,bt)
        
        return beadPositions
    
    doc = xml.dom.minidom.parse( filePath )
    beadPositions =treat_beadPositions_tag( doc )
    
    return beadPositions


class BeadPositions :
    """ A class to store spatial positions of various beads in a complex
    
    This will typically be used to mark observed position of beads in space,
    or to force a bead location in space
    """
    @staticmethod
    def get_from_xml_file(filePath):
        """returns a MarkerSet object from a chimera file"""
        return _get_bead_positions_from_xml_file(filePath)
    
    class Position():
        def __init__(self,x,y,z,threshold,name=""):
            self.__x = float(x)
            self.__y = float(y)
            self.__z = float(z)
            self.__t = float(threshold)
            self.__name = name
        def __str__(self):
            return '<position name="{0:s}" x="{1:.2f}" y="{2:.2f}" z="{3:.2f}" threshold="{4:.2f}"/>'.format(
                                self.__name,self.__x,self.__y,self.__z,self.__t
                                )
        def get_x(self):
            return self.__x
        def get_y(self):
            return self.__y
        def get_z(self):
            return self.__z
        def get_threshold(self):
            return self.__t
        def get_coordinates(self):
            return (self.get_x(),self.get_y(),self.get_z())
        def get_name(self):
            return self.__name
    
    class Bead():
        def __init__(self,subunit_name,bead_name):
            """
            """
            self.__subunit_name     = subunit_name
            self.__bead_name        = bead_name
            self.__positions        = []
        def __str__(self):
            ret_lines  = []
            ret_lines.append('<bead subunit_name="{0:s}" bead_name="{1:s}">'.format(self.get_subunit_name(),self.get_bead_name()))
            ret_lines.extend([str(p) for p in self.__positions])
            ret_lines.append('</bead>')
            return "\n".join(ret_lines)
        def get_subunit_name(self):
            return self.__subunit_name
        def get_bead_name(self):
            return self.__bead_name
        def get_full_name(self):
            return self.get_subunit_name() + "-" + self.get_bead_name()
        def get_positions(self):
            return self.__positions
        def add_position(self,x,y,z,t=_DEFAULT_THRESHOLD_VALUE,name=None):
            """ 
            @param x: 
            @param y:
            @param z:
            @param t:
            @param name: 
            """
            p = BeadPositions.Position(x,y,z,t,name)
            self.__positions.append(p)
            return p
            
    def __init__(self,name):
        self.__name             = name
#        self.__version          = version
        self.__beads            = []
        self.__bead_name_to_position = {}
    def __str__(self):
        ret_lines = ['<bead_positions name="{0:s}">'.format(self.get_name())]
        ret_lines.extend([str(b) for b in self.__beads])
        ret_lines.append('</bead_positions>')
        return "\n".join(ret_lines)
     
    def add_bead(self,subunit_name,bead_name):
        p=BeadPositions.Bead(subunit_name,bead_name)
        self.__beads.append(p)
        self.__bead_name_to_position[ (subunit_name,bead_name) ] = p
        return p
        
    def get_beads(self):
        return self.__beads
    
    def get_bead(self,subunit_name,bead_name):
        return self.__bead_name_to_position[subunit_name,bead_name]
    
    def get_bead_names(self):
        return self.__bead_name_to_position.keys()
    
    def get_name(self):
        return self.__name
    
    def write_to_xml_file(self,filePath,header_lines=[]):
        f=open(filePath,'w')
        _header_lines = []
        _header_lines.extend(["<!--","file automatically produced"])
        _header_lines.extend(header_lines)
        _header_lines.append("-->\n\n")
        f.write("\n".join(_header_lines))
        f.write(str(self))
        f.write("\n")
        f.close()
    
            
