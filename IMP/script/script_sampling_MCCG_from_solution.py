'''
Create models from solution



'''
import os
import sys

import time

import IMP, IMP.core, IMP.container, IMP.algebra

import HGM
import HGM.sampling
import HGM.display
import HGM.helpers
import HGM.times

from alternate_configs import configs




#
#    PARAMETERS
#
#
#


#config_name_for_this_run    = "fixedGeom_EM_1_0"
#config_name_for_this_run    = "fixedGeom_EM_1_1"
#config_name_for_this_run    = "fixedGeom_EM_1_2"

#config_name_for_this_run    = "arp_EM_0_1"
#config_name_for_this_run    = "arp_EM_0_2aLM"
config_name_for_this_run    = "arp_EM_0_2aLA"
#config_name_for_this_run    = "arp_EM_0_2aLMs"
#config_name_for_this_run    = "arp_EM_0_2aL"
#config_name_for_this_run    = "arp_EM_0_2"
#config_name_for_this_run    = "arp_EM_0_2aLFc4"
#config_name_for_this_run    = "arp_EMd_0_2aLFc4"

tfiihRepresentationFileName = configs[config_name_for_this_run][0]

runDir                      = os.path.join("results",config_name_for_this_run)
saveDirSample               = os.path.join(runDir,"samples")
savePrefix                  = "saves"

for d in [runDir,saveDirSample] :
    HGM.helpers.check_or_create_dir(d)

model_max_score = 20000


#    MC CG sampling
#MC_default_nb_CG_steps  = 10
#MC_default_nb_CG_steps  = 50
MC_default_nb_CG_steps  = 100

#MC_default_nb_MC_steps  = 100
#MC_default_nb_MC_steps  = 500
#MC_default_nb_MC_steps  = 50000
#MC_default_nb_MC_steps  = 5000
#MC_default_nb_MC_steps  = 1000

# for ARP
MC_default_nb_MC_steps  = 2000

#MC_default_attempts     = 500
#MC_default_attempts     = 50
MC_default_attempts     = 200
#MC_default_attempts     = 5
#MC_default_attempts     = 1
#MC_default_attempts     = 2

#
#    Sample configuration
#
          
#sample_indexes      = [10002]
#sample_indexes      = [10003]
sample_indexes      = range(0,20) #10 attempts MCCGsampler
#sample_indexes      = range(20,25) # 5 attempts MCCGsampler ubh_steep = 50, 1000/100 MC/CG
#sample_indexes      = range(25,30) # 5 attempts MCCGsampler ubh_steep = 50, 1000/100 MC/CG
#sample_indexes      = [9,10,12,13,15,16,17,18,19]
#


#    import the function responsible for modelisation of TFIIH complex
#exec ( "from {0:s} import build_TFIIH_subunits_info".format( tfiihRepresentationFileName ) )
exec ( "from {0:s} import build_subunits_info".format( tfiihRepresentationFileName ) )





def output_sample_energies(mcs):
    energies=[]
    for idx in range( mcs.get_number_of_configurations() ) :
        mcs.load_configuration(idx)
        energies.append(mcs.get_model().evaluate(False))
    print "energies",energies
    
def output_energies_decomposition(tfiihinfo):
    evaluated_restraints = []
    se   = tfiihinfo.get_model().evaluate(False)
    sevr = tfiihinfo.evr.evaluate(False)
    sstr = sum ( map( ( lambda r:r.evaluate(False)) , tfiihinfo.str ) )
    sscr = sum ( map( ( lambda r:r.evaluate(False)) , tfiihinfo.scr ) )
    semr = tfiihinfo.emr.evaluate(False)
    for (name,val) in [("total-energy",se  ), ("sub-cohes",sstr ), ("sub-inter", sscr ),("excl-vol", sevr ),("EM",semr ) ] :
        evaluated_restraints.append("{0:s}{1:10.2f}".format(name, val))
    try :
        locr = tfiihinfo.locr.evaluate(False)
        evaluated_restraints.append("LOC:{0:10.2f}".format(locr))
    except :
        pass
    try : 
        fdr = tfiihinfo.fdr.evaluate(False)
        evaluated_restraints.append("FRET:{0:10.2f}".format(fdr))
    except :
        pass
    
    print "["+" ".join(evaluated_restraints)
    
        
#    print "[total-energy:{0:10.2f}] sub-cohes:{1:10.2f} sub-inter:{2:10.2f} excl-vol:{3:10.2f} EM:{4:10.2f}".format(
#           se , sstr, sscr, sevr, semr )

    
#    print "[total-energy:{0:10.2f}] sub-cohes:{1:10.2f} sub-inter:{2:10.2f} excl-vol:{3:10.2f} EM:{4:10.2f} LOC:{5:10.2f}".format(
#           se , sstr, sscr, sevr, semr, locr )

#    fdr = tfiihinfo.fdr.evaluate(False)
#    print "[total-energy:{0:10.2f}] sub-cohes:{1:10.2f} sub-inter:{2:10.2f} excl-vol:{3:10.2f} EM:{4:10.2f} FRET:{5:10.2f}".format(
#           se , sstr, sscr, sevr, semr, fdr )  


def save_sample(mcs,sample_idx):    
    print "writing configuration file",
    saveName        = savePrefix+"--"+str(sample_idx)+".txt"
    print os.path.join(saveDirSample,saveName)
    mcs.save_all_configs_to_file(os.path.join(saveDirSample,saveName))




def generate_sample_mccg(tfiihInfos,bb) :
    print " == sample generation == "
#    mcs     = HGM.representation.MyConfigurationSet(tfiihInfos)
    mcs=HGM.representation.MyConfigurationSet(tfiihInfos)
    mcs_sol=HGM.representation.MyConfigurationSet(tfiihInfos)
    
    sol_file_path="/home/arnaud/Desktop/TFIIH/data/ARP/save-1TYQ-HGM.txt"

    
    
    for i in range(MC_default_attempts):
        mcs_sol.read_all_configs_from_file(sol_file_path)
        mcs_sol.load_configuration(0)
  
        sampler= IMP.core.MCCGSampler(mcs_sol.get_model())
        sampler.set_bounding_box(bb)
        # magic numbers, experiment with them and make them large enough for things to work
        sampler.set_number_of_conjugate_gradient_steps(MC_default_nb_CG_steps)
        sampler.set_number_of_monte_carlo_steps(MC_default_nb_MC_steps)
    
#        sampler.set_number_of_attempts(MC_default_attempts)
        sampler.set_number_of_attempts(1)

  
        print "  sampler.set_number_of_conjugate_gradient_steps(", MC_default_nb_CG_steps ,")"
        print "  sampler.set_number_of_monte_carlo_steps(", MC_default_nb_MC_steps ,")"
    
#        print "  sampler.set_number_of_attempts(", MC_default_attempts ,")"
        print "  sampler.set_number_of_attempts(", 1 ,")"
    
#        uncomment for saving the whole MC processes instead of just the final position 
#        ops = HGM.sampling.OptimizerStatePeriodicSave(tfiihInfos.get_model())
#        sampler.add_optimizer_state( ops )

#        uncomment to show the energies
        opst = HGM.sampling.OptimizerStateIncrementalPing("MCCG")
        sampler.add_optimizer_state( opst )
    
        sampler.set_save_rejected_configurations(True)
        sampler.set_is_refining(True)
    
    #    We don't care to see the output from the sampler
        sampler.set_log_level(IMP.SILENT)
#        sampler.set_log_level(IMP.TERSE)
#        sampler.set_log_level(IMP.VERBOSE)

    #    return the IMP.ConfigurationSet storing all the found configurations that
    #    meet the various restraint maximum scores.
        cs      = sampler.get_sample()
        nbgc    = cs.get_number_of_configurations()
        mcs.read_configurationSet(cs)
        cs      = sampler.get_rejected_configurations()
        nbrc    = cs.get_number_of_configurations()
        mcs.read_configurationSet(cs)
        print "got {0} good configurations and {1} rejected".format(nbgc,nbrc)
    
    
#        mcs.read_configurationSet(ops.get_configuration_set())
    return mcs_sol
    
#    mc = HGM.representation.MyConfigurationSet()
#    mc=ops.get_configuration_set()
#    print "configuration set registered",mc.get_number_of_configurations(),"configs"
#    if mc.get_number_of_configurations() > 0:
#        mcs.read_configurationSet(mc)
    


def refine_sample_mccg(tfiihInfos,mcs):
    mcsr = HGM.representation.MyConfigurationSet(tfiihInfos)
#    mcsr=tfiihInfos
    #    Some locally global variables ( I am a pig )
    particles       = mcsr.get_particles()
    xparticles      = [ IMP.core.XYZR_decorate_particle(p) for p in particles ]
    movers          = []
    m               = tfiihInfos.get_model()
    size            = len (xparticles)
    
    nb_local_cg_steps   = 10
    mc_alternate_moves  = True
    
    #    Set the conjugate gradient optimizers
    opti_cg     = IMP.core.ConjugateGradients(m)
    #    Set the Monte Carlo optimizerMyConfigurationSet
#    opti_mc     = IMP.core.MonteCarlo(m)
    opti_mc     = IMP.core.MonteCarloWithLocalOptimization( opti_cg , nb_local_cg_steps )
    # add movers
    for x in xparticles :
        movers.append(IMP.core.BallMover([x], x.get_radius()*3))
        movers[-1].set_was_used(True)
    if mc_alternate_moves :
        sm= IMP.core.SerialMover(movers)
        opti_mc.add_mover(sm)
    else :
        for mo in movers : 
            opti_mc.add_mover(mo)
    
    
    
    
#    ops = HGM.sampling.OptimizerStatePeriodicSave(tfiihInfos.get_model())
#    opti_mc.add_optimizer_state( ops )
    
    nb_MC_runs = 10
    def compute_temperature_for_run( j ) :
        T_fst  = 1600.00
        T_last =  100.00
        t =  (float(nb_MC_runs-1-j))/(nb_MC_runs-1)
        return t*T_fst + (1-t)*T_last
    compute_nb_MC_steps_for_run = lambda j : 20 * size * (j+1)
    def reset_mover_size_for_run(j):
        moverFactor_first = 2.0
        moverFactor_last  =  .25
        t=(float(nb_MC_runs-1-j))/(nb_MC_runs-1)
        factor = t*moverFactor_first + (1-t)*moverFactor_last
        for mo in movers :
            mo.set_radius( IMP.core.XYZR_decorate_particle(mo.get_output_particles()[0]).get_radius() * factor )
    def print_radius_moved_particle(i):
        return movers[i].get_radius()
    
    # for each configuration in the sample
    for cfg in range(mcs.get_number_of_configurations()) :
        # refine by applying some new mccg
        print "refining config",cfg
        mcs.load_configuration(cfg)
        output_energies_decomposition(tfiihInfos)
        for j in range(nb_MC_runs):
            T = compute_temperature_for_run(j)
            N = compute_nb_MC_steps_for_run(j)
            reset_mover_size_for_run(j)
            opti_mc.set_kt( T )      
            print " accuracy loop",j,"(",T,",",N,"){",print_radius_moved_particle(6),"}",
    #        print opti_mc.optimize(N),m.evaluate(False),opti_cg.optimize(nb_cg_steps)
            opti_mc.optimize(N)
            print m.evaluate(False)
        output_energies_decomposition(tfiihInfos)
        mcsr.save_current_config()
        
#    mcsr.read_configurationSet(ops.get_configuration_set())
    return mcsr
    



def refine_sample_mccg_per_subunits(tfiihInfos,mcs,configs):
    
    mcsr = HGM.representation.MyConfigurationSet(tfiihInfos)
    
    m               = tfiihInfos.get_model()
    size            = len (tfiihInfos.get_all_particles())
    subunitNames    = tfiihInfos.get_subunit_names()
    particles       = {}
    movers          = {}
    sms             = {}
    for subunitName in subunitNames :
        ps = tfiihInfos.get_subunit_info(subunitName).get_all_particles()
        xps      = [ IMP.core.XYZR_decorate_particle(p) for p in ps ]
        particles[subunitName] = xps
        
        mvs=[]
        for x in xps :
            mvs.append(IMP.core.BallMover([x], x.get_radius()*3))
            mvs[-1].set_was_used(True)
            sm = IMP.core.SerialMover(mvs)
            movers[subunitName] = mvs
            sms[subunitName]    = sm
        
    nb_local_cg_steps   = 10
    mc_alternate_moves  = True
    opti_cg     = IMP.core.ConjugateGradients(m)
    opti_mc     = IMP.core.MonteCarloWithLocalOptimization( opti_cg , nb_local_cg_steps )
    
    
    
    
#    ops = HGM.sampling.OptimizerStatePeriodicSave(tfiihInfos.get_model())
#    opti_mc.add_optimizer_state( ops )
    
    for cfg in range(mcs.get_number_of_configurations()) :
        print "refining config",cfg
        mcs.load_configuration(cfg)
        output_energies_decomposition(tfiihInfos)
        for subunitName in subunitNames :
            print "toying around with subunit",subunitName
#            print "removed ",len(opti_mc.get_movers()),"movers"
            opti_mc.remove_movers( opti_mc.get_movers() )
            sm = sms[subunitName]
            mvs = movers[subunitName]
            opti_mc.add_mover(sm)
            j=0
            for T,N,R in configs :
                print "  subunit loop",j,"(",T,",",N,",",R,")",
                opti_mc.set_kt(T)
                for mo in mvs :
                    mo.set_radius(R)
                    print opti_mc.optimize(N),
                print ""
                j+=1
#            #
#            mcsr.save_current_config()
#            #
        output_energies_decomposition(tfiihInfos)
        mcsr.save_current_config()
        
#    mcsr.read_configurationSet(ops.get_configuration_set())    
    return mcsr





def main():
    
#    sample_indexes = [ int(sys.argv[1]) ]

    time_start = time.time()
    
    print "-- create the universe"
    m = IMP.Model()
    m.set_log_level(IMP.SILENT)
#    m.set_log_level(IMP.TERSE)
#    m.set_log_level(IMP.VERBOSE)
    m.set_maximum_score(model_max_score)
    
    tfiihInfos = build_subunits_info(m)
    
    
        
    bbEM = tfiihInfos.emSpheres.compute_bbox()
    print "BBOX EM:",bbEM
    v=bbEM.get_corner(1)-bbEM.get_corner(0)
    bb = IMP.algebra.BoundingBox3D( 
            bbEM.get_corner(0) - v/2.,
            bbEM.get_corner(1) + v/2.
             )
    
    HGM.helpers.mute_all_restraints(m)
    
    times = HGM.times.Times()
    
#    mcs         = HGM.representation.MyConfigurationSet(tfiihInfos)
    
    print "-- generate sample"
    loop_i = 1
    for i in sample_indexes:
        time_loop_start = time.time()
#        generate_sample_md(i,tfiihInfos,mcs,bb)
#        generate_sample_mymccg(i,tfiihInfos,mcs,bb)

        print "MCCG SAMPLING   ","-"*10
        mcs = generate_sample_mccg(tfiihInfos,bb)

#        mc  = HGM.representation.MyConfigurationSet(tfiihInfos)
#        mc.save_current_config()
        print "MCCG REFINING   ","-"*10
        mcsr = refine_sample_mccg(tfiihInfos,mcs)
#        mcsr = refine_sample_mccg(tfiihInfos,mc)

        configs = [ (800,100,2),(600,200,1.5),(400,300,1.5),(200,500,1)]
#        configs = [ (800,100,2),(600,50,1.5),(400,100,1.5),(200,500,1)]
#        mc  = HGM.representation.MyConfigurationSet(tfiihInfos)
#        mc.save_current_config()
        print "MCCG SUBUNITS REFINING   ","-"*10
        mcsr2 = refine_sample_mccg_per_subunits(tfiihInfos,mcsr,configs)
#        mcsr2 = refine_sample_mccg_per_subunits(tfiihInfos,mc,configs)
        print "MCCG SUBUNITS REREFINING   ","-"*10
#        mc  = HGM.representation.MyConfigurationSet(tfiihInfos)
#        mc.save_current_config()
        configs = [ (400,200,1.5),(300,400,1),(100,600,.5)]
#        mcsr3 = refine_sample_mccg_per_subunits(tfiihInfos,mc,configs)
        mcsr3 = refine_sample_mccg_per_subunits(tfiihInfos,mcsr2,configs)

#        mcs.read_configurationSet(mcsr)
#        mcs.read_configurationSet(mcsr2)
#        mcs.read_configurationSet(mcsr3)
        print "SAVE       ","-"*10
        print " ",mcs.get_number_of_configurations(),"configurations"
        save_sample(mcsr3,i)
#        save_sample(mcsr,i)
        
        
        time_loop_stop = time.time()
        elapse_time = int(time_loop_stop-time_loop_start)
        times.set_sample_time(i,elapse_time)
        print "{0:d}({1:d}s)..".format( i , elapse_time ),
        if loop_i % 40 == 0 : print "" 
        sys.stdout.flush()
        loop_i+=1
        
        mcs.delete_all_configs()
    
    time_stop = time.time()

    print "full sample generated in {0:d}s".format( int(time_stop - time_start) )
    
if __name__ == "__main__" :
    main()
    print "...Finished !"
    
