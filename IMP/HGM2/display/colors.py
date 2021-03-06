'''
'''



import xml.dom.minidom
import re

_reColorStringHexa         = re.compile("^\#([0-9a-fA-F]{2})([0-9a-fA-F]{2})([0-9a-fA-F]{2})$")
_reColorStringRGBc         = re.compile("^\s*(\d{1,3})\s*,\s*(\d{1,3})\s*,\s*(\d{1,3})\s*$")
#_reColorStringRGBf         = re.compile("^(1\.?|0\.?|0?\.[0-9]+),(1\.?|0\.?|0?\.[0-9]+),(1\.?|0\.?|0?\.[0-9]+)$")
_reColorStringRGBf         = re.compile("^\s*([01]?\.?[0-9]*)\s*,\s*([01]?\.?[0-9]*)\s*,\s*([01]?\.?[0-9]*)\s*$")

reEmptyLine         = re.compile("^\s*$")
# a segment has format x<y
reSegment           = re.compile("^\s*(\d+)\s*-\s*(\d+)\s*$")
# a chain id is one character
reChain             = re.compile("^\s*([\S])\s*$")



_predifined_colors = {
        "white"                   : (255,255,255),
        "black"                   : (0,0,0),
        "gray"                    : (115,111,110),
        "gray0"                   : (21,5,23),
        "gray18"                  : (37,5,23),
        "gray21"                  : (43,27,23),
        "gray23"                  : (48,34,23),
        "gray24"                  : (48,34,38),
        "gray25"                  : (52,40,38),
        "gray26"                  : (52,40,44),
        "gray27"                  : (56,45,44),
        "gray28"                  : (59,49,49),
        "gray29"                  : (62,53,53),
        "gray30"                  : (65,56,57),
        "gray31"                  : (65,56,60),
        "gray32"                  : (70,62,63),
        "gray34"                  : (74,67,68),
        "gray35"                  : (76,70,70),
        "gray36"                  : (78,72,72),
        "gray37"                  : (80,74,75),
        "gray38"                  : (84,78,79),
        "gray39"                  : (86,80,81),
        "gray40"                  : (89,84,84),
        "gray41"                  : (92,88,88),
        "gray42"                  : (95,90,89),
        "gray43"                  : (98,93,93),
        "gray44"                  : (100,96,96),
        "gray45"                  : (102,99,98),
        "gray46"                  : (105,101,101),
        "gray47"                  : (109,105,104),
        "gray48"                  : (110,106,107),
        "gray49"                  : (114,110,109),
        "gray50"                  : (116,113,112),
        "gray60"                  : (120,115,114),
        "gray-10"                 : (1*255/10,)*3,
        "gray-20"                 : (2*255/10,)*3,
        "gray-30"                 : (3*255/10,)*3,
        "gray-40"                 : (4*255/10,)*3,
        "gray-50"                 : (5*255/10,)*3,
        "gray-60"                 : (6*255/10,)*3,
        "gray-70"                 : (7*255/10,)*3,
        "gray-80"                 : (8*255/10,)*3,
        "gray-90"                 : (9*255/10,)*3,
        "slate gray"              : (101,115,131),
        "slate gray1"             : (194,223,255),
        "slate gray2"             : (180,207,236),
        "slate gray3"             : (152,175,199),
        "slate gray4"             : (97,109,126),
        "light slate gray"        : (109,123,141),
        "dark slate gray"         : (37,56,60),
        "dark slate gray1"        : (154,254,255),
        "dark slate gray2"        : (142,235,236),
        "dark slate gray3"        : (120,199,199),
        "dim gray"                : (70,62,65),

        "blue"                    : (0,0,255),
        "blue1"                   : (0,0,225),
        "blue2"                   : (0,0,195),
        "blue3"                   : (0,0,165),
        "blue4"                   : (0,0,135),
        "cadet blue3"             : (119,191,199),
        "cadet blue4"             : (76,120,126),
        "midnight blue"           : (21,27,84),
        "slate blue"              : (53,126,199),
        "slate blue2"             : (105,96,236),
        "slate blue3"             : (115,124,161),
        "slate blue4"             : (52,45,126),
        "light slate blue"        : (115,106,255),
        "medium slate blue"       : (94,90,128),
        "dark slate blue"         : (43,56,86),
        "dark slate gray4"        : (76,125,126),
        "cornflower blue"         : (21,27,141),
        "royal blue"              : (43,96,222),
        "royal blue1"             : (48,110,255),
        "royal blue2"             : (43,101,236),
        "royal blue3"             : (37,84,199),
        "royal blue4"             : (21,49,126),
        "deep sky blue"           : (59,185,255),
        "deep sky blue2"          : (56,172,236),
        "deep sky blue3"          : (48,144,199),
        "deep sky blue4"          : (37,88,126),
        "dodger blue"             : (21,137,255),
        "dodger blue2"            : (21,125,236),
        "dodger blue3"            : (21,105,199),
        "dodger blue4"            : (21,62,126),
        "steel blue"              : (72,99,160),
        "steel blue1"             : (92,179,255),
        "steel blue2"             : (86,165,236),
        "steel blue3"             : (72,138,199),
        "steel blue4"             : (43,84,126),
        "light steel blue"        : (114,143,206),
        "light steel blue1"       : (198,222,255),
        "light steel blue2"       : (183,206,236),
        "light steel blue4"       : (100,109,126),
        "sky blue"                : (102,152,255),
        "sky blue3"               : (101,158,199),
        "sky blue4"               : (65,98,126),
        "light blue"              : (173,223,255),
        "light blue1"             : (189,237,255),
        "light blue2"             : (175,220,236),
        "light blue3"             : (149,185,199),
        "light blue4"             : (94,118,126),
        "sky blue"                : (130,202,255),
        "sky blue2"               : (121,186,236),
        "light sky blue"          : (130,202,250),
        "light sky blue2"         : (160,207,236),
        "light sky blue3"         : (135,175,199),
        "light sky blue4"         : (86,109,126),
        "cyan"                    : (0,255,255),
        "cyan1"                   : (87,254,255),
        "cyan2"                   : (80,235,236),
        "cyan3"                   : (70,199,199),
        "cyan4"                   : (48,125,126),
        "light cyan"              : (224,255,255),
        "light cyan2"             : (207,236,236),
        "light cyan3"             : (175,199,199),
        "light cyan4"             : (113,125,125),

        "thistle4"                : (128,109,126),
        
        "violet"                  : (141,56,201),
        "medium purple"           : (132,103,215),
        "medium purple1"          : (158,123,255),
        "medium purple2"          : (145,114,236),
        "medium purple3"          : (122,93,199),
        "medium purple4"          : (78,56,126),
        "violet red"              : (246,53,138),
        "violet red1"             : (246,53,138),
        "violet red2"             : (228,49,127),
        "deep pink"               : (245,40,135),
        "deep pink2"              : (228,40,124),
        "deep pink3"              : (193,34,103),
        "deep pink4"              : (125,5,63),
        "medium violet red"       : (202,34,107),
        "violet red3"             : (193,40,105),
        "firebrick"               : (128,5,23),
        "violet red4"             : (125,5,65),
        "medium orchid"           : (176,72,181),
        "medium orchid1"          : (212,98,255),
        "medium orchid2"          : (196,90,236),
        "medium orchid3"          : (167,74,199),
        "medium orchid4"          : (106,40,126),
        "purple"                  : (142,53,239),
        "purple1"                 : (137,59,255),
        "purple2"                 : (127,56,236),
        "purple3"                 : (108,45,199),
        "purple4"                 : (70,27,126),
        "dark violet"             : (132,45,206),
        "dark orchid"             : (125,27,126),
        "dark orchid1"            : (176,65,255),
        "dark orchid2"            : (162,59,236),
        "dark orchid3"            : (139,49,199),
        "dark orchid4"            : (87,27,126),
        "pale violet red"         : (209,101,135),
        "pale violet red1"        : (247,120,161),
        "pale violet red2"        : (229,110,148),
        "pale violet red3"        : (194,90,124),
        "pale violet red4"        : (126,53,77),
        "plum"                    : (185,59,143),
        "plum1"                   : (249,183,255),
        "plum2"                   : (230,169,236),
        "plum3"                   : (195,142,199),
        "plum4"                   : (126,88,126),
        "thistle"                 : (210,185,211),
        "thistle1"                : (252,223,255),
        "thistle2"                : (233,207,236),
        "thistle3"                : (198,174,199),
        "lavender"                : (227,228,250),
        "lavender blush"          : (253,238,244),
        "lavender blush2"         : (235,221,226),
        "lavender blush3"         : (200,187,190),
        
        "turquoise"               : (67,198,219),
        "turquoise1"              : (82,243,255),
        "turquoise2"              : (78,226,236),
        "turquoise3"              : (67,191,199),
        "medium turquoise"        : (72,204,205),
        
        "pale turquoise3"         : (146,199,199),
        "pale turquoise4"         : (94,125,126),
        "dark turquoise"          : (59,156,156),
        "light sea green"         : (62,169,159),
        "dark sea green4"         : (97,124,88),
        "medium aquamarine"       : (52,135,129),
        "green"                   : (0,255,0),
        "green1"                  : (95,251,23),
        "green2"                  : (89,232,23),
        "green3"                  : (76,196,23),
        "green4"                  : (52,124,23),
        "dark green"              : (37,65,23),
        "medium spring green"     : (52,128,23),
        "spring green"            : (74,160,44),
        "lime green"              : (65,163,23),
        "spring green"            : (74,160,44),
        "yellow green"            : (82,208,23),
        "spring green1"           : (94,251,110),
        "spring green2"           : (87,233,100),
        "spring green3"           : (76,197,82),
        "spring green4"           : (52,124,44),
        "sea green"               : (78,137,117),
        "sea green1"              : (106,251,146),
        "sea green2"              : (100,233,134),
        "sea green3"              : (84,197,113),
        "sea green4"              : (56,124,68),
        "medium sea green"        : (48,103,84),
        "dark sea green"          : (139,179,129),
        "dark sea green1"         : (195,253,184),
        "dark sea green2"         : (181,234,170),
        "dark sea green3"         : (153,198,142),
        "lawn green"              : (135,247,23),
        "forest green"            : (78,146,88),
        "medium forest green"     : (52,114,53),
        "chartreuse"              : (138,251,23),
        "chartreuse2"             : (127,232,23),
        "chartreuse3"             : (108,196,23),
        "chartreuse4"             : (67,124,23),
        "green yellow"            : (177,251,23),
        "dark olive green1"       : (204,251,93),
        "dark olive green2"       : (188,233,84),
        "dark olive green3"       : (160,197,68),
        "dark olive green4"       : (102,124,38),
        "dark olive green"        : (85,107,47),
        "yellow"                  : (255,255,0),
        "yellow1"                 : (255,252,23),
        "khaki"                   : (173,169,110),
        "khaki1"                  : (255,243,128),
        "khaki2"                  : (237,226,117),
        "khaki3"                  : (201,190,98),
        "khaki4"                  : (130,120,57),
        
        "red"                     : (255,0,0),
        "red1"                    : (246,34,23),
        "red2"                    : (228,27,23),
        "indian red1"             : (247,93,89),
        "indian red2"             : (229,84,81),
        "indian red3"             : (194,70,65),
        "indian red4"             : (126,34,23),
        "firebrick1"              : (246,40,23),
        "firebrick2"              : (228,34,23),
        "firebrick3"              : (193,27,23),
        "magenta"                 : (255,0,255),
        "magenta1"                : (244,51,255),
        "magenta2"                : (226,56,236),
        "magenta3"                : (192,49,199),
        "orange"                  : (255,165,0),
        "orange red"              : (255,70,0),
        "dark orange"             : (248,128,23),
        "dark orange1"            : (248,114,23),
        "dark orange2"            : (229,103,23),
        "dark orange3"            : (195,86,23),
        "dark orange3"            : (126,49,23),

        
        "sienna"                  : (138,65,23),
        "sienna1"                 : (248,116,49),
        "sienna2"                 : (230,108,44),
        "sienna3"                 : (195,88,23),
        "sienna4"                 : (126,53,23),
        "chocolate"               : (200,90,23),
        "coral"                   : (247,101,65),
        "coral1"                  : (231,116,113),
        "coral2"                  : (229,91,60),
        "coral3"                  : (195,74,44),
        "light coral"             : (231,116,113),
        "dark salmon"             : (225,139,107),
        "salmon1"                 : (248,129,88),
        "salmon2"                 : (230,116,81),
        "salmon3"                 : (195,98,65),
        "salmon4"                 : (126,56,23),
        "light salmon"            : (249,150,107),
        "light salmon2"           : (231,138,97),
        "light salmon3"           : (196,116,81),
        "light salmon4"           : (127,70,44),
        "sandy brown"             : (238,154,77),
        
        "pink"                    : (250,175,190),
        "pink2"                   : (231,161,176),
        "pink3"                   : (196,135,147),
        "pink4"                   : (127,82,93),
        "light pink"              : (250,175,186),
        "light pink1"             : (249,167,176),
        "light pink2"             : (231,153,163),
        "light pink3"             : (196,129,137),
        "light pink4"             : (127,78,82),
        "hot pink"                : (246,96,171),
        "hot pink1"               : (246,101,171),
        "hot pink2"               : (228,94,157),
        "hot pink3"               : (194,82,131),
        "hot pink4"               : (125,34,82),
        "rosy brown1"             : (251,187,185),
        "rosy brown"              : (179,132,129),
        "rosy brown2"             : (232,173,170),
        "rosy brown3"             : (197,144,142),
        "rosy brown4"             : (127,90,88),
        "lavender blush4"         : (129,118,121),
        "fuchsia"                 : (255,0,255),
        "fuchsia1"                : (225,5,225),
        "fuchsia2"                : (205,10,205),
        "fuchsia3"                : (185,15,185),
        "fuchsia4"                : (155,20,155),
        "dark fuchsia"            : (155,0,155),
        
        "lemon chiffon2"          : (236,229,182),
        "lemon chiffon3"          : (201,194,153),
        "lemon chiffon4"          : (130,123,96),
        "lemon chiffon"           : (255,248,198),
        
        "gold"                    : (212,160,23),
        "gold1"                   : (253,208,23),
        "gold2"                   : (234,193,23),
        "gold3"                   : (199,163,23),
        "gold4"                   : (128,101,23),
        "light golden2"           : (236,214,114),
        "goldenrod"               : (237,218,116),
        "goldenrod1"              : (251,185,23),
        "goldenrod2"              : (233,171,23),
        "goldenrod3"              : (198,142,23),
        "goldenrod4"              : (128,88,23),
        "light goldenrod"         : (236,216,114),
        "light goldenrod1"        : (255,232,124),
        "light goldenrod3"        : (200,181,96),
        "light goldenrod4"        : (129,115,57),
        "light goldenrod yellow"  : (250,248,204),
        "dark goldenrod"          : (175,120,23),
        "dark goldenrod1"         : (251,177,23),
        "dark goldenrod2"         : (232,163,23),
        "dark goldenrod3"         : (197,137,23),
        "dark goldenrod4"         : (127,82,23),
        
        "maroon"                  : (129,5,65),
        "maroon1"                 : (245,53,170),
        "maroon2"                 : (227,49,157),
        "maroon3"                 : (193,34,131),
        "maroon4"                 : (125,5,82),
        "burlywood"               : (222, 184, 135),
        "burlywood1"              : (202, 164, 125),
        "burlywood2"              : (182, 144, 115),
        "burlywood3"              : (162, 124, 105),
        "burlywood4"              : (142, 104,  95),

        }





class ColorException(Exception):
    
    def __init__(self, message):
        Exception.__init__(self, message)
        
        
        

class Color :

    @staticmethod
    def get_color_names():
        """ returns the name of all registered colors
        """
        return _predifined_colors.keys()    
    @staticmethod
    def get_by_name(name):
        name=name.lower().replace('_',' ')
        try :
            color_channels = _predifined_colors[name]
        except :
            raise ColorException("unknown color name "+name)
        color=Color()
        color.set_channels( color_channels )
        return color

    @staticmethod
    def get_from_hexaString( s ):
        """ if s is a regular color hexa string, return the corresponding Color
            otherwise, raise an exception """
        try :
            r,g,b = map(lambda x:int(x,16) , _reColorStringHexa.match( s ).groups() )
        except AttributeError :
            raise ColorException( "fishy hexa color string"+s )
        color = Color()
        color.set_channels( (r,g,b) )
        return color
        
    @staticmethod
    def get_from_floatString( s ):
        """ if s is a regular
        """
        try :
            r,g,b = map( lambda x: int(255*x), map( float,_reColorStringRGBf.match( s ).groups() ))
        except AttributeError :
            raise ColorException( "fishy float color string"+s )
        color = Color()
        color.set_channels( (r,g,b) )
        return color
        
    @staticmethod
    def get_from_charString( s ):
        """
        generating a Color from a regular char color string 
        @Example : "2,034,256"
        """
        try :
            r,g,b = map( int, _reColorStringRGBc.match( s ).groups() )
        except AttributeError :
            raise ColorException( "fishy char color string"+s )
        color = Color()
        color.set_channels( (r,g,b) )
        return color
    
    @staticmethod
    def get_from_rgb(r,g,b):
        """
        """
        color = Color()
        color.set_channels( (r,g,b) )
        return color
        
    def get_from_channels(self,c):
        """
        """
        color = Color()
        color.set_channels( c )
        return color
        
                
    @staticmethod
    def get_from_string( s ):
        """
        @param s: a string encoding for a color
        @note : this function merely tries in turn one of the get_from_Xstring methods
        """
        try :
            return Color.get_by_name( s )
        except :
            try :
                return Color.get_from_hexaString( s )
            except :
                try :
                    return Color.get_from_charString( s )
                except :
                    try :
                        return Color.get_from_floatString( s )
                    except :
                        raise ColorException("fishy color string : "+s)
        
    @staticmethod
    def __char2hexa( c ):
        h=hex(c)[2:]
        if len(h) == 1 :
            h = "0"+h
        return h
    
    def __init__(self) :
        """ define a color
        @param channels: a triplet of int values between 0 and 256"""
        self.__color = (0 , 0 , 0)
        
    def __str__(self):
#        return ("color(r:{0:d},g:{1:d},b:{2:d})".format(*self.__color))
        return ("#{0:s}{1:s}{2:s}".format(*(map(Color.__char2hexa,self.__color))))
        
    def get_red(self):
        return self.__color[0]
    
    def get_green(self):
        return self.__color[1]
        
    def get_blue(self):
        return self.__color[2]

    def get_channels(self):
        return self.__color

    def set_channels(self,c):
        """ @param c: a triplet of 'char' integers (i.e int in [0,255]) """
        r,g,b = map(int,c)
        if r>=0 and r<256 and g>=0 and g<256 and b>=0 and b<256 :
            self.__color=(r,g,b)
        else :
            raise ColorException("out of bound values for color :"+str(c))
        
        

#__DEFAULT_DOMAIN_COLOR      = Color.get_by_name("gray60")
_DEFAULT_COMPLEX_COLOR      = Color.get_by_name("gray-60")


def _get_complex_colors_from_xml_file( filePath ):
    
    def treat_domain_tag(subunit_C,dt):
        if not dt.hasAttribute("name") :
            raise Exception("domain should have a name")
        
        d_name     = dt.getAttribute("name")
        
        if dt.hasAttribute("color") :
            d_c         = dt.getAttribute("color")
            d_color     = Color.get_from_string(d_c)
            subunit_C.add_domain( d_name, d_color )
        else :
            subunit_C.add_domain( d_name )
            
    def treat_subunit_tag(cplx_C,st):
        if not st.hasAttribute("name") :
            raise Exception("subunit should have a name")
        s_name          = st.getAttribute("name")
        if st.hasAttribute("color") :
            s_c         = st.getAttribute("color")
            s_color     = Color.get_from_string(s_c)
            s_C = cplx_C.add_subunit( s_name, s_color )
        else :
            s_C = cplx_C.add_subunit( s_name )
        
        bl = st.getElementsByTagName("domain")
        for bt in bl :
            treat_domain_tag(s_C,bt)

    def treat_complex_tag( doc ):
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
            
        cplx_color=_DEFAULT_COMPLEX_COLOR
        if cplx.hasAttribute("color") :
            cplx_c=cplx.getAttribute("color")
            cplx_color=Color.get_from_string(cplx_c)
            cplx_C = ComplexColors(cplx_name,version=cplx_version,color=cplx_color)
        else :
            cplx_C = ComplexColors(cplx_name,version=cplx_version)
            
        subunits        = cplx.getElementsByTagName("subunit")
        for st in subunits :
            treat_subunit_tag(cplx_C,st)
        
        return cplx_C
    
    doc = xml.dom.minidom.parse( filePath )
    cplx_C =treat_complex_tag( doc )
    
    return cplx_C





class ComplexColors :
    
    @staticmethod
    def get_from_xml( filePath ):
        return  _get_complex_colors_from_xml_file(filePath)
    
    class Domain :
        def __init__(self,subunit, name, color=None):
            self.__subunit  = subunit
            self.__name     = name
            self.__color    = subunit.get_color() if (color == None) else color
            
        def __str__(self):
            return "domain {0:s} colored {1:s}".format(self.__name,self.__color)
            
        def get_subunit(self):
            return self.__subunit
        def get_name(self):
            return self.__name
#        def get_full_name(self):
#            return self.get_subunit().get_name() + "-" + self.get_name()
        def get_color(self):
            return self.__color
    
    class Subunit :
        def __init__(self,cplx,name,color=None):
            self.__cplx             = cplx
            self.__name             = name
            self.__color            = cplx.get_color() if (color == None) else color
            self.__domains          = []
            self.__name_to_domain   = {}
            
        def __str__(self):
            lines=["subunit {0:s} colored {1:s}".format(self.__name,self.__color)]
            lines.extend( [str(d) for d in self.get_domains()] )
            return "\n".join(lines)

        def add_domain(self,domain_name,color=None):
            di=None
            try :
                di = self.__name_to_domain[domain_name]
                print "there is already a domain with such a name(",domain_name,") in subunit(",self.get_name(),")"
            except:
                di = ComplexColors.Domain(self,domain_name,color)
                self.__name_to_domain[domain_name]=di
                self.__domains.append( di )
            return di
        
        def get_name(self):
            return self.__name
        def get_domain(self,d_ref):
            """@param d_ref: a reference to a domain; might be a name or an int, in which case it should be a bead index between 0 and the number of domains in that subunit"""
            if isinstance(d_ref, basestring) :
                return self.__name_to_domain[d_ref]
            else :
                return self.__domains[d_ref]
        def get_domains(self):
            return self.__domains
        def get_domain_names(self):
            return self.__name_to_domain.keys()
        def get_complex(self):
            return self.__cplx
        def get_number_of_domains(self):
            return len(self.__domains)
        def get_color(self):
            return self.__color
        
        
    def __init__(self, name, version=None, color=_DEFAULT_COMPLEX_COLOR):
        self.__name     = name
        self.__version  = version
        self.__color    = color
        self.__subunits=[]
        self.__name_to_subunit={}
        
    def __str__(self):
        lines = ["COMPLEX COLOR {0:s} colored {1:s}".format(
                        self.__name +("" if (self.__version == None) else (" v"+str(self.__version) ) ),
                        str(self.__color)
                        )]
        lines.extend([str(s) for s in self.get_subunits()]) 
        return "\n".join(lines)
                
    def add_subunit(self,name,color=None):
        """ adds a subunit to the complex and returns that subunit
        """
        si=None
        try :
            si = self.__name_to_subunit[name]
            print "there is already a subunit named "+name+" in the complex"
        except :
            si = self.Subunit(self,name,color)
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
    
    def get_subunit(self,subunit_ref):
        """@param subunit_ref: a reference to a subunit; either a name or an integer index"""
        if isinstance(subunit_ref, basestring) :
            return self.__name_to_subunit[subunit_ref]
        else :
            return self.__subunits[subunit_ref]
        
    def get_subunits(self):
        return self.__subunits
        
    def get_color(self):
        return self.__color
    


def __test_color_loaders():
    cs_n = "green"
#    cs_n = "gray-60"
    cs_f = "0.0,.145,1.0"
    cs_c = "255,13,001"
    cs_h = "#ffa201"
    
    print "testing specialized loaders"
    print " "+str( Color.get_by_name(cs_n) ) 
    print " "+str( Color.get_from_floatString(cs_f) )
    print " "+str( Color.get_from_charString(cs_c) ) 
    print " "+str( Color.get_from_hexaString(cs_h) )
    
    for c in [cs_n,cs_f,cs_c,cs_h] :
        print str(c) , str(Color.get_from_string(c))
    
if __name__ == "__main__":
    __test_color_loaders()
