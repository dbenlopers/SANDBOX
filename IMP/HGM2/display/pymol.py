'''

'''


import colors

def get_pymol_color_channels( ben_color ):
    """ returns the three rgb channels in [0,1] """
    return map( lambda x: x/255. , ben_color.get_channels() )

def get_pymol_color_CGO_string( ben_color ):
    """ returns the three rgb channels in [0,1] """
    return "COLOR, {0:f}, {1:f}, {2:f},".format(  *get_pymol_color_channels( ben_color )  )
