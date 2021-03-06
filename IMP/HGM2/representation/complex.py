'''

'''

import os
import math

__protein_density                 = 0.84 # Da / A^3

import xml.dom.minidom
import HGM2.pdb.segments


#def trace( msg ):
#    pass

def trace( msg ):
    print msg






def compute_bead_mass( bead_size ):
    """ Computes the mass of a bead that constitutes a globular domain
    @param bead_size: number of AA composing the bead
    """
    return 110 * bead_size

def compute_bead_radius( bead_size ):
    """ Computes the radius of a bead that constitutes a globular domain
    @param bead_size: number of AA composing the bead
    """
    bead_mass   = compute_bead_mass( bead_size )
    bead_volume = bead_mass / __protein_density
    bead_radius = math.pow(  (3*bead_volume) / (4*math.pi),\
                             .33333)
    return bead_radius




#<complex name="ARP" version="1.0">
#<subunit name="arp2">
#  <bead name="" size="" radius="" mass=""/>

def _get_complex_from_xml_file( filePath ):
    
    def treat_subunit_tag(cplx_R,st):
        if not st.hasAttribute("name") :
            raise Exception("subunit should have a name")
        s_name          = st.getAttribute("name")
        s_R             = cplx_R.add_subunit(s_name)
        bl = st.getElementsByTagName("bead")
        for bt in bl :
            treat_bead_tag(s_R,bt)

    def treat_bead_tag(subunit_R,bt):
        if not bt.hasAttribute("name") :
            raise Exception("domain should have a name")
        if not bt.hasAttribute("radius") :
            raise Exception("domain should have a radius")
        if not bt.hasAttribute("mass") :
            raise Exception("domain should have a mass")
        
        d_name     = bt.getAttribute("name")
        d_radius   = float(bt.getAttribute("radius"))
        d_mass     = float(bt.getAttribute("mass"))
        try :
            d_size     = int(bt.getAttribute("size"))
        except :
            d_size     = 0
        
        b_R = subunit_R.add_bead( d_name, d_size )
        b_R.set_mass(d_mass)
        b_R.set_radius(d_radius)

    
    doc = xml.dom.minidom.parse( filePath )
    cplxs       = doc.getElementsByTagName("complex")
    if len(cplxs) > 1 :
        raise Exception("cannot handle more than one complex")
    elif len(cplxs) == 0 :
        raise Exception("need one complex")
    cplx        = cplxs[0]
    
    if not cplx.hasAttribute("name") :
        raise Exception("complex should have a name")
    cplx_name   = cplx.getAttribute("name")
    
    cplx_version=None
    if cplx.hasAttribute("version") :
        cplx_version= cplx.getAttribute("version")
        
    cplx_R = Complex(cplx_name,version=cplx_version)
    subunits        = cplx.getElementsByTagName("subunit")
    for st in subunits :
        treat_subunit_tag(cplx_R,st)
        
    return cplx_R
        

def _output_complex_to_xml_file( cplx, filePath , header_lines=[]) :
    """ """
    def treat_domain(b):
        return '    <bead name="{0:s}" size="{1:d}" radius="{2:f}" mass="{3:f}"/>'.format(b.get_name(),b.get_size(),b.get_radius(),b.get_mass())
    def treat_subunit(s):
        lines = []
        lines.append('  <subunit name="{0:s}">'.format(s.get_name()))
        lines.extend([treat_domain(d) for d in s.get_beads()])
        lines.append('  </subunit>')
        return lines
    def treat_complex(c):
        lines=[]
        c_name      = cplx.get_name()
        c_version   = cplx.get_version()
        if c_version == None :
            lines.append('<complex name="{0:s}">'.format(c_name))
        else :
            lines.append('<complex name="{0:s}" version="{1:s}">'.format(c_name,c_version))
        for s in c.get_subunits() : lines.extend( treat_subunit(s) )
        lines.append('</complex>')
        return lines
    lines=treat_complex(cplx)
    _header_lines=["<!--","file automatically produced"]
    _header_lines.extend(header_lines)
    _header_lines.append("-->\n\n")
    f = open(filePath,'w')
    f.write( "\n".join(_header_lines ) )
    f.write( "\n".join(lines) )
    f.close()
    return len(lines)

    
    
def _get_complex_from_ComplexChainSegmentMapping( cplxm ) :
    """ """
#        cplxm=HGM2.pdb.segments.ComplexChainSegmentMapping()
    cplx = Complex( cplxm.get_name() , cplxm.get_version() )
    for sm in cplxm.get_subunits() :
        s=cplx.add_subunit(sm.get_name())
        for dm in sm.get_domains():
            s.add_bead(dm.get_name(),dm.get_size())
    return cplx


class Complex:
    """ representation of a protein complex in terms of subunits and beads
    """
    
    @staticmethod
    def get_complex_from_xml_file(filePath):
        return _get_complex_from_xml_file(filePath)
    @staticmethod
    def write_complex_to_xml_file(cplx,filePath,header_lines=[]):
        return _output_complex_to_xml_file(filePath,header_lines)
    def write_to_xml_file(self,filePath,header_lines=[]):
        return _output_complex_to_xml_file(self,filePath,header_lines)
    @staticmethod
    def get_from_ComplexChainSegmentMapping( cplxm ) :
        """ """
        return _get_complex_from_ComplexChainSegmentMapping( cplxm )
        
    
    
    class Bead:
        """ domain bead
        @param subunit: attach the bead to the subunit to which it belongs
        @param name: bead name
        @param size: in number of AA
        @kwargs: mass and radius are automatically computed from size but can be overriden using 'mass' and 'radius' keyword args
        """
        def __init__ (self,subunit,name,size,**kwargs):
            self.__subunit  = subunit
            self.__name     = name
            self.__size     = None
            self.__radius   = None
            self.__mass     = None
            self.reset_bead_to_size(size)
            try :
                mass = kwargs["mass"]
                self.__mass = mass
            except :
                pass
            try :
                radius = kwargs["radius"]
                self.__radius = radius
            except :
                pass
        
        
        def __str__(self):
            return " ".join(["bead",self.get_name(), str( (self.__size,self.__radius,self.__mass) )])
            
        def __eq__(self,other):
            """ merely checks for bead content equality """
#            epsilon = 0.01
            for tst in (
                        self.get_name()                 == other.get_name(),
                        self.get_radius() == other.get_radius(),
                        self.get_mass() == other.get_mass(),
                        self.get_size() == other.get_size() 
#                        abs(self.get_radius() - other.get_radius()) < epsilon,
#                        abs(self.get_mass() - other.get_mass()) < epsilon,
#                        abs(self.get_size() - other.get_size()) < epsilon
                         ) :
                if tst == False :
                    return False
            return True
        
        def __ne__(self,other):
            return not self.__eq__(other)
            
        def __hash__(self):
            return id(self)
            
        def reset_bead_to_size(self,size):
            self.__size     = size
            self.__radius   = compute_bead_radius(size)
            self.__mass     = compute_bead_mass(size)
            
        def get_subunit(self):
            return self.__subunit
        def get_name(self):
            return self.__name
        def get_full_name(self):
            return self.get_subunit().get_name() + "-" + self.get_name()
        def get_size(self):
            return self.__size
        def get_radius(self):
            return self.__radius
        def get_mass(self):
            return self.__mass
        def set_radius(self,radius):
            self.__radius   = radius
        def set_mass(self,mass):
            self.__mass     = mass
        
        
    class Subunit():
        """
        """
        def __init__(self,cplx,name):
            self.__cplx             = cplx
            self.__name             = name
            self.__domains          = []
            self.__name_to_domain   = {}
        
        def __str__(self):
            repl = ["subunit",self.get_name()]
            repl.extend(["["+str(d)+"]" for d in self.get_beads()])
            return " ".join(repl)
        
        def __eq__(self,other):
            """ merely checks for subunit content equality
                subunit name should be similar, as well as beads content and the order in which they come """
            if self.get_name() != other.get_name() :
                return False
            try :
                for bs,bo in zip(self.get_beads(),other.get_beads()) :
                    if bs != bo :
                        return False
                return True
            except :
                return False
                
        def __ne__(self,other):
            return not self.__eq__(other)
        
        def __hash__(self):                 # identify the object by its memory addr, needed use subunits as dict keys
            return id(self)
    
    
        def add_bead(self,domain_name,segment_list):
            di=None
            try :
                di = self.__name_to_domain[domain_name]
                print "there is already a bead with such a name(",domain_name,") in subunit(",self.get_name(),")"
            except:
                di = Complex.Bead(self,domain_name,segment_list)
                self.__name_to_domain[domain_name]=di
                self.__domains.append( di )
            return di
        
        def get_name(self):
            return self.__name
        def get_bead(self,bead_ref):
            """@param bead_ref: a reference to a bead; might be a bead name or an int, in which case it should be a bead index between 0 and the number of beads in that subunit"""
            if isinstance(bead_ref, basestring) :
                return self.__name_to_domain[bead_ref]
            else :
                return self.__domains[bead_ref]
        def get_beads(self):
            return self.__domains
        def get_bead_names(self):
            return self.__name_to_domain.keys()
        def get_complex(self):
            return self.__cplx
            
        def get_size(self):
            """returns the number of AA composing the subunit"""
            return sum([d.get_size() for d in self.get_beads()])
        def get_mass(self):
            """returns the mass of the subunit (in Da)"""
            return sum([d.get_mass() for d in self.get_beads()])
        
        def get_number_of_beads(self):
            return len(self.__domains)
        
        
    def __init__(self,name,version=None):
        self.__name = name
        self.__version = version
        self.__subunits=[]
        self.__name_to_subunit={}
        
    def __str__(self):
        repl = [" ".join( ["complex",self.get_name(),\
                          ("(v"+str(self.get_version())+")") if self.has_version() else ""] \
                        )]
        repl.extend([str(s) for s in self.get_subunits()])
        return "\n".join(repl)
    
    def __eq__(self,other):
        try :
            if ( (self.get_name()    != other.get_name()) or
                 (self.get_version() != other.get_version()) ) : 
                return False
            for s1,s2 in zip ( self.get_subunits(),other.get_subunits() ) :
                if s1 != s2 :
                    return False
            return True
        except :
            return False
    
    def __ne__(self,other):
        return not self.__eq__(other)
        

        
    def add_subunit(self,name):
        """ adds a subunit to the complex and returns that subunit
        """
        si=None
        try :
            si = self.__name_to_subunit[name]
            print "there is already a subunit named "+name+" in the complex"
        except :
            si = self.Subunit(self,name)
            self.__subunits.append(si)
            self.__name_to_subunit[name]=si
        return si
    
    def get_name(self):
        return self.__name
    
    def get_full_name(self):
        return (self.__name + (("") if (not self.has_version()) else (" v"+self.get_version())))
    
    def has_version(self):
        return self.__version != None
    
    def get_version(self):
        return self.__version
        
    def get_subunit_names(self):
        return self.__name_to_subunit.keys()
    
    def get_subunit(self,subunit_ref):
        """@param subunit_ref: a reference to a subunit; either a name or an integer index"""
        if isinstance(subunit_ref, basestring) :
            return self.__name_to_subunit[subunit_ref]
        else :
            return self.__subunits[subunit_ref]
        
    
    def get_subunits(self):
        return self.__subunits
    
    def get_size(self):
        return sum([s.get_size() for s in self.get_subunits()])

    def get_mass(self):
        return sum([s.get_mass() for s in self.get_subunits()])
    
    def get_subunit_number_of_beads(self,subunit_name):
        return self.get_subunit(subunit_name).get_number_of_beads()
    
    def get_number_of_subunits(self):
        return len(self.__subunits)
    
    def get_number_of_beads(self):
        return sum ([ self.get_subunit(subunit_name).get_number_of_beads() for subunit_name in self.get_subunit_names() ])

    def get_beads(self):
        return [ b for s in self.get_subunits() for b in s.get_beads() ]
        
        
        
        
#        
#        
#        
#        
#class Coordinates():
#    """ hosts coordinates for a complex """
#    
#    def __init__(self,cplx):
#        """ @param cplx: a Complex object
#        """
#        self.__rep = cplx
#        self.__nb_beads = cplx.get_number_of_beads()
#        self.__coordinates      = [ 0.0 ] * (3*self.__nb_beads)
##        self.__subunit_size     = {}
##        self.__bead_indices     = {}
##        
##        for s in cplx.get_subunits() :
##            sn  = s.get_name()
##            snb = s.get_subunit_number_of_beads()
##            self.__subunit_size[sn] = snb
##        
##        bi = 0
##        for bead in cplx.get_beads() :
##            self.__bead_indices[bead] = bi
##            bi += 1
##            
##        self.__coordinates      = [ 0.0 ] * (3*bi)
##        
##            
##    def __get_bead_cood_index( self , bead):
##        return self.__bead_index[bead]        
##    
##    def set_bead_coordinates(self,bead):
##        """ 
##        @param bead: a bead in the complex
##        """
###        bci = self.__get_bead_cood_index(bead)
###        return list( self.__coordinates[bci:bci+3] )
##        
##    def get_bead_coordinates(self,bead):
##        """
##        @param bead: a bead in the complex
##        """    
##    
##    def set_subunit_coordinates(self,subunit):
##        
##    def get_subunit_coordinates(self,subunit):
#        
#    def set_coordinates(self,coordinates):
#        if len(coordinates) != 3*self.get_number_of_beads() :
#            raise Exception("'coordinates' should be a floating point vector of size",3*self.get_number_of_beads())
#        self.__coordinates = coordinates
#    
#    def get_coordinates(self):
#        return self.__coordinates
#        
#    def get_number_of_beads(self):
#        return self.__nb_beads
        
        
class CoordinatesSet :
    
    class __ComplexMapper :
        def __init__(self,cplx):
            self.__cplx = cplx
            self.__subunit_extent_indices   = {}
            self.__bead_index               = {}
            start                           = 0
            for s in cplx.get_subunits() :
                self.__subunit_extent_indices[s] = [start,start]
                for b in s.get_beads() :
                    self.__bead_index[b]    = start
                    start+=1;
                self.__subunit_extent_indices[s][1] = start
#                print str(s),self.__subunit_extent_indices[s]
            
        def get_bead_index(self,bead):
            return self.__bead_index[bead]

        def get_subunit_extent(self,subunit):
            return self.__subunit_extent[subunit]
        
        def get_number_of_beads(self):
            return len ( self.__bead_index.keys() )
        
        def get_complex(self):
            return self.__cplx
        
        def get_beads(self):
            return self.__cplx.get_beads()
                
        
    class Coordinates:
        """ An interface to access to coordinates of one specific "configuration", or model
            Basically, this is merely supposed to be a decorator to access coordinates in a CoordinatesSet
        """
        
        def __init__(self,mapper,coordinates):
            self.__mapper = mapper
            self.__coordinates = coordinates
            
        def get_bead_coordinates(self,bead):
            bidx = self.__mapper.get_bead_index(bead)
            return self.__coordinates[bidx]
            
        def set_bead_coordinates(self,bead,coods):
            if len(coods) != 3 :
                raise Exception("'coordinates' should contain 3 floating points")
            bidx = self.__mapper.get_bead_index(bead)
            self.__coordinates[bidx] = coods
            
        def __str__(self):
            beadlines = []
            for bead in self.__mapper.get_beads():
                beadlines.append( bead.get_full_name() + "  [" + str(self.get_bead_coordinates(bead)) + "]" )
            return "\n".join(beadlines)
        
        def get_complex(self):
            return self.__mapper.get_complex()
        
        
    
    def __init__(self,cplx):
        self.__cplx             = cplx
        self.__mapper = self.__ComplexMapper(cplx)
        self.__coordinates      = [ ]
        self.__number_of_beads = self.__mapper.get_number_of_beads()
    
    def add_configuration(self):
        coods = [ [0.0]*3 for i in range(self.__number_of_beads) ]
        self.__coordinates.append( coods )
        return self.Coordinates(self.__mapper,coods)
    
    def get_number_of_configurations(self):
        return len( self.__coordinates )
    
    def get_configuration(self,idx):
        try :
            return self.Coordinates( self.__mapper, self.__coordinates[idx] )
        except IndexError as e :
            raise IndexError("model index out of range, asked mdl({0:d}) when CoordinatesSet has ({1:d}) mdls".format(
                                        idx , self.get_number_of_configurations()
                                        )
                             )
    
    def __write_header(self, f):
        header_lines = []
        header_lines.append( "# --- Configurations save" )
        header_lines.append( "# number of subunits : " + str( self.__cplx.get_number_of_subunits() ) )
        for s in self.__cplx.get_subunits() :
            header_lines.append( "# subunit : " + s.get_name() + " : " + str(s.get_number_of_beads()) )
        f.write("\n".join(header_lines))
        f.write("\n\n")
    
    def write_configurations_to_file(self,filePath,decimals=None):
        """ write conformation coordinates to file
        @param filePath:
        @param decimals: optional parameter to cut coordinate values after a certain decimal  
        """
        f = open(filePath,"w")
        self.__write_header(f)
        num_lines_written=0
        if decimals == None :
            coodformat="{0:f},{1:f},{2:f}"
        else :
            coodformat="{{0:.{0:d}f}},{{1:.{0:d}f}},{{2:.{0:d}f}}".format(decimals)
        for coods in self.__coordinates :
#            print ">>> ", coods," <<<<"
            line_tokens = []
            for cood in coods :
#                print "--<< ",cood
#                x,y,z = cood
#                x,y,z = str(x),str(y),str(z)
#                line_tokens.append(",".join([x,y,z]))
                line_tokens.append(coodformat.format(*cood))
            f.write(" ".join(line_tokens)+"\n")
            num_lines_written+=1
        f.close()
        return num_lines_written
    
#    def get_complex(self):
#        return self.__cplx
        
        
    def __read_header(self,f):
        # stop on the first empty line
        # for the moment we don't do anything with the header... 
        # though it would be a good idea to verify data content adequation
        for line in f:
            if line == "\n":
                break
            
    def read_all_configs_from_file(self, filePath):
        """read all configurations from a file
        @note: should be deprecated soon, use the more generic function read_configs_from_file instead"""
        num_lines_read=0
        try :
            f = open(filePath)
            self.__read_header(f)
            for line in f :
                config = []
                for cood in line.strip().split(" ") :
                    x,y,z = cood.split(",")
                    coods = [float(x),float(y),float(z)]
                    config.append(coods)
                self.__coordinates.append(config)
                num_lines_read+=1
            f.close()
        except :
            print "error while reading file>",filePath
            raise
#            num_lines_read = -1
        return num_lines_read
    
    def read_configs_from_file(self, filePath,**kwargs):
        """read complex coordinates from a given file, and load it in the current container
        @param filePath: where the coordinates are store
        @keyword indices: an optional subset of indices, load only these ones and forget the others
        
        @return: a pair of integer values, respectively the number of model coordinates that were read in the file, and the number of solutions that were loaded in the container"""
        
        indices = None
        if kwargs.has_key("indices") :
            indices = kwargs["indices"]
            print ">>>>>",indices
        
        try :
            f = open(filePath)
            self.__read_header(f)
            num_lines_read=0
            num_lines_loaded=0
            for line in f :
                if (indices == None) or (num_lines_read in indices) :
                    config = []
                    for cood in line.strip().split(" ") :
                        x,y,z = cood.split(",")
                        coods = [float(x),float(y),float(z)]
                        config.append(coods)
                    self.__coordinates.append(config)
                    num_lines_loaded+=1
                num_lines_read+=1
            f.close()
        except :
            print "CoordinatesSet : error while reading file>",filePath
            raise
        
        return num_lines_read,num_lines_loaded



#class Restraints():
#    """ """
#
#


#
#<complex name="ARP" version="1.0">
#  <subunit name="arp3">
#    <link name="" size="" ="d1" ="d2"/>
#
def _get_topology_from_xml_file( filePath ):
    
    def treat_link_tag(subunit,lt):
#        if not bt.hasAttribute("name") :
#            raise Exception("link should have a name")
#        if not bt.hasAttribute("size") :
#            raise Exception("link should have a size")
        if not lt.hasAttribute("d1") :
            raise Exception("a link should have an attribute named d1")
        if not lt.hasAttribute("d2") :
            raise Exception("a link should have an attribute named d2")
        
        l_d1            = lt.getAttribute("d1")
        l_d2            = lt.getAttribute("d2")        
        try :
            l_name      = lt.getAttribute("name")
        except :
            l_name      = None
            
        try :
            l_size      = int(lt.getAttribute("size"))
        except:
            l_size      = 0
        
        l_R = subunit.add_link( l_d1,l_d2,l_size,l_name )
        return l_R
    
    def treat_subunit_tag(cplx_R,st):
        if not st.hasAttribute("name") :
            raise Exception("topology subunit should have a name")
        s_name          = st.getAttribute("name")
        s_R             = cplx_R.add_subunit(s_name)
        ll = st.getElementsByTagName("link")
        for lt in ll :
            treat_link_tag(s_R,lt)
    
    def treat_complex_tag( doc ):
    
        cplxs       = doc.getElementsByTagName("topology")
        if len(cplxs) > 1 :
            raise Exception("cannot handle more than one complex")
        elif len(cplxs) == 0 :
            raise Exception("need one complex")
        cplx        = cplxs[0]
        
        if not cplx.hasAttribute("name") :
            raise Exception("complex should have a name")
        cplx_name   = cplx.getAttribute("name")
        
        cplx_version=None
        if cplx.hasAttribute("version") :
            cplx_version= cplx.getAttribute("version")
            
        cplx_R = Topology(cplx_name,version=cplx_version)
        subunits        = cplx.getElementsByTagName("subunit")
        for st in subunits :
            treat_subunit_tag(cplx_R,st)
            
        return cplx_R
    
    doc     = xml.dom.minidom.parse( filePath )
    topo    = treat_complex_tag(doc)
    return topo
#        
#
#def _output_complex_to_xml_file( cplx, filePath , header_lines=[]) :
#    """ """
#    def treat_domain(b):
#        return '    <bead name="{0:s}" size="{1:d}" radius="{2:f}" mass="{3:f}"/>'.format(b.get_name(),b.get_size(),b.get_radius(),b.get_mass())
#    def treat_subunit(s):
#        lines = []
#        lines.append('  <subunit name="{0:s}">'.format(s.get_name()))
#        lines.extend([treat_domain(d) for d in s.get_beads()])
#        lines.append('  </subunit>')
#        return lines
#    def treat_complex(c):
#        lines=[]
#        c_name      = cplx.get_name()
#        c_version   = cplx.get_version()
#        if c_version == None :
#            lines.append('<complex name="{0:s}">'.format(c_name))
#        else :
#            lines.append('<complex name="{0:s}" version="{1:s}">'.format(c_name,c_version))
#        for s in c.get_subunits() : lines.extend( treat_subunit(s) )
#        lines.append('</complex>')
#        return lines
#    lines=treat_complex(cplx)
#    _header_lines=["<!--","file automatically produced"]
#    _header_lines.extend(header_lines)
#    _header_lines.append("-->\n\n")
#    f = open(filePath,'w')
#    f.write( "\n".join(_header_lines ) )
#    f.write( "\n".join(lines) )
#    f.close()
#    return len(lines)


class Topology():
    """ 
    Hosts subunit topology inside a complex, and eases read/write in xml format
    
    A (complex)Topology contains subunits, and each subunit  
    """
    
    @staticmethod
    def get_from_xml_file(filePath) :
        return _get_topology_from_xml_file(filePath)
    
    class Link():
        """ """
        def __init__(self, subunit, bead_name1, bead_name2, size=0, name=None):
            self.__subunit      = subunit
            self.__size         = size
            self.__bead_name1   = bead_name1
            self.__bead_name2   = bead_name2
            if name == None or name == "":
                self.__name     = "-".join(["link",bead_name1,bead_name2])
            else :
                self.__name     = name
                
        def __str__(self):
            return "<{0:s}:{1:d}>".format(self.__name,self.__size)
            
        def get_name(self):
            return self.__name
        
        def get_size(self):
            return self.__size
        
        def get_bead_names(self):
            return (self.__bead_name1,self.__bead_name2)
        
        def get_subunit(self):
            return self.__subunit
        
    
    class Subunit():
        """
        """
        def __init__(self,cplxTopo,name):
            self.__cplx             = cplxTopo
            self.__name             = name
            self.__links            = []
        
        def __str__(self):
            repl = ["subunit topology",self.get_name()]
            repl.extend(["["+str(l)+"]" for l in self.get_links()])
            return " ".join(repl)
    
        def add_link(self, bead_name1, bead_name2, size=0, name=None):
            """ @todo: should check existence of an existing link between the two beads"""
            li = Topology.Link(self,bead_name1, bead_name2, size, name)
            self.__links.append( li )
            return li
        
        def get_name(self):
            return self.__name
        
        def get_link(self,link_idx):
            """@param link_idx: an integer index"""
            return self.__links[link_idx]
        def get_links(self):
            return self.__links
        
        def get_complex(self):
            return self.__cplx
                    
        def get_number_of_links(self):
            return len(self.__links)
                
    def __init__(self,name,version=None):
        self.__name = name
        self.__version = version
        self.__subunits=[]
        self.__name_to_subunit={}
        
    def __str__(self):
        repl = [" ".join( ["complex topology",self.get_name(),\
                          ("(v"+str(self.get_version())+")") if self.has_version() else ""] \
                        )]
        repl.extend([str(s) for s in self.get_subunits()])
        return "\n".join(repl)
    
    def __eq__(self,other):
        if ( (self.get_name()    != other.get_name()) or
             (self.get_version() != other.get_version()) ) : 
            return False
        # BEWARE : Here there might be something fishy if the subunit list content is similar but not the order 
        for s1,s2 in zip ( self.get_subunits(),other.get_subunits() ) :
            if s1 != s2 :
                return False
        return True
    
    def __ne__(self,other):
        return not self.__eq__(other)
        

        
    def add_subunit(self,name):
        si=None
        try :
            si = self.__name_to_subunit[name]
            print "there is already a subunit named "+name+" in the complex topology"
        except :
            si = self.Subunit(self,name)
            self.__subunits.append(si)
            self.__name_to_subunit[name]=si
        return si
    
    def get_name(self):
        return self.__name
    
    def get_full_name(self):
        return (self.__name + (("") if (not self.has_version()) else (" v"+self.get_version())))
    
    def has_version(self):
        return self.__version != None
    
    def get_version(self):
        return self.__version
        
    def get_subunit_names(self):
        return self.__name_to_subunit.keys()
    
    def get_subunit(self,subunit_ref):
        """@param subunit_ref: a reference to a subunit; either a name or an integer index"""
        if isinstance(subunit_ref, basestring) :
            return self.__name_to_subunit[subunit_ref]
        else :
            return self.__subunits[subunit_ref]
        
    
    def get_subunits(self):
        return self.__subunits
    
    def get_number_of_subunits(self):
        return len(self.__subunits)
    
    def get_number_of_links(self):
        return sum ([ self.get_subunit(subunit_name).get_number_of_links() for subunit_name in self.get_subunit_names() ])

    def get_links(self):
        return [ l for s in self.get_subunits() for l in s.get_links() ]
    
    
    
