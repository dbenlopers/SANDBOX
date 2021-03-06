'''

'''

import re
import xml.dom.minidom


reRemarkLine        = re.compile("^\s*\#")
reEmptyLine         = re.compile("^\s*$")
# a segment has format x-y
reSegment           = re.compile("^\s*(\d+)\s*-\s*(\d+)\s*$")
# a chain id is one character
reChain             = re.compile("^\s*([\S])\s*$")


class NoChainException (Exception):
    def __init__(self,message):
        Exception.__init__(self,message)
    

def get_segments_from_string(segments_string):
    """ """
    return [Segment.get_from_string(s) for s in segments_string.split(",")]

class Segment():
    """ a Segment is a range of values [start, .. ,stop] encoded by the pair (start,stop) """
    @staticmethod
    def get_from_range( r ):
        """ get a segment from a pair r=(start,stop) 
        @param r: a pair of floats (start,stop)"""
        return Segment(*r)
    @staticmethod
    def get_from_string( s ):
        """ get a segment from a string such as s="1-107" 
        @param r: a pair of floats (start,stop)"""
        ms      = reSegment.match(s)
        s1,s2   = ms.groups()
        return Segment(int(s1),int(s2))
    
    def __init__(self,start,stop):
        self.__AA_start = int(start)
        self.__AA_stop  = int(stop)
        
    def __str__(self):
        return "-".join([str(self.__AA_start),str(self.__AA_stop)])
        
    def get_start(self):
        return self.__AA_start
    
    def get_stop(self):
        return self.__AA_stop
    
#    def get_chain(self):
#        return self.__chain
    
    def get_range(self):
        return (self.__AA_start, self.__AA_stop)
    
    def get_size(self):
        return(self.__AA_stop - self.__AA_start + 1)
    
    
    def is_in(self,value):
        return (value >= self.__AA_start) and (value <= self.__AA_stop)
    
    
        


def get_chainSegments_from_chain_and_string(c,s):
    return [ChainSegment.get_from_chain_and_string(c,seg) for seg in s.split(",") ]

def get_chainSegments_from_string(s):
    c,segment_list=s.split(":")
    return ChainSegment.get_from_chain_and_string(c,segment_list)

class ChainSegment():
    """ a ChainSegment is a segment attached to a specific PDB chain """
    @staticmethod
    def get_from_chain_and_string(c,s):
        ms  = reSegment.match(s)
        s1,s2 = ms.groups()
        return ChainSegment(c,int(s1),int(s2))
    @staticmethod
    def get_from_string(s):
        """ get a ChainSegment from a string 
        @param s: a string of format 'chain:start-stop' """
        c,segment = s.split(":")
        return ChainSegment.get_from_chain_and_string(c,segment)
    @staticmethod
    def get_from_chain_and_range(c,r):
        return ChainSegment(c,r[0],r[1])
    

    def __init__(self,chain,start,stop):
        self.__chain    = chain
        self.__AA_start = start
        self.__AA_stop  = stop
        
    def get_start(self):
        return self.__AA_start
    
    def get_stop(self):
        return self.__AA_stop
    
    def get_chain(self):
        return self.__chain
    
    def get_range(self):
        return (self.__AA_start, self.__AA_stop)
    
    def get_size(self):
        return(self.__AA_stop - self.__AA_start + 1)




class ChainSegmentMapping():
    """ stores a mapping between segments of PDB chains and a renaming of the chains
        
        a segment is a range of AA indices on a PDB chain
        
        This object offers links
            from a chain ID to all segments on that chain
            from a new chain ID to all segments related to it
    """
    
    def __init__(self,**kwargs):
        """ 
        @keyword path: a path to a file containing segment mappings
        @keyword mapping:  a string containing segment mappings
        @requires: one and only one keyword must be given amongst 'path' and 'mapping'
         
         format describing the mapping of segments to new chain ID
            " <ChainId> : <segment specification> : <NewChainId>" 
        """
#        self._segments=[]
        self.__segments={}               # maps one segment to a new chain ID
        self.__chain_segments={}         # maps one chain ID to ts segments
        self.__new_chain_segments={}     # maps one new chain ID to its segments
        
        path    = kwargs.get("path")
        mapping  = kwargs.get("mapping")
        
        
        if path != None :
            self.__read_map_from_file(path)
        else :
            self.__read_map_from_string(mapping)
        
        
    def __read_map_from_string(self,mapString):
        for line in mapString.split("\n") :
            line = line.strip()
            if (reRemarkLine.match(line) != None) or (reEmptyLine.match(line) != None):
                continue
            try :
                c,s,nc = line.split(":")
            except :
                print ' expected "<ChainId> : <segment specification> : <NewChainId>", but got (',line,')' 
                raise
            
            try :
                mc  = reChain.match(c)
                mnc = reChain.match(nc)
                c   = mc.group(1)
                nb  = mnc.group(1)
#                sl=s.split(",")
                sl=get_chainSegments_from_chain_and_string(c,s)
                for seg in sl :
                    segment_info=seg
#                    ms  = reSegment.match(seg)
#                    s1,s2 = ms.groups()
#                    segment_info = Segment(c,int(s1),int(s2))
                    
                    self.__segments[segment_info]=nb
                    
                    try :
                        self.__chain_segments[c].append( segment_info )
                    except : # should specify keyerror or something
                        self.__chain_segments[c]=[segment_info]
                    
                    try :
                        self.__new_chain_segments[nc].append( segment_info )
                    except : # should specify keyerror or something
                        self.__new_chain_segments[nc]=[segment_info]
                    
                        
                
            except :
                print """ something fishy in the format <ChainId> : <segment specification> : <NewChainId>
                <ChainId> ({0:s}) should be one character
                <segment> ({1:s}) should be a (list of) range(s) such as "1-12,23-56,123-256"
                <NewChainId> ({2:s}) should be one character
                """.format(c,s,nc)
                raise
        
    def __read_map_from_file(self,filePath):
            f=open(filePath)
            self.__read_map_from_string("\n".join(f.readlines()))
                
    def iter_segments(self):
        return (self.__segments.keys())
    
    def get_new_chain(self,segment):
        return (self.__segments[segment])
    
    
    
def _get_ComplexChainSegmentMapping_from_xml_file( filename ):
    doc = xml.dom.minidom.parse( filename )
    cplxs       = doc.getElementsByTagName("complex")
    if len(cplxs) > 1 :
        raise Exception("cannot handle more than one complex")
    elif len(cplxs) == 0 :
        raise Exception("need one complex")
    cplx        = cplxs[0]
    
    if not cplx.hasAttribute("name") :
        raise Exception("complex should have a name")
    cplx_name   = str(cplx.getAttribute("name"))
    
    cplx_version=None
    if cplx.hasAttribute("version") :
        cplx_version= str(cplx.getAttribute("version"))
    cplx_I = ComplexChainSegmentMapping(cplx_name,version=cplx_version)
    subunits        = cplx.getElementsByTagName("subunit")
    for s in subunits :
        if not s.hasAttribute("name") :
            raise Exception("subunit should have a name")
        s_name  = str(s.getAttribute("name"))
        s_chain = None
        if s.hasAttribute("chain") :
            s_chain = str(s.getAttribute("chain"))
            if reChain.match(s_chain) == None:
                raise Exception("invalid chain ID for subunit "+s_name+"("+str(s_chain)+")")             
        s_I=cplx_I.add_subunit(s_name, s_chain)
        dl = s.getElementsByTagName("domain")
        for d in dl :
            if not d.hasAttribute("name") :
                raise Exception("domain should have a name")
            if not d.hasAttribute("segments") :
                raise Exception("domain should have a segment list attached")
            d_name     = str(d.getAttribute("name"))
            d_chain = None
            if d.hasAttribute("chain") :
                d_chain = str(d.getAttribute("chain"))
                if reChain.match(d_chain) == None:
                    raise Exception("invalid chain ID for domain "+d_name+"("+str(d_chain)+")")
            d_segments = str(d.getAttribute("segments"))
            segments = get_segments_from_string(d_segments)
            s_I.add_domain( d_name, segments, d_chain )
    return cplx_I

class ComplexChainSegmentMapping():
    """  Stores a description for a protein complex 
            in terms of subunits, domains, and segments for these domains
            optionnally, if chain specification are provided for segments,
            provides these too, as well as new chain specifications for the subunits
    """
    @staticmethod
    def get_from_xml_file(filePath):
        return _get_ComplexChainSegmentMapping_from_xml_file(filePath)
    
    class DomainInfo():
        def __init__(self,subunit,name,segment_list,domain_chain=None):
            self.__subunit      = subunit
            self.__name         = name
            self.__segments     = segment_list
            self.__domain_chain = domain_chain
        
        def get_name(self):
            return self.__name
        def get_full_name(self):
            return self.get_subunit().get_name() + "-" + self.get_name()
        def get_segments(self):
            return self.__segments
        def has_subunit_chain(self):
            return self.get_subunit().has_chain()
        def get_subunit_chain(self):
            return self.get_subunit().get_chain()
        def has_domain_chain(self):
            return self.__domain_chain != None
        def get_domain_chain(self):
            if self.has_domain_chain() :
                return self.__domain_chain
            else:
                raise NoChainException("this domain-info has no attached chain ID ("+self.get_full_name()+")")
        def get_size(self):
            return sum ([seg.get_size() for seg in self.get_segments()])
        def get_subunit(self):
            return self.__subunit
            
        def __str__(self):
            return " ".join(["domain",self.get_name()])
            
    class SubunitInfo():
        def __init__(self,cplx,name,chain=None):
            """ """
            self.__cplx             = cplx
            self.__name             = name
            self.__chain            = chain
            self.__domains          = []
            self.__name_to_domain   = {}
            
        def __str__(self):
            repl = ["subunit",self.get_name()]
            repl.extend(["["+str(d)+"]" for d in self.get_domains()])
            return " ".join(repl)
        
        def add_domain(self,domain_name,segment_list,domain_chain=None):
            di=None
            try :
                di = self.__name_to_domain[domain_name]
                print "there is already a domain with such a name(",domain_name,") in the subunit(",self.get_name(),")"
            except:
                di = ComplexChainSegmentMapping.DomainInfo(self,domain_name,segment_list,domain_chain)
                self.__name_to_domain[domain_name]=di
                self.__domains.append( di )
            return di
        
        def get_name(self):
            return self.__name
        def has_chain(self):
            return (self.__chain != None)
        def get_chain(self):
            if self.has_chain() == True :
                return self.__chain
            else:
                raise NoChainException("this subunit-info has no attached chain ID ("+self.get_name()+")")
        def get_domain(self,d_name):
            return self.__name_to_domain[d_name]
        def get_domains(self):
            return self.__domains
#        def iter_domain(self):
#            return (self.__domains)
        def get_complex(self):
            return self.__cplx
            
            
        def get_size(self):
            return sum([d.get_size() for d in self.get_domains()])
            
            
    def __init__(self,name,version=None):
        """ """
        self.__name=name
        self.__version=version
        self.__subunits=[]
        self.__name_to_subunit={}
        
    def __str__(self):
        repl = [" ".join( ["complex",self.get_name(),\
                          ("(v"+str(self.get_version())+")") if self.has_version() else ""] \
                        )]
        repl.extend([str(s) for s in self.get_subunits()])
        return "\n".join(repl)
        
        
    def add_subunit(self,name,chain=None):
        """ adds a subunit to the complex and returns that subunit
        """
        si=None
        try :
            si = self.__name_to_subunit[name]
            print "there is already a subunit with such a name in the complex"
        except : 
            si = self.SubunitInfo(self,name,chain)
            self.__subunits.append(si)
            self.__name_to_subunit[name]=si
        return si
    
    def get_name(self):
        return self.__name
    
    def has_version(self):
        return self.__version != None
    
    def get_version(self):
        return self.__version
        
    def get_subunit_names(self):
        return self.__name_to_subunit.keys()
    
    def get_subunit(self,name):
        return self.__name_to_subunit[name]
    
    def get_subunits(self):
        return self.__subunits
    
    def get_size(self):
        return sum([s.get_size() for s in self.get_subunits()])
        
    def get_domains(self):
        return [d for s in self.get_subunits() for d in s.get_domains()]

