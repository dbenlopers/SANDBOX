'''

'''
import IMP
import HGM, HGM.representation, HGM.display
#from representation_TFIIH_models_arnaud1 import build_TFIIH_subunits_info
#from representation_TFIIH_models_arnaud2 import build_TFIIH_subunits_info
from representation_TFIIH_models_arnaud3 import build_TFIIH_subunits_info 
from representation_TFIIH_display import get_TFIIH_imp_colors




#print "Create subunits in model, along with intra subunit connectivity"
#all                     = representation.create_TFIIH_representation(m,protein_info_dict)

#configsFileName         = "./scrap2/MD/samplesSaves/TFIIH-sample-MD---BBs(200)(CG)--Berendsen-T(1000)-tau(100)-nbSteps(20000)-saveStep(100)--sample-size-200--0.txt"
#pymolFileName           = "./scrap2/MD/pymolDisplay/TFIIH-sample-MD---BBs(200)(CG)--Berendsen-T(1000)-tau(100)-nbSteps(20000)-saveStep(100)--sample-size-200--0.pym"

#configsFileName         = "./scrap2/MD/samplesSaves/TFIIH-2-sample-MD---BBs(200)(CG)--Berendsen-T(300)-tau(100)-nbSteps(20000)-saveStep(100)--sample-size-200--0.txt"
#pymolFileName           = "./scrap2/MD/pymolDisplay/TFIIH-2-sample-MD---BBs(200)(CG)--Berendsen-T(300)-tau(100)-nbSteps(20000)-saveStep(100)--sample-size-200--0.pym"

configsFileName         = "./scrap2/MD/samplesSaves/TFIIH-3--sample-MD---BBs(200)(CG)--Berendsen-T(300)-tau(100)-nbSteps(20000)-saveStep(100)--sample-size-200--0.txt"
pymolFileName           = "./scrap2/MD/pymolDisplay/TFIIH-3--sample-MD---BBs(200)(CG)--Berendsen-T(300)-tau(100)-nbSteps(20000)-saveStep(100)--sample-size-200--0.pym"

#configsFileName         = "./scrap2/MD/samplesSaves/TFIIH-sample-MD---BBs(200)(CG)--Berendsen-T(300)-tau(100)-nbSteps(20000)-saveStep(100)--sample-size-200--0.txt"
#pymolFileName           = "./scrap2/MD/pymolDisplay/TFIIH-sample-MD---BBs(200)(CG)--Berendsen-T(300)-tau(100)-nbSteps(20000)-saveStep(100)--sample-size-200--0.pym"

if __name__ == "__main__" :
    print "Create IMP model"
    m           = IMP.Model()
    m.set_log_level(IMP.SILENT)
    
    print "-- create and crowd my TFIIH universe"
    tfiihInfo = build_TFIIH_subunits_info(m)
    
    subunit_imp_color_dict = get_TFIIH_imp_colors()
    renderer = HGM.display.ModelRenderer(tfiihInfo)
    renderer.set_subunit_colors(subunit_imp_color_dict)
    
    
    print "read configurations from config file {0:s} to init my TFIIH universe".format(configsFileName)
    mcs         = HGM.representation.MyConfigurationSet(tfiihInfo)
    mcs.read_all_configs_from_file(configsFileName)
    #mcs.read_configs_from_file(configsFileName,range(100))
    print "...got",mcs.get_number_of_configurations(),"configurations"
    
    print "saving configurations to",pymolFileName
    renderer.write_configuration_set_to_pymol_file(mcs, pymolFileName)
    
    print "...all done !"
    
