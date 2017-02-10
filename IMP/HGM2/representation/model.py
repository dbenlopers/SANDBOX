'''

'''

import complex
import IMP, IMP.core, IMP.atom

class Model():
    """ Concrete implementation of an HGM system in the IMP paradigm
    
        Based on descriptions, this class is responsible for the actual building of an IMP::Model, crowded  
        with particules and scores, and ease access to these elements
        """
        
    def __init__(self , cplx_rep , topology = None , restraints = None):
        self.__imp_model = IMP.Model()
        self.__rep = cplx_rep
        self.__subunit_particles = []
#        self.__bead_to_particles = {}
#        self.__topology = topology
        
        print "crowding universe"
        self.__build_complex_particles(cplx_rep)
        
#    def __build_complex_particles(self,cplx_rep):
    def __build_complex_particles(self):
        cplx_rep = self.__rep
        for sr in cplx_rep.get_subunits() :
            for br in sr.get_beads():
                p = IMP.Particle(self.__imp_model,br.get_full_name())
                IMP.atom.Mass.setup_particle(p, br.get_mass())
                xyzd=IMP.core.XYZR.setup_particle(p);
                self.__subunit_particles.append(xyzd)
                xyzd.set_radius(br.get_radius());
                xyzd.set_coordinates_are_optimized(True);
                
#    def __build_topology(self):
#        if self.__topology == None :
#            raise Exception("No topology")
        
                
        
        
    
    def get_imp_model(self):
        return self.__imp_model
        
