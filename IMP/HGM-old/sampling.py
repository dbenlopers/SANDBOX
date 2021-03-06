'''

'''

import IMP
import IMP.core, IMP.atom, IMP.algebra

import representation
#import helpers

BERENDSEN = "Berendsen"
LANGEVIN  = "Langevin"


def get_origin_bbox(bbox_size):
    BBs = bbox_size / 2.0
    bb          = IMP.algebra.BoundingBox3D(
        IMP.algebra.Vector3D(-BBs,-BBs,-BBs),
        IMP.algebra.Vector3D(BBs, BBs, BBs)
        )
    return bb

class OptimizerStateIncrementalPing(IMP.OptimizerState):
    """
    """
    def __init__(self,name,evaluate=True):
        IMP.OptimizerState.__init__(self)
        self._idx = 0
        self._name = name
        self._evaluate = evaluate
#        self.set_name(name)
        
    def update(self):
        self._idx += 1
#        print " <<< " + self.get_name() + " >>> " + str(self.__idx__)
        score=""
        if self._evaluate == True :
            score = " ("+str(self.get_optimizer().get_scoring_function().evaluate(False))+")"
        print " <<< " + self._name + " >>> " + str(self._idx) + score
        
    def reset(self):
        self._idx = 0


class OptimizerStatePeriodicSave(IMP.OptimizerState):
    """ This optimizerState saves a snapshot of the model configuration every "p" steps 
    
    configurations are saved to an internal ConfgurationSet that can be accessed via class methods
    """
    def __init__(self,m,p=1,running=False):
        """
        @param m:        The Model
        @param p:        The saving periodicity
        """
        IMP.OptimizerState.__init__(self)
        self._cs=IMP.ConfigurationSet(m)
        self._cs.set_log_level(IMP.SILENT)
        self._m             = m
        self._periodicity   = p
        self._count         = 0
#        self._running       = running
        #
    def update(self):
        """
        This method is called by the optimizer, and shouldn't be accessed by the user
        """
#        self.get_optimizer().get_model().show_restraint_score_statistics()
        if (self._count % self._periodicity) == 0: 
            self._cs.save_configuration()
        self._count+=1
#        print "DumpAllToConfigurationSetOptimizerState called; model evaluated to",self._m.evaluate(False)
        #
    def get_configuration_set(self):
        """
        Returns the ConfigurationSet containing the saved configurations
        """
        return self._cs
        #
    def reset_configuration_set(self):
        """
        resets the object state so that it can be directly re-used
        """
        del self._cs
        self._cs=IMP.ConfigurationSet(self._m)
        self._cs.set_log_level(IMP.SILENT)
        self._count = 0
        
    def get_model(self):
        return self._m
    
    def get_periodicity(self):
        return self._periodicity
    
    def set_periodicity(self,p):
        """ Sets the step size for periodicity saving, and returns previous value
        """
        previous_p = self._p
        self._periodicity = p
        return previous_p










class SamplerSimpleMD:
    """
        Generates a sample of configurations based on an MD trajectory
        
        
    """
    
    def __init__(self,mi,md_type=BERENDSEN,T=300,tau=0.01,saving_step=1):
        """
        @param mi:             the ModelInfo object describing the model on which we work
        @param md_type:        the MD engine type ("Berendsen", or "Langevin")
        @param T:              Temperature    (related to the energy sampled )
        @param tau:            Delta t        (the step size between two frames in the MD process)
        @param saving_step:    when generating the sample we will only take one frame every saving_step frames
        """
        
        
        self.default_bbox_size  = 200 # should change that to reflect the size of the problem
        self.default_cg_steps   = 500
        self.default_MD_stabilization_maximum_attempts      = 100
        self.default_MD_stabilization_sample_size           = 100
        
#        self._verbose_mode      = IMP.VERBOSE
#        self._verbose_mode      = IMP.TERSE
        self._verbose_mode      = IMP.SILENT
        
        self._bbox              = None
        self._bbox              = self.set_bbox( get_origin_bbox(self.default_bbox_size))
        
#        mii = representation.ModelInfo()
        self._mi                = mi
        self._model             = self._mi.get_model()
        self._md_type           = md_type
        self._T                 = T
        self._tau               = tau
#        self._saving_step       = saving_step

        self._opti_CG           = None
        
        self._opti_md           = None
        self._opti_md_st        = None
        self._opti_md_sos       = None
        
        self._opti_CG           = IMP.core.ConjugateGradients( self._mi.get_model() )
        self._opti_CG.set_stop_on_good_score(True)
        self._opti_CG.set_log_level(IMP.SILENT)

        self._opti_md=IMP.atom.MolecularDynamics()
        self._opti_md.set_model(self.get_model())
        self._opti_md.set_stop_on_good_score(False)
        self._opti_md.assign_velocities( T )
        self._opti_md.set_time_step( tau )
        self._opti_md.set_log_level(IMP.SILENT)
        # this optimizer state is absolutely required to equilibrate the MD : constant T
        if      md_type == BERENDSEN :
            self._opti_md_st = IMP.atom.BerendsenThermostatOptimizerState(self._opti_md.get_simulation_particles(), self._T,self._tau)
        elif    md_type == LANGEVIN :
            self._opti_md_st = IMP.atom.LangevinThermostatOptimizerState(self._opti_md.get_simulation_particles(), self._T,self._tau)
        else :
            raise KeyError("cannot understand md_type("+str(md_type)+"), should be either 'BERENDSEN', or 'LANGEVIN'")
        self._opti_md_st.set_log_level(IMP.SILENT)
        self._opti_md.add_optimizer_state(self._opti_md_st)
        # now add the frame saver
        self._opti_md_sos     = OptimizerStatePeriodicSave(self._model,saving_step)
        self._opti_md_sos.set_log_level(IMP.SILENT)
        self._opti_md.add_optimizer_state(self._opti_md_sos)
        
        self._opti_CG.add_optimizer_state(self._opti_md_sos)
        

    def set_imp_verbode_mode(self,v_mode):
        self._opti_md_sos.set_log_level(v_mode)
        self._opti_md_st.set_log_level(v_mode)
        self._opti_CG.set_log_level(v_mode)
        
    def set_verbose_mode(self,v_mode):
        self._verbose_mode = v_mode
    
    def get_model(self):
        """ """
        return self._model
    
    def get_velocities(self):
        """ """
        return self._T
    
    def set_velocities(self,T):
        """ """
        self._T = T
        self._opti_md_st.set_temperature(T)
        self._opti_md.set_temperature(T)
    
    def get_delta(self):
        """ """
        return self._tau
    
    def set_delta(self,tau):
        """ """
        self._tau = tau
        self._opti_md_st.set_tau(tau)
        self._opti_md.set_time_step(tau)
    
    def get_saving_step(self):
        return self._opti_md_sos.get_periodicity()
        
    def set_saving_step(self,saving_step):
        self._opti_md_sos.set_periodicity(saving_step)


    def get_bbox(self):
        return self._bbox
    
    def set_bbox(self,bbox):
        prev_bbox = self.get_bbox()
        self._bbox = bbox
        return prev_bbox

    
    def do_randomize_model(self, bbox_size=None):
        """
            Randomly place all bead paticles of the model in a bounding box of side bbox_size centered at the origin
        """
        if bbox_size == None :
            bb = self.get_bbox()
        else :
            bb = get_origin_bbox(bbox_size)
        particleXs  = [IMP.core.XYZ_decorate_particle(p) for p in self._mi.get_all_particles()]
        set_random_coods = lambda x : x.set_coordinates( IMP.algebra.get_random_vector_in(bb) )
        map(set_random_coods,particleXs)
#        helpers.randomize_particles_in_bbox(bb, particleXs)
        
        
    def do_CG(self,nb_cg_steps = None):
        """
            Performs a number of GC steps
            This function should be used for instance after a randomization to quickly 
        """
        if nb_cg_steps == None :
            nb_cg_steps = self.default_cg_steps
        self._opti_CG.optimize( nb_cg_steps )
    
#    def do_stabilize_around_energy(self,e):
#        """
#            
#        """
        
#    def do_MD_equilibrate(self):
#        """
#            runs MD simulations until an energy equilibrium is reached;            
#            that is, the mean value for the energies that are mesured on a series of frames do not vary anymore
#            
#            returns the number of iterations that were needed for the equilibration
#        """
#        sample_size = self.default_MD_stabilization_sample_size
#        
##        def ups_and_downs_statistics(l):
##            ups      = 0
##            downs    = 0
##            up_acc   = 0.0
##            down_acc = 0.0
##            n        = len(l)
##            for i in range(n-1) :
##                v = l[i] - l[i+1]
##                if      v > 0 :
##                    downs+=1; down_acc += v
##                elif    v < 0:
##                    ups+=1; up_acc -= v
##            return ((ups,downs),(up_acc,down_acc))
##
#        def ups_and_downs_around_mean_statistics(l):
#            
#            ups      = 0
#            downs    = 0
#            n        = len(l)
#            E = sum(l)/n
#            for i in range(n-1) :
#                v = l[i] - E
#                if      v > 0 :
#                    downs+=1
#                elif    v < 0:
#                    ups+=1
#            return (ups,downs)
#           
#        def MD_is_stabilized( ups_and_downs_stats ):
##            (u,d),(ua,da) = ups_and_downs_stats
#            (u,d) = ups_and_downs_stats
##            trajectory is considered equilibrated when
##                - there is a large number of stationnary or
##                    - there is approx the same number of ups and downs
##                    ( - the cumulated magnitude of ups and dows is equivalent ) <-- not yet taken into account
#            if (sample_size / float(u+d) > .5) :
#                return True
#            else :
#                if (abs(u - d) / float(sample_size)) > 0.1 : 
#                    return False
#                else :
#                    return True
#            
#                 
#        for i in range(self.default_MD_stabilization_maximum_attempts):
#            cs = self.do_generate_sample(sample_size, False)
#            energies=helpers.compute_sample_energies(cs, self.get_model())
##            uds = ups_and_downs_statistics(energies)
#            uds = ups_and_downs_around_mean_statistics(energies)
#            if self._verbose_mode ==IMP.VERBOSE :
#                print "do_MD_equilibrate; step",i,"; ups and downs statistics",uds
#            if MD_is_stabilized(uds) : break
#
##        prev_std=0
##        for i in range(self.default_MD_stabilization_maximum_attempts):
##            cs = self.do_generate_sample(sample_size, False)
##            energies=helpers.compute_sample_energies(cs, self.get_model())
##            E,std = helpers.compute_list_statistics(energies)
##        return i

    def do_generate_sample(self,sample_size,from_scratch=True):
        """
        @param sample_size:     The size of the resulting sample
        @param from_scratch:    If set to False, the sample is generated using the current model as seed, 
            otherwise, start with a random positionning of beads in a bbox, a CG
            
        @return : a ConfigurationSet
        """
        if from_scratch == True :
            self.do_randomize_model()
            self.do_CG()
#            self.do_MD_equilibrate()
        
        nbMD = self.get_saving_step() * sample_size
        self._opti_md.optimize(nbMD)
        cs                  = self._opti_md_sos.get_configuration_set()
        self._opti_md_sos.reset_configuration_set()
        return cs
        
