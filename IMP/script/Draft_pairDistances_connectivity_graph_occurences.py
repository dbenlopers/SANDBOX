'''
Created on end mars 2013
    script based on Script_pairDistances_connectivity_graph_occurences.py made by Ben
    Output : latex table or html
@author: kopp
'''
import os
import getpass
import IMP
import HGM
import HGM.distances, HGM.helpers
import time 

import numpy as N
import pylab as P

from alternate_configs import configs
#    MY TFIIH REPRESENTATION
# config_name_for_this_run    = "3NIG_EM_0_2aC"                  
# config_name_for_this_run    = "3NIG_EM_0_2aC_20"     
# config_name_for_this_run    = "3NIG_EM_0_2lmC"
# config_name_for_this_run    = "3NIG_EM_0_2lmC_20"
# config_name_for_this_run    = "3NIG_EM_0_2lC"
# config_name_for_this_run    = "3NIG_EM_0_2lC_20" 
# config_name_for_this_run    = "3NIG_EM_0_3ambiC"  
# config_name_for_this_run    = "3NIG_EM_0_3ambiC_20"
        

# config_name_for_this_run        = "arp_EM_0_2aLA"

# config_name_for_this_run    = "3IAM_EM_0_3a"
# config_name_for_this_run    = "3IAM_EM_0_3lm"
# config_name_for_this_run    = "3IAM_EM_0_3l"

# config_name_for_this_run    = "3IAM_EM_0_4a"
# config_name_for_this_run    = "3IAM_EM_0_4lm"
# config_name_for_this_run    = "3IAM_EM_0_4l"

# config_name_for_this_run    = "3IAM_EM_0_5a"
# config_name_for_this_run    = "3IAM_EM_0_5lm"
# config_name_for_this_run    = "3IAM_EM_0_5l"

# config_name_for_this_run    = "4FXG_EM_0_1a_40"
# config_name_for_this_run    = "4FXG_EM_0_1lm_40"
# config_name_for_this_run    = "4FXG_EM_0_1l_40"
# config_name_for_this_run    = "4FXG_EM_0_1a_30"
# config_name_for_this_run    = "4FXG_EM_0_1lm_30"
# config_name_for_this_run    = "4FXG_EM_0_1l_30"
# config_name_for_this_run    = "4FXG_EM_0_1a_20"
# config_name_for_this_run    = "4FXG_EM_0_1lm_20"
config_name_for_this_run    = "4FXG_EM_0_1l_20"

#    AUTO SETTINGS
#
savePrefix = "saves"
runDir = os.path.join("results", config_name_for_this_run)
sDir = os.path.join(runDir, "samples")

# solutionFilePath = "/home/arnaud/Desktop/3IAM/save-3IAM-HGM.txt"
solutionFilePath = "/home/arnaud/Desktop/4FXG/save-4FXG-HGM.txt"
sample_tag   = 'low'

#    SCRIPT PARAMS
#

htmlDir = os.path.join(runDir, "html_contact")
html_file = os.path.join(htmlDir, "Contact_prediction.html") 

for d in [htmlDir] :
    HGM.helpers.check_or_create_dir(d)

sample_indices = HGM.helpers.read_all_sample_indices(sDir, savePrefix)
# sample_indices = range(1, 50)
representationFileName = configs[config_name_for_this_run][0]
runDir = os.path.join("results", config_name_for_this_run)
saveDirSample = os.path.join(runDir, "samples")
savePrefix = "saves"
lowEconfigsFileName = "low_energy_subsamples__0-50__1000.txt"


asDir = os.path.join(runDir, "samples-alt")
lowEconfigsFilePath = os.path.join(asDir, lowEconfigsFileName)


exec ("from {0:s} import build_subunits_info".format(representationFileName))


def get_samples_paths(sample_indices):
    samples_paths = []
    for sample_index in sample_indices :
        samples_paths.append(
                os.path.join(sDir,
                             HGM.helpers.forge_sample_name(savePrefix, sample_index))
                             )
    return samples_paths

def create_html_stat_file(html_file, c):
    content = '<!DOCTYPE html>\n\
    <html>\n\
    <head>\n\
        <meta charset=\"utf-8\" />\n\
        <title>CONTACT PREDICTION</title>\n\
        <p>Sum-up</p>\n\
        <link rel=\"stylesheet\" type=\"text/css\" href=\"/home/arnaud/Desktop/style.css">\n\
        <script type=\"text/javascript\" language=\"Javascript\" \n\
        src=\"http://www.kryogenix.org/code/browser/sorttable/sorttable.js\">\n\
        </script>\n\
    </head>\n\
    <body>\n\
     <h1>Contact summary</h1>\n\
     <p><i>report created by </i>' + getpass.getuser() + '<i> the </i>' + time.strftime('%d/%m/%y %H:%M:%S', time.localtime()) + '\n\
     </p>\n\
     <pre>\n\
     ' + config_name_for_this_run +'  sample_tag : '+sample_tag+'\n\
     \n\
     </pre>\n\
     <table  class=\"sortable\">\n\
     <thead>\n\
        <tr>\n\
            <th>Type</th>\n\
            <th>Domain1 - Domain2</th>\n\
            <th>1</th>\n\
            <th>2</th>\n\
            <th>3</th>\n\
            <th>4</th>\n\
            <th>5</th>\n\
            <th>6</th>\n\
            <th>7</th>\n\
            <th>8</th>\n\
            <th>9</th>\n\
            <th>10</th>\n\
            <th>12</th>\n\
            <th>14</th>\n\
            <th>16</th>\n\
            <th>18</th>\n\
            <th>20</th>\n\
        </tr>\n\
     </thead> \n\
     <tbody> \n\
    '+c+'\n\
     </tbody> \n\
     </table>\n\
    </body>\n\
    </html>'

    f = open(html_file, "w")
    f.write(content)
    f.close()

# a modifier pour chaque cas
def get_edge_tag(s):
    #print "get_tag(",s,")"
    tags= {
    "3IAM9-9b(1) - 3IAM9-9a(0)":"A",
    "3IAM9-9a(0) - 3IAM9-9b(1)":"A",
    "3IAM9-9a(0) - 3IAM6-6a(0)":"A",
    "3IAM6-6a(0) - 3IAM9-9a(0)":"A",
    "3IAM9-9b(1) - 3IAM4-4c(2)":"LM",
    "3IAM4-4c(2) - 3IAM9-9b(1)":"LM",
    "3IAM9-9b(1) - 3IAM4-4b(1)":"A",
    "3IAM4-4b(1) - 3IAM9-9b(1)":"A",
    "3IAM9-9b(1) - 3IAM3-3b(1)":"LM",
    "3IAM3-3b(1) - 3IAM9-9b(1)":"LM",
    "3IAM9-9a(0) - 3IAM7-7a(0)":"S",
    "3IAM7-7a(0) - 3IAM9-9a(0)":"S",
    "3IAM7-7a(0) - 3IAM2-2a(0)":"A",
    "3IAM2-2a(0) - 3IAM7-7a(0)":"A",
    "3IAM6-6a(0) - 3IAM4-4c(2)":"A",
    "3IAM4-4c(2) - 3IAM6-6a(0)":"A",
    "3IAM5-5a(0) - 3IAM4-4a(0)":"A",
    "3IAM4-4a(0) - 3IAM5-5a(0)":"A",
    "3IAM3-3f(5) - 3IAM3-3e(4)":"A",
    "3IAM3-3e(4) - 3IAM3-3f(5)":"A",
    "3IAM3-3d(3) - 3IAM3-3b(1)":"A",
    "3IAM3-3b(1) - 3IAM3-3d(3)":"A",
    "3IAM3-3c(2) - 3IAM3-3f(5)":"A",
    "3IAM3-3f(5) - 3IAM3-3c(2)":"A",
    "3IAM4-4a(0) - 3IAM4-4c(2)":"A",
    "3IAM4-4c(2) - 3IAM4-4a(0)":"A",
    "3IAM1-1a(0) - 3IAM1-1b(1)":"A",
    "3IAM1-1b(1) - 3IAM1-1a(0)":"A",
    "3IAM3-3c(2) - 3IAM3-3f(5)":"A",
    "3IAM3-3f(5) - 3IAM3-3c(2)":"A",
    "3IAM4-4b(1) - 3IAM4-4c(2)":"A",
    "3IAM4-4c(2) - 3IAM4-4b(1)":"A",
    "3IAM4-4a(0) - 3IAM4-4b(1)":"A",
    "3IAM4-4b(1) - 3IAM4-4a(0)":"A",
    "3IAM1-1b(1) - 3IAM2-2a(0)":"A",
    "3IAM2-2a(0) - 3IAM1-1b(1)":"A",
    "3IAM3-3a(0) - 3IAM3-3c(2)":"A",
    "3IAM3-3c(2) - 3IAM3-3a(0)":"A",
    "3IAM3-3d(3) - 3IAM3-3f(5)":"A",
    "3IAM3-3f(5) - 3IAM3-3d(3)":"A",
    "3IAM4-4b(1) - 3IAM5-5a(0)":"A",
    "3IAM5-5a(0) - 3IAM4-4b(1)":"A",
    "3IAM3-3d(3) - 3IAM7-7a(0)":"A",
    "3IAM7-7a(0) - 3IAM3-3d(3)":"A",
    "3IAM3-3c(2) - 3IAM3-3e(4)":"A",
    "3IAM3-3e(4) - 3IAM3-3c(2)":"A",
    "3IAM1-1b(1) - 3IAM2-2b(1)":"A",
    "3IAM2-2b(1) - 3IAM1-1b(1)":"A",
    "3IAM1-1c(2) - 3IAM2-2b(1)":"A",
    "3IAM2-2b(1) - 3IAM1-1c(2)":"A",
    "3IAM1-1a(0) - 3IAM1-1c(2)":"A",
    "3IAM1-1c(2) - 3IAM1-1a(0)":"A",
    "3IAM3-3b(1) - 3IAM4-4b(1)":"A",
    "3IAM4-4b(1) - 3IAM3-3b(1)":"A",
    "3IAM3-3a(0) - 3IAM3-3b(1)":"A",
    "3IAM3-3b(1) - 3IAM3-3a(0)":"A",
    "3IAM2-2a(0) - 3IAM3-3d(3)":"A",
    "3IAM3-3d(3) - 3IAM2-2a(0)":"A",
    "3IAM4-4a(0) - 3IAM6-6a(0)":"A",
    "3IAM6-6a(0) - 3IAM4-4a(0)":"A",
    "3IAM1-1a(0) - 3IAM2-2b(1)":"A",
    "3IAM2-2b(1) - 3IAM1-1a(0)":"A",
    "3IAM1-1b(1) - 3IAM2-2b(1)":"A",
    "3IAM2-2b(1) - 3IAM1-1b(1)":"A",
    "3IAM3-3c(2) - 3IAM3-3d(3)":"A",
    "3IAM3-3d(3) - 3IAM3-3c(2)":"A",
    "3IAM2-2b(1) - 3IAM7-7a(0)":"A",
    "3IAM7-7a(0) - 3IAM2-2b(1)":"A",
    "3IAM4-4c(2) - 3IAM9-9a(0)":"A",
    "3IAM9-9a(0) - 3IAM4-4c(2)":"A",
    "3IAM7-7a(0) - 3IAM9-9b(1)":"A",
    "3IAM9-9b(1) - 3IAM7-7a(0)":"A",
    "3IAM1-1b(1) - 3IAM1-1c(2)":"A",
    "3IAM1-1c(2) - 3IAM1-1b(1)":"A",
    "3IAM1-1c(2) - 3IAM3-3b(1)":"A",
    "3IAM3-3b(1) - 3IAM1-1c(2)":"A",
    "3IAM6-6a(0) - 3IAM9-9b(1)":"A",
    "3IAM9-9b(1) - 3IAM6-6a(0)":"A",
    "3IAM3-3a(0) - 3IAM3-3d(3)":"A",
    "3IAM3-3d(3) - 3IAM3-3a(0)":"A",
    "3IAM1-1b(1) - 3IAM2-2b(1)":"A",
    "3IAM2-2b(1) - 3IAM1-1b(1)":"A",
    "3IAM3-3d(3) - 3IAM9-9b(1)":"A",
    "3IAM9-9b(1) - 3IAM3-3d(3)":"A",
    "3IAM4-4b(1) - 3IAM6-6a(0)":"A",
    "3IAM6-6a(0) - 3IAM4-4b(1)":"A",
    "3IAM1-1c(2) - 3IAM3-3a(0)":"A",
    "3IAM3-3a(0) - 3IAM1-1c(2)":"A",
    "3IAM1-1c(2) - 3IAM3-3d(3)":"A",
    "3IAM3-3d(3) - 3IAM1-1c(2)":"A",
    "3IAM4-4b(1) - 3IAM7-7a(0)":"A",
    "3IAM7-7a(0) - 3IAM4-4b(1)":"A",
    "3IAM2-2a(0) - 3IAM2-2b(1)":"A",
    "3IAM2-2b(1) - 3IAM2-2a(0)":"A",
    "3IAM3-3d(3) - 3IAM3-3e(4)":"LM",
    "3IAM3-3e(4) - 3IAM3-3d(3)":"LM",    
    "3IAM3-3a(0) - 3IAM3-3f(5)":"LM",
    "3IAM3-3f(5) - 3IAM3-3a(0)":"LM",    
    "3IAM1-1b(1) - 3IAM3-3d(3)":"LM",
    "3IAM3-3d(3) - 3IAM1-1b(1)":"LM",
    "3IAM3-3f(5) - 3IAM9-9b(1)":"LM",
    "3IAM9-9b(1) - 3IAM3-3f(5)":"LM",
    "3IAM1-1c(2) - 3IAM7-7a(0)":"LM",
    "3IAM7-7a(0) - 3IAM1-1c(2)":"LM",
    "3IAM3-3b(1) - 3IAM7-7a(0)":"LM",
    "3IAM7-7a(0) - 3IAM3-3b(1)":"LM",
    "3IAM3-3d(3) - 3IAM4-4b(1)":"S",
    "3IAM4-4b(1) - 3IAM3-3d(3)":"S",
    "3IAM1-1b(1) - 3IAM3-3a(0)":"S",
    "3IAM3-3a(0) - 3IAM1-1b(1)":"S",
    "3IAM1-1b(1) - 3IAM3-3c(2)":"S",
    "3IAM3-3c(2) - 3IAM1-1b(1)":"S",
    "3IAM1-1c(2) - 3IAM2-2a(0)":"S",
    "3IAM2-2a(0) - 3IAM1-1c(2)":"S",
    "3IAM2-2a(0) - 3IAM3-3c(2)":"S",
    "3IAM3-3c(2) - 3IAM2-2a(0)":"S",    
    "3IAM3-3b(1) - 3IAM3-3f(5)":"S",
    "3IAM3-3f(5) - 3IAM3-3b(1)":"S",  
    "3IAM1-1c(2) - 3IAM3-3c(2)":"S",
    "3IAM3-3c(2) - 3IAM1-1c(2)":"S",
    }
    tag = " "
    try :
        tag = tags[s]
    except :
        pass
    return tag


def dump_domains_table(EOA, pdms):
    

    
    print "-- Edges repartitions --"
    ts = sorted(EOA.keys())
    print "ts", ts
#    p = HGM.distances.ParticlesPairDistanceMatrixSet()
    p_names = map(lambda p:p.get_name(), pdms.get_particles())
#    print "EOA",EOA
        
    edges = EOA[ts[0]].get_sorted_edges()
    

    
    print r"\begin{table}[htbp!]"
    print r"\centering"
    print r"{\footnotesize"
    print r"\begin{tabular}{|c|l" + ("|r"*len(ts)) + "|}"
    print r"\cline{2-" + str(len(ts) + 2) + "}"
    print "\multicolumn{1}{c|}{} & edge &" + "&".join(map(lambda x:str(x), ts)) + r"\\"
    print r"\hline"
    
    for (node1, node2, nb) in edges :
#        print " {0:>10s} - {1:<10s}".format(p_names[node1],p_names[node2]),
#        print " &{0:>10s} - {1:<10s}".format(p_names[node1],p_names[node2]),
        tag = get_edge_tag("{0:>10s} - {1:<10s}".format(p_names[node1], p_names[node2]))
        print "{2:s}&{0:>10s} - {1:<10s}".format(p_names[node1], p_names[node2], tag),
        for t in ts :
            eoa = EOA[t]
            norm_coef = 100. / eoa.get_number_of_configurations()
            nb = eoa.get_edge_count(node1, node2)
#            print "&{0:>5d} ({1:3.2f}%)".format (nb,nb*norm_coef),
            print "&{0:3.2f} ".format (nb * norm_coef),
        print r"\\"
    
    print r"\hline" 
    print r"\end{tabular}"
    print r"}"
    print "%"
    print r"%\caption{}"
    print r"%\label{}"
    print r"\end{table}"        



def dump_domains_table_html(EOA, pdms):
    content = ''
        
    #print "-- Edges repartitions --"
    ts = sorted(EOA.keys())
    #print "ts", ts
#    p = HGM.distances.ParticlesPairDistanceMatrixSet()
    p_names = map(lambda p:p.get_name(), pdms.get_particles())
#    print "EOA",EOA
        
    edges = EOA[ts[0]].get_sorted_edges()

    
    for (node1, node2, nb) in edges :
        
        tag = get_edge_tag("{0:>10s} - {1:<10s}".format(p_names[node1], p_names[node2]))
        content += '<tr>\n\
<td>'+tag+'</td>'
        res = "{0:>10s} - {1:<10s}".format(p_names[node1], p_names[node2])
        content += '<td>' + str(res) + '</td>\n'
        for t in ts :
            eoa = EOA[t]
            norm_coef = 100. / eoa.get_number_of_configurations()
            nb = eoa.get_edge_count(node1, node2)
#            print "&{0:>5d} ({1:3.2f}%)".format (nb,nb*norm_coef),
            res1 = "{0:3.2f} ".format (nb * norm_coef)
            content += '<td>' + str(res1) + '</td>\n'
        content += '</tr>\n'
          
    content += '</tr>'
    return content

def dump_table_solution(pdms):
    p_names = map(lambda p:p.get_name(), pdms.get_particles())
    print p_names
    return 0

def main():
    m = IMP.Model()
    m.set_log_level(IMP.SILENT)
    cplxInfos = build_subunits_info(m)
    HGM.helpers.mute_all_restraints(m)
    
#     sampleFiles = get_samples_paths(sample_indices)
    sampleFiles = lowEconfigsFilePath
    mcs = HGM.representation.MyConfigurationSet(cplxInfos)
    
    # solution matrix distances
    #mcs.read_all_configs_from_file(solutionFilePath)
    #pdms_sol = HGM.distances.ParticlesPairDistanceMatrixSet(mcs)
#     print pdms_sol.get_distance(0, 0, 0)
    
#     print pdms_sol.get_matrix(0)
#     dump_table_solution(pdms_sol)
    
    #mcs.delete_all_configs()
    mcs.read_all_configs_from_file(sampleFiles)
    print 'Found ', mcs.get_number_of_configurations(), ' Configuration'
    
    pdms = HGM.distances.ParticlesPairDistanceMatrixSet(mcs)
    
    # DOMAINS
    nodes = range(len(pdms.get_particles()))
    
    EOA = {}
    

    # thresholds = [5,10,15,20]
    thresholds = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 14, 16, 18, 20]
    print "computing connectivity graph edge-accumulator"
    for t in thresholds :
        print "computing distance graph for threshold", t
        # DOMAINS
        eoa = HGM.distances.EdgeOccurenceAccumulator(pdms, t, nodes)
        EOA[t] = eoa
    # DOMAINS
    result = dump_domains_table_html(EOA, pdms)

    create_html_stat_file(html_file, result)
    
#    dump_plots(EOA)

if __name__ == "__main__" :
    main()
    print "------------------------------------ END ------------------------------------"
