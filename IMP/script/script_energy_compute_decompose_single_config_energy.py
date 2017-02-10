'''

'''

import os
import sys
import re

import time

import IMP
import HGM
import HGM.energies
#import HGM.sampling
#import HGM.display

import HGM.helpers
#import HGM.helpersPlot

from alternate_configs import configs
#    MY TFIIH REPRESENTATION
#config_name_for_this_run    = "fixedGeom_0"
#config_name_for_this_run    = "fixedGeom_1_godzilla"
#config_name_for_this_run    = "fixedGeom_1"
#config_name_for_this_run    = "fixedGeom_1_1"
#config_name_for_this_run    = "test_fixedGeom_1_1"
#config_name_for_this_run    = "test_fixedGeom_1_2"
#config_name_for_this_run    = "test_fixedGeom_1_3"
#config_name_for_this_run    = "fixedGeom_EM_1_0"
#config_name_for_this_run    = "fixedGeom_EM_1_1"
#config_name_for_this_run    = "fixedGeom_EM_1_2"

#config_name_for_this_run    = "arp_EM_0_1"
#config_name_for_this_run    = "arp_EM_0_2"

#config_name_for_this_run    = "arp_EM_0_2a"
#config_name_for_this_run    = "arp_EM_0_2aLM"
#config_name_for_this_run    = "arp_EM_0_2aL"

#config_name_for_this_run    = "arp_EM_0_2aLFc1"
#config_name_for_this_run    = "arp_EM_0_2aLFRET1"
#config_name_for_this_run    = "arp_EM_0_2aLFc4"
#config_name_for_this_run    = "arp_EM_0_2aLFc5"
#config_name_for_this_run    = "arp_EM_0_2aLFc3"
#config_name_for_this_run    = "arp_EM_0_2aLFc2"

#config_name_for_this_run    = "arp_EM_0_2Fc1"
#config_name_for_this_run    = "arp_EM_0_2Fc3"
#config_name_for_this_run    = "arp_EM_0_2Fc4"
##config_name_for_this_run    = "arp_EM_0_2F2"
##config_name_for_this_run    = "arp_EM_0_2F3"
          
#config_name_for_this_run    = "arp_EM_0_2FRET1"


#config_name_for_this_run    = "arp_EM_0_2aLA1"
#config_name_for_this_run    = "arp_EM_0_2aLA2"
#config_name_for_this_run    = "arp_EM_0_2aLA3"
#config_name_for_this_run    = "arp_EM_0_2aLA"
#config_name_for_this_run    = "arp_EM_0_2aLA5"
#config_name_for_this_run    = "arp_EM_0_2aLA6"
#config_name_for_this_run    = "arp_EM_0_2aLA7"
#config_name_for_this_run    = "arp_EM_0_2aLA8"

#config_name_for_this_run    = "arp_EM_0_2aLAI2"

#config_name_for_this_run    = "arp_EM_0_2aLFc1Fc3"
#config_name_for_this_run    = "arp_EM_0_2aLMe1"
#config_name_for_this_run    = "arp_EM_0_2aLMe2"
#config_name_for_this_run    = "arp_EM_0_2aLMe3"

#config_name_for_this_run    = "arp_EMd_0_2a"
#config_name_for_this_run    = "arp_EMd_0_2aLM"
#config_name_for_this_run    = "arp_EMd_0_2aL"

#config_name_for_this_run    = "arp_EMd_0_2aLFc1"
#config_name_for_this_run    = "arp_EMd_0_2aLFc2"
#config_name_for_this_run    = "arp_EMd_0_2aLFc3"
#config_name_for_this_run    = "arp_EMd_0_2aLFc4"
#config_name_for_this_run    = "arp_EMd_0_2aLFc5"
#config_name_for_this_run    = "arp_EMd_0_2aLFc1Fc3"


#config_name_for_this_run    = "4FXG_EM_0_1a_40"
#config_name_for_this_run    = "4FXG_EM_0_1lm_40"
#config_name_for_this_run    = "4FXG_EM_0_1l_40"

config_name_for_this_run    = "4FXG_EM_0_2a_40"
#config_name_for_this_run    = "4FXG_EM_0_2lm_40"
#config_name_for_this_run    = "4FXG_EM_0_2l_40"

#
#    PARAMETERS
#
#
#
currentRepresentationFileName = configs[config_name_for_this_run][0]
#runDir                      = os.path.join("Users","schwarz","Dev","TFIIH","src","coarse2","results",config_name_for_this_run)
runDir                      = os.path.join("results",config_name_for_this_run)
saveDirSample               = os.path.join(runDir,"samples")
savePrefix                  = "saves"

#eDir                        = os.path.join(runDir,"energies")
#eFileName                   = "sample-energies.txt"
#eStatFileName               = "sample-energy-stats.txt"
#eStatsortedFileName         = "sample-energy-stats-sorted.txt"

lDir                        = os.path.join(runDir,"LaTex")
laTeX_fileName              = config_name_for_this_run +"--score-solution.tex"
laTeX_filePath              = os.path.join(lDir,laTeX_fileName)

hDir                        = os.path.join(runDir,"html")
hsDir                       = os.path.join(hDir,"subDocs")
html_fileName               = config_name_for_this_run +"score-solution--html-table.txt"
html_filePath               = os.path.join(hsDir,html_fileName)

#for d in [eDir] :
for d in [lDir,hDir,hsDir] :
    HGM.helpers.check_or_create_dir(d)

#
#    Sample configuration
#
#sample_indexes      = range(25)

#sample_indexes      = range(100,150)
#sample_indexes      = range(100,187)

#sample_indexes      = range(100)
#sample_indexes      = range(130)
#sample_indexes      = range(10)
#sample_indexes      = range(3000)
#sample_indexes      = range(1000)
#sample_indexes      = range(1010,1020)
#sample_indexes      = range(310,322)
#sample_indexes      = range(322);sample_indexes.append(1000)
#sample_indexes      = [300]
sample_indexes      = HGM.helpers.read_all_sample_indices(saveDirSample,savePrefix)



#    import the function responsible for modelisation of TFIIH complex
#exec ( "from {0:s} import build_TFIIH_subunits_info".format( tfiihRepresentationFileName ) )
exec ( "from {0:s} import build_subunits_info".format( currentRepresentationFileName ) )


energyTypes = ["Total","Clashes","Cohesion","Contacts","EM","Location","Fret"]

def compute_current_decomposed_energies(cplxInfos):
    results = []
    se   = cplxInfos.get_model().evaluate(False)
    results.append( ("Total",se) )
    sevr = cplxInfos.evr.evaluate(False)
    results.append( ("Clashes",sevr) )
    sstr = sum ( map( ( lambda r:r.evaluate(False)) , cplxInfos.str ) )
    results.append( ("Cohesion",sstr) )
    sscr = sum ( map( ( lambda r:r.evaluate(False)) , cplxInfos.scr ) )
    results.append( ("Contacts",sscr) )
    semr = cplxInfos.emr.evaluate(False)
    results.append( ("EM",semr) )
    try :
        locr = cplxInfos.locr.evaluate(False)
        results.append( ("Location",locr) )
    except :
#        results.append(("Location",-0.0))
        pass
    try :
        fdr = cplxInfos.fdr.evaluate(False)
        results.append( ("Fret",fdr) )
    except :
#        results.append(("Fret",-0.0))
        pass
    return results


def get_current_decomposed_energies_as_dict(cplxInfos):
    results = {}
    se   = cplxInfos.get_model().evaluate(False)
    results["Total"]=se
    sevr = cplxInfos.evr.evaluate(False)
    results["Clashes"]=sevr
    sstr = sum ( map( ( lambda r:r.evaluate(False)) , cplxInfos.str ) )
    results["Cohesion"]=sstr
    sscr = sum ( map( ( lambda r:r.evaluate(False)) , cplxInfos.scr ) )
    results["Contacts"]=sscr
    semr = cplxInfos.emr.evaluate(False)
    results["EM"]=semr
    try :
        locr = cplxInfos.locr.evaluate(False)
        results["Location"]=locr
    except :
#        results.append(("Location",-0.0))
        pass
    try :
        fdr = cplxInfos.fdr.evaluate(False)
        results["Fret"]=fdr
    except :
#        results.append(("Fret",-0.0))
        pass
    return results


def get_latex_table_for_energies(ed,caption="",label=""):
    nb_e = len(ed.keys())
    _tags,_values=[],[]
    for t in energyTypes :
        try :
            v = ed[t]
            _tags.append(t)
            _values.append(v)
        except :
            pass
    res = \
    "\n".join( [r"\begin{table}[htbp!]",r"\centering",
#                r"{\scriptsize",
    r"\begin{tabular}{|"+"r|"*nb_e +"}",
    r"\hline",
    "&".join(_tags)+r"\\",r"\hline",
    "&".join( map( lambda x:"{0:8.2f}".format(x) , _values ))+r"\\",
    r"\hline",r"\end{tabular}",
    r"\caption{" + caption +"}",
    r"\label{" + label +"}",
    r"\end{table}"
    ])
    return res
    #    print "&".join(map( lambda x:"{1:8.2f}".format(*x) , el ))+r"\\"


def get_html_table_for_energies(ed,caption="",label=""):
    nb_e = len(ed.keys())
    _tags,_values=[],[]
    for t in energyTypes :
        try :
            v = ed[t]
            _tags.append(t)
            _values.append(v)
        except :
            pass
    res = \
    "\n".join( [r"<TABLE>",
    ("<TR><TD>"+"</TD><TD>".join(_tags)+r"</TD></TR>"),
    ("<TR><TD>"+"</TD><TD>".join( map( lambda x:"{0:8.2f}".format(x) , _values ))+r"</TD></TR>"),
    r"</TABLE>"]
    )
    return res
    #    print "&".join(map( lambda x:"{1:8.2f}".format(*x) , el ))+r"\\"
    
def get_latex_table_two_columns(pairs_list,caption="",label=""):
    
    if not pairs_list : # implicit boolean conversion to False for empty lists
        return ""
    else :
        return \
        "\n".join( [r"\begin{table}[htbp!]",r"\centering",
#                    r"{\scriptsize",
        r"\begin{tabular}{|c|c|}",
        r"\hline",r"restraint&value\\",r"\hline"]+
        map( lambda p: "{0}&  {1:8.2f}\\\\".format(*p), pairs_list)+
        [r"\hline",r"\end{tabular}",
        r"\caption{" + caption +"}",
        r"\label{" + label +"}",
        r"\end{table}"]
        )

def get_html_table_two_columns(pairs_list,caption="",label=""):
    
    if not pairs_list : # implicit boolean conversion to False for empty lists
        return ""
    else :
        return \
        "\n".join( [r"<TABLE>",
        r"<TR><TD>restraint</TD><TD>value</TD></TR>"]+
#        map( lambda p: "<TR>\n<TD>{0}</TD><TD>{1:8.2f}</TD>\n</TR>".format(*p), pairs_list)+
        map( lambda p: "<TR><TD>{0}</TD><TD>{1:8.2f}</TD></TR>".format(*p), pairs_list)+
        [r"</TABLE>"]
        )


def output_energies_decomposition(cplxInfos):
#    se   = tfiihinfo.get_model().evaluate(False)
#    sevr = tfiihinfo.evr.evaluate(False)
#    sstr = sum ( map( ( lambda r:r.evaluate(False)) , tfiihinfo.str ) )
#    sscr = sum ( map( ( lambda r:r.evaluate(False)) , tfiihinfo.scr ) )
#    semr = tfiihinfo.emr.evaluate(False)
##    print "[total-energy:{0:10.2f}] sub-cohes:{1:10.2f} sub-inter:{2:10.2f} excl-vol:{3:10.2f} EM:{4:10.2f}".format(
##           se , sstr, sscr, sevr, semr )
#    fdr = tfiihinfo.fdr.evaluate(False)
#    print "[total-energy:{0:10.2f}] sub-cohes:{1:10.2f} sub-inter:{2:10.2f} excl-vol:{3:10.2f} EM:{4:10.2f} FRET:{5:10.2f}".format(
#           se , sstr, sscr, sevr, semr, fdr )
#    el = compute_current_decomposed_energies(cplxInfos)
    ed = get_current_decomposed_energies_as_dict(cplxInfos)
    el = ed.iteritems()
    print "===== energy per type"
    print " ".join(map( lambda x:"{0}:{1:10.2f}".format(*x) , el ))
#    print "== LaTex table line"
#    print "&".join(map( lambda x:"{1:8.2f}".format(*x) , el ))+r"\\"
#    tab=get_latex_table_for_energies(ed)
#    print tab
    
    print "  ===== decomposing interaction restraint ( diff subunits ) ====="
    threshold=0.0
#    tab_scr=get_latex_table_two_columns(filter ( lambda x:x[1] > threshold, [ (r.get_name(),r.evaluate(False)) for r in cplxInfos.scr ]))
    for e in filter ( lambda x:x[1] > threshold, [ (r.get_name(),r.evaluate(False)) for r in cplxInfos.scr ]) :
        print "   {0:>30s} ---> {1:10.2f}".format(*e)
#    print tab_scr

    print "  ===== decomposing cohesion restrain (same subunit) ====="
    threshold=0.0
#    tab_str=get_latex_table_two_columns(filter ( lambda x:x[1] > threshold, [ (r.get_name(),r.evaluate(False)) for r in cplxInfos.str ]))
    for e in filter ( lambda x:x[1] > threshold, [ (r.get_name(),r.evaluate(False)) for r in cplxInfos.str ]) :
        print "   {0:>30s} ---> {1:10.2f}".format(*e)
#    print tab_str
    
    
def dump_latex_energies_decomposition(cplxInfos,filePath):
    
    latexify = lambda s:re.sub('_',r'\_',s)
    
    run_name = latexify(config_name_for_this_run)
    run_label= config_name_for_this_run
    ed = get_current_decomposed_energies_as_dict(cplxInfos)
    tab=get_latex_table_for_energies(ed,
        caption=("Score decomposition in the solution model for representation "+run_name),
        label=("tab.score.solution.total."+run_label) )
    threshold=0.0
    tab_str=get_latex_table_two_columns(\
        filter ( lambda x:x[1] > threshold, [ (r.get_name(),r.evaluate(False)) for r in cplxInfos.str ]),
        caption = "Cohesion restraint penalty in the solution model for representation "+run_name,
        label   = "tab.score.solution.cohesion"+run_label
    )
    tab_scr=get_latex_table_two_columns(\
        filter ( lambda x:x[1] > threshold, [ (r.get_name(),r.evaluate(False)) for r in cplxInfos.scr ]),
        caption = "Interaction restraint penalty in the solution model for representation "+run_name,
        label   = "tab.score.solution.interaction"+run_label
    )
    
    fd=open(filePath,"w")
    fd.write("\n\n".join([tab,tab_str,tab_scr,""]))
    fd.close()
    
def  dump_html_energies_decomposition(cplxInfos,filePath):
    
    ed = get_current_decomposed_energies_as_dict(cplxInfos)
    tab=get_html_table_for_energies(ed)
    threshold=0.0
    tab_str=get_html_table_two_columns(\
        filter ( lambda x:x[1] > threshold, [ (r.get_name(),r.evaluate(False)) for r in cplxInfos.str ])
    )
    tab_scr=get_html_table_two_columns(\
        filter ( lambda x:x[1] > threshold, [ (r.get_name(),r.evaluate(False)) for r in cplxInfos.scr ])
    )
#    print "\n\n".join([tab,tab_str,tab_scr,""])
    fd=open(filePath,"w")
    fd.write("\n\n".join([tab,tab_str,tab_scr,""]))
    fd.close()
    
    
def main():
        
    m = IMP.Model()
    m.set_log_level(IMP.SILENT)
#    tfiihInfos = build_TFIIH_subunits_info(m)
    cplxInfos = build_subunits_info(m)
    HGM.helpers.mute_all_restraints(m)
    
    dataDirSample   = "../../data/ARP"
    sampleFileName  = "save-1TYQ-HGM.txt"
    sampleFilePath  = os.path.join(dataDirSample,sampleFileName)
    
    mcs         = HGM.representation.MyConfigurationSet(cplxInfos)
    mcs.read_all_configs_from_file(sampleFilePath)
    mcs.load_configuration(0)
    print m.evaluate(False)
    
    output_energies_decomposition(cplxInfos)
    
    dump_latex_energies_decomposition(cplxInfos,laTeX_filePath)
    dump_html_energies_decomposition(cplxInfos,html_filePath)
        
if __name__ == "__main__" :
    main()
    print "...Finished !"
    
