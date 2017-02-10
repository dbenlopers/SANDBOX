'''

'''
import IMP, IMP.display

class ImpPredifinedColors(dict):
    def __init__(self) :
        self["black"]                   = IMP.display.Color(0/255.,0/255.,0/255.)
        self["gray0"]                   = IMP.display.Color(21/255.,5/255.,23/255.)
        self["gray18"]                  = IMP.display.Color(37/255.,5/255.,23/255.)
        self["gray21"]                  = IMP.display.Color(43/255.,27/255.,23/255.)
        self["gray23"]                  = IMP.display.Color(48/255.,34/255.,23/255.)
        self["gray24"]                  = IMP.display.Color(48/255.,34/255.,38/255.)
        self["gray25"]                  = IMP.display.Color(52/255.,40/255.,38/255.)
        self["gray26"]                  = IMP.display.Color(52/255.,40/255.,44/255.)
        self["gray27"]                  = IMP.display.Color(56/255.,45/255.,44/255.)
        self["gray28"]                  = IMP.display.Color(59/255.,49/255.,49/255.)
        self["gray29"]                  = IMP.display.Color(62/255.,53/255.,53/255.)
        self["gray30"]                  = IMP.display.Color(65/255.,56/255.,57/255.)
        self["gray31"]                  = IMP.display.Color(65/255.,56/255.,60/255.)
        self["gray32"]                  = IMP.display.Color(70/255.,62/255.,63/255.)
        self["gray34"]                  = IMP.display.Color(74/255.,67/255.,68/255.)
        self["gray35"]                  = IMP.display.Color(76/255.,70/255.,70/255.)
        self["gray36"]                  = IMP.display.Color(78/255.,72/255.,72/255.)
        self["gray37"]                  = IMP.display.Color(80/255.,74/255.,75/255.)
        self["gray38"]                  = IMP.display.Color(84/255.,78/255.,79/255.)
        self["gray39"]                  = IMP.display.Color(86/255.,80/255.,81/255.)
        self["gray40"]                  = IMP.display.Color(89/255.,84/255.,84/255.)
        self["gray41"]                  = IMP.display.Color(92/255.,88/255.,88/255.)
        self["gray42"]                  = IMP.display.Color(95/255.,90/255.,89/255.)
        self["gray43"]                  = IMP.display.Color(98/255.,93/255.,93/255.)
        self["gray44"]                  = IMP.display.Color(100/255.,96/255.,96/255.)
        self["gray45"]                  = IMP.display.Color(102/255.,99/255.,98/255.)
        self["gray46"]                  = IMP.display.Color(105/255.,101/255.,101/255.)
        self["gray47"]                  = IMP.display.Color(109/255.,105/255.,104/255.)
        self["gray48"]                  = IMP.display.Color(110/255.,106/255.,107/255.)
        self["gray49"]                  = IMP.display.Color(114/255.,110/255.,109/255.)
        self["gray50"]                  = IMP.display.Color(116/255.,113/255.,112/255.)
        self["gray"]                    = IMP.display.Color(115/255.,111/255.,110/255.)
        self["slate_gray4"]             = IMP.display.Color(97/255.,109/255.,126/255.)
        self["slate_gray"]              = IMP.display.Color(101/255.,115/255.,131/255.)
        self["light_steel_blue4"]       = IMP.display.Color(100/255.,109/255.,126/255.)
        self["light_slate_gray"]        = IMP.display.Color(109/255.,123/255.,141/255.)
        self["cadet_blue4"]             = IMP.display.Color(76/255.,120/255.,126/255.)
        self["dark_slate_gray4"]        = IMP.display.Color(76/255.,125/255.,126/255.)
        self["thistle4"]                = IMP.display.Color(128/255.,109/255.,126/255.)
        self["medium_slate_blue"]       = IMP.display.Color(94/255.,90/255.,128/255.)
        self["medium_purple4"]          = IMP.display.Color(78/255.,56/255.,126/255.)
        self["midnight_blue"]           = IMP.display.Color(21/255.,27/255.,84/255.)
        self["dark_slate_blue"]         = IMP.display.Color(43/255.,56/255.,86/255.)
        self["dark_slate_gray"]         = IMP.display.Color(37/255.,56/255.,60/255.)
        self["dim_gray"]                = IMP.display.Color(70/255.,62/255.,65/255.)
        self["cornflower_blue"]         = IMP.display.Color(21/255.,27/255.,141/255.)
        self["royal_blue4"]             = IMP.display.Color(21/255.,49/255.,126/255.)
        self["slate_blue4"]             = IMP.display.Color(52/255.,45/255.,126/255.)
        self["royal_blue"]              = IMP.display.Color(43/255.,96/255.,222/255.)
        self["royal_blue1"]             = IMP.display.Color(48/255.,110/255.,255/255.)
        self["royal_blue2"]             = IMP.display.Color(43/255.,101/255.,236/255.)
        self["royal_blue3"]             = IMP.display.Color(37/255.,84/255.,199/255.)
        self["deep_sky_blue"]           = IMP.display.Color(59/255.,185/255.,255/255.)
        self["deep_sky_blue2"]          = IMP.display.Color(56/255.,172/255.,236/255.)
        self["slate_blue"]              = IMP.display.Color(53/255.,126/255.,199/255.)
        self["deep_sky_blue3"]          = IMP.display.Color(48/255.,144/255.,199/255.)
        self["deep_sky_blue4"]          = IMP.display.Color(37/255.,88/255.,126/255.)
        self["dodger_blue"]             = IMP.display.Color(21/255.,137/255.,255/255.)
        self["dodger_blue2"]            = IMP.display.Color(21/255.,125/255.,236/255.)
        self["dodger_blue3"]            = IMP.display.Color(21/255.,105/255.,199/255.)
        self["dodger_blue4"]            = IMP.display.Color(21/255.,62/255.,126/255.)
        self["steel_blue4"]             = IMP.display.Color(43/255.,84/255.,126/255.)
        self["steel_blue"]              = IMP.display.Color(72/255.,99/255.,160/255.)
        self["slate_blue2"]             = IMP.display.Color(105/255.,96/255.,236/255.)
        self["violet"]                  = IMP.display.Color(141/255.,56/255.,201/255.)
        self["medium_purple3"]          = IMP.display.Color(122/255.,93/255.,199/255.)
        self["medium_purple"]           = IMP.display.Color(132/255.,103/255.,215/255.)
        self["medium_purple2"]          = IMP.display.Color(145/255.,114/255.,236/255.)
        self["medium_purple1"]          = IMP.display.Color(158/255.,123/255.,255/255.)
        self["light_steel_blue"]        = IMP.display.Color(114/255.,143/255.,206/255.)
        self["steel_blue3"]             = IMP.display.Color(72/255.,138/255.,199/255.)
        self["steel_blue2"]             = IMP.display.Color(86/255.,165/255.,236/255.)
        self["steel_blue1"]             = IMP.display.Color(92/255.,179/255.,255/255.)
        self["sky_blue3"]               = IMP.display.Color(101/255.,158/255.,199/255.)
        self["sky_blue4"]               = IMP.display.Color(65/255.,98/255.,126/255.)
        self["slate_blue"]              = IMP.display.Color(115/255.,124/255.,161/255.)
        self["slate_blue"]              = IMP.display.Color(115/255.,124/255.,161/255.)
        self["slate_gray3"]             = IMP.display.Color(152/255.,175/255.,199/255.)
        self["violet_red"]              = IMP.display.Color(246/255.,53/255.,138/255.)
        self["violet_red1"]             = IMP.display.Color(246/255.,53/255.,138/255.)
        self["violet_red2"]             = IMP.display.Color(228/255.,49/255.,127/255.)
        self["deep_pink"]               = IMP.display.Color(245/255.,40/255.,135/255.)
        self["deep_pink2"]              = IMP.display.Color(228/255.,40/255.,124/255.)
        self["deep_pink3"]              = IMP.display.Color(193/255.,34/255.,103/255.)
        self["deep_pink4"]              = IMP.display.Color(125/255.,5/255.,63/255.)
        self["medium_violet_red"]       = IMP.display.Color(202/255.,34/255.,107/255.)
        self["violet_red3"]             = IMP.display.Color(193/255.,40/255.,105/255.)
        self["firebrick"]               = IMP.display.Color(128/255.,5/255.,23/255.)
        self["violet_red4"]             = IMP.display.Color(125/255.,5/255.,65/255.)
        self["maroon4"]                 = IMP.display.Color(125/255.,5/255.,82/255.)
        self["maroon"]                  = IMP.display.Color(129/255.,5/255.,65/255.)
        self["maroon3"]                 = IMP.display.Color(193/255.,34/255.,131/255.)
        self["maroon2"]                 = IMP.display.Color(227/255.,49/255.,157/255.)
        self["maroon1"]                 = IMP.display.Color(245/255.,53/255.,170/255.)
        self["magenta"]                 = IMP.display.Color(255/255.,0/255.,255/255.)
        self["magenta1"]                = IMP.display.Color(244/255.,51/255.,255/255.)
        self["magenta2"]                = IMP.display.Color(226/255.,56/255.,236/255.)
        self["magenta3"]                = IMP.display.Color(192/255.,49/255.,199/255.)
        self["medium_orchid"]           = IMP.display.Color(176/255.,72/255.,181/255.)
        self["medium_orchid1"]          = IMP.display.Color(212/255.,98/255.,255/255.)
        self["medium_orchid2"]          = IMP.display.Color(196/255.,90/255.,236/255.)
        self["medium_orchid3"]          = IMP.display.Color(167/255.,74/255.,199/255.)
        self["medium_orchid4"]          = IMP.display.Color(106/255.,40/255.,126/255.)
        self["purple"]                  = IMP.display.Color(142/255.,53/255.,239/255.)
        self["purple1"]                 = IMP.display.Color(137/255.,59/255.,255/255.)
        self["purple2"]                 = IMP.display.Color(127/255.,56/255.,236/255.)
        self["purple3"]                 = IMP.display.Color(108/255.,45/255.,199/255.)
        self["purple4"]                 = IMP.display.Color(70/255.,27/255.,126/255.)
        self["dark_orchid4"]            = IMP.display.Color(87/255.,27/255.,126/255.)
        self["dark_orchid"]             = IMP.display.Color(125/255.,27/255.,126/255.)
        self["dark_violet"]             = IMP.display.Color(132/255.,45/255.,206/255.)
        self["dark_orchid3"]            = IMP.display.Color(139/255.,49/255.,199/255.)
        self["dark_orchid2"]            = IMP.display.Color(162/255.,59/255.,236/255.)
        self["dark_orchid1"]            = IMP.display.Color(176/255.,65/255.,255/255.)
        self["plum4"]                   = IMP.display.Color(126/255.,88/255.,126/255.)
        self["pale_violet_red"]         = IMP.display.Color(209/255.,101/255.,135/255.)
        self["pale_violet_red1"]        = IMP.display.Color(247/255.,120/255.,161/255.)
        self["pale_violet_red2"]        = IMP.display.Color(229/255.,110/255.,148/255.)
        self["pale_violet_red3"]        = IMP.display.Color(194/255.,90/255.,124/255.)
        self["pale_violet_red4"]        = IMP.display.Color(126/255.,53/255.,77/255.)
        self["plum"]                    = IMP.display.Color(185/255.,59/255.,143/255.)
        self["plum1"]                   = IMP.display.Color(249/255.,183/255.,255/255.)
        self["plum2"]                   = IMP.display.Color(230/255.,169/255.,236/255.)
        self["plum3"]                   = IMP.display.Color(195/255.,142/255.,199/255.)
        self["thistle"]                 = IMP.display.Color(210/255.,185/255.,211/255.)
        self["thistle3"]                = IMP.display.Color(198/255.,174/255.,199/255.)
        self["lavender_blush2"]         = IMP.display.Color(235/255.,221/255.,226/255.)
        self["lavender_blush3"]         = IMP.display.Color(200/255.,187/255.,190/255.)
        self["thistle2"]                = IMP.display.Color(233/255.,207/255.,236/255.)
        self["thistle1"]                = IMP.display.Color(252/255.,223/255.,255/255.)
        self["lavender"]                = IMP.display.Color(227/255.,228/255.,250/255.)
        self["lavender_blush"]          = IMP.display.Color(253/255.,238/255.,244/255.)
        self["light_steel_blue1"]       = IMP.display.Color(198/255.,222/255.,255/255.)
        self["light_blue"]              = IMP.display.Color(173/255.,223/255.,255/255.)
        self["light_blue1"]             = IMP.display.Color(189/255.,237/255.,255/255.)
        self["light_cyan"]              = IMP.display.Color(224/255.,255/255.,255/255.)
        self["slate_gray1"]             = IMP.display.Color(194/255.,223/255.,255/255.)
        self["slate_gray2"]             = IMP.display.Color(180/255.,207/255.,236/255.)
        self["light_steel_blue2"]       = IMP.display.Color(183/255.,206/255.,236/255.)
        self["turquoise1"]              = IMP.display.Color(82/255.,243/255.,255/255.)
        self["cyan"]                    = IMP.display.Color(0/255.,255/255.,255/255.)
        self["cyan1"]                   = IMP.display.Color(87/255.,254/255.,255/255.)
        self["cyan2"]                   = IMP.display.Color(80/255.,235/255.,236/255.)
        self["turquoise2"]              = IMP.display.Color(78/255.,226/255.,236/255.)
        self["medium_turquoise"]        = IMP.display.Color(72/255.,204/255.,205/255.)
        self["turquoise"]               = IMP.display.Color(67/255.,198/255.,219/255.)
        self["dark_slate_gray1"]        = IMP.display.Color(154/255.,254/255.,255/255.)
        self["dark_slate_gray2"]        = IMP.display.Color(142/255.,235/255.,236/255.)
        self["dark_slate_gray3"]        = IMP.display.Color(120/255.,199/255.,199/255.)
        self["cyan3"]                   = IMP.display.Color(70/255.,199/255.,199/255.)
        self["turquoise3"]              = IMP.display.Color(67/255.,191/255.,199/255.)
        self["cadet_blue3"]             = IMP.display.Color(119/255.,191/255.,199/255.)
        self["pale_turquoise3"]         = IMP.display.Color(146/255.,199/255.,199/255.)
        self["light_blue2"]             = IMP.display.Color(175/255.,220/255.,236/255.)
        self["dark_turquoise"]          = IMP.display.Color(59/255.,156/255.,156/255.)
        self["cyan4"]                   = IMP.display.Color(48/255.,125/255.,126/255.)
        self["light_sea_green"]         = IMP.display.Color(62/255.,169/255.,159/255.)
        self["light_sky_blue"]          = IMP.display.Color(130/255.,202/255.,250/255.)
        self["light_sky_blue2"]         = IMP.display.Color(160/255.,207/255.,236/255.)
        self["light_sky_blue3"]         = IMP.display.Color(135/255.,175/255.,199/255.)
        self["sky_blue"]                = IMP.display.Color(130/255.,202/255.,255/255.)
        self["sky_blue2"]               = IMP.display.Color(121/255.,186/255.,236/255.)
        self["light_sky_blue4"]         = IMP.display.Color(86/255.,109/255.,126/255.)
        self["sky_blue"]                = IMP.display.Color(102/255.,152/255.,255/255.)
        self["light_slate_blue"]        = IMP.display.Color(115/255.,106/255.,255/255.)
        self["light_cyan2"]             = IMP.display.Color(207/255.,236/255.,236/255.)
        self["light_cyan3"]             = IMP.display.Color(175/255.,199/255.,199/255.)
        self["light_cyan4"]             = IMP.display.Color(113/255.,125/255.,125/255.)
        self["light_blue3"]             = IMP.display.Color(149/255.,185/255.,199/255.)
        self["light_blue4"]             = IMP.display.Color(94/255.,118/255.,126/255.)
        self["pale_turquoise4"]         = IMP.display.Color(94/255.,125/255.,126/255.)
        self["dark_sea_green4"]         = IMP.display.Color(97/255.,124/255.,88/255.)
        self["medium_aquamarine"]       = IMP.display.Color(52/255.,135/255.,129/255.)
        self["medium_sea_green"]        = IMP.display.Color(48/255.,103/255.,84/255.)
        self["sea_green"]               = IMP.display.Color(78/255.,137/255.,117/255.)
        self["dark_green"]              = IMP.display.Color(37/255.,65/255.,23/255.)
        self["sea_green4"]              = IMP.display.Color(56/255.,124/255.,68/255.)
        self["forest_green"]            = IMP.display.Color(78/255.,146/255.,88/255.)
        self["medium_forest_green"]     = IMP.display.Color(52/255.,114/255.,53/255.)
        self["spring_green4"]           = IMP.display.Color(52/255.,124/255.,44/255.)
        self["dark_olive_green4"]       = IMP.display.Color(102/255.,124/255.,38/255.)
        self["chartreuse4"]             = IMP.display.Color(67/255.,124/255.,23/255.)
        self["green4"]                  = IMP.display.Color(52/255.,124/255.,23/255.)
        self["medium_spring_green"]     = IMP.display.Color(52/255.,128/255.,23/255.)
        self["spring_green"]            = IMP.display.Color(74/255.,160/255.,44/255.)
        self["lime_green"]              = IMP.display.Color(65/255.,163/255.,23/255.)
        self["spring_green"]            = IMP.display.Color(74/255.,160/255.,44/255.)
        self["dark_sea_green"]          = IMP.display.Color(139/255.,179/255.,129/255.)
        self["dark_sea_green3"]         = IMP.display.Color(153/255.,198/255.,142/255.)
        self["green3"]                  = IMP.display.Color(76/255.,196/255.,23/255.)
        self["chartreuse3"]             = IMP.display.Color(108/255.,196/255.,23/255.)
        self["yellow_green"]            = IMP.display.Color(82/255.,208/255.,23/255.)
        self["spring_green3"]           = IMP.display.Color(76/255.,197/255.,82/255.)
        self["sea_green3"]              = IMP.display.Color(84/255.,197/255.,113/255.)
        self["spring_green2"]           = IMP.display.Color(87/255.,233/255.,100/255.)
        self["spring_green1"]           = IMP.display.Color(94/255.,251/255.,110/255.)
        self["sea_green2"]              = IMP.display.Color(100/255.,233/255.,134/255.)
        self["sea_green1"]              = IMP.display.Color(106/255.,251/255.,146/255.)
        self["dark_sea_green2"]         = IMP.display.Color(181/255.,234/255.,170/255.)
        self["dark_sea_green1"]         = IMP.display.Color(195/255.,253/255.,184/255.)
        self["green"]                   = IMP.display.Color(0/255.,255/255.,0/255.)
        self["lawn_green"]              = IMP.display.Color(135/255.,247/255.,23/255.)
        self["green1"]                  = IMP.display.Color(95/255.,251/255.,23/255.)
        self["green2"]                  = IMP.display.Color(89/255.,232/255.,23/255.)
        self["chartreuse2"]             = IMP.display.Color(127/255.,232/255.,23/255.)
        self["chartreuse"]              = IMP.display.Color(138/255.,251/255.,23/255.)
        self["green_yellow"]            = IMP.display.Color(177/255.,251/255.,23/255.)
        self["dark_olive_green1"]       = IMP.display.Color(204/255.,251/255.,93/255.)
        self["dark_olive_green2"]       = IMP.display.Color(188/255.,233/255.,84/255.)
        self["dark_olive_green3"]       = IMP.display.Color(160/255.,197/255.,68/255.)
        self["yellow"]                  = IMP.display.Color(255/255.,255/255.,0/255.)
        self["yellow1"]                 = IMP.display.Color(255/255.,252/255.,23/255.)
        self["khaki1"]                  = IMP.display.Color(255/255.,243/255.,128/255.)
        self["khaki2"]                  = IMP.display.Color(237/255.,226/255.,117/255.)
        self["goldenrod"]               = IMP.display.Color(237/255.,218/255.,116/255.)
        self["gold2"]                   = IMP.display.Color(234/255.,193/255.,23/255.)
        self["gold1"]                   = IMP.display.Color(253/255.,208/255.,23/255.)
        self["goldenrod1"]              = IMP.display.Color(251/255.,185/255.,23/255.)
        self["goldenrod2"]              = IMP.display.Color(233/255.,171/255.,23/255.)
        self["gold"]                    = IMP.display.Color(212/255.,160/255.,23/255.)
        self["gold3"]                   = IMP.display.Color(199/255.,163/255.,23/255.)
        self["goldenrod3"]              = IMP.display.Color(198/255.,142/255.,23/255.)
        self["dark_goldenrod"]          = IMP.display.Color(175/255.,120/255.,23/255.)
        self["khaki"]                   = IMP.display.Color(173/255.,169/255.,110/255.)
        self["khaki3"]                  = IMP.display.Color(201/255.,190/255.,98/255.)
        self["khaki4"]                  = IMP.display.Color(130/255.,120/255.,57/255.)
        self["dark_goldenrod1"]         = IMP.display.Color(251/255.,177/255.,23/255.)
        self["dark_goldenrod2"]         = IMP.display.Color(232/255.,163/255.,23/255.)
        self["dark_goldenrod3"]         = IMP.display.Color(197/255.,137/255.,23/255.)
        self["sienna1"]                 = IMP.display.Color(248/255.,116/255.,49/255.)
        self["sienna2"]                 = IMP.display.Color(230/255.,108/255.,44/255.)
        self["dark_orange"]             = IMP.display.Color(248/255.,128/255.,23/255.)
        self["dark_orange1"]            = IMP.display.Color(248/255.,114/255.,23/255.)
        self["dark_orange2"]            = IMP.display.Color(229/255.,103/255.,23/255.)
        self["dark_orange3"]            = IMP.display.Color(195/255.,86/255.,23/255.)
        self["sienna3"]                 = IMP.display.Color(195/255.,88/255.,23/255.)
        self["sienna"]                  = IMP.display.Color(138/255.,65/255.,23/255.)
        self["sienna4"]                 = IMP.display.Color(126/255.,53/255.,23/255.)
        self["indian_red4"]             = IMP.display.Color(126/255.,34/255.,23/255.)
        self["dark_orange3"]            = IMP.display.Color(126/255.,49/255.,23/255.)
        self["salmon4"]                 = IMP.display.Color(126/255.,56/255.,23/255.)
        self["dark_goldenrod4"]         = IMP.display.Color(127/255.,82/255.,23/255.)
        self["gold4"]                   = IMP.display.Color(128/255.,101/255.,23/255.)
        self["goldenrod4"]              = IMP.display.Color(128/255.,88/255.,23/255.)
        self["light_salmon4"]           = IMP.display.Color(127/255.,70/255.,44/255.)
        self["chocolate"]               = IMP.display.Color(200/255.,90/255.,23/255.)
        self["coral3"]                  = IMP.display.Color(195/255.,74/255.,44/255.)
        self["coral2"]                  = IMP.display.Color(229/255.,91/255.,60/255.)
        self["coral"]                   = IMP.display.Color(247/255.,101/255.,65/255.)
        self["dark_salmon"]             = IMP.display.Color(225/255.,139/255.,107/255.)
        self["salmon1"]                 = IMP.display.Color(248/255.,129/255.,88/255.)
        self["salmon2"]                 = IMP.display.Color(230/255.,116/255.,81/255.)
        self["salmon3"]                 = IMP.display.Color(195/255.,98/255.,65/255.)
        self["light_salmon3"]           = IMP.display.Color(196/255.,116/255.,81/255.)
        self["light_salmon2"]           = IMP.display.Color(231/255.,138/255.,97/255.)
        self["light_salmon"]            = IMP.display.Color(249/255.,150/255.,107/255.)
        self["sandy_brown"]             = IMP.display.Color(238/255.,154/255.,77/255.)
        self["hot_pink"]                = IMP.display.Color(246/255.,96/255.,171/255.)
        self["hot_pink1"]               = IMP.display.Color(246/255.,101/255.,171/255.)
        self["hot_pink2"]               = IMP.display.Color(228/255.,94/255.,157/255.)
        self["hot_pink3"]               = IMP.display.Color(194/255.,82/255.,131/255.)
        self["hot_pink4"]               = IMP.display.Color(125/255.,34/255.,82/255.)
        self["light_coral"]             = IMP.display.Color(231/255.,116/255.,113/255.)
        self["indian_red1"]             = IMP.display.Color(247/255.,93/255.,89/255.)
        self["indian_red2"]             = IMP.display.Color(229/255.,84/255.,81/255.)
        self["indian_red3"]             = IMP.display.Color(194/255.,70/255.,65/255.)
        self["red"]                     = IMP.display.Color(255/255.,0/255.,0/255.)
        self["red1"]                    = IMP.display.Color(246/255.,34/255.,23/255.)
        self["red2"]                    = IMP.display.Color(228/255.,27/255.,23/255.)
        self["firebrick1"]              = IMP.display.Color(246/255.,40/255.,23/255.)
        self["firebrick2"]              = IMP.display.Color(228/255.,34/255.,23/255.)
        self["firebrick3"]              = IMP.display.Color(193/255.,27/255.,23/255.)
        self["pink"]                    = IMP.display.Color(250/255.,175/255.,190/255.)
        self["rosy_brown1"]             = IMP.display.Color(251/255.,187/255.,185/255.)
        self["rosy_brown2"]             = IMP.display.Color(232/255.,173/255.,170/255.)
        self["pink2"]                   = IMP.display.Color(231/255.,161/255.,176/255.)
        self["light_pink"]              = IMP.display.Color(250/255.,175/255.,186/255.)
        self["light_pink1"]             = IMP.display.Color(249/255.,167/255.,176/255.)
        self["light_pink2"]             = IMP.display.Color(231/255.,153/255.,163/255.)
        self["pink3"]                   = IMP.display.Color(196/255.,135/255.,147/255.)
        self["rosy_brown3"]             = IMP.display.Color(197/255.,144/255.,142/255.)
        self["rosy_brown"]              = IMP.display.Color(179/255.,132/255.,129/255.)
        self["light_pink3"]             = IMP.display.Color(196/255.,129/255.,137/255.)
        self["rosy_brown4"]             = IMP.display.Color(127/255.,90/255.,88/255.)
        self["light_pink4"]             = IMP.display.Color(127/255.,78/255.,82/255.)
        self["pink4"]                   = IMP.display.Color(127/255.,82/255.,93/255.)
        self["lavender_blush4"]         = IMP.display.Color(129/255.,118/255.,121/255.)
        self["light_goldenrod4"]        = IMP.display.Color(129/255.,115/255.,57/255.)
        self["lemon_chiffon4"]          = IMP.display.Color(130/255.,123/255.,96/255.)
        self["lemon_chiffon3"]          = IMP.display.Color(201/255.,194/255.,153/255.)
        self["light_goldenrod3"]        = IMP.display.Color(200/255.,181/255.,96/255.)
        self["light_golden2"]           = IMP.display.Color(236/255.,214/255.,114/255.)
        self["light_goldenrod"]         = IMP.display.Color(236/255.,216/255.,114/255.)
        self["light_goldenrod1"]        = IMP.display.Color(255/255.,232/255.,124/255.)
        self["lemon_chiffon2"]          = IMP.display.Color(236/255.,229/255.,182/255.)
        self["lemon_chiffon"]           = IMP.display.Color(255/255.,248/255.,198/255.)
        self["light_goldenrod_yellow"]  = IMP.display.Color(250/255.,248/255.,204/255.)
        
    def get_color_names(self):
        """ returns the name of all registered colors
        """
        return self.keys()

    def get_color_by_name(self,color_name):
        """
        @param : color_name
        """
        return self[color_name]
    
    def set_color(self,color_name,imp_color):
        """ insert a novel named IMP color in the present dictionnary
        """
        self[color_name] = imp_color
        return self[color_name]
        
    def get_color_by_channels(self,r,g,b):
        """ returns the IMP color corresponding to the provided r g b channels
        @param r: red (int in [0-255])
        @param g: green (int in [0-255])
        @param b: blue (int in [0-255])
        """
        return IMP.display.Color(r/255.,g/255.,b/255.)
    
    