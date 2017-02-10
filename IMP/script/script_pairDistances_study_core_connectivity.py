'''

'''

import os
from time import time

import IMP
#print "IMP version : ",IMP.get_module_version_info().get_version()
import HGM
#import HGM.sampling
#import HGM.display
import HGM.distances
import HGM.connectivity

#import HGM.helpers
#import HGM.helpersPlot

from numpy import corrcoef

from alternate_configs import configs
#    MY TFIIH REPRESENTATION
#config_name_for_this_run    = "fixedGeom_0"
#config_name_for_this_run    = "fixedGeom_1_1"
#config_name_for_this_run    = "fixedGeom_EM_1_1"
config_name_for_this_run    = "fixedGeom_EM_1_2"

#
#    PARAMETERS
#
#
#
tfiihRepresentationFileName = configs[config_name_for_this_run][0]
runDir                      = os.path.join("results",config_name_for_this_run)
saveDirSample               = os.path.join(runDir,"samples")
savePrefix                  = "saves"


dDir                        = os.path.join(runDir,"distances")
dmDir                       = os.path.join(dDir,"distMatrices")

# When computing not directly on the dist-matrix, but on a sampleFile
altConfigDir                = os.path.join(runDir,"altConfigs")
lowEconfigsFilePath         = os.path.join(altConfigDir,"lowE-configs-112.txt")
mediumEconfigsFilePath      = os.path.join(altConfigDir,"mediumE-configs-112.txt")
highEconfigsFilePath        = os.path.join(altConfigDir,"highE-configs-112.txt") 

sampleFilePath              = highEconfigsFilePath

#for d in [dDir,dmDir,dhDir,ccDir] :
#    HGM.helpers.check_or_create_dir(d)

#
#    Sample configuration
#

#sample_indexes      = range(10)
#sampleDescription   = 10
#distMatrixFileName  = "dist_matrix_test_10.pickle"
#htmlFileName        = "subunits_dist_histo_test_10.html"
#ccFileName          = "crossCorelations-10.txt"


#sample_indexes      = range(1000)
#sampleDescription   = 1000
#distMatrixFileName  = "dist_matrix_test_1000.pickle"
#htmlFileName        = "subunits_dist_histo_test_1000.html"
#ccFileName          = "crossCorelations-1000.txt"



##sample_indexes      = range(1000)
#sampleDescription   = "963"
#distMatrixFileName  = "dist_matrix_test_963.pickle"
##htmlFileName        = "subunits_dist_histo_test_1000.html"
##ccFileName          = "crossCorelations-1000.txt"

###################

#sampleDescription   = "963"
#distMatrixFileName  = "dist_matrix_test_EM1.1-87.pickle"
#distMatrixFileName  = "dist_matrix_test_EM1.1i-223.pickle"
distMatrixFileName  = "dist_matrix_test_EM1.2-112.pickle"

thresholds          = range(10)
thresholds.append(0.1)


distMatrixFilePath  = os.path.join(dmDir,distMatrixFileName)


exec ( "from {0:s} import build_TFIIH_subunits_info".format( tfiihRepresentationFileName ) )


def compute_stats_complete(sdms,c_threshold=3.0):
    csgo=HGM.connectivity.CountSgraphOccurences(sdms,["p52","p62","p44","p34","XPB"],c_threshold)
    
    count           = float(csgo.get_number_of_configurations())
    coeff_corr      = 100./count
    
    result = {}
    
    def output_stats_line(s,n,p,subhashkey=None) : 
        print "{0:<20s} : {1:7d} {2:6.2f}".format(s,n,p)
        if subhashkey==None :
            result[s]=(n,p)
        else :
            try :
                result[subhashkey][s]=(n,p)
            except :
                result[subhashkey]={s:(n,p)}
    
    # 1.a P52 XPB both ?
    # 1.b.1 when P52, who is touched ?
    # 1.b.2 when XPB, who is touched ?
    #
    #
    
    # 1.a
    xpb_edges = [("XPB","p44"),("XPB","p34"),("XPB","p62")]
    p52_edges = [("p52","p44"),("p52","p34"),("p52","p62")]
    #
    gis_with_xpb_link       = set (csgo.get_graph_indices_with_one_edge(xpb_edges))
    gis_with_p52_link       = set (csgo.get_graph_indices_with_one_edge(p52_edges))
    gis_with_xpb_only       = gis_with_xpb_link.difference(gis_with_p52_link)
    gis_with_p52_only       = gis_with_p52_link.difference(gis_with_xpb_link)
    gis_with_p52_or_xpb     = gis_with_p52_link.union(gis_with_xpb_link)
    gis_with_both           = gis_with_p52_link.intersection(gis_with_xpb_link)
    #
    nb_xpb                  = csgo.get_accumulated_count(gis_with_xpb_link)
    nb_p52                  = csgo.get_accumulated_count(gis_with_p52_link)
    nb_xpb_only             = csgo.get_accumulated_count(gis_with_xpb_only)
    nb_p52_only             = csgo.get_accumulated_count(gis_with_p52_only)
    nb_p52_or_xpb           = csgo.get_accumulated_count(gis_with_p52_or_xpb)
    nb_p52_and_xpb          = csgo.get_accumulated_count(gis_with_both)
    
    output_stats_line ("XPB implicated"         , nb_xpb            , nb_xpb * coeff_corr )
    output_stats_line ("P52 implicated"         , nb_p52            , nb_p52 * coeff_corr )
    output_stats_line ("XPB exclusive"          , nb_xpb_only       , nb_xpb_only * coeff_corr )
    output_stats_line ("P52 exclusive"          , nb_p52_only       , nb_p52_only * coeff_corr )
    output_stats_line ("one of XPB or P52"      , nb_p52_or_xpb     , nb_p52_or_xpb  * coeff_corr )
    output_stats_line ("both XPB and P52"       , nb_p52_and_xpb    , nb_p52_and_xpb * coeff_corr )
    
    # 1.b.1
    gis_with_xpb_to_p44        = set( csgo.get_graph_indices_with_one_edge([("XPB","p44")]) )
    gis_with_xpb_to_p34        = set( csgo.get_graph_indices_with_one_edge([("XPB","p34")]) )
    gis_with_xpb_to_p62        = set( csgo.get_graph_indices_with_one_edge([("XPB","p62")]) )
    #
    gis_with_xpb_only_to_p44                = gis_with_xpb_to_p44.difference(gis_with_xpb_to_p34).difference(gis_with_xpb_to_p62)
    gis_with_xpb_only_to_p34                = gis_with_xpb_to_p34.difference(gis_with_xpb_to_p44).difference(gis_with_xpb_to_p62)
    gis_with_xpb_only_to_p62                = gis_with_xpb_to_p62.difference(gis_with_xpb_to_p44).difference(gis_with_xpb_to_p34)
    gis_with_xpb_only_to_p44_and_p34        = gis_with_xpb_to_p44.intersection(gis_with_xpb_to_p34).difference(gis_with_xpb_to_p62)
    gis_with_xpb_only_to_p44_and_p62        = gis_with_xpb_to_p44.intersection(gis_with_xpb_to_p62).difference(gis_with_xpb_to_p34)
    gis_with_xpb_only_to_p34_and_p62        = gis_with_xpb_to_p62.intersection(gis_with_xpb_to_p34).difference(gis_with_xpb_to_p44)
    gis_with_xpb_to_p44_and_p34_and_p62     = gis_with_xpb_to_p62.intersection(gis_with_xpb_to_p44).intersection(gis_with_xpb_to_p34)
    #
    nb_gis_with_xpb_to_p44                  = csgo.get_accumulated_count(gis_with_xpb_to_p44)
    nb_gis_with_xpb_to_p34                  = csgo.get_accumulated_count(gis_with_xpb_to_p34)
    nb_gis_with_xpb_to_p62                  = csgo.get_accumulated_count(gis_with_xpb_to_p62)
    nb_gis_with_xpb_only_to_p44             = csgo.get_accumulated_count(gis_with_xpb_only_to_p44)
    nb_gis_with_xpb_only_to_p34             = csgo.get_accumulated_count(gis_with_xpb_only_to_p34)
    nb_gis_with_xpb_only_to_p62             = csgo.get_accumulated_count(gis_with_xpb_only_to_p62)
    nb_gis_with_xpb_only_to_p44_and_p34     = csgo.get_accumulated_count(gis_with_xpb_only_to_p44_and_p34)
    nb_gis_with_xpb_only_to_p44_and_p62     = csgo.get_accumulated_count(gis_with_xpb_only_to_p44_and_p62)
    nb_gis_with_xpb_only_to_p34_and_p62     = csgo.get_accumulated_count(gis_with_xpb_only_to_p34_and_p62)
    nb_gis_with_xpb_to_p44_and_p34_and_p62  = csgo.get_accumulated_count(gis_with_xpb_to_p44_and_p34_and_p62)
    #
    print "------ under XPB contact -------"
    output_stats_line("connection to p44", nb_gis_with_xpb_to_p44, nb_gis_with_xpb_to_p44 * 100. / nb_xpb, "under XPB contact" )
    output_stats_line("connection to p34", nb_gis_with_xpb_to_p34, nb_gis_with_xpb_to_p34 * 100. / nb_xpb, "under XPB contact" )
    output_stats_line("connection to p62", nb_gis_with_xpb_to_p62, nb_gis_with_xpb_to_p62 * 100. / nb_xpb, "under XPB contact" )
    output_stats_line("solely to p44", nb_gis_with_xpb_only_to_p44, nb_gis_with_xpb_only_to_p44 * 100. / nb_xpb, "under XPB contact" )
    output_stats_line("solely to p34", nb_gis_with_xpb_only_to_p34, nb_gis_with_xpb_only_to_p34 * 100. / nb_xpb, "under XPB contact" )
    output_stats_line("solely to p62", nb_gis_with_xpb_only_to_p62, nb_gis_with_xpb_only_to_p62 * 100. / nb_xpb, "under XPB contact" )
    output_stats_line("p44 and p34 only", nb_gis_with_xpb_only_to_p44_and_p34, nb_gis_with_xpb_only_to_p44_and_p34 * 100. / nb_xpb, "under XPB contact" )
    output_stats_line("p44 and p62 only", nb_gis_with_xpb_only_to_p44_and_p62, nb_gis_with_xpb_only_to_p44_and_p62 * 100. / nb_xpb, "under XPB contact" )
    output_stats_line("p34 and p62 only", nb_gis_with_xpb_only_to_p34_and_p62, nb_gis_with_xpb_only_to_p34_and_p62 * 100. / nb_xpb, "under XPB contact" )
    output_stats_line("p44 and p34 and p62", nb_gis_with_xpb_to_p44_and_p34_and_p62, nb_gis_with_xpb_to_p44_and_p34_and_p62 * 100. / nb_xpb, "under XPB contact" )

    # 1.b.2
    gis_with_p52_to_p44        = set ( csgo.get_graph_indices_with_one_edge([("p52","p44")]) )
    gis_with_p52_to_p34        = set ( csgo.get_graph_indices_with_one_edge([("p52","p34")]) )
    gis_with_p52_to_p62        = set ( csgo.get_graph_indices_with_one_edge([("p52","p62")]) )
    #
    gis_with_p52_only_to_p44                = gis_with_p52_to_p44.difference(gis_with_p52_to_p34).difference(gis_with_p52_to_p62)
    gis_with_p52_only_to_p34                = gis_with_p52_to_p34.difference(gis_with_p52_to_p44).difference(gis_with_p52_to_p62)
    gis_with_p52_only_to_p62                = gis_with_p52_to_p62.difference(gis_with_p52_to_p44).difference(gis_with_p52_to_p34)
    gis_with_p52_only_to_p44_and_p34        = gis_with_p52_to_p44.intersection(gis_with_p52_to_p34).difference(gis_with_p52_to_p62)
    gis_with_p52_only_to_p44_and_p62        = gis_with_p52_to_p44.intersection(gis_with_p52_to_p62).difference(gis_with_p52_to_p34)
    gis_with_p52_only_to_p34_and_p62        = gis_with_p52_to_p62.intersection(gis_with_p52_to_p34).difference(gis_with_p52_to_p44)
    gis_with_p52_to_p44_and_p34_and_p62     = gis_with_p52_to_p62.intersection(gis_with_p52_to_p44).intersection(gis_with_p52_to_p34)
    #
    nb_gis_with_p52_to_p44                  = csgo.get_accumulated_count(gis_with_p52_to_p44)
    nb_gis_with_p52_to_p34                  = csgo.get_accumulated_count(gis_with_p52_to_p34)
    nb_gis_with_p52_to_p62                  = csgo.get_accumulated_count(gis_with_p52_to_p62)
    nb_gis_with_p52_only_to_p44             = csgo.get_accumulated_count(gis_with_p52_only_to_p44)
    nb_gis_with_p52_only_to_p34             = csgo.get_accumulated_count(gis_with_p52_only_to_p34)
    nb_gis_with_p52_only_to_p62             = csgo.get_accumulated_count(gis_with_p52_only_to_p62)
    nb_gis_with_p52_only_to_p44_and_p34     = csgo.get_accumulated_count(gis_with_p52_only_to_p44_and_p34)
    nb_gis_with_p52_only_to_p44_and_p62     = csgo.get_accumulated_count(gis_with_p52_only_to_p44_and_p62)
    nb_gis_with_p52_only_to_p34_and_p62     = csgo.get_accumulated_count(gis_with_p52_only_to_p34_and_p62)
    nb_gis_with_p52_to_p44_and_p34_and_p62  = csgo.get_accumulated_count(gis_with_p52_to_p44_and_p34_and_p62)
    #
    print "------ under P52 contact -------"
    output_stats_line("connection to p44", nb_gis_with_p52_to_p44, nb_gis_with_p52_to_p44 * 100. / nb_p52, "under P52 contact" )
    output_stats_line("connection to p34", nb_gis_with_p52_to_p34, nb_gis_with_p52_to_p34 * 100. / nb_p52, "under P52 contact" )
    output_stats_line("connection to p62", nb_gis_with_p52_to_p62, nb_gis_with_p52_to_p62 * 100. / nb_p52, "under P52 contact" )
    output_stats_line("solely to p44", nb_gis_with_p52_only_to_p44, nb_gis_with_p52_only_to_p44 * 100. / nb_p52, "under P52 contact" )
    output_stats_line("solely to p34", nb_gis_with_p52_only_to_p34, nb_gis_with_p52_only_to_p34 * 100. / nb_p52, "under P52 contact" )
    output_stats_line("solely to p62", nb_gis_with_p52_only_to_p62, nb_gis_with_p52_only_to_p62 * 100. / nb_p52, "under P52 contact" )
    output_stats_line("p44 and p34 only", nb_gis_with_p52_only_to_p44_and_p34, nb_gis_with_p52_only_to_p44_and_p34 * 100. / nb_p52, "under P52 contact" )
    output_stats_line("p44 and p62 only", nb_gis_with_p52_only_to_p44_and_p62, nb_gis_with_p52_only_to_p44_and_p62 * 100. / nb_p52, "under P52 contact" )
    output_stats_line("p34 and p62 only", nb_gis_with_p52_only_to_p34_and_p62, nb_gis_with_p52_only_to_p34_and_p62 * 100. / nb_p52, "under P52 contact" )
    output_stats_line("p44 and p34 and p62", nb_gis_with_p52_to_p44_and_p34_and_p62, nb_gis_with_p52_to_p44_and_p34_and_p62 * 100. / nb_p52, "under P52 contact" )
    
    
    
    # 2.a P44 P34 P62 ?
    # 2.b.1 ...
    #
    # 2.a
    #
    print "="*40
    p44_edges = [("XPB","p44"),("p52","p44")]
    p34_edges = [("XPB","p34"),("p52","p34")]
    p62_edges = [("XPB","p62"),("p52","p62")]
    #
    gis_with_p44_link       = set (csgo.get_graph_indices_with_one_edge(p44_edges))
    gis_with_p34_link       = set (csgo.get_graph_indices_with_one_edge(p34_edges))
    gis_with_p62_link       = set (csgo.get_graph_indices_with_one_edge(p62_edges))
    gis_with_p44_only       = gis_with_p44_link.difference(gis_with_p34_link.union(gis_with_p62_link))
    gis_with_p34_only       = gis_with_p34_link.difference(gis_with_p44_link.union(gis_with_p62_link))
    gis_with_p62_only       = gis_with_p62_link.difference(gis_with_p34_link.union(gis_with_p44_link))
    gis_with_p44_P34_only   = gis_with_p44_link.intersection(gis_with_p34_link)
    gis_with_p44_P62_only   = gis_with_p44_link.intersection(gis_with_p62_link)
    gis_with_p34_P62_only   = gis_with_p34_link.intersection(gis_with_p62_link)
    gis_with_p44_P34_p62    = gis_with_p34_P62_only.intersection(gis_with_p44_link)
    gis_with_one_of_the_three = gis_with_p44_link.union(gis_with_p34_link).union(gis_with_p62_link)
    #
    nb_gis_with_p44_link       = csgo.get_accumulated_count(gis_with_p44_link)
    nb_gis_with_p34_link       = csgo.get_accumulated_count(gis_with_p34_link)
    nb_gis_with_p62_link       = csgo.get_accumulated_count(gis_with_p62_link)
    nb_gis_with_p44_only       = csgo.get_accumulated_count(gis_with_p44_only)
    nb_gis_with_p34_only       = csgo.get_accumulated_count(gis_with_p34_only)
    nb_gis_with_p62_only       = csgo.get_accumulated_count(gis_with_p62_only)
    nb_gis_with_p44_P34_only   = csgo.get_accumulated_count(gis_with_p44_P34_only)
    nb_gis_with_p44_P62_only   = csgo.get_accumulated_count(gis_with_p44_P62_only)
    nb_gis_with_p34_P62_only   = csgo.get_accumulated_count(gis_with_p34_P62_only)
    nb_gis_with_p44_P34_p62    = csgo.get_accumulated_count(gis_with_p44_P34_p62)
    nb_gis_with_one_of_the_three = csgo.get_accumulated_count(gis_with_one_of_the_three)
    #
    output_stats_line ("p44 implicated"           , nb_gis_with_p44_link, nb_gis_with_p44_link * coeff_corr)
    output_stats_line ("p34 implicated"       , nb_gis_with_p34_link,nb_gis_with_p34_link * coeff_corr)
    output_stats_line ("p62 implicated"       , nb_gis_with_p62_link, nb_gis_with_p62_link * coeff_corr)
    output_stats_line ("p44 only"       , nb_gis_with_p44_only, nb_gis_with_p44_only * coeff_corr)
    output_stats_line ("p34 only"       , nb_gis_with_p34_only, nb_gis_with_p34_only * coeff_corr)
    output_stats_line ("p62 only"       , nb_gis_with_p62_only, nb_gis_with_p62_only * coeff_corr)
    output_stats_line ("p44 and p34 solely"       , nb_gis_with_p44_P34_only, nb_gis_with_p44_P34_only * coeff_corr)
    output_stats_line ("p44 and p62 solely"       , nb_gis_with_p44_P62_only, nb_gis_with_p44_P62_only * coeff_corr)
    output_stats_line ("p34 and p62 solely"       , nb_gis_with_p34_P62_only, nb_gis_with_p34_P62_only * coeff_corr)
    output_stats_line ("all three"       , nb_gis_with_p44_P34_p62, nb_gis_with_p44_P34_p62 * coeff_corr)
    output_stats_line ("one of the three", nb_gis_with_one_of_the_three, nb_gis_with_one_of_the_three * coeff_corr,)
    # 2.b.1 ...
    
    # 1.b.1
    gis_with_p44_only_to_xpb                = gis_with_xpb_to_p44.difference(   gis_with_p52_to_p44 )
    gis_with_p44_only_to_p52                = gis_with_p52_to_p44.difference(   gis_with_xpb_to_p44 )
    gis_with_p44_to_both                    = gis_with_xpb_to_p44.intersection( gis_with_p52_to_p44 ) 
    #
    nb_gis_with_p44_only_to_xpb             = csgo.get_accumulated_count(gis_with_p44_only_to_xpb)
    nb_gis_with_p44_only_to_p52             = csgo.get_accumulated_count(gis_with_p44_only_to_p52)
    nb_gis_with_p44_to_both                 = csgo.get_accumulated_count(gis_with_p44_to_both)
    #
    print "------ under P44 contact -------"
    output_stats_line("connection to XPB", nb_gis_with_xpb_to_p44, nb_gis_with_xpb_to_p44 * 100. / nb_gis_with_p44_link , "under P44 contact")
    output_stats_line("connection to p52", nb_gis_with_p52_to_p44, nb_gis_with_p52_to_p44 * 100. / nb_gis_with_p44_link , "under P44 contact")
    output_stats_line("solely to XPB", nb_gis_with_p44_only_to_xpb, nb_gis_with_p44_only_to_xpb * 100. / nb_gis_with_p44_link , "under P44 contact")
    output_stats_line("solely to p52", nb_gis_with_p44_only_to_p52, nb_gis_with_p44_only_to_p52 * 100. / nb_gis_with_p44_link , "under P44 contact")
    output_stats_line("both XPB and P52", nb_gis_with_p44_to_both, nb_gis_with_p44_to_both * 100. / nb_gis_with_p44_link , "under P44 contact")

    # 1.b.2
    gis_with_p34_only_to_xpb                = gis_with_xpb_to_p34.difference(   gis_with_p52_to_p34 )
    gis_with_p34_only_to_p52                = gis_with_p52_to_p34.difference(   gis_with_xpb_to_p34 )
    gis_with_p34_to_both                    = gis_with_xpb_to_p34.intersection( gis_with_p52_to_p34 ) 
    #
    nb_gis_with_p34_only_to_xpb             = csgo.get_accumulated_count(gis_with_p34_only_to_xpb)
    nb_gis_with_p34_only_to_p52             = csgo.get_accumulated_count(gis_with_p34_only_to_p52)
    nb_gis_with_p34_to_both                 = csgo.get_accumulated_count(gis_with_p34_to_both)
    #
    print "------ under P34 contact -------"
    output_stats_line("connection to XPB", nb_gis_with_xpb_to_p34, nb_gis_with_xpb_to_p34 * 100. / nb_gis_with_p34_link , "under P34 contact")
    output_stats_line("connection to p52", nb_gis_with_p52_to_p34, nb_gis_with_p52_to_p34 * 100. / nb_gis_with_p34_link , "under P34 contact")
    output_stats_line("solely to XPB", nb_gis_with_p34_only_to_xpb, nb_gis_with_p34_only_to_xpb * 100. / nb_gis_with_p34_link , "under P34 contact")
    output_stats_line("solely to p52", nb_gis_with_p34_only_to_p52, nb_gis_with_p34_only_to_p52 * 100. / nb_gis_with_p34_link , "under P34 contact")
    output_stats_line("both XPB and P52", nb_gis_with_p34_to_both, nb_gis_with_p34_to_both * 100. / nb_gis_with_p34_link , "under P34 contact")

    # 1.b.3
    gis_with_p62_only_to_xpb                = gis_with_xpb_to_p62.difference(   gis_with_p52_to_p62 )
    gis_with_p62_only_to_p52                = gis_with_p52_to_p62.difference(   gis_with_xpb_to_p62 )
    gis_with_p62_to_both                    = gis_with_xpb_to_p62.intersection( gis_with_p52_to_p62 ) 
    #
    nb_gis_with_p62_only_to_xpb             = csgo.get_accumulated_count(gis_with_p62_only_to_xpb)
    nb_gis_with_p62_only_to_p52             = csgo.get_accumulated_count(gis_with_p62_only_to_p52)
    nb_gis_with_p62_to_both                 = csgo.get_accumulated_count(gis_with_p62_to_both)
    #
    print "------ under P62 contact -------"
    output_stats_line("connection to XPB", nb_gis_with_xpb_to_p62, nb_gis_with_xpb_to_p62 * 100. / nb_gis_with_p62_link , "under P62 contact")
    output_stats_line("connection to p52", nb_gis_with_p52_to_p62, nb_gis_with_p52_to_p62 * 100. / nb_gis_with_p62_link , "under P62 contact")
    output_stats_line("solely to XPB", nb_gis_with_p62_only_to_xpb, nb_gis_with_p62_only_to_xpb * 100. / nb_gis_with_p62_link , "under P62 contact")
    output_stats_line("solely to p52", nb_gis_with_p62_only_to_p52, nb_gis_with_p62_only_to_p52 * 100. / nb_gis_with_p62_link , "under P62 contact")
    output_stats_line("both XPB and P52", nb_gis_with_p62_to_both, nb_gis_with_p62_to_both * 100. / nb_gis_with_p62_link , "under P62 contact")
    
    return result





def compute_stats(sdms):
    

    c_threshold=3.0
    csgo=HGM.connectivity.CountSgraphOccurences(sdms,["p52","p62","p44","p34","XPB"],c_threshold)
    
#    threshold=10
#    print "Show graphs with more than",threshold,"occurences"
#    csgo.show_graphs_with_count_above(threshold)

#    print "Check subunits connection restraints are respected"
#    forced_edges = [("XPB","p52"),("p62","p44"),("p34","p44")]
#    print "forced edges : ",forced_edges
#    print "",csgo.get_count_with_all_edges(forced_edges),"have all edges"
#    print "",csgo.get_count_without_one_of_edges(forced_edges),"lack at least one of the edges"

    count = float(csgo.get_number_of_configurations())
    
    xpb_edges = [("XPB","p44"),("XPB","p34"),("XPB","p62")]
    p52_edges = [("p52","p44"),("p52","p34"),("p52","p62")]
    
    gis_with_xpb_link       = set (csgo.get_graph_indices_with_one_edge(xpb_edges))
    gis_with_p52_link       = set (csgo.get_graph_indices_with_one_edge(p52_edges))
    gis_with_xpb_only       = gis_with_xpb_link.difference(gis_with_p52_link)
    gis_with_p52_only       = gis_with_p52_link.difference(gis_with_xpb_link)
    gis_with_p52_or_xpb     = gis_with_p52_link.union(gis_with_xpb_link)
    gis_with_both           = gis_with_p52_link.intersection(gis_with_xpb_link)
    
#    print "----"
#    print "{0:7d} configurations".format(count)
##    print "XPB implicated : {0:%7d} ({%5.2f})".format(gis_with_xpb_link,)
#    print "P52 implicated : {} ()"
#    


    p44_edges = [("p44","XPB"),("p44","p52")]
    p34_edges = [("p34","XPB"),("p34","p52")]
    p62_edges = [("p62","XPB"),("p62","p52")]

    gis_with_p44_link       = set (csgo.get_graph_indices_with_one_edge(p44_edges))
    gis_with_p34_link       = set (csgo.get_graph_indices_with_one_edge(p34_edges))
    gis_with_p62_link       = set (csgo.get_graph_indices_with_one_edge(p62_edges))
    gis_with_p44_only       = gis_with_p44_link.difference( gis_with_p34_link.union(gis_with_p62_link) )
    gis_with_p34_only       = gis_with_p34_link.difference( gis_with_p44_link.union(gis_with_p62_link) )
    gis_with_p62_only       = gis_with_p62_link.difference( gis_with_p34_link.union(gis_with_p44_link) )

#    print "   -count internal connections in core"
    nb_xpb_only     = csgo.get_accumulated_count(list(gis_with_xpb_only))
    nb_p52_only     = csgo.get_accumulated_count(list(gis_with_p52_only))
    nb_xpb_or_p52   = csgo.get_accumulated_count(list(gis_with_p52_or_xpb))
    nb_xpb_and_p52  = csgo.get_accumulated_count(list(gis_with_both))
    nb_p44          = csgo.get_accumulated_count(list(gis_with_p44_link))
    nb_p44_only     = csgo.get_accumulated_count(list(gis_with_p44_only))
    nb_p34          = csgo.get_accumulated_count(list(gis_with_p34_link))
    nb_p34_only     = csgo.get_accumulated_count(list(gis_with_p34_only))
    nb_p62          = csgo.get_accumulated_count(list(gis_with_p62_link))
    nb_p62_only     = csgo.get_accumulated_count(list(gis_with_p62_only))
    
#    print " only XPB   ",nb_xpb_only
#    print " only p52   ",nb_p52_only
#    print " XPB or P52 ",nb_xpb_or_p52,csgo.get_number_of_configurations()
#    print " XPB and P52",nb_xpb_and_p52,nb_xpb_or_p52-nb_xpb_only-nb_p52_only
    
    print count
    print " only XPB    %5d (%4.2f%%)" % (nb_xpb_only, (nb_xpb_only/count)*100)
    print " only p52    %5d (%4.2f%%)" % (nb_p52_only, (nb_p52_only/count)*100)
    print " XPB and P52 %5d (%4.2f%%)" % (count-nb_xpb_only-nb_p52_only, ( (count-nb_xpb_only-nb_p52_only)/count)*100)
    #
    print "Analysis sub connexions"
    print " XPB-p44: %d" % csgo.get_count_with_all_edges([("XPB","p44")])
    print " XPB-p34: %d" % csgo.get_count_with_all_edges([("XPB","p34")])
    print " XPB-p62: %d" % csgo.get_count_with_all_edges([("XPB","p62")])
    #
    print "Yet a finer analysis" 
    gis_with_xpb_to_p44                     = set( csgo.get_graph_indices_with_one_edge( [("XPB","p44")] ) )
    gis_with_xpb_to_p34                     = set( csgo.get_graph_indices_with_one_edge( [("XPB","p34")] ) )
    gis_with_xpb_to_p62                     = set( csgo.get_graph_indices_with_one_edge( [("XPB","p62")] ) )
    gis_with_xpb_only_to_p44                = gis_with_xpb_to_p44.difference(gis_with_xpb_to_p34).difference(gis_with_xpb_to_p62)
    gis_with_xpb_only_to_p34                = gis_with_xpb_to_p34.difference(gis_with_xpb_to_p44).difference(gis_with_xpb_to_p62)
    gis_with_xpb_only_to_p62                = gis_with_xpb_to_p62.difference(gis_with_xpb_to_p44).difference(gis_with_xpb_to_p34)
    gis_with_xpb_only_to_p44_and_p34        = gis_with_xpb_to_p44.intersection(gis_with_xpb_to_p34).difference(gis_with_xpb_to_p62)
    gis_with_xpb_only_to_p44_and_p62        = gis_with_xpb_to_p44.intersection(gis_with_xpb_to_p62).difference(gis_with_xpb_to_p34)
    gis_with_xpb_only_to_p34_and_p62        = gis_with_xpb_to_p62.intersection(gis_with_xpb_to_p34).difference(gis_with_xpb_to_p44)
    gis_with_xpb_to_p44_and_p34_and_p62     = gis_with_xpb_to_p62.intersection(gis_with_xpb_to_p44).intersection(gis_with_xpb_to_p34)
    #
    nb_gis_with_xpb_to_p44                  = csgo.get_accumulated_count(gis_with_xpb_to_p44)
    nb_gis_with_xpb_to_p34                  = csgo.get_accumulated_count(gis_with_xpb_to_p34)
    nb_gis_with_xpb_to_p62                  = csgo.get_accumulated_count(gis_with_xpb_to_p62)
    nb_gis_with_xpb_only_to_p44             = csgo.get_accumulated_count(gis_with_xpb_only_to_p44)
    nb_gis_with_xpb_only_to_p34             = csgo.get_accumulated_count(gis_with_xpb_only_to_p34)
    nb_gis_with_xpb_only_to_p62             = csgo.get_accumulated_count(gis_with_xpb_only_to_p62)
    nb_gis_with_xpb_only_to_p44_and_p34     = csgo.get_accumulated_count(gis_with_xpb_only_to_p44_and_p34)
    nb_gis_with_xpb_only_to_p44_and_p62     = csgo.get_accumulated_count(gis_with_xpb_only_to_p44_and_p62)
    nb_gis_with_xpb_only_to_p34_and_p62     = csgo.get_accumulated_count(gis_with_xpb_only_to_p34_and_p62)
    nb_gis_with_xpb_to_p44_and_p34_and_p62  = csgo.get_accumulated_count(gis_with_xpb_to_p44_and_p34_and_p62)
    #
    nb_xpb_implicated                       = nb_gis_with_xpb_only_to_p44 +\
        nb_gis_with_xpb_only_to_p34 +\
        nb_gis_with_xpb_only_to_p62 +\
        nb_gis_with_xpb_only_to_p44_and_p34 +\
        nb_gis_with_xpb_only_to_p44_and_p62 +\
        nb_gis_with_xpb_only_to_p34_and_p62 +\
        nb_gis_with_xpb_to_p44_and_p34_and_p62 
    #
    print " XPB-P44 implied : %5d" % (nb_gis_with_xpb_to_p44)
    print " XPB-P34 implied : %5d" % (nb_gis_with_xpb_to_p34)
    print " XPB-P62 implied : %5d" % (nb_gis_with_xpb_to_p62)
    print " -- "
    print "  XPB implicated in : %5d configurations" % (nb_xpb_implicated)
    nb_xpb_implicated=float(nb_xpb_implicated/100.0)
    print " XPB-P44 only         : %5d (%3.2f%%)" % (nb_gis_with_xpb_only_to_p44 ,nb_gis_with_xpb_only_to_p44/nb_xpb_implicated)
    print " XPB-P34 only         : %5d (%3.2f%%)" % (nb_gis_with_xpb_only_to_p34 ,nb_gis_with_xpb_only_to_p34/nb_xpb_implicated)
    print " XPB-P62 only         : %5d (%3.2f%%)" % (nb_gis_with_xpb_only_to_p62 ,nb_gis_with_xpb_only_to_p62/nb_xpb_implicated)
    print " XPB-P44 XPB-P34 only : %5d (%3.2f%%)" % (nb_gis_with_xpb_only_to_p44_and_p34 ,nb_gis_with_xpb_only_to_p44_and_p34/nb_xpb_implicated) 
    print " XPB-P44 XPB-P62 only : %5d (%3.2f%%)" % (nb_gis_with_xpb_only_to_p44_and_p62 ,nb_gis_with_xpb_only_to_p44_and_p62/nb_xpb_implicated)
    print " XPB-P34 XPB-P62 only : %5d (%3.2f%%)" % (nb_gis_with_xpb_only_to_p34_and_p62 ,nb_gis_with_xpb_only_to_p34_and_p62/nb_xpb_implicated)
    print " XPB linked to all 3  : %5d (%3.2f%%)" % (nb_gis_with_xpb_to_p44_and_p34_and_p62 ,nb_gis_with_xpb_to_p44_and_p34_and_p62/nb_xpb_implicated)
    
    


def print_all_results_per_thresholds( rpt ):
    """
      @param rpt : a dict, results per threshold 
    """

#    # value extraction
#    percent = lambda x:x[1]
#    nb      = lambda x:x[0]

    
    thresholds = sorted(rpt.keys())
    nb_cols = len(thresholds) + 1
    print ">>>", thresholds

    def print_regular_percent_line(tag) :
        res=[]
        for t in thresholds :
#            print ">>> ",t,tag,rpt[t][tag]
            res.append( "{0:6.2f}".format(rpt[t][tag][1]) )
        print "{0:<20s}&".format(tag) + "&".join(res) + r"\\"
        
    def print_cond_percent_line(tag,cond) :
        res=[]
        for t in thresholds :
            res.append( "{0:6.2f}".format(rpt[t][cond][tag][1]) )
        print "{0:<20s}&".format(tag) + "&".join(res) + r"\\"

    def print_regular_nb_line(tag) :
        res=[]
        for t in thresholds :
            res.append( "{0:8d}".format(rpt[t][tag][0]) )
        print "{0:<20s}&".format(tag) + "&".join(res) + r"\\"
        
    def print_cond_nb_line(tag,cond) :
        res=[]
        for t in thresholds :
            res.append( "{0:8d}".format(rpt[t][cond][tag][0]) )
        print "{0:<20s}&".format(tag) + "&".join(res) + r"\\"
        
    def print_table(print_regular_line,print_cond_line):
        print r"\begin{table}"
        print r"\begin{tabular}{|l|"+"r|"*(nb_cols-1)+"}"
        print r"\cline{2-"+str(nb_cols)+"}"
        print r"\multicolumn{1}{c|}{}   & \multicolumn{"+str(nb_cols-1)+r"}{|c|}{threshold}\\"
        print r"\cline{2-"+str(nb_cols)+"}"
        print r"\multicolumn{1}{c|}{}   &","&".join(map (lambda x:str(x),thresholds))+r"\\"
        print r"\hline"
        for k in ["XPB implicated",   
            "P52 implicated",
            "XPB exclusive",
            "P52 exclusive",
            "both XPB and P52",
            "one of XPB or P52",] :
            print_regular_line(k)
        print r"\hline"
        for cond in [
            "under XPB contact",
            "under P52 contact"] :
#            print r" &\multicolumn{"+str(nb_cols-1)+"}{|c|}{"+cond+r"}\\"
            print r" \multicolumn{"+str(nb_cols)+"}{|l|}{"+cond+r"}\\"
            print r"\hline"
            for k in [
                "connection to p44",
                "connection to p34",
                "connection to p62",
                "solely to p44",
                "solely to p34",
                "solely to p62",
                "p44 and p34 only",
                "p44 and p62 only",
                "p34 and p62 only",
                "p44 and p34 and p62"
                ] :
                print_cond_line(k,cond)
            print r"\hline"
        print r"\end{tabular}"
        print r"\caption{}"
        print r"\label{}"
        print r"\end{table}"
        
        print r"\begin{table}"
        print r"\begin{tabular}{|l|"+"r|"*(nb_cols-1)+"}"
        print r"\cline{2-"+str(nb_cols)+"}"
        print r"\multicolumn{1}{c|}{}   & \multicolumn{"+str(nb_cols-1)+r"}{|c|}{threshold}\\"
        print r"\cline{2-"+str(nb_cols)+"}"
        print "\multicolumn{1}{c|}{}   &","&".join(map (lambda x:str(x),thresholds))+r"\\"
        print r"\hline"
        for k in [
            "p44 implicated",
            "p34 implicated",
            "p62 implicated",
            "p44 only",
            "p34 only",
            "p62 only",
            "p44 and p34 solely",
            "p44 and p62 solely",
            "p34 and p62 solely",
            "all three",
            "one of the three"] :
            print_regular_line(k)
        print r"\hline"
        for cond in [
            "under P44 contact",
            "under P34 contact",
            "under P62 contact"] :
#            print r" &\multicolumn{"+str(nb_cols-1)+"}{|c|}{"+cond+r"}\\"
            print r" \multicolumn{"+str(nb_cols)+"}{|l|}{"+cond+r"}\\"
            print r"\hline"
            for k in [        
                "connection to XPB",
                "connection to p52",
                "solely to XPB",
                "solely to p52",
                "both XPB and P52"
                ] :
                print_cond_line(k,cond)
            print r"\hline"
        print r"\end{tabular}"
        print r"\caption{}"
        print r"\label{}"
        print r"\end{table}"
        
    print_table (print_regular_percent_line,print_cond_percent_line)
    print "\n"
    print_table (print_regular_nb_line,print_cond_nb_line)
    
    
    
def load_dist_matrix(tfiihInfos):
    time_start = time()
    try :
        sdms = HGM.helpers.loadPickleDistMatrix(distMatrixFilePath,tfiihInfos)
        print "   loaded subunit dist matrix set from existing pickled file {0:s}".format(distMatrixFilePath)
    except :
        return
    time_stop = time()
    print "  -> dist-matrix loaded in ({0:.1f}s)".format(time_stop-time_start)
    return sdms

def compute_dist_matrix_for_sample_in_file( sampleFilePath, tfiihInfo ):
    mcs         = HGM.representation.MyConfigurationSet(tfiihInfo)
    mcs.read_all_configs_from_file(sampleFilePath)
    print "-- Computing dist matrix",
    pdms = HGM.distances.ParticlesPairDistanceMatrixSet(mcs)
    print "    (",pdms.get_number_of_configurations(),"configurations)"
    print "-- Computing subunits dist matrix",
    sdms = HGM.distances.SubunitsPairDistanceMatrixSet(tfiihInfo,pdms)
    print "    (",sdms.get_number_of_configurations(), "configurations)"
    return sdms

def main():

    m = IMP.Model()
    m.set_log_level(IMP.SILENT)
    
    tfiihInfos = build_TFIIH_subunits_info(m)
    HGM.helpers.mute_all_restraints(m)
    
#    sdms = load_dist_matrix(tfiihInfos)
    sdms = compute_dist_matrix_for_sample_in_file( sampleFilePath, tfiihInfos )
    
    res = {}
#    compute_stats(sdms)
#    thresholds = [1,3,9]
#    thresholds = range(1,10)
    for threshold in thresholds:
        print " * *"
        print " * *  THRESHOLD",threshold
        print " * *"
        res[threshold] = compute_stats_complete(sdms,threshold)
    
    print_all_results_per_thresholds(res)
    
    
    
if __name__ == "__main__" :
    time_start = time()
    main()
    time_stop = time()
    print "All done... (in {0:.1f}s)".format(time_stop-time_start)
    
    
