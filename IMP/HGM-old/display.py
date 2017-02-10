'''

'''

from colors_definitions import * 
import IMP
import IMP.display, IMP.core, IMP.atom


#
#    NEEDS : kaki, light_orange, light_green
#

#
#
#
#protein_color={}
##            CORE ------
#protein_color["p_8"]         = IMP.display.Color(162/255.0 ,205/255.0 , 90/255.0)    # DarkOliveGreen_3
#protein_color["p_52"]        = IMP.display.Color(112/255.0 ,219/255.0 ,147/255.0)    # Aquamarine
#protein_color["p_34"]        = IMP.display.Color(152/255.0 ,245/255.0 ,255/255.0)    # CadetBlue_1
#protein_color["p_44"]        = IMP.display.Color(  0/255.0 ,191/255.0 ,255/255.0)    # DeepSkyBlue
#protein_color["p_62"]        = IMP.display.Color(123/255.0 ,104/255.0 ,238/255.0)    # MediumSlateBlue
##            Glue ------
#protein_color["XPB"]        = IMP.display.Color(255/255.0,255/255.0,0)              # yellow_1
#protein_color["XPD"]        = IMP.display.Color(238/255.0,200/255.0,0)              # orange-yellow
##            CAK  ------
#protein_color["MAT_1"]       = IMP.display.Color(1.,1.,1.)                           # red 
#protein_color["CDK_7"]       = IMP.display.Color(255/255.0,0,255/255.0)              # fuchsia
#protein_color["CyclinH"]    = IMP.display.Color(238/255.0,106/255.0,80/255.0)       # coral_2

class ModelRenderer:
    """ 
    """
    
    def __init__(self,mi):
        """ 
        @param mi: a ModelInfo object"""
        self.__mi         = mi
        self.__colors_s   = {}   # subunit colors
        self.__colors_s_b = {}   # subunit beads colors
        
    def set_subunit_color(self,subunit_name,imp_color):
        """
        """
        if self.__mi.has_key(subunit_name) :
            self.__colors_s[subunit_name] = imp_color
            
    def set_subunit_colors(self,subunit_color_dict):
        """
        """
        for subunit_name,imp_color in subunit_color_dict.iteritems():
            self.set_subunit_color(subunit_name, imp_color)
        
#    def set_subunit_bead_color(self,subunit_name,bead_number,color):

    def __is_state_displayable(self):
        """
        mainly check if I have a color for each of my subunits
        """
        return (set(self.__colors_s.keys()) == set(self.__mi.keys()))

    def __init_pymol_display_rendering(self):
        """
        returns a list of hierarchy geometries corresponding to the actual state of the ModelRepresentation
        """
        geoms=[]
        for subunit_name,subunit_info in self.__mi.iteritems():
#            h                   = subunit_info.get_hierarchy()
            h                   = subunit_info.get_beads_hierarchy()
#            h                   = subunit_info.get_linkers_hierarchy()
            subunit_color       = self.__colors_s[subunit_name]
            try :
                geom                = IMP.atom.HierarchyGeometry(h)
            except :
                geom                = IMP.display.HierarchyGeometry(h)
            geom.set_color(subunit_color)
            geoms.append(geom)
        return geoms

    def __init_pymol_display_rendering_linkers(self):
        """
        returns a list of hierarchy geometries corresponding to the actual state of the ModelRepresentation
        """
        geoms=[]
        for subunit_name,subunit_info in self.__mi.iteritems():
            h                   = subunit_info.get_linkers_hierarchy()
            for hl in h.get_children() :
#            bpl = [ IMP.core.XYZR.decorate_particle(p) for p in subunit_info.get_particles() ]
#            lpl = [ IMP.core.XYZR.decorate_particle(p) for p in subunit_info.get_linker_particles() ]
                subunit_color       = self.__colors_s[subunit_name]
                subunit_color       = IMP.display.Color(subunit_color.get_red()/2.,subunit_color.get_green()/2.,subunit_color.get_blue()/2.)
#                subunit_color=IMP.display.Color(255/255.,248/255.,198/255.)
                geom                = IMP.display.HierarchyGeometry(h)
                geom.set_color(subunit_color)
                geoms.append(geom)
        return geoms
    
    def write_configuration_set_to_pymol_file(self,cs,fileName):
        """
        @param cs: a ConfigurationSet or MyConfigurationDet object
        @param fileName: guess what...
        """
        # for each of the configuration, dump it to a file to view in pymol
        gs = self.__init_pymol_display_rendering()
        gs.extend(self.__init_pymol_display_rendering_linkers())
        w= IMP.display.PymolWriter(fileName)
#        w= IMP.display.ChimeraWriter(fileName+"%1%.py")
        for i in range(0, cs.get_number_of_configurations()):
            cs.load_configuration(i)
            w.set_frame(i)
            for g in gs:
                w.add_geometry(g)
        del w
#        w.do_close()
        

class PredifinedColors(dict):
    def __init__(self) :
        
        self["black"]                    = [0,0,0]
        self["gray_0"]                   = [21,5,23]
        self["gray_18"]                  = [37,5,23]
        self["gray_21"]                  = [43,27,23]
        self["gray_23"]                  = [48,34,23]
        self["gray_24"]                  = [48,34,38]
        self["gray_25"]                  = [52,40,38]
        self["gray_26"]                  = [52,40,44]
        self["gray_27"]                  = [56,45,44]
        self["gray_28"]                  = [59,49,49]
        self["gray_29"]                  = [62,53,53]
        self["gray_30"]                  = [65,56,57]
        self["gray_31"]                  = [65,56,60]
        self["gray_32"]                  = [70,62,63]
        self["gray_34"]                  = [74,67,68]
        self["gray_35"]                  = [76,70,70]
        self["gray_36"]                  = [78,72,72]
        self["gray_37"]                  = [80,74,75]
        self["gray_38"]                  = [84,78,79]
        self["gray_39"]                  = [86,80,81]
        self["gray_40"]                  = [89,84,84]
        self["gray_41"]                  = [92,88,88]
        self["gray_42"]                  = [95,90,89]
        self["gray_43"]                  = [98,93,93]
        self["gray_44"]                  = [100,96,96]
        self["gray_45"]                  = [102,99,98]
        self["gray_46"]                  = [105,101,101]
        self["gray_47"]                  = [109,105,104]
        self["gray_48"]                  = [110,106,107]
        self["gray_49"]                  = [114,110,109]
        self["gray_50"]                  = [116,113,112]
        self["gray"]                     = [115,111,110]
        self["white"]                    = [255,255,255]
        self["blue"]                     = [0,0,255]
        self["slate_gray_4"]             = [97,109,126]
        self["slate_gray"]               = [101,115,131]
        self["light_steel_blue_4"]       = [100,109,126]
        self["light_slate_gray"]         = [109,123,141]
        self["cadet_blue"]               = [95,158,160]
        self["cadet_blue_1"]             = [152,245,255]
        self["cadet_blue_2"]             = [142,229,238]
        self["cadet_blue_3"]             = [119,191,199]
        self["cadet_blue_4"]             = [76,120,126]
        self["dark_slate_gray_4"]        = [76,125,126]
        self["thistle_4"]                = [128,109,126]
        self["medium_slate_blue"]        = [94,90,128]
        self["medium_purple_4"]          = [78,56,126]
        self["midnight_blue"]            = [21,27,84]
        self["dark_slate_blue"]          = [43,56,86]
        self["dark_slate_gray"]          = [37,56,60]
        self["dim_gray"]                 = [70,62,65]
        self["cornflower_blue"]          = [21,27,141]
        self["royal_blue_4"]             = [21,49,126]
        self["slate_blue_4"]             = [52,45,126]
        self["royal_blue"]               = [43,96,222]
        self["royal_blue_1"]             = [48,110,255]
        self["royal_blue_2"]             = [43,101,236]
        self["royal_blue_3"]             = [37,84,199]
        self["deep_sky_blue"]            = [59,185,255]
        self["deep_sky_blue_2"]          = [56,172,236]
        self["slate_blue"]               = [53,126,199]
        self["deep_sky_blue_3"]          = [48,144,199]
        self["deep_sky_blue_4"]          = [37,88,126]
        self["dodger_blue"]              = [21,137,255]
        self["dodger_blue_2"]            = [21,125,236]
        self["dodger_blue_3"]            = [21,105,199]
        self["dodger_blue_4"]            = [21,62,126]
        self["steel_blue_4"]             = [43,84,126]
        self["steel_blue"]               = [72,99,160]
        self["slate_blue_2"]             = [105,96,236]
        self["violet"]                   = [141,56,201]
        self["medium_purple_3"]          = [122,93,199]
        self["medium_purple"]            = [132,103,215]
        self["medium_purple_2"]          = [145,114,236]
        self["medium_purple_1"]          = [158,123,255]
        self["light_steel_blue"]        = [114,143,206]
        self["steel_blue_3"]             = [72,138,199]
        self["steel_blue_2"]             = [86,165,236]
        self["steel_blue_1"]             = [92,179,255]
        self["sky_blue_3"]               = [101,158,199]
        self["sky_blue_4"]               = [65,98,126]
        self["slate_blue"]              = [115,124,161]
        self["slate_blue"]              = [115,124,161]
        self["slate_gray_3"]             = [152,175,199]
        self["violet_red"]              = [246,53,138]
        self["violet_red_1"]             = [246,53,138]
        self["violet_red_2"]             = [228,49,127]
        self["deep_pink"]               = [245,40,135]
        self["deep_pink_2"]              = [228,40,124]
        self["deep_pink_3"]              = [193,34,103]
        self["deep_pink_4"]              = [125,5,63]
        self["medium_violet_red"]       = [202,34,107]
        self["violet_red_3"]             = [193,40,105]
        self["firebrick"]               = [128,5,23]
        self["violet_red_4"]             = [125,5,65]
        self["maroon_4"]                 = [125,5,82]
        self["maroon"]                  = [129,5,65]
        self["maroon_3"]                 = [193,34,131]
        self["maroon_2"]                 = [227,49,157]
        self["maroon_1"]                 = [245,53,170]
        self["magenta"]                 = [255,0,255]
        self["magenta_1"]                = [244,51,255]
        self["magenta_2"]                = [226,56,236]
        self["magenta_3"]                = [192,49,199]
        self["medium_orchid"]           = [176,72,181]
        self["medium_orchid_1"]          = [212,98,255]
        self["medium_orchid_2"]          = [196,90,236]
        self["medium_orchid_3"]          = [167,74,199]
        self["medium_orchid_4"]          = [106,40,126]
        self["purple"]                  = [142,53,239]
        self["purple_1"]                 = [137,59,255]
        self["purple_2"]                 = [127,56,236]
        self["purple_3"]                 = [108,45,199]
        self["purple_4"]                 = [70,27,126]
        self["dark_orchid_4"]            = [87,27,126]
        self["dark_orchid"]             = [125,27,126]
        self["dark_violet"]             = [132,45,206]
        self["dark_orchid_3"]            = [139,49,199]
        self["dark_orchid_2"]            = [162,59,236]
        self["dark_orchid_1"]            = [176,65,255]
        self["plum_4"]                   = [126,88,126]
        self["pale_violet_red"]         = [209,101,135]
        self["pale_violet_red_1"]        = [247,120,161]
        self["pale_violet_red_2"]        = [229,110,148]
        self["pale_violet_red_3"]        = [194,90,124]
        self["pale_violet_red_4"]        = [126,53,77]
        self["plum"]                    = [185,59,143]
        self["plum_1"]                   = [249,183,255]
        self["plum_2"]                   = [230,169,236]
        self["plum_3"]                   = [195,142,199]
        self["thistle"]                 = [210,185,211]
        self["thistle_3"]                = [198,174,199]
        self["lavender_blush_2"]         = [235,221,226]
        self["lavender_blush_3"]         = [200,187,190]
        self["thistle_2"]                = [233,207,236]
        self["thistle_1"]                = [252,223,255]
        self["lavender"]                = [227,228,250]
        self["lavender_blush"]          = [253,238,244]
        self["light_steel_blue_1"]       = [198,222,255]
        self["light_blue"]              = [173,223,255]
        self["light_blue_1"]             = [189,237,255]
        self["light_cyan"]              = [224,255,255]
        self["slate_gray_1"]             = [194,223,255]
        self["slate_gray_2"]             = [180,207,236]
        self["light_steel_blue_2"]       = [183,206,236]
        self["turquoise_1"]              = [82,243,255]
        self["cyan"]                    = [0,255,255]
        self["cyan_1"]                   = [87,254,255]
        self["cyan_2"]                   = [80,235,236]
        self["turquoise_2"]              = [78,226,236]
        self["medium_turquoise"]        = [72,204,205]
        self["turquoise"]               = [67,198,219]
        self["dark_slate_gray_1"]        = [154,254,255]
        self["dark_slate_gray_2"]        = [142,235,236]
        self["dark_slate_gray_3"]        = [120,199,199]
        self["cyan_3"]                   = [70,199,199]
        self["turquoise_3"]              = [67,191,199]
        self["pale_turquoise_3"]         = [146,199,199]
        self["light_blue_2"]             = [175,220,236]
        self["dark_turquoise"]          = [59,156,156]
        self["cyan_4"]                   = [48,125,126]
        self["light_sea_green"]         = [62,169,159]
        self["light_sky_blue"]          = [130,202,250]
        self["light_sky_blue_2"]         = [160,207,236]
        self["light_sky_blue_3"]         = [135,175,199]
        self["sky_blue"]                = [130,202,255]
        self["sky_blue_2"]               = [121,186,236]
        self["light_sky_blue_4"]         = [86,109,126]
        self["sky_blue"]                = [102,152,255]
        self["light_slate_blue"]        = [115,106,255]
        self["light_cyan_2"]             = [207,236,236]
        self["light_cyan_3"]             = [175,199,199]
        self["light_cyan_4"]             = [113,125,125]
        self["light_blue_3"]             = [149,185,199]
        self["light_blue_4"]             = [94,118,126]
        self["pale_turquoise_4"]         = [94,125,126]
        self["dark_sea_green_4"]         = [97,124,88]
        self["medium_aquamarine"]       = [52,135,129]
        self["medium_sea_green"]        = [48,103,84]
        self["sea_green"]               = [78,137,117]
        self["dark_green"]              = [37,65,23]
        self["sea_green_4"]              = [56,124,68]
        self["forest_green"]            = [78,146,88]
        self["medium_forest_green"]     = [52,114,53]
        self["spring_green_4"]           = [52,124,44]
        self["dark_olive_green_4"]       = [102,124,38]
        self["chartreuse_4"]             = [67,124,23]
        self["green_4"]                  = [52,124,23]
        self["medium_spring_green"]     = [52,128,23]
        self["spring_green"]            = [74,160,44]
        self["lime_green"]              = [65,163,23]
        self["spring_green"]            = [74,160,44]
        self["dark_sea_green"]          = [139,179,129]
        self["dark_sea_green_3"]         = [153,198,142]
        self["green_3"]                  = [76,196,23]
        self["chartreuse_3"]             = [108,196,23]
        self["yellow_green"]            = [82,208,23]
        self["spring_green_3"]           = [76,197,82]
        self["sea_green_3"]              = [84,197,113]
        self["spring_green_2"]           = [87,233,100]
        self["spring_green_1"]           = [94,251,110]
        self["sea_green_2"]              = [100,233,134]
        self["sea_green_1"]              = [106,251,146]
        self["dark_sea_green_2"]         = [181,234,170]
        self["dark_sea_green_1"]         = [195,253,184]
        self["green"]                   = [0,255,0]
        self["lawn_green"]              = [135,247,23]
        self["green_1"]                  = [95,251,23]
        self["green_2"]                  = [89,232,23]
        self["chartreuse_2"]             = [127,232,23]
        self["chartreuse"]              = [138,251,23]
        self["green_yellow"]            = [177,251,23]
        self["dark_olive_green_1"]       = [204,251,93]
        self["dark_olive_green_2"]       = [188,233,84]
        self["dark_olive_green_3"]       = [160,197,68]
        self["yellow"]                  = [255,255,0]
        self["yellow_1"]                 = [255,252,23]
        self["khaki_1"]                  = [255,243,128]
        self["khaki_2"]                  = [237,226,117]
        self["goldenrod"]               = [237,218,116]
        self["gold_2"]                   = [234,193,23]
        self["gold_1"]                   = [253,208,23]
        self["goldenrod_1"]              = [251,185,23]
        self["goldenrod_2"]              = [233,171,23]
        self["gold"]                     = [212,160,23]
        self["gold_3"]                   = [199,163,23]
        self["goldenrod_3"]              = [198,142,23]
        self["khaki"]                    = [173,169,110]
        self["khaki_3"]                  = [201,190,98]
        self["khaki_4"]                  = [130,120,57]
        self["dark_goldenrod"]           = [175,120,23]
        self["dark_goldenrod_1"]         = [251,177,23]
        self["dark_goldenrod_2"]         = [232,163,23]
        self["dark_goldenrod_3"]         = [197,137,23]
        self["sienna_1"]                 = [248,116,49]
        self["sienna_2"]                 = [230,108,44]
        self["orange"]                   = [255,165,0]        
        self["orange_1"]                 = [255,165,0]
        self["orange_2"]                 = [238,154,0]
        self["orange_3"]                 = [205,133,0]
        self["orange_4"]                 = [139,90,0]
        self["dark_orange"]              = [248,128,23]
        self["dark_orange_1"]            = [248,114,23]
        self["dark_orange_2"]            = [229,103,23]
        self["dark_orange_3"]            = [195,86,23]
        self["dark_orange_4"]            = [126,49,23]
        self["cadmium_orange"]           = [255,97,3]
        self["orange_red"]               = [255,69,0]
        self["orange_red_1"]             = [255,69,0]
        self["orange_red_2"]             = [238,64,0]
        self["orange_red_3"]             = [205,55,0]
        self["orange_red_4"]             = [139,37,0]       
        self["sienna_3"]                 = [195,88,23]
        self["sienna"]                   = [138,65,23]
        self["sienna_4"]                 = [126,53,23]
        self["indian_red_4"]             = [126,34,23]
        self["salmon_4"]                 = [126,56,23]
        self["dark_goldenrod_4"]         = [127,82,23]
        self["gold_4"]                   = [128,101,23]
        self["goldenrod_4"]              = [128,88,23]
        self["light_salmon_4"]           = [127,70,44]
        self["chocolate"]                = [200,90,23]
        self["coral_3"]                  = [195,74,44]
        self["coral_2"]                  = [229,91,60]
        self["coral"]                    = [247,101,65]
        self["dark_salmon"]              = [225,139,107]
        self["salmon_1"]                 = [248,129,88]
        self["salmon_2"]                 = [230,116,81]
        self["salmon_3"]                 = [195,98,65]
        self["light_salmon_3"]           = [196,116,81]
        self["light_salmon_2"]           = [231,138,97]
        self["light_salmon"]            = [249,150,107]
        self["sandy_brown"]             = [238,154,77]
        self["hot_pink"]                = [246,96,171]
        self["hot_pink_1"]               = [246,101,171]
        self["hot_pink_2"]               = [228,94,157]
        self["hot_pink_3"]               = [194,82,131]
        self["hot_pink_4"]               = [125,34,82]
        self["light_coral"]             = [231,116,113]
        self["indian_red_1"]             = [247,93,89]
        self["indian_red_2"]             = [229,84,81]
        self["indian_red_3"]             = [194,70,65]
        self["red"]                     = [255,0,0]
        self["red_1"]                    = [246,34,23]
        self["red_2"]                    = [228,27,23]
        self["firebrick_1"]              = [246,40,23]
        self["firebrick_2"]              = [228,34,23]
        self["firebrick_3"]              = [193,27,23]
        self["pink"]                    = [250,175,190]
        self["rosy_brown_1"]             = [251,187,185]
        self["rosy_brown_2"]             = [232,173,170]
        self["pink_2"]                   = [231,161,176]
        self["light_pink"]               = [250,175,186]
        self["light_pink_1"]             = [249,167,176]
        self["light_pink_2"]             = [231,153,163]
        self["pink_3"]                   = [196,135,147]
        self["rosy_brown_3"]             = [197,144,142]
        self["rosy_brown"]               = [179,132,129]
        self["light_pink_3"]             = [196,129,137]
        self["rosy_brown_4"]             = [127,90,88]
        self["light_pink_4"]             = [127,78,82]
        self["pink_4"]                   = [127,82,93]
        self["lavender_blush_4"]         = [129,118,121]
        self["light_goldenrod_4"]        = [129,115,57]
        self["lemon_chiffon_4"]          = [130,123,96]
        self["lemon_chiffon_3"]          = [201,194,153]
        self["light_goldenrod_3"]        = [200,181,96]
        self["light_golden_2"]           = [236,214,114]
        self["light_goldenrod"]          = [236,216,114]
        self["light_goldenrod_1"]        = [255,232,124]
        self["lemon_chiffon_2"]          = [236,229,182]
        self["lemon_chiffon"]            = [255,248,198]
        self["light_goldenrod_yellow"]   = [250,248,204]
        self["fuchsia"]                  = [255,0,255]
        self["aquamarine"]               = [127,255,212]
        self["aquamarine_1"]             = [127,255,212]
        self["aquamarine_2"]             = [118,238,198]
        self["aquamarine_3"]             = [102,205,170]
        self["aquamarine_4"]             = [69,139,116]
        
        
        
        
    def get_color_names(self):
        """ returns the name of all registered colors
        """
        return self.keys()

    def get_color_by_name(self,color_name):
        """
        @param : color_name
        """
        return self[color_name]
    
    def insert_color(self,color_name,rgb_triplet):
        """ insert a novel named color in the present dictionnary
        """
        self[color_name] = rgb_triplet
        return self[color_name]
        
#    def get_color_by_channels(self,r,g,b):
#        """ returns the IMP color corresponding to the provided r g b channels
#        @param r: red (int in [0-255])
#        @param g: green (int in [0-255])
#        @param b: blue (int in [0-255])
#        """
#        return IMP.display.Color(r/255.,g/255.,b/255.)
    
def get_IMP_color(r,g,b):
    """ returns the IMP color corresponding to the provided r g b channels
    @param r: red (int in [0-255])
    @param g: green (int in [0-255])
    @param b: blue (int in [0-255])
    """
    return IMP.display.Color(r/255.,g/255.,b/255.)

#        
#
#def init_display_rendering(h):
#    gs=[]
#    for i in range(h.get_number_of_children()):
##        color= IMP.display.get_display_color(i)
#        n= h.get_child(i)
#        name= n.get_name()
#        color = protein_color[name]
#        g= IMP.display.HierarchyGeometry(n)
#        g.set_color(color)
#        gs.append(g)
#    return gs
#
#def init_display_rendering_detailed(h):
#    gs=[]
#    for i in range(h.get_number_of_children()):
##        color= IMP.display.get_display_color(i)
#        n= h.get_child(i)
#        name= n.get_name()
#        color = protein_color[name]
#        balls = []
#        nb_beads = n.get_number_of_children()
#        for bi in range(nb_beads) :        
#            g= IMP.display.HierarchyGeometry( n.get_child(bi) )
#            coef = 1. - (.5*bi/nb_beads)
#            bcolor = IMP.display.Color(
#                                       coef * color.get_red(),
#                                       coef * color.get_green(),
#                                       coef * color.get_blue(), 
#                                       )
#            g.set_color(bcolor)
#            gs.append(g)
#    return gs

#def get_conformations_aligned_on_selection(cs,selection):
#    acs = IMP.ConfigurationSet(cs.get_model(),"aligned configurations")
#    particles = selection.get_selected_particles()
#    return acs

#def dump_to_pymol_file(cs,gs,fileName):
#    # for each of the configuration, dump it to a file to view in pymol
#    w= IMP.display.PymolWriter(fileName)
#    for i in range(0, cs.get_number_of_configurations()):
#        cs.load_configuration(i)
#        w.set_frame(i)
#        for g in gs:
#            w.add_geometry(g)
#    w.do_close()
