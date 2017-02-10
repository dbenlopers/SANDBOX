
import os
import sys

import time

import IMP, IMP.core, IMP.container, IMP.algebra

import HGM
import HGM.sampling
import HGM.display
import HGM.helpers
import HGM.times

import xml.dom.minidom
from xml.dom.minidom import Node
    
from alternate_configs import configs




#
#    PARAMETERS
#
#
#

#config_name_for_this_run    = None
#config_name_for_this_run    = "fixedGeom_0"
#config_name_for_this_run    = "fixedGeom_1_l0"
#config_name_for_this_run    = "fixedGeom_1_1"
config_name_for_this_run    = "test_fixedGeom_1_1"

tfiihRepresentationFileName = configs[config_name_for_this_run][0]


runDir                      = os.path.join("results",config_name_for_this_run)
saveDirSample               = os.path.join(runDir,"samples")
savePrefix                  = "saves"

for d in [runDir,saveDirSample] :
    HGM.helpers.check_or_create_dir(d)


#ubh_steepness = 5000
#ubh_steepness = 500
#ubh_steepness = 300
ubh_steepness = 50
max_out_of_enveloppe_score = ubh_steepness
model_max_score = 2000

#
#    Models generation
#
BBs             = 500
nb_cg_steps     = 500
#
md_type         = HGM.sampling.BERENDSEN
T               = 3000
tau             = 100
sampling_step   = 200

dryRun_size         = 500


#sample_size         = 200
sample_size         = 5


#    MC CG sampling
MC_default_nb_CG_steps  = 50
#MC_default_nb_MC_steps  = 50000
MC_default_nb_MC_steps  = 100
MC_default_attempts     = 1

#
#    Sample configuration
#
#number_samples      = 1
#number_samples      = 1
#sample_indexes      = range(number_samples)
#sample_indexes      = range(10,100)
#sample_indexes      = [1]
#sample_indexes      = range(200)        # 200 first attempts with ubh_steep = 50
#sample_indexes      = range(200,300)     # next 100 attempts with ubh_steep = 500
#sample_indexes      = range(300,310)     # next 10 attempts with MCCG 1000/500 steepness 500
#sample_indexes      = range(310,315)     # next 5 attempts with MCCG 10000/500 steepness 300
#sample_indexes      = range(315,320)     # next 5 attempts with MCCG 10000/500 steepness 300 added max score to fit in EM
#sample_indexes      = range(320,322)     # next 5 attempts with MCCG 50000/500 steepness 300 added max score to fit in EM

sample_indexes      = range(1010,1020)
#
#
#dmapFileName        = "/Users/schwarz/Desktop/TFIIH-maps/fixed_holoIIH.mrc"
#dmapResolution      = 30.00
#dmapThreshold       =  1.16



#    import the function responsible for modelisation of TFIIH complex
exec ( "from {0:s} import build_TFIIH_subunits_info".format( tfiihRepresentationFileName ) )



#myBallsFileName = "/Users/schwarz/Desktop/TFIIH.cmm"
#myBallsFileName = "/Users/schwarz/Desktop/TFIIH-fat.cmm"
myBallsFileName = "../../data/TFIIH-fat.cmm"


def read_cover_spheres(myBallsFileName):
    # 1. read spheres
    #
    doc = xml.dom.minidom.parse( myBallsFileName )
    ms = doc.getElementsByTagName("marker")
    coverSpheres = []
    for m in ms :
        s=map(lambda x:float(m.getAttribute(x)),["x","y","z","radius"])
        coverSpheres.append(s)
    return coverSpheres

def get_bbox_from_cover_spheres( coverSpheres ) :
    """ """
    spheres = [ IMP.algebra.Sphere3D( IMP.algebra.Vector3D(s[0:3]),s[3]) for s in coverSpheres ]
#    print "speheres"
#    for s in spheres : print s

    bb = IMP.algebra.get_bounding_box( spheres[0] )
    xM,yM,zM = bb.get_corner(1)
    xm,ym,zm = bb.get_corner(0)
    for s in spheres[1:] :
        bb = IMP.algebra.get_bounding_box( s )
        xsM,ysM,zsM = bb.get_corner(1)
        xsm,ysm,zsm = bb.get_corner(0)
        if xsM > xM : xM = xsM
        if ysM > yM : yM = ysM
        if zsM > zM : zM = zsM
        if xsm < xm : xm = xsm
        if ysm < ym : ym = ysm
        if zsm < zm : zm = zsm
    return IMP.algebra.BoundingBox3D( IMP.algebra.Vector3D(xm,ym,zm) , IMP.algebra.Vector3D(xM,yM,zM) )

def get_enveloppe_restraints( coverSpheres , particles ) :
    """ """
    restraints = []
    idx=0
    for p in particles :
        px = IMP.core.XYZR_decorate_particle(p)
        restraintName = "stickin"+p.get_name()
        scores = []
        for s in coverSpheres :
            offset = s[3] - 2*px.get_radius()
            unaryf = IMP.core.HarmonicUpperBound( offset , ubh_steepness )
    #        score  = IMP.core.DistanceToSingletonScore( unaryf , IMP.algebra.Vector3D(*s[0]) )
            score  = IMP.core.SphereDistanceToSingletonScore( unaryf , IMP.algebra.Vector3D(*s[0:3]) )
            scores.append(score)
#        print "restraint ",restraintName,"built on",len(scores),"scores"
        minScore = IMP.container.MinimumSingletonScore( scores, 1 , "min"+str(idx))
        r= IMP.container.SingletonsRestraint( minScore, IMP.container.ListSingletonContainer( [px] ), restraintName )
        r.set_maximum_score( max_out_of_enveloppe_score )
        restraints.append(r)
        idx+=1
        
    return restraints
    




def generate_sample_md(i,tfiihInfos,mcs,bb) :
    smd = HGM.sampling.SamplerSimpleMD(tfiihInfos,md_type,T,tau,sampling_step)
    smd.set_bbox(bb)
    
#        cs = smd.do_generate_sample(1)               #
    smd.do_generate_sample(dryRun_size)               # a dry run before
    cs = smd.do_generate_sample(sample_size,False)    # actually generating the sample
    saveName        = savePrefix+"--"+str(i)+".txt"

    mcs.read_configurationSet(cs)
    mcs.save_all_configs_to_file(os.path.join(saveDirSample,saveName))
    mcs.delete_all_configs()

def generate_sample_mccg(i,tfiihInfos,mcs,bb) :
    sampler= IMP.core.MCCGSampler(tfiihInfos.get_model())
    sampler.set_bounding_box(bb)
    # magic numbers, experiment with them and make them large enough for things to work
    sampler.set_number_of_conjugate_gradient_steps(MC_default_nb_CG_steps)
    sampler.set_number_of_monte_carlo_steps(MC_default_nb_MC_steps)
    sampler.set_number_of_attempts(MC_default_attempts)
    
    print "sampler.set_number_of_conjugate_gradient_steps(", MC_default_nb_CG_steps ,")"
    print "sampler.set_number_of_monte_carlo_steps(", MC_default_nb_MC_steps ,")"
    print "sampler.set_number_of_attempts(", MC_default_attempts ,")"
    
    sampler.set_save_rejected_configurations(True)
    print "attention les yeux"
    print "-"*20
    sampler.show()
    print "-"*20
    
    # We don't care to see the output from the sampler
    sampler.set_log_level(IMP.SILENT)
#    sampler.set_log_level(IMP.TERSE)
#    sampler.set_log_level(IMP.VERBOSE)

#    opst = HGM.sampling.OptimizerStatePeriodicSave(tfiihInfos.get_model())
    opst = HGM.sampling.OptimizerStateIncrementalPing("MCCG")
    sampler.add_optimizer_state( opst )

    # return the IMP.ConfigurationSet storing all the found configurations that
    # meet the various restraint maximum scores.
    cs      = sampler.get_sample()
    nbgc    = cs.get_number_of_configurations()
    mcs.read_configurationSet(cs)
    cs      = sampler.get_rejected_configurations()
    nbrc    = cs.get_number_of_configurations()
    mcs.read_configurationSet(cs)
    print "got {0} good configurations and {1} rejected".format(nbgc,nbrc)
    
    energies=[]
    for idx in range( mcs.get_number_of_configurations() ) :
        mcs.load_configuration(idx)
        energies.append(mcs.get_model().evaluate(False))
        
    print "energies",energies
    
    print "writing configuration file",
    saveName        = savePrefix+"--"+str(i)+".txt"
    print os.path.join(saveDirSample,saveName)
    mcs.save_all_configs_to_file(os.path.join(saveDirSample,saveName))
    
    mcs.delete_all_configs()
        

def main():
    
    time_start = time.time()
    
    print "-- create the universe"
    m = IMP.Model()
    m.set_log_level(IMP.SILENT)
#    m.set_log_level(IMP.TERSE)
#    m.set_log_level(IMP.VERBOSE)
    m.set_maximum_score(model_max_score)
    
    tfiihInfos = build_TFIIH_subunits_info(m)
    
    print "-- read the cover spheres"
    coverSpheres = read_cover_spheres( myBallsFileName )
    print "-- create and inject the EM sticking restraints"
    rs = get_enveloppe_restraints( coverSpheres , tfiihInfos.get_particles() )
    for r in rs :
        m.add_restraint(r)
#    print "spheres :"; 
#    for s in coverSpheres : print s
    bb = get_bbox_from_cover_spheres(coverSpheres)
    print "BBOX:",bb
    
    HGM.helpers.mute_all_restraints(m)
    
    times = HGM.times.Times()
    
    mcs         = HGM.representation.MyConfigurationSet(tfiihInfos)
    
    print "-- generate sample"
    loop_i = 1
    for i in sample_indexes:
        time_loop_start = time.time()
#        generate_sample_md(i,tfiihInfos,mcs,bb)
        generate_sample_mccg(i,tfiihInfos,mcs,bb)
        time_loop_stop = time.time()
        elapse_time = int(time_loop_stop-time_loop_start)
        times.set_sample_time(i,elapse_time)
        print "{0:d}({1:d}s)..".format( i , elapse_time ),
        if loop_i % 40 == 0 : print "" 
        sys.stdout.flush()
        loop_i+=1
    
    time_stop = time.time()

    print "full sample generated in {0:d}s".format( int(time_stop - time_start) )
    
if __name__ == "__main__" :
    main()
    print "...Finished !"
    