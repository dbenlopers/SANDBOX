'''

reads given samples, compute RMSD to solution by subunit and stat them in html file,
 making boxplot/violin plot, and remake them for a consensus solution  (modele le plus proche du centroid)


TODO : reduce code
'''

import os
import math
import re
import numpy ;
import getpass
import IMP
import HGM
import IMP, IMP.algebra, IMP.core, IMP.atom
import HGM, HGM.helpers, HGM.helpersPlot, HGM.representation, HGM.samples
import time
from alternate_configs import configs
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from pylab import *

from matplotlib.pyplot import figure, show
from scipy.stats import gaussian_kde
from numpy.random import normal
from numpy import arange


# config_name_for_this_run    = "3NIG_EM_0_2aC"                  
# config_name_for_this_run    = "3NIG_EM_0_2aC_20"     
# config_name_for_this_run    = "3NIG_EM_0_2lmC"
# config_name_for_this_run    = "3NIG_EM_0_2lmC_20"
# config_name_for_this_run    = "3NIG_EM_0_2lC"
# config_name_for_this_run    = "3NIG_EM_0_2lC_20" 
# config_name_for_this_run    = "3NIG_EM_0_3ambiC"  
# config_name_for_this_run    = "3NIG_EM_0_3ambiC_20"

#config_name_for_this_run    = "3NIG_EM_0_2aC_f"                  
#config_name_for_this_run    = "3NIG_EM_0_2aC_f_20"     
#config_name_for_this_run    = "3NIG_EM_0_2lmC_f"
#config_name_for_this_run    = "3NIG_EM_0_2lmC_f_20"
#config_name_for_this_run    = "3NIG_EM_0_2lC_f"
#config_name_for_this_run    = "3NIG_EM_0_2lC_f_20" 
#config_name_for_this_run    = "3NIG_EM_0_3ambiC_f"  
#config_name_for_this_run    = "3NIG_EM_0_3ambiC_f_20"

#config_name_for_this_run    =  "3NIG_EM_0_4a_f"
#config_name_for_this_run    = "3NIG_EM_0_4a_f_20"
#config_name_for_this_run    = "3NIG_EM_0_4lm_f"
#config_name_for_this_run    = "3NIG_EM_0_4lm_f_20"
#config_name_for_this_run    = "3NIG_EM_0_4l_f"
#config_name_for_this_run    = "3NIG_EM_0_4l_f_20"
          
#config_name_for_this_run    = "3NIG_EM_0_5a_f"
#config_name_for_this_run    = "3NIG_EM_0_5a_f_20"
#config_name_for_this_run    = "3NIG_EM_0_5lm_f"
#config_name_for_this_run    = "3NIG_EM_0_5lm_f_20"
#config_name_for_this_run    = "3NIG_EM_0_5l_f"
config_name_for_this_run    = "3NIG_EM_0_5l_f_20"


# config_name_for_this_run    = "3IAM_EM_0_3a"
# config_name_for_this_run    = "3IAM_EM_0_3lm"
# config_name_for_this_run    = "3IAM_EM_0_3l"

#config_name_for_this_run    = "3IAM_EM_0_4a"
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
# config_name_for_this_run    = "4FXG_EM_0_1l_20"

#    AUTO SETTINGS
#
savePrefix = "saves"
runDir = os.path.join("results", config_name_for_this_run)
sDir = os.path.join(runDir, "samples")
gDir = os.path.join(runDir, "graphics")
varDir = os.path.join(gDir, "RMSD_variation_study")

for d in [gDir, varDir] :
    HGM.helpers.check_or_create_dir(d)


#    SCRIPT PARAMS
# solutionFilePath="None"

# solutionFilePath        = "/home/arnaud/Desktop/TFIIH/data/4FXG/save-4FXG-HGM.txt"
# solutionFilePath        = "/home/arnaud/Desktop/3IAM/save-3IAM-HGM.txt"
solutionFilePath        = "/home/arnaud/Desktop/TFIIH/data/3NIG/save-3NIG-HGM.txt"
# solutionFilePath        = "/home/arnaud/Desktop/TFIIH/data/ARP/save-1TYQ-HGM.txt"

sample_indices = HGM.helpers.read_all_sample_indices(sDir, savePrefix)
# sample_indices = range(1, 50)
sample_tag = 'low'

#sampleFiles = get_samples_paths(sample_indices)
sampleFiles = ['/home/arnaud/Desktop/TFIIH/src/coarse2/results/' + config_name_for_this_run + '/samples-alt/low_energy_subsamples__0-50__1000.txt']

#    === HERE WE GO
#    print "getting subsamples energies from subsample energy file"
#    sse.read_from_file(subsamplesEnergyfilePath)


subunitsRepresentationFileName = configs[config_name_for_this_run][0]
exec ("from {0:s} import build_subunits_info".format(subunitsRepresentationFileName))



def get_samples_paths(sample_indices):
    samples_paths = []
    for sample_index in sample_indices :
        samples_paths.append(
                os.path.join(sDir,
                             HGM.helpers.forge_sample_name(savePrefix, sample_index))
                             )
    return samples_paths
        
def gather_coordinates_for_current_config(xyzl):
    """ outputs the concatenated list of partile coordinates for a given model"""
    vect = []
    for X in xyzl :
        vect.extend([X.get_x(), X.get_y(), X.get_z()])
    return vect

def compute_current_energy(m):
    return m.evaluate(False)

def compute_rmsd(coods_current, coods_solution):
    rmsd = HGM.helpers.compute_coods_rmsd(coods_current, coods_solution)
    return rmsd

def compute_gravity_center(coord):
    x = []
    y = []
    z = []
    for i in range(len(coord) / 3):
        x.append(coord[3 * i])
        y.append(coord[3 * i + 1])
        z.append(coord[3 * i + 2])
    mass_center = []
    mass_center.append(numpy.mean(x))
    mass_center.append(numpy.mean(y))
    mass_center.append(numpy.mean(z))
    return mass_center


def Output_html_file(html_file_path,content1,content2):
    content="""
<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8" />
        <title>Variablity Statistique</title>
    </head>
    <body>
    <p><i>report created by </i>""" + getpass.getuser() + """<i> the </i>""" + time.strftime('%d/%m/%y %H:%M:%S', time.localtime()) + """
     </p>
     <pre>
     """ + config_name_for_this_run +"""  sample_tag : """+sample_tag+"""
     </pre>
     <h1>Variablity Results Statistique</h1>
     <h2>Variablity to solution (if available)</h2>
    """+content1+"""
     <h2>Variablity to centroid solution</h2>
     """+content2+"""
     

    </body>
</html>


"""
    f = open(html_file_path, "w")
    f.write(content)
    f.close()

# compute centroid sample and closer models, save all
def compute_centroid_save(mcs, centroids_filePath):
    c = HGM.samples.compute_centroid_for_models(mcs, update_model=True)

    mcs_centers = HGM.representation.MyConfigurationSet(mcs.get_prot_info_model())
    mcs_centers.save_current_config()
    
    i, d = HGM.samples.compute_index_of_central_model_for_models(mcs, centroid=c)
#    print "central config is the number",i,"with a distance",d,"from centroid"
    mcs.load_configuration(i)
    mcs_centers.save_current_config()

    mcs_centers.save_all_configs_to_file(centroids_filePath)

#make a simple boxplot
def Boxplot_Output(data,x_name,file_name,title):
        '''
        make a boxplot from the data
        '''
        plt.figure()
        fig = plt.figure()
        fig.subplots_adjust(bottom=0.2)
        ax1 = fig.add_subplot(111)
        plt.subplots_adjust(left=0.075, right=0.95, top=0.9, bottom=0.25)
        bp = plt.boxplot(data, notch=0, sym='+', vert=1, whis=1.5)
        plt.setp(bp['boxes'], color='black')
        plt.setp(bp['whiskers'], color='black')
        plt.setp(bp['fliers'], color='red', marker='+')
        ax1.yaxis.grid(True, linestyle='-', which='major', color='lightgrey', alpha=0.5)
        ax1.set_axisbelow(True)
        xticks(range(1, len(x_name) + 1), (x_name), rotation=65, size=8)
        ax1.set_title(title)
        ax1.set_xlabel('Domain')
        ax1.set_ylabel('RMSD')
        plt.ylim(ymin=0)
        plt.savefig(os.path.join(varDir, file_name))

def Violin_plot_Output(data,x_name,file_name,title):
        '''
        create violin plots(density) on an axis
        '''
        def violin(ax, data, pos):
            dist = max(pos) - min(pos)
            w = min(0.15 * max(dist, 1.0), 0.5)
            for d, p in zip(data, pos):
                k = gaussian_kde(d)  # calculates the kernel density
                m = k.dataset.min()  # lower bound of violin
                M = k.dataset.max()  # upper bound of violin
                x = arange(m, M, (M - m) / 100.)  # support for violin
                v = k.evaluate(x)  # violin profile (density curve)
                v = v / v.max() * w  # scaling the violin to the available space
                ax.fill_betweenx(x, p, v + p, facecolor='y', alpha=0.3)
                ax.fill_betweenx(x, p, -v + p, facecolor='y', alpha=0.3)
                ax.set_title(title)
                ax.set_xlabel('Domain')
                ax.set_ylabel('RMSD')
                xticks(range(0, len(x_name)), (x_name), rotation=65, size=8)

        pos = range(len(x_name))
        data = data
        fig = plt.figure()
        ax = fig.add_subplot(111)
        plt.subplots_adjust(left=0.075, right=0.95, top=0.9, bottom=0.25)
        violin(ax, data, pos)
        plt.ylim(ymin=0)
        plt.savefig(os.path.join(varDir, file_name))

def Violin_Boxplot_Output(data,x_name,file_name,title):
        '''
        create violin plots and boxplot on an axis
        '''
        def violin_boxplot(ax, data, pos, bp=False):
            dist = max(pos) - min(pos)
            w = min(0.15 * max(dist, 1.0), 0.5)
            for d, p in zip(data, pos):
                k = gaussian_kde(d)  # calculates the kernel density
                m = k.dataset.min()  # lower bound of violin
                M = k.dataset.max()  # upper bound of violin
                x = arange(m, M, (M - m) / 100.)  # support for violin
                v = k.evaluate(x)  # violin profile (density curve)
                v = v / v.max() * w  # scaling the violin to the available space
                ax.fill_betweenx(x, p, v + p, facecolor='y', alpha=0.3)
                ax.fill_betweenx(x, p, -v + p, facecolor='y', alpha=0.3)
                ax.set_title(title)
                ax.set_xlabel('Domain')
                ax.set_ylabel('RMSD')
                xticks(range(1, len(x_name) + 1), (x_name), rotation=65, size=8)
            if bp:
                bp1 = ax.boxplot(data, notch=1, positions=pos, vert=1)
                plt.setp(bp1['boxes'], color='black')
                plt.setp(bp1['whiskers'], color='black')
                plt.setp(bp1['fliers'], color='red', marker='+')
        
        pos = range(len(x_name))
        data = data
        fig = plt.figure()
        ax = fig.add_subplot(111)
        plt.subplots_adjust(left=0.075, right=0.95, top=0.9, bottom=0.25)
        violin_boxplot(ax, data, pos, bp=1)
        plt.ylim(ymin=0)
        plt.savefig(os.path.join(varDir, file_name))

def Compute_Variability_Stat_HTMLoutput(subunitnames,mcs,subunit_liste_rmsd,subunit_liste_mass_center_rmsd,domain_liste_rmsd):
        '''
        Compute stat and put them in html format
        '''
        content_results=""
        k = 0
        j = 0
        for subunitname in subunitnames:
            # rmsd of subunit
            average = "{0:.2f}".format(numpy.average(subunit_liste_rmsd[k]))
            median = "{0:.2f}".format(numpy.median(subunit_liste_rmsd[k]))
            std = "{0:.2f}".format(numpy.std(subunit_liste_rmsd[k]))
            var = "{0:.2f}".format(numpy.var(subunit_liste_rmsd[k]))
            mini = "{0:.2f}".format(min(subunit_liste_rmsd[k]))
            maxi = "{0:.2f}".format(max(subunit_liste_rmsd[k]))
            content_results +="<p><code>"
            content_results +='-------Stat for subunit ' + subunitname + ' --------<br>'
            content_results +='Min rmsd       : ' + mini + ' <br>'
            content_results +='Max rmsd       : ' + maxi + ' <br>'
            content_results +='Average rmsd   : ' + average + ' <br>'
            content_results +='Median rmsd    : ' + median + ' <br>'
            content_results += 'Std rmsd       : ' + std + ' <br>'
            content_results += 'var rmsd       : ' + var + ' <br></code>'
            content_results+="</p>"
            # rmsd of  Gravity center of subunit
            average_gc = "{0:.2f}".format(numpy.average(subunit_liste_mass_center_rmsd[k]))
            median_gc = "{0:.2f}".format(numpy.median(subunit_liste_mass_center_rmsd[k]))
            std_gc = "{0:.2f}".format(numpy.std(subunit_liste_mass_center_rmsd[k]))
            var_gc = "{0:.2f}".format(numpy.var(subunit_liste_mass_center_rmsd[k]))
            mini_gc = "{0:.2f}".format(min(subunit_liste_mass_center_rmsd[k]))
            maxi_gc = "{0:.2f}".format(max(subunit_liste_mass_center_rmsd[k]))
            content_results+='<p><code>'
            content_results += '-------Stat of Gravity center for subunit ' + subunitname + ' --------<br>'
            content_results +='Min rmsd of Gravity Center       : ' + mini_gc + ' <br>'
            content_results += 'Max rmsd of Gravity Center       : ' + maxi_gc + ' <br>'
            content_results += 'Average rmsd of Gravity Center   : ' + average_gc + ' <br>'
            content_results += 'Median rmsd of Gravity Center    : ' + median_gc + ' <br>'
            content_results += 'Std rmsd of Gravity Center       : ' + std_gc + ' <br>'
            content_results += 'var rmsd of Gravity Center       : ' + var_gc + ' <br></code>'
            content_results+="</p>"
            # print 'Calculated with '+str(len(subunit_liste_rmsd))+' elements'
            domain = mcs.get_subunit_particles(subunitname)
            size = mcs.get_number_of_beads(subunitname)
            k = k + 1
            
            for i in range(size):
                average = "{0:.2f}".format(numpy.average(domain_liste_rmsd[j]))
                median = "{0:.2f}".format(numpy.median(domain_liste_rmsd[j]))
                std = "{0:.2f}".format(numpy.std(domain_liste_rmsd[j]))
                var = "{0:.2f}".format(numpy.var(domain_liste_rmsd[j]))
                min_sol = "{0:.2f}".format(min(domain_liste_rmsd[j]))
                max_sol = "{0:.2f}".format(max(domain_liste_rmsd[j]))
                content_results+='<p style="margin-left: 20em;"><code>'
                content_results += '---------->Stat for domain  ' + str(domain[i]) + ' <br>'
                content_results += 'Min rmsd       : ' + min_sol + ' <br>'
                content_results += 'Max rmsd       : ' + max_sol + ' <br>'
                content_results += 'Average rmsd   : ' + average + ' <br>'
                content_results += 'Median rmsd    : ' + median + ' <br>'
                content_results += 'Std rmsd       : ' + std + ' <br>'
                content_results += 'var rmsd       : ' + var + ' <br></code>'
                content_results+='</p>'
                # print '                        Calculated with '+str(len(domain))+' elements'
                j = j + 1
        return content_results


def Consensus_Variability(sampleFiles):
        '''
        Compute Variability stat with consensus solution
        '''
        con_content=""
        print " -- creating universe"
        m = IMP.Model()
        m.set_log_level(IMP.SILENT)
        print " -- crowding universe"
        subunitsInfos = build_subunits_info(m)
        HGM.helpers.mute_all_restraints(m)
        xyzl = map (HGM.helpers.XYZdecorate, subunitsInfos.get_particles())

        # Sample loading parts
        print " -- loading sample names...",
        print "found", len(sampleFiles)
        print " -- loading samples"
        mcs = HGM.representation.MyConfigurationSet(subunitsInfos)

        loop_index = 0
        for samplePath in sampleFiles :
            loop_index += 1
            if loop_index % 15 == 0 : print ""
            print loop_index, "..",
            mcs.read_all_configs_from_file(samplePath)
            
        print " \n-- Computing the solution"
        # save centroid and closest models
        compute_centroid_save(mcs, os.path.join(varDir, "centroid_structure_"+sample_tag+"_.txt"))

        solution = HGM.samples.compute_centroid_for_models(mcs, update_model=True)
        coods_solution = solution
        
        subnames = mcs.get_subunit_names()
        xyzsol = {}
        for subname in subnames: 
            xyzl = map (HGM.helpers.XYZdecorate, subunitsInfos.get_subunit_info(subname).get_all_particles())        
            xyzsol[subname] = gather_coordinates_for_current_config(xyzl)
        
        subunitnames = mcs.get_subunit_names()
        domainenames = []


        subunit_liste_rmsd = []
        subunit_liste_mass_center_rmsd = []

        domain_liste_rmsd = []

        #search domain name
        for subunitname in subunitnames:
            subunit_liste_rmsd.append([])
            subunit_liste_mass_center_rmsd.append([])
            name_doma = mcs.get_subunit_particles(subunitname)
            for i in range(len(name_doma)):
                domainenames.append(name_doma[i])


        nb_beads = mcs._nb_beads
        for i in range(nb_beads):
            domain_liste_rmsd.append([])

        # Computing parts
        time_start_compute = time.time()
        
        
        
        for i in range(mcs.get_number_of_configurations()) :
                mcs.load_configuration(i)
                z = 0
                y = 0
                subunitnames = mcs.get_subunit_names()
                
                # Compute subunit rmsd
                for subunitname in subunitnames:
                    xyzl = map(HGM.helpers.XYZdecorate, subunitsInfos.get_subunit_info(subunitname).get_all_particles())
                    coods_current = gather_coordinates_for_current_config(xyzl)
                    coods_solution = xyzsol.get(subunitname)
                    
                    # Compute rmsd of subunit
                    rmsd = compute_rmsd(coods_current, coods_solution)              
                    subunit_liste_rmsd[z].append(rmsd)
                    
                    # Compute rmsd of gravity center
                    gravity_center_solution = compute_gravity_center(coods_solution)
                    gravity_center = compute_gravity_center(coods_current)
                    rmsd_mc = compute_rmsd(gravity_center, gravity_center_solution)
                    subunit_liste_mass_center_rmsd[z].append((rmsd_mc))

                    size = mcs.get_number_of_beads(subunitname)
                    # Compute domain rmsd
                    for i in range(size):
                        domaine_pos = []
                        domaine_pos.append(coods_current[3 * i])
                        domaine_pos.append(coods_current[3 * i + 1])
                        domaine_pos.append(coods_current[3 * i + 2])
                        sol_domaine_pos = []
                        sol_domaine_pos.append(coods_solution[3 * i])
                        sol_domaine_pos.append(coods_solution[3 * i + 1])
                        sol_domaine_pos.append(coods_solution[3 * i + 2])
                        # Compute rmsd of domain
                        rmsd = compute_rmsd(domaine_pos, sol_domaine_pos)
                        domain_liste_rmsd[y].append(rmsd)
                        y += 1                     
                    z += 1
        mcs.delete_all_configs()
        time_stop_compute = time.time()

        # Stat parts
        time_start_stat = time.time()
        con_content=Compute_Variability_Stat_HTMLoutput(subunitnames,mcs,subunit_liste_rmsd,subunit_liste_mass_center_rmsd,domain_liste_rmsd)

        time_stop_stat = time.time()
        
        
        data = []
        for i in range(len(subunit_liste_rmsd)):
            data.append(subunit_liste_rmsd[i])
            data.append(subunit_liste_mass_center_rmsd[i])
        

        time_start_plot = time.time()    
        #plotting
        Boxplot_Output(subunit_liste_rmsd, subunitnames, 'Consensus_Subunit_variation_' + sample_tag + '.png','Consensus model RMSD by Subunit ' + sample_tag + '')
        Boxplot_Output(subunit_liste_mass_center_rmsd, subunitnames, 'Consensus_Subunit_center_variation_' + sample_tag + '.png', 'Consensus model RMSD by Subunit center  sample : ' + sample_tag + '')
        Boxplot_Output(domain_liste_rmsd, domainenames, 'Consensus_Domain_variation_' + sample_tag + '.png', 'Consensus model RMSD by Domain  sample : ' + sample_tag + '')
        Violin_Boxplot_Output(domain_liste_rmsd, domainenames, 'Consensus_Domain_variation_density_' + sample_tag + '.png', 'Consensus model RMSD by Domain  sample : ' + sample_tag + '')
        Violin_plot_Output(domain_liste_rmsd, domainenames, 'Consensus_Domain_variation_density2_' + sample_tag + '.png', 'Consensus model Density RMSD by Domain  sample : ' + sample_tag + '')

        
        time_stop_plot = time.time()
        
        
        print "Load models and Computing rmsd take : {0:.2f}s".format(float(time_stop_compute - time_start_compute))
        print "Stat output take : {0:.2f}s".format(float(time_stop_stat - time_start_stat))
        print "Plot output take : {0:.2f}s".format(float(time_stop_plot - time_start_plot))

        return con_content




def main(sampleFiles):
        '''
        Compute variability stat with solution (if availaible)
        '''
        sol_content=""
        print " -- creating universe"
        m = IMP.Model()
        m.set_log_level(IMP.SILENT)
        print " -- crowding universe"
        subunitsInfos = build_subunits_info(m)
        HGM.helpers.mute_all_restraints(m)
        xyzl = map (HGM.helpers.XYZdecorate, subunitsInfos.get_particles())

        print " -- loading the solution", solutionFilePath,
        solution = HGM.representation.MyConfigurationSet(subunitsInfos)
        solution.read_all_configs_from_file(solutionFilePath)
        print ""
        solution.load_configuration(0)
        coods_solution = gather_coordinates_for_current_config(xyzl)

        subnames = solution.get_subunit_names()
        xyzsol = {}
        for subname in subnames: 
            xyzl = map (HGM.helpers.XYZdecorate, subunitsInfos.get_subunit_info(subname).get_all_particles())        
            xyzsol[subname] = gather_coordinates_for_current_config(xyzl)

        # Sample loading parts
        print " -- loading sample names...",
        print "found", len(sampleFiles)
        print " -- loading samples to compute  RMSD"
        mcs = HGM.representation.MyConfigurationSet(subunitsInfos)

        subunitnames = mcs.get_subunit_names()
        domainenames = []


        subunit_liste_rmsd = []
        subunit_liste_mass_center_rmsd = []

        domain_liste_rmsd = []

        #search domain name
        for subunitname in subunitnames:
            subunit_liste_rmsd.append([])
            subunit_liste_mass_center_rmsd.append([])
            name_doma = mcs.get_subunit_particles(subunitname)
            for i in range(len(name_doma)):
                domainenames.append(name_doma[i])


        nb_beads = mcs._nb_beads
        for i in range(nb_beads):
            domain_liste_rmsd.append([])

        # Computing parts
        time_start_compute = time.time()
        
        loop_index = 0
        for samplePath in sampleFiles :
            loop_index += 1
            if loop_index % 15 == 0 : print ""
            print loop_index, "..",
            mcs.read_all_configs_from_file(samplePath)
            for i in range(mcs.get_number_of_configurations()) :
                mcs.load_configuration(i)
                z = 0
                y = 0
                subunitnames = mcs.get_subunit_names()
                
                # Compute subunit rmsd
                for subunitname in subunitnames:
                    xyzl = map(HGM.helpers.XYZdecorate, subunitsInfos.get_subunit_info(subunitname).get_all_particles())
                    coods_current = gather_coordinates_for_current_config(xyzl)
                    coods_solution = xyzsol.get(subunitname)
                    
                    # Compute rmsd of subunit
                    rmsd = compute_rmsd(coods_current, coods_solution)              
                    subunit_liste_rmsd[z].append(rmsd)
                    
                    # Compute rmsd of gravity center
                    gravity_center_solution = compute_gravity_center(coods_solution)
                    gravity_center = compute_gravity_center(coods_current)
                    rmsd_mc = compute_rmsd(gravity_center, gravity_center_solution)
                    subunit_liste_mass_center_rmsd[z].append((rmsd_mc))

                    size = mcs.get_number_of_beads(subunitname)
                    # Compute domain rmsd
                    for i in range(size):
                        domaine_pos = []
                        domaine_pos.append(coods_current[3 * i])
                        domaine_pos.append(coods_current[3 * i + 1])
                        domaine_pos.append(coods_current[3 * i + 2])
                        sol_domaine_pos = []
                        sol_domaine_pos.append(coods_solution[3 * i])
                        sol_domaine_pos.append(coods_solution[3 * i + 1])
                        sol_domaine_pos.append(coods_solution[3 * i + 2])
                        # Compute rmsd of domain
                        rmsd = compute_rmsd(domaine_pos, sol_domaine_pos)
                        domain_liste_rmsd[y].append(rmsd)
                        y += 1                     
                    z += 1
            mcs.delete_all_configs()
        time_stop_compute = time.time()

        # Stat parts
        time_start_stat = time.time()
        sol_content=Compute_Variability_Stat_HTMLoutput(subunitnames,mcs,subunit_liste_rmsd,subunit_liste_mass_center_rmsd,domain_liste_rmsd)
        time_stop_stat = time.time()
        
        
        data = []
        for i in range(len(subunit_liste_rmsd)):
            data.append(subunit_liste_rmsd[i])
            data.append(subunit_liste_mass_center_rmsd[i])
        

        time_start_plot = time.time()    
        #plotting
        Boxplot_Output(subunit_liste_rmsd,subunitnames, 'Subunit_variation_' + sample_tag + '.png', 'RMSD by Subunit  sample : ' + sample_tag + '')
        Boxplot_Output(subunit_liste_mass_center_rmsd,subunitnames,'Subunit_center_variation_' + sample_tag + '.png','RMSD by Subunit center  sample : ' + sample_tag + '')
        Boxplot_Output(domain_liste_rmsd, domainenames, 'Domain_variation_' + sample_tag + '.png', 'RMSD by Domain  sample : ' + sample_tag + '')
        Violin_Boxplot_Output(domain_liste_rmsd, domainenames, 'Domain_variation_density_' + sample_tag + '.png', 'RMSD by Domain  sample : ' + sample_tag + '')
        Violin_plot_Output(domain_liste_rmsd, domainenames, 'Domain_variation_density2_' + sample_tag + '.png', 'Density RMSD by Domain  sample : ' + sample_tag + '')

        time_stop_plot = time.time()
        
        
        print "Load models and Computing rmsd take : {0:.2f}s".format(float(time_stop_compute - time_start_compute))
        print "Stat output take : {0:.2f}s".format(float(time_stop_stat - time_start_stat))
        print "Plot output take : {0:.2f}s".format(float(time_stop_plot - time_start_plot))
        
        return sol_content
        
if __name__ == "__main__":
    time_start = time.time()
    
    # utilise une solution calculer = centroid
    print "------------------Using Calculated consensus Solution------------------"
    
    content2=Consensus_Variability(sampleFiles)
    # utilise une solution 
    if solutionFilePath=="None":
        content1="<p><code> Not available</code></p>"
    else:
        print "------------------Using Solution------------------"
        content1=main(sampleFiles)
    time_stop = time.time()
    
    html_file_path   = os.path.join(varDir,"Stat_results_"+sample_tag+"_.html")
    Output_html_file(html_file_path, content1, content2)
    
    print "------------------------------------ END ------------------------------------"
    print "full job take : {0:.2f}s".format(float(time_stop - time_start))
