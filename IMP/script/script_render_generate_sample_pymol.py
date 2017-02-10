
'''

generate pymol trajectories for selected samples
'''

import os

import IMP
import HGM
import HGM.sampling
import HGM.display
import HGM.helpers


from alternate_configs import configs

#
#    PARAMETERS
#
#
#

#config_name_for_this_run    = "fixedGeom_0"
#config_name_for_this_run    = "fixedGeom_1"
#config_name_for_this_run    = "fixedGeom_1_l0"
#config_name_for_this_run    = "fixedGeom_1_1"
#config_name_for_this_run    = "test_fixedGeom_1_1"
#config_name_for_this_run    = "test_fixedGeom_1_2"
#config_name_for_this_run    = "test_fixedGeom_1_3"
#config_name_for_this_run    = "fixedGeom_EM_1_0"
#config_name9_for_this_run    = "fixedGeom_EM_1_1"
#config_name_for_this_run    = "fixedGeom_EM_1_2"

#config_name_for_this_run    = "arp_EM_0_1"
#config_name_for_this_run    = "arp_EM_0_2"

#config_name_for_this_run    = "arp_EM_0_2FRET"
#config_name_for_this_run    = "arp_EM_0_2aLFc4"
#config_name_for_this_run    = "arp_EM_0_2aLMs"

#config_name_for_this_run    = "3NIG_EM_0_2aC"                  
#config_name_for_this_run    = "3NIG_EM_0_2aC_20"     
#config_name_for_this_run    = "3NIG_EM_0_2lmC"
#config_name_for_this_run    = "3NIG_EM_0_2lmC_20"
#config_name_for_this_run    = "3NIG_EM_0_2lC"
#config_name_for_this_run    = "3NIG_EM_0_2lC_20" 
#config_name_for_this_run    = "3NIG_EM_0_3ambiC"  
#config_name_for_this_run    = "3NIG_EM_0_3ambiC_20"
        
#config_name_for_this_run    = "3NIG_EM_0_2aC_f"

#config_name_for_this_run    = "3NIG_EM_0_5a_f_20"

#config_name_for_this_run    = "3NIG_EM_0_2lCF_1"
config_name_for_this_run    = "3NIG_EM_0_2lC_f"

#config_name_for_this_run    = "3IAM_EM_0_1aC"
#config_name_for_this_run    = "3IAM_EMc_0_1aC"
#config_name_for_this_run    = "3IAM_EM_0_2aC"
#config_name_for_this_run    = "3IAM_EMc_0_2aC"

#config_name_for_this_run    = "3IAM_EM_0_3a"
#config_name_for_this_run    = "3IAM_EM_0_3lm"
#config_name_for_this_run    = "3IAM_EM_0_3l"

#config_name_for_this_run    = "3IAM_EM_0_4a"
#config_name_for_this_run    = "3IAM_EM_0_4lm"
#config_name_for_this_run    = "3IAM_EM_0_4l"

#config_name_for_this_run    = "3IAM_EM_0_5a"
#config_name_for_this_run    = "3IAM_EM_0_5lm"
#config_name_for_this_run    = "3IAM_EM_0_5l"

#config_name_for_this_run    = "3IAM_EM_0_6aV2"


#config_name_for_this_run    = "4FXG_EM_0_1a_40"
#config_name_for_this_run    = "4FXG_EM_0_1lm_40"
#config_name_for_this_run    = "4FXG_EM_0_1l_40"
#config_name_for_this_run    = "4FXG_EM_0_1a_30"
#config_name_for_this_run    = "4FXG_EM_0_1lm_30"
#config_name_for_this_run    = "4FXG_EM_0_1l_30"
#config_name_for_this_run    = "4FXG_EM_0_1a_20"
#config_name_for_this_run    = "4FXG_EM_0_1lm_20"
#config_name_for_this_run    = "4FXG_EM_0_1l_20"

subunitsRepresentationFileName = configs[config_name_for_this_run][0]
runDir                      = os.path.join("results",config_name_for_this_run)
saveDirSample               = os.path.join(runDir,"samples")
asDir                       = os.path.join(runDir,"samples-alt")
cDir                        = os.path.join(runDir,"clusters")
dDir                        = "/home/arnaud/Desktop/TFIIH/data/3NIG/"
gDir   = os.path.join(runDir,"graphics")
varDir = os.path.join(gDir,"RMSD_variation_study")
savePrefix                  = "saves"
#savePrefix                  = "saves-concat"
pymolDir                    = os.path.join(runDir,"pymol")
pymolFilePrefix             = "sample"

for d in [pymolDir] :
    HGM.helpers.check_or_create_dir(d)

#
#    Sample configuration
#

#sample_indexes      = [3,33]
#sample_indexes=[0]
#sample_indexes      = range(100,105)
#sample_indexes      = [0,]
#sample_indexes      = [37]
#sample_indexes       = [36,39]
#sample_indexes      = range(20,25)
#sample_indexes      = [73]
#sample_indexes      = [21]
#sample_indexes      = [35,54,19,83,112,5,27,21]
#sample_indexes      = [360]
#sample_indexes      = [779]
#sample_indexes      = [300]
#sample_indexes      = [816]
#sample_indexes      = [119,613,174,948,803,67,582,295,241]
#sample_indexes      = [241,261,7,732,267] 

#sample_indexes=[55,130,90,62,47,178]
#sample_indexes=[253,211,270,202,289,263]
#sample_indexes=[304,300,303,307]
#sample_indexes = range(310,315)
#sample_indexes=[1]

best_scores_112_10     = ['19:49', '42:48', '43:48', '30:35', '66:14', '5:0', '81:2', '64:0', '12:21', '128:19']
best_scores_112_50     = ['19:49', '42:48', '43:48', '30:35', '66:14', '5:0', '81:2', '64:0', '12:21', '128:19', '45:40', '148:8', '136:26', '4:11', '30:12', '79:0', '140:21', '16:0', '101:19', '74:39', '124:2', '53:44', '97:5', '170:40', '171:40', '120:7', '65:32', '116:28', '181:30', '161:0', '66:47', '125:22', '91:37', '82:7', '61:44', '94:43', '83:0', '66:40', '49:19', '65:44', '37:48', '19:38', '68:0', '148:1', '26:49', '116:41', '5:29', '49:0', '127:36', '13:49']
best_scores_112_200    = ['19:49', '42:48', '43:48', '30:35', '66:14', '5:0', '81:2', '64:0', '12:21', '128:19', '45:40', '148:8', '136:26', '4:11', '30:12', '79:0', '140:21', '16:0', '101:19', '74:39', '124:2', '53:44', '97:5', '170:40', '171:40', '120:7', '65:32', '116:28', '181:30', '161:0', '66:47', '125:22', '91:37', '82:7', '61:44', '94:43', '83:0', '66:40', '49:19', '65:44', '37:48', '19:38', '68:0', '148:1', '26:49', '116:41', '5:29', '49:0', '127:36', '13:49', '10:23', '59:10', '19:10', '75:30', '80:0', '58:0', '120:18', '74:17', '93:24', '76:1', '7:11', '95:44', '100:7', '95:4', '89:5', '137:20', '116:38', '66:15', '136:8', '72:7', '63:38', '120:25', '125:31', '45:6', '91:1', '33:49', '1:31', '60:14', '29:17', '126:40', '86:2', '4:46', '69:10', '136:22', '27:0', '28:0', '128:47', '151:15', '76:37', '54:47', '127:26', '169:41', '19:8', '51:44', '56:45', '114:37', '98:35', '169:24', '90:0', '45:29', '120:31', '30:15', '115:0', '158:37', '49:33', '90:7', '97:23', '92:35', '101:22', '41:14', '181:33', '128:23', '75:26', '29:18', '11:44', '66:28', '58:29', '135:41', '6:0', '57:39', '59:11', '78:4', '23:49', '24:49', '55:36', '140:29', '74:1', '55:10', '120:23', '91:12', '64:18', '32:7', '82:3', '100:9', '91:38', '116:42', '7:3', '99:43', '128:0', '63:25', '16:19', '99:30', '19:20', '64:11', '116:8', '126:35', '100:27', '97:30', '69:29', '103:30', '32:19', '98:49', '137:35', '137:43', '120:10', '51:14', '57:8', '11:41', '103:0', '170:43', '171:43', '136:11', '1:29', '99:31', '51:26', '56:33', '27:18', '28:18', '135:9', '1:36', '32:0', '7:28', '56:37', '150:36', '103:9', '12:49', '97:13', '165:0', '99:33', '13:16', '41:5', '97:24', '138:16', '137:27', '3:0', '96:36', '169:6', '128:22', '62:34', '8:11', '9:11', '148:14', '137:17', '181:26', '92:33', '150:20', '6:10', '79:3', '3:48', '125:32']
worst_scores_112_10    = ['59:18', '75:36', '74:2', '51:12', '91:32', '86:4', '105:7', '106:7', '30:47', '98:34']
worst_scores_112_50    = ['93:19', '11:47', '63:22', '62:44', '78:21', '37:9', '137:34', '10:20', '47:28', '48:28', '86:47', '91:6', '41:12', '87:34', '88:34', '5:40', '89:32', '127:5', '69:14', '32:4', '55:49', '158:12', '6:22', '135:19', '86:39', '27:39', '28:39', '116:12', '32:17', '125:48', '72:3', '63:17', '53:49', '81:25', '53:16', '79:18', '127:47', '1:23', '125:29', '93:38', '59:18', '75:36', '74:2', '51:12', '91:32', '86:4', '105:7', '106:7', '30:47', '98:34']
worst_scores_112_200   = ['75:18', '15:23', '75:13', '65:3', '66:45', '82:36', '79:48', '127:20', '103:44', '87:19', '88:19', '98:11', '56:4', '6:49', '165:33', '120:4', '93:7', '97:45', '81:48', '54:40', '53:37', '82:18', '76:34', '59:49', '120:24', '32:26', '120:12', '62:7', '47:33', '48:33', '12:4', '120:41', '29:45', '115:25', '5:2', '66:13', '181:3', '8:49', '9:49', '42:1', '43:1', '53:23', '10:21', '158:19', '15:27', '53:9', '54:38', '54:4', '54:31', '12:32', '4:3', '12:28', '59:19', '115:3', '8:43', '9:43', '92:7', '135:28', '114:41', '136:21', '32:38', '10:47', '63:43', '4:10', '52:21', '85:42', '68:15', '83:26', '58:28', '7:27', '181:14', '33:37', '126:28', '76:8', '16:29', '15:39', '47:11', '48:11', '5:30', '150:17', '103:27', '161:49', '49:48', '87:25', '88:25', '70:43', '140:30', '65:6', '69:43', '101:35', '78:46', '3:32', '140:16', '37:8', '68:27', '1:8', '165:41', '99:16', '94:16', '12:42', '65:18', '126:9', '101:33', '13:14', '148:18', '113:33', '4:15', '158:13', '72:24', '66:12', '181:5', '99:26', '72:8', '71:44', '93:21', '68:45', '33:7', '85:17', '69:35', '32:36', '29:14', '125:19', '26:28', '105:2', '106:2', '63:35', '66:48', '70:17', '103:47', '23:21', '24:21', '69:4', '86:6', '19:2', '74:26', '82:42', '116:0', '80:46', '67:8', '96:13', '165:36', '60:29', '6:20', '5:11', '135:15', '101:6', '83:38', '3:28', '148:12', '1:45', '93:19', '11:47', '63:22', '62:44', '78:21', '37:9', '137:34', '10:20', '47:28', '48:28', '86:47', '91:6', '41:12', '87:34', '88:34', '5:40', '89:32', '127:5', '69:14', '32:4', '55:49', '158:12', '6:22', '135:19', '86:39', '27:39', '28:39', '116:12', '32:17', '125:48', '72:3', '63:17', '53:49', '81:25', '53:16', '79:18', '127:47', '1:23', '125:29', '93:38', '59:18', '75:36', '74:2', '51:12', '91:32', '86:4', '105:7', '106:7', '30:47', '98:34']


subsample_indices   = best_scores_112_200
subsample_indices   = worst_scores_112_200 

pymolFileName_best_scores_112       = "configs_best_scores_112_200.pym"
pymolFileName_worst_scores_112      = "configs_worst_scores_112_200.pym"
pymolFileName       = pymolFileName_best_scores_112
pymolFileName       = pymolFileName_worst_scores_112

pymolFilePath       = os.path.join(pymolDir,pymolFileName)



#
#    dir and name of specific samples for which I want a pymol file
#
caDir   = os.path.join(cDir,"cluster_samples_centroid_file-15-meth:complete low-1000")
sampleFilePathes    = [
#        (asDir,"low_rmsd_subsamples__0-10__100.txt"),
#        (asDir,"high_rmsd_subsamples__0-10__100.txt"),
#        (asDir,"high_energy_subsamples__0-20__100.txt"),
#         (asDir,"low_energy_subsamples__0-50__1000.txt")
#        (varDir,"centroid_structure.txt")
#        (dDir,"save-3IAM-HGM.txt")
        (caDir,"id_clust_12.txt"),
#        (caDir,"id_clust_2.txt"),
#        (caDir,"id_clust_3.txt"),
#        (caDir,"id_clust_4.txt"),
#        (caDir,"id_clust_5.txt"),
#        (caDir,"id_clust_15.txt"),
#        (caDir,"id_clust_20.txt"),
#        (caDir,"id_clust_433.txt"),
        #(saveDirSample,'saves--100.txt')
        ]




#    import the function responsible for modelisation of TFIIH complex
#exec ( "from {0:s} import build_TFIIH_subunits_info".format( tfiihRepresentationFileName ) )
#    import the function responsible for display of TFIIH complex

exec ( "from {0:s} import build_subunits_info".format( subunitsRepresentationFileName ) )
#from representation_TFIIH_display import get_TFIIH_imp_colors
#from representation_ARP_display import get_ARP_imp_colors
from representation_3NIG_display import get_3NIG_imp_colors
#from representation_3IAM_display import get_3IAM_imp_colors
#from representation_4FXG_display import get_4FXG_imp_colors


def fetch_and_render_pymol_for_full_sample_by_index(sample_indexes,renderer,tfiihInfos) :
    mcs         = HGM.representation.MyConfigurationSet(tfiihInfos)
    for i in sample_indexes:
        print i,"..",
        saveName        = savePrefix+"--"+str(i)+".txt"
        mcs.read_all_configs_from_file(os.path.join(saveDirSample,saveName))
        pymolFileName   = pymolFilePrefix + "--" + str(i) + ".pym"
    #        pymolFileName   = pymolFilePrefix + "--" + str(i)
        renderer.write_configuration_set_to_pymol_file(mcs, os.path.join(pymolDir, pymolFileName))
        mcs.delete_all_configs()
        
def fetch_and_render_pymol_for_subsample(subsample_indices,renderer,pymolFilePath,tfiihInfos) :
    mcs         = HGM.representation.MyConfigurationSet(tfiihInfos)
    for idx in subsample_indices :
        i,si = map( int, idx.split(":"))
        fileName        = savePrefix+"--"+str(i)+".txt"
        filePath        = os.path.join(saveDirSample,fileName)
        mcs.read_configs_from_file(filePath, [si])
    renderer.write_configuration_set_to_pymol_file( mcs , pymolFilePath )
    
def fetch_and_render_pymol_for_named_samples(sampleFilePathes,renderer,subunitsInfos):
    """
    @param sampleFilePathes: list of pairs : Directory, save file path
    """
    mcs         = HGM.representation.MyConfigurationSet(subunitsInfos)
    for fd,fn in sampleFilePathes :
        mcs.read_all_configs_from_file(os.path.join(fd,fn))
        pymolFileName   = fn[:-4]+".pym"
        print "treating",pymolFileName
    #        pymolFileName   = pymolFilePrefix + "--" + str(i)
        renderer.write_configuration_set_to_pymol_file(mcs, os.path.join(pymolDir, pymolFileName))
        mcs.delete_all_configs()

def main():
    
        
    m = IMP.Model()
    m.set_log_level(IMP.SILENT)

    subunitsInfos = build_subunits_info(m)
    HGM.helpers.mute_all_restraints(m)

#    subunit_imp_color_dict = get_TFIIH_imp_colors()
    subunit_imp_color_dict = get_3NIG_imp_colors()
#    subunit_imp_color_dict = get_3IAM_imp_colors()
#    subunit_imp_color_dict = get_4FXG_imp_colors()
    renderer = HGM.display.ModelRenderer(subunitsInfos)
    renderer.set_subunit_colors(subunit_imp_color_dict)
    
#    print "-- read samples and create pymol"
#    fetch_and_render_pymol_for_full_sample_by_index(sample_indexes,renderer,subunitsInfos)

#    print "-- read subsamples and create pymol"
#    fetch_and_render_pymol_for_subsample(subsample_indices,renderer,pymolFilePath,subunitsInfos)
    
    print "-- read specific samples and create pymol"
    fetch_and_render_pymol_for_named_samples(sampleFilePathes,renderer,subunitsInfos)
    
    
        
if __name__ == "__main__" :
    main()
    print "...Finished !"
