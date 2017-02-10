'''

generate sample via MD, for various variables
and save samples in txt files
'''





import os

import IMP, IMP.algebra, IMP.atom, IMP.core, IMP.container
import HGM, HGM.representation
#from representation_TFIIH_models_arnaud1 import build_TFIIH_subunits_info
from representation_TFIIH_models_arnaud3 import build_TFIIH_subunits_info
#from representation_TFIIH_models_arnaud2 import build_TFIIH_subunits_info

import time
default_ev_spring_constant              = HGM.representation.default_ev_spring_constant
#excluded_volume_restraint_max_score     = representation.default_ev_spring_constant
default_playground_size                 = 100
#default_nb_samples                      = 5
default_nb_samples                      = 1
default_cg_steps                        = 500
default_sample_size                     = 200
default_save_dir                        = "scrap2/MD/samplesSaves"
#prefix                                  = "TFIIH-sample-MD---"
#prefix                                  = "TFIIH-2-sample-MD---"
#prefix                                  = "TFIIH-2-LJ-sample-MD---"
prefix                                  = "TFIIH-3--sample-MD---"

print "Create model"
m           = IMP.Model()
m.set_log_level(IMP.SILENT)

print "Create CG optimizer"
cgo = IMP.core.ConjugateGradients(m)
cgo.set_stop_on_good_score(True)
cgo.set_log_level(IMP.SILENT)

def randomize_particles_in_bbox(bb,particles):
    """ Sets a list of particles randomly in a bbox
    @param bb: the bounding box
    @param particles:  the list of partcles to move
    """
    #
    for p in particles :
        x = IMP.core.XYZ(p)
        x.set_coordinates( IMP.algebra.get_random_vector_in(bb) )


def initialize_configuration(BBs,init_type,Xparticles):
    """
    initialize a configuration prior to MD simulation
    this is achieved by randomly setting the particles in a bbox of size BBs,
    then optionnally (if init_type == "CG"), by applying a conjugate gradiant in order to get a
    first solution with a good score prior to launch the MD simulation 
    """
#    print ">> initialize_configuration << build a bbox of size ",BBs
    bb=IMP.algebra.BoundingBox3D(
            IMP.algebra.Vector3D(-BBs,-BBs,-BBs),
            IMP.algebra.Vector3D(BBs, BBs, BBs)
            )
#    print ">> initialize_configuration << randomize points in my bbox of size ",BBs
#    randomize_particles_in_bbox(bb, particles)
    set_random_coods = lambda x : x.set_coordinates( IMP.algebra.get_random_vector_in(bb) )
    map(set_random_coods,Xparticles)

    if init_type == "CG" :
#        print ">> initialize_configuration << CG optimization of my random config"
        cgo.optimize(default_cg_steps)

#    print Xparticles
    

class saveConfigurationsOptimizerState(IMP.OptimizerState):
    """ an optimizerState to save the model configuration every "P" steps
    
    configurations are saved to an internal ConfgurationSet that can be accessed via class methods
    """
    def __init__(self,m,p=1):
        """
        @param m:        The Model
        @param p:        The saving periodicity
        """
        IMP.OptimizerState.__init__(self)
        self._cs=IMP.ConfigurationSet(m)
        self._cs.set_log_level(IMP.SILENT)
        self._m=m
        self._periodicity=p
        self._count=0
        #
    def update(self):
        """
        this method is called by the optimizer, and shouldn't be accessed by the user
        """
#        self.get_optimizer().get_model().show_restraint_score_statistics()
        if (self._count % self._periodicity) == 0: 
            self._cs.save_configuration()
        self._count+=1
#        print "DumpAllToConfigurationSetOptimizerState called; model evaluated to",self._m.evaluate(False)
        #
    def get_configuration_set(self):
        """
        returns the set of saved configurations
        """
        return self._cs
    
    def reset_configuration_set(self):
        """
        resets the object state so that it can be directly re-used
        """
        del self._cs
        self._cs=IMP.ConfigurationSet(self._m)
        self._count = 0

def generate_MD_sample(m,md_type="Berendsen",T=300,tau=0.01,nbMD=100,saving_step=1,) :
    """
    @param m:              IMP model
    @param md_type:        the MD engine type ("Berendsen", or "Langevin")
    @param T:              Temperature
    @param tau:            Delta t
    @param nbMD:           Number of steps in the MD
    @param saving_step:    we will save only a configuration every saving_step steps
    """

    sos     = saveConfigurationsOptimizerState(m,saving_step)
    #
    md=IMP.atom.MolecularDynamics()
    md.set_model(m)
    md.set_stop_on_good_score(False)
    md.assign_velocities(T)
    md.set_time_step(tau)
    if      md_type == "Berendsen" :
        st = IMP.atom.BerendsenThermostatOptimizerState(md.get_simulation_particles(), T,tau)
    elif    md_type == "Langevin" :
        st = IMP.atom.LangevinThermostatOptimizerState(md.get_simulation_particles(), T,tau)
    else :
        raise KeyError("cannot understand md_type("+str(md_type)+"), should be either 'Langevin', or 'Berendsen'")
    
    md.add_optimizer_state(st)
    md.add_optimizer_state(sos)
    md.set_log_level(IMP.SILENT)
    st.set_log_level(IMP.SILENT)
    sos.set_log_level(IMP.SILENT)
    
    md.optimize(nbMD)
    cs                  = sos.get_configuration_set()

    return cs


def save_sample(cs,saveDir,saveName):
#    cs = representation.MyConfigurationSet
    cs.save_all_configs_to_file(os.path.join(saveDir,saveName))       



def main () :
            
    
    
    print "-- build TFIIH representation"
#    # build informations
#    protein_info_dict = HGM.representation.build_TFIIH_subunits_info()
#    # create hierarchy and interanl connections
#    all = HGM.representation.create_TFIIH_representation(m, protein_info_dict)
#    # create inter subunit connections
#    representation.create_TFIIH_connections(m, protein_info_dict)
#    #    add excluded volume
#    evr=IMP.core.ExcludedVolumeRestraint( IMP.container.ListSingletonContainer(IMP.atom.get_leaves(all)) , default_ev_spring_constant )
#    m.add_restraint( evr )
#    m.set_maximum_score(evr,default_ev_spring_constant)
    tfiihInfos = build_TFIIH_subunits_info(m)
    
#    T               = 1000
#    tau             = 100
#    nbMD            = 50000
#    nbMDsaves       =   100

#    particleXs = [IMP.core.XYZ_decorate_particle(p) for p in IMP.atom.get_leaves(all)]
#    particleXs = [IMP.core.XYZ_decorate_particle(p) for p in tfiihInfos.get_particles()]
    particleXs = [IMP.core.XYZ_decorate_particle(p) for p in tfiihInfos.get_all_particles()]
    print "  got ",len(particleXs),"XYZ decorated particles"
    print particleXs
    
    mcs= HGM.representation.MyConfigurationSet(tfiihInfos)
    print "--generate samples"
    for sample_index in range(default_nb_samples) :
#        for BBs in [500,100,20] :
        for BBs in [200] :
#            for init_type in ["Random","CG"] :
            for init_type in ["CG"] :
#                for T in [300,1000,10000] :
                for T in [300] :
#                    for tau in [1,10,100] :
                    for tau in [100] :
#                        for md_type in ["Berendsen","Langevin"] :
                        for md_type in ["Berendsen"] :
#                            for nbMD in [default_sample_size,default_sample_size*10,default_sample_size*100] :
                            for nbMD in [default_sample_size*100] :
                                
                                loop_start_time = time.time()
                                
                                saving_step=int(nbMD/default_sample_size)

                                prefixtag = "BBs({1})({2})--{5}-T({3})-tau({4})-nbSteps({6})-saveStep({8})--sample-size-{7}--{0:d}".format(
                                sample_index,   # 0
                                BBs,            # 1
                                init_type,      # 2
                                T,              # 3
                                tau,            # 4
                                md_type,        # 5
                                nbMD,           # 6
                                default_sample_size, # 7
                                saving_step     # 8
                                )
                                
                                print "working on ",prefixtag,"... "

                                initialize_configuration(BBs,init_type,particleXs)
                                cs = generate_MD_sample(m,md_type,T,tau,nbMD,saving_step)
                                
                                mcs.delete_all_configs()
                                mcs.read_configurationSet(cs)
                                
                                saveDir         = default_save_dir
                                saveName        = prefix + prefixtag + ".txt"
                                save_sample(mcs,saveDir,saveName)
                                
                                loop_stop_time = time.time()
                                
                                print "  done in ",loop_stop_time-loop_start_time
    
if __name__ == "__main__" :
    start_time = time.time()
    main()
    stop_time = time.time()
    print "all done in ",stop_time-start_time,"seconds"
