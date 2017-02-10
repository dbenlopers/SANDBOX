'''


Contains generic classes and function to help with the representation of a system
'''



import IMP
import IMP.atom
import IMP.core, IMP.statistics, IMP.container, IMP.algebra
import IMP.display

import math
import time
#import glob
#import pickle
#from os import path,mkdir

try :
    r=IMP.RandomNumberGenerator()
except :
    try :
        r=IMP.base.RandomNumberGenerator()
    except :
        pass
r.seed(time.time())

fully_extended_Ca_max_len       = 3.8 # A    found on wikipedia Beta_strand : fully extended size between Carbons alpha i and i+2 is 7.6
protein_density                 = 0.84 # Da / A^3

default_spring_constant         = 100
default_ev_spring_constant      = 100
excluded_volume_restraint_max_score = default_ev_spring_constant

EM_coveringSpheres_ubh_steepness                = 50
EM_coveringSpheres_ubh_steepness_max_score      = EM_coveringSpheres_ubh_steepness

linker_nb_AA_per_bead           = 10
linker_bead_radius              = 0
linker_ratio_radius_to_extended = 2.0 / 3.0
def recompute_linker_bead_radius():
    global linker_bead_radius
    linker_bead_radius = linker_ratio_radius_to_extended  * linker_nb_AA_per_bead * fully_extended_Ca_max_len
    return linker_bead_radius
recompute_linker_bead_radius()

def get_linker_ratio_radius_to_extended():
    return linker_ratio_radius_to_extended
def set_linker_ratio_radius_to_extended(r):
    global linker_ratio_radius_to_extended
    linker_ratio_radius_to_extended = r
def get_linker_nb_AA_per_bead():
    return linker_nb_AA_per_bead
def set_linker_nb_AA_per_bead(nbaapb):
    global linker_nb_AA_per_bead 
    linker_nb_AA_per_bead=nbaapb
def get_linker_bead_radius():
    return linker_bead_radius
def set_linker_bead_radius(r):
    global linker_bead_radius
    linker_bead_radius = r

score_HUBSDS_default = IMP.core.HarmonicUpperBoundSphereDistancePairScore( 0 , default_spring_constant )
#score_HDPS_default  = IMP.core.HarmonicDistancePairScore( 0 , default_spring_constant )



__verbose = False
#__verbose = True
def emote(message):
    if __verbose :
        print message
            
def set_verbose(verbose_mode=True):
    __verbose = verbose_mode
    


def compute_bead_mass( bead_size ):
    """ Computes the mass of a bead that constitutes a globular domain
    @param bead_size: number of AA composing the bead
    """
    return 110 * bead_size

def compute_bead_radius( bead_size ):
    """ Computes the radius of a bead that constitutes a globular domain
    @param bead_size: number of AA composing the bead
    """
    bead_mass   = compute_bead_mass( bead_size )
    bead_volume = bead_mass / protein_density
    bead_radius = math.pow(  (3*bead_volume) / (4*math.pi),\
                             .33333)
    return bead_radius
    
def compute_chain_max_len( link_size ):
    """ Computes the size of a linker between two beads
    @param link_size: number of AA composing the link
    """
#    return compute_bead_radius( link_size )
    return link_size * fully_extended_Ca_max_len





linker_bead_mass                = compute_bead_mass(linker_nb_AA_per_bead)

class SubunitInfo:
    
    class Bead(dict):
        def __init__(self,name,size):
            self["name"]    = name
            self["size"]    = size
            self["radius"]  = compute_bead_radius(size)
            self["mass"]    = compute_bead_mass(size)
            self.__particle = None
#            self.__color    = None
            
        def get_name(self):
            return self["name"]
        def get_size(self):
            return self["size"]
        def get_radius(self):
            return self["radius"]
        def get_mass(self):
            return self["mass"]
        def assign_particle(self,p):
            self.__particle = p
        def has_particle(self):
            return self.__particle != None
        def get_particle(self):
            return self.__particle
        def get_XYZR(self):
            return IMP.core.XYZR.decorate_particle(self.__particle)
        
    class Linker:
        def __init__(self,name,b1,b2,size_in_AA):
            self.__name                    = name
            self.__connected_beads         = (b1,b2)
            self.__size_in_AA              = size_in_AA
#            self.__sizeA       = self.__get_linker_max_span(size)
#            self.__sizeNbBeads = self.__get_linker_nb_beads(size)
            self.__particles               = []
            self.__restraints              = []
            
            self.__nb_beads_in_linker      = size_in_AA / 10
            
        def get_name(self):
            return self.__name
        def get_size(self):
            return self.__size_in_AA
        def get_nb_beads(self):
            return self.__nb_beads_in_linker
#        def get_max_span(self):
#            return self.__span
        def get_particles(self):
                return self.__particles
        def get_number_of_particles(self):
            return len(self.__particles)
        def get_restraints(self):
            return self.__restraints
        def get_linked_bead_indices(self):
            return self.__connected_beads
        
        def create_hierarchy(self,m):
            linkers_hierarchy_name = "hierarchy linker "  + self.get_name()
#            hl=IMP.atom.Fragment.setup_particle( IMP.Particle(m,linkers_hierarchy_name) )
            hl=IMP.atom.Hierarchy.setup_particle( IMP.Particle(m,linkers_hierarchy_name) )
            #
            # create linker beads
            #
            for lbi in range(self.__nb_beads_in_linker) :
                p = IMP.Particle(m,self.__name+" "+str(lbi))
                xyzd=IMP.core.XYZR.setup_particle(p)
                xyzd.set_radius(linker_bead_radius)
                xyzd.set_coordinates_are_optimized(True)
                IMP.atom.Mass.setup_particle(p, linker_bead_mass)
#                hlr = IMP.atom.Residue.setup_particle( p )
                hlr = IMP.atom.Hierarchy.setup_particle( p )
                hl.add_child(hlr)
                self.__particles.append(p)
#                print "LINKER BEAD",p.get_name(),xyzd.show()
            #
            # glue beads
            #
#            def __connect_linker_particles(m,pi1,pi2):
#                r = IMP.core.PairRestraint( score_HUBSDS_default,
#                    IMP.ParticlePair(self.__particles[pi1],self.__particles[pi2])
#                  )
#                r.set_name("linker restraint <"+self.get_name()+">["+str( (pi1,pi2) )+"]")
#                m.add_restraint(r)
#                m.set_maximum_score(r, default_spring_constant)
#                return r
#            for lbi in range(self.__nb_beads_in_linker-1) :
#                r = __connect_linker_particles(m,lbi,lbi+1)
#                self.__restraints.append(r)
##            print "LINKER RESTRAINT : ",self.__name,len(self.__restraints)

            pps = [ IMP.ParticlePair(self.__particles[pi],self.__particles[pi+1]) for 
                    pi in range(self.__nb_beads_in_linker-1)]
            lpps=IMP.container.ListPairContainer(pps)
            r = IMP.container.PairsRestraint(score_HUBSDS_default,lpps)
            r.set_name("linker restraint <"+self.get_name()+">")
            m.add_restraint(r)
            m.set_maximum_score(r, default_spring_constant)
            self.__restraints.append(r)
            
            return hl,self.__restraints
        
    def __init__(self,protein_name):
        """
        @param protein_name:    the name of the protein
        """
        self.__name     = protein_name
        self.__beads    = []
        self.__link     = []
        self.__linkers  = []
        self.__verbose  = False
        self.__hierarchy= None
        self.__beads_hierarchy= None
        self.__linkers_hierarchy= None
        self.__m        = None      # the attached IMP Model, will be set as soon as particles are enterred
    
    def __check_bead_index(self, index):
        if (index < 0) or (index >= self.get_number_of_beads()):
            raise KeyError("link cannot be created, bead index out of range")
        
    
    def __compute_linker_max_span(self, size_in_AA):
        return (compute_chain_max_len(size_in_AA) / 3.)

    def get_mass(self):
        return sum ([b["mass"] for b in self.__beads])
            
    def get_number_of_beads(self):
        return len(self.__beads)
    
    def get_number_of_links(self):
        return len(self.__link)
    
    def get_number_of_linker_beads(self):
        nblb = 0
        for l in self.__linkers :
            nblb+=l.get_number_of_particles()
        return nblb
    
    def get_name(self):
        return self.__name
        
    def add_bead(self, name, size):
        """ 
        @return: the index of the bead in the protein"""
        self.__beads.append( SubunitInfo.Bead(name,size) )
        return len(self.__beads) - 1
        
    def add_link(self, bead_index_1, bead_index_2, size):
        """ 
        Adds a linker between two beads as a maximal possible distance between the two beads
        @param bead_index_1: 
        @param bead_index_2: 
        @param size: """
        for index in (bead_index_1, bead_index_2) :
            self.__check_bead_index(index)
        emote("adding link from bead "+str(bead_index_1)+" to bead "+str(bead_index_2)+" in molecule "+self.__name)
        self.__link.append( (bead_index_1, bead_index_2,size) )
        
    def add_linker(self, bead_index_1, bead_index_2, size, name=None):
        """
        Adds a linker represented as a series of small (linker) beads between two protein beads 
        """
        if name == None :
            name = self.get_name()+" linker "+str(self.get_number_of_linkers())
        self.__linkers.append(SubunitInfo.Linker(name, bead_index_1, bead_index_2, size))
        
        
        
    def get_link_bead_indices(self,link_index):
        """ returns the pair of bead indices that are connected through this link
        @param link_index :
        """
        if link_index < 0 or link_index >= self.get_number_of_links() :
            raise KeyError("link index out of range "+str(link_index)+" for subunit "+self.get_name())
        return self.__link[link_index][0:2]
        
    def get_bead(self,bead_index):
        return self.__beads[bead_index]
    
    def get_beads(self):
        return self.__beads
    
    def get_linkers(self):
        return self.__linkers
    
    def get_number_of_linkers(self):
        return len(self.__linkers)
    
    def get_particles(self):
        """ returns all bead particles attached to the subunit 
        @precondition: all beads of the protein should have a particle attached"""
        return [ bead.get_particle() for bead in [ self.get_bead(i) for i in range(0,self.get_number_of_beads()) ] ]
    
    def get_linker_particles(self):
        ps = []
        for l in self.get_linkers():
            ps.extend(l.get_particles())
#        map( lambda l:ps.extend(l.get_particles()), self.get_linkers())
        return ps
    
    def get_all_particles(self):
        ps = self.get_particles()
        ps.extend(self.get_linker_particles())
        return ps
        
    def glue_together_rigidify(self, bead_index_list, name=""):
        """ rigidify together a set of beads
        @param bead_index_list:    a list of bead indices that are to be moved together in the optimization
        @param name:               the name of the associated rigid body particle
        @return: the rigid body hosting selected beads
        
        @precondition: this method should be called after the SubunitInfo is populated, 
        that is, after a call to create_hierarchy 
        """
        #
        rbp = IMP.Particle(self.__m,"Rigid Body "+name)
        xyzrl = IMP.core.XYZs([self.get_bead(b).get_XYZR() for b in bead_index_list])
        rb  = IMP.core.RigidBody.setup_particle(rbp,xyzrl)
        # apparently, the set_coordinates_are_optimized sets False for the members
#        for x in xyzrl :
#            x.set_coordinates_are_optimized(False)
        rb.set_coordinates_are_optimized(True)
#        rb.update_members()
        return rb

    def fix_distance_between_beads(self,b1,b2,name=None):
        """ """
        if name == None :
            name = self.get_name()
        
        x1=self.get_bead(b1).get_XYZR()
        x2=self.get_bead(b2).get_XYZR()
        vector = x1.get_coordinates() - x2.get_coordinates()
        inter_beads_distance = vector.get_magnitude()
        
        score = IMP.core.HarmonicDistancePairScore( inter_beads_distance , 
                                                    default_spring_constant 
                                                )
        r = IMP.core.PairRestraint( score,
                                    IMP.ParticlePair(x1,x2),
                                    "rigidity restraint "+name+" "+str(b1)+"-"+str(b2)
                                  )
        self.__m.add_restraint(r)
        self.__m.set_maximum_score(r, default_spring_constant)
        return r
        
#    def fif_angle_between_beads(self,b1,b2,b3):
        
        
    def glue_together_with_restraints(self, bead_index_list,name=None):
        """ computes a set of restraints to be used to rigidify a set of beads together 
        @param bead_index_list:    a list of bead indices that are to be moved together in the optimization
        @return: the list of restraints to add to the model
        
        @precondition: this method should be called after the SubunitInfo is populated, 
        that is, after a call to create_hierarchy; and after the geometry of beads has been set 
        """
        restraints = []
        for i in range( 1,len(bead_index_list) ) :
            for j in range( i ) :
                restraints.append( self.fix_distance_between_beads(bead_index_list[i], bead_index_list[j], name) )
        return restraints
        
    def create_hierarchy(self, m ):
        """Creates a set of particles and restraints to model the current protein in a given IMP model object 
        @param m: the IMP model in which the particles are created
        @return : a pair (h,r) comprising the hierarchy for the particle and the internal cohesion restraints"""
        emote("create molecule "+self.__name)
        
        self.__m = m
#        root = IMP.atom.Hierarchy.setup_particle( IMP.Particle(m) )
        root = IMP.atom.Molecule.setup_particle( IMP.Particle(m , self.__name) )
        beads_hierarchy = IMP.atom.Hierarchy.setup_particle( IMP.Particle(m , self.__name) )
        beadParticles=[]
        for i in range(0,self.get_number_of_beads()):
            b=self.__beads[i]
            pb = IMP.Particle(m)
            hb = IMP.atom.Hierarchy.setup_particle(pb)
#            hb = IMP.atom.Fragment.setup_particle(pb)
            name = self.get_name() +"-"+ b.get_name()+"("+str(i)+")"
            hb.set_name(name)
            xyzd=IMP.core.XYZR.setup_particle(pb);
            xyzd.set_radius(b.get_radius());
            xyzd.set_coordinates_are_optimized(True);
            IMP.atom.Mass.setup_particle(pb, b.get_mass())
            beads_hierarchy.add_child(hb)
            beadParticles.append(pb)
            b.assign_particle(pb)
            emote( name + " r:" + str(b.get_radius()) + " m:"+str(b.get_mass()) )
#        IMP.atom.Molecule.setup_particle(root)
#        root.set_name(self.__name)
        root.add_child(beads_hierarchy)
        self.__beads_hierarchy = beads_hierarchy
        
        restraints = []
        for link in self.__link :
            bead_i_1, bead_i_2, size = link
#            score = IMP.core.HarmonicUpperBoundSphereDistancePairScore( compute_link_max_len(size),default_spring_constant )
            score = score_HUBSDS_default
            r = IMP.core.PairRestraint(
                                       score,
                                        IMP.ParticlePair(beadParticles[bead_i_1],beadParticles[bead_i_2])
                                      )
            r.set_name("cohesion restraint("+self.get_name()+")["+str(bead_i_1)+","+str(bead_i_2)+"]")
            m.add_restraint(r)
            m.set_maximum_score(r, default_spring_constant)
            restraints.append(r)
        emote("inserted "+str(len(self.__link))+" bead connection restraints in the system for "+self.get_name())
        
        hl = IMP.atom.Hierarchy.setup_particle( IMP.Particle(m,"L "+self.get_name()) )
        for l in self.__linkers:
            hlr,rl = l.create_hierarchy(m)
            restraints.extend(rl)
            hl.add_child(hlr)
#            l.create_hierarchy(m)
            # then attach the linker to its two connected beads
            b1,b2 = l.get_linked_bead_indices()
            for bi,lbi in ((b1,0),(b2,l.get_number_of_particles()-1) ) :
                r = IMP.core.PairRestraint( score,
                                            IMP.ParticlePair(beadParticles[bi],l.get_particles()[lbi] )
                                          )
                m.add_restraint(r)
                m.set_maximum_score(r, default_spring_constant)
                restraints.append(r)
                r.set_name("linker attach ("+self.get_name()+")["+str( (bi,lbi) )+"]")
        self.__linkers_hierarchy = hl
        root.add_child(hl)
        self.__hierarchy=root
        return root,restraints

    def get_hierarchy(self):
        """ """
        return self.__hierarchy
    
    def get_beads_hierarchy(self):
        return self.__beads_hierarchy

    def get_linkers_hierarchy(self):
        return self.__linkers_hierarchy



class ModelInfo(dict):
    """This class contains all the information that should be needed to run a modelling experiment
    """
    
    def __init__(self,m):
        """ initialize the Model info 
        @param m: an IMP Model object"""
        self._m             = m
        self._restraints    = {}
    
    def add_subunit(self,si):
        """ adds a ProteinInfoModel object"""
        self[si.get_name()]     = si
        
    def add_restraint(self,r_name,r):
        """ adds a Restraint object"""
        self._restraints[r_name]    = r
        
    def get_model(self):
        """ """
        return self._m
    
    def get_subunit_names(self):
        """ """
        return self.keys()
    
    def get_subunit_info(self,subunit_name):
        """ """
        return self[subunit_name]
    
    def iter_subunits(self):
        """ an iterator on contained subunits"""
        return self.itervalues()
    
    def get_particles(self):
        "return all bead particles in the Model"
        ps = []
        for subunit in self.iter_subunits() :
            ps.extend(subunit.get_particles())
        return ps
    
    def get_linker_particles(self):
        """return all linker particles in the model"""
        ps = []
        for subunit in self.iter_subunits() :
            ps.extend(subunit.get_linker_particles())
        return ps
    
    def get_all_particles(self):
        """ return every (beads and linkers) particles in the model"""
        ps=self.get_particles()
        ps.extend(self.get_linker_particles())
        return ps
    
    def get_mass(self):
        """ returns the total mass for the complex """
        return sum ([s.get_mass() for s in self.itervalues() ])

class MyConfigurationSet:
    """ stores a set of coordinates associated with a set of named particles in a model
     The idea here is to be able to save and load particle positions based on a name rather than a particle 
    """
#    class _MyConfiguration():
#        """ """
#        
#        def load(self):
#        
    def __init__ (self, prot_info_mdl):
        """ @param prot_info_mdl: a dictionnary of ModelInfo object """
        #
        #    self._pim                                     a link to an object containing all informations on the current model
        #    self._subunit_number_of_beads                 number of beads for a subunit 
        #    self._subunit_index_of_first_bead             registers the index of the first bead of a given subunit in a configuration
        #    self._subunits_order                          how subunit 
        #    self._nb_beads                                total number of registered beads in the model (size of a configuration)
        #    self._config                                  list of configurations
        #    self._particles
        #    self.number_of_subunits
        
        self._pim = prot_info_mdl
        #
        self._subunit_number_of_beads       = {}
        self._subunit_index_of_first_bead   = {}
        for subunit_name, subunit_info in prot_info_mdl.iteritems() :
#            self._subunit_number_of_beads[subunit_name] = subunit_info.get_number_of_beads()
            self._subunit_number_of_beads[subunit_name] =\
                  subunit_info.get_number_of_beads() \
                + subunit_info.get_number_of_linker_beads()
        #
        self._subunits_order = sorted( self._subunit_number_of_beads.keys() )
        self.number_of_subunits = len(self._subunits_order)
        self._particles = []
        for subunit_name in self._subunits_order :
#            for p in self._pim[subunit_name].get_particles() :
            for p in self._pim[subunit_name].get_all_particles() :
                self._particles.append(p)
        #
        self._nb_beads = 0
        for subunit_name in self._subunits_order :
            self._subunit_index_of_first_bead[ subunit_name ] = self._nb_beads
            self._nb_beads += self._subunit_number_of_beads[ subunit_name ]
        # 
        self._config=[] 
    #
    def get_number_of_configurations(self):
        return len(self._config)
    #
    def get_subunit_names(self):
        return self._subunits_order
    #
    def get_number_of_beads(self,subunit_name):
        return self._subunit_number_of_beads[subunit_name]
    #
    def get_prot_info_model(self):
        return self._pim
    #
    def get_particles(self):
        return self._particles
    #
    def get_subunit_particles(self,subunit_name):
        return self._pim[subunit_name].get_particles() 
    #
    def load_configuration(self,config_number):
        """loads coordinates of a given configuration into the current model's beads
        @param config_number: the index of the configuration from which we get the coordinates"""
        config = self._config[config_number]
        for i in range(0,self._nb_beads) :
            p = self._particles[i]
            coods = config[i]
            IMP.core.XYZ_decorate_particle(p).set_coordinates(coods)
    #   
    def delete_config(self,config_number):
        del self._config[config_number]
    #
    def delete_configs(self,config_numbers):
        for config_number in config_numbers :
            del self._config[config_number]
    #
    def delete_all_configs(self):
        self._config = []
    #   
    def save_current_config(self):
        config = []
        for i in range(0,self._nb_beads) :
            p = self._particles[i]
            config.append( IMP.core.XYZ_decorate_particle(p).get_coordinates() )
        self._config.append(config)
    #
    def read_configurationSet(self,impConfigs):
        for i in range(0, impConfigs.get_number_of_configurations()):
#            print "load and save config",i
            impConfigs.load_configuration(i)
            self.save_current_config()
    #
    #
    def _write_header(self, f):
        header_lines = []
        header_lines.append( "# --- Configurations save" )
        header_lines.append( "# number of subunits : " + str( self.number_of_subunits ) )
        for s_name in self._subunits_order :
            header_lines.append( "# subunit : " + s_name + " : " + str(self._subunit_number_of_beads[s_name]))
        f.write("\n".join(header_lines))
        f.write("\n\n")
    #    
    def _read_header(self, f):
        # stop on the first empty line
        # for the moment we don't do anything withe the header... though it would be a good idea to verify data content adequation
        for line in f:
            if line == "\n":
                break            
    #
    def save_all_configs_to_file(self, fileName):
        f = open(fileName,"w")
        self._write_header(f)
        num_lines_written=0
        for config in self._config :
            line_tokens = []
            for cood in config :
                x,y,z = cood
                x,y,z = str(x),str(y),str(z)
                line_tokens.append(",".join([x,y,z]))
            f.write(" ".join(line_tokens)+"\n")
            num_lines_written+=1
        f.close()
        return num_lines_written
    #   
    def read_all_configs_from_file(self, fileName):
        num_lines_read=0
        try :
            f = open(fileName)
            self._read_header(f)
            for line in f :
                config = []
                for cood in line.strip().split(" ") :
                    x,y,z = cood.split(",")
                    coods = [float(x),float(y),float(z)]
                    config.append(coods)
                self._config.append(config)
                num_lines_read+=1
            f.close()
        except :
            print "error while reading file>",fileName
            raise
#            num_lines_read = -1
        return num_lines_read

    def read_configs_from_file(self, fileName, config_index_list):
        f = open(fileName)
        self._read_header(f)
        num_lines_read=0
        for line in f :
            config = []
            try :
                config_index_list.index(num_lines_read)
                for cood in line.strip().split(" ") :
                    x,y,z = cood.split(",")
                    coods = [float(x),float(y),float(z)]
                    config.append(coods) 
                self._config.append(config)
            except :
                pass
            num_lines_read+=1
        f.close()
        return num_lines_read
    
    def get_model(self):
        """ returns the model attached to the ProteinModelInfo"""
        return self._pim.get_model()
    
    
def create_linear_connectivity(prot):
    """ add links of size 0 between each succesive beads in the list 
    @param prot: a ProteinModelInfo object whose beads will be "connected"
    """
    for index in range(0,prot.get_number_of_beads()-1) :
        prot.add_link(index,index+1,0)

def connect_beads(m,b1,b2):
#    score = score_HUBSD_default
    r = IMP.core.PairRestraint( score_HUBSDS_default,
                                IMP.ParticlePair(b1.get_particle(),b2.get_particle())
                              )
    m.add_restraint(r)
    m.set_maximum_score(r, default_spring_constant)
    return r


def ambiguous_connect_proteins(m,p1,p2):
    """ 'ambiguous' connection of two proteins (one does not know which beads are connected)
    @param m: the model in which the connection is to be made
    @param p1: a ProteinModelInfo objects
    @param p2: a ProteinModelInfo objects"""
    
    particles1 = p1.get_particles()
    particles2 = p2.get_particles()
    emote( "connecting proteins"+p1.get_name()+"("+str(len(particles1))+")"+"and"+p2.get_name()+"("+str(len(particles2))+")" )
    
    # choose a representative for each protein   
    #
    rep1 = particles1[0]
    rep2 = particles2[0]
    # then associate that representative with all particles in the protein
    tr = IMP.core.TableRefiner()
    tr.add_particle(rep1,particles1)
    tr.add_particle(rep2,particles2)
    
    s = IMP.core.KClosePairsPairScore( score_HUBSDS_default , tr , 1 )
    r = IMP.core.ConnectivityRestraint(s, IMP.container.ListSingletonContainer([rep1,rep2]) )
    m.add_restraint(r)
    m.set_maximum_score(r, default_spring_constant)
#    m.set_maximum_score(r, 100)
    return(r)

def ambiguous_connect_bead_lists(m,beads1,beads2) :
    """
    """
    rep1 = beads1[0]
    rep2 = beads2[0]
    
    tr = IMP.core.TableRefiner()
    tr.add_particle(rep1,beads1)
    tr.add_particle(rep2,beads2)
    
    s = IMP.core.KClosePairsPairScore( score_HUBSDS_default , tr , 1 )
    r = IMP.core.ConnectivityRestraint(s, IMP.container.ListSingletonContainer([rep1,rep2]) )
    m.add_restraint(r)
    m.set_maximum_score(r, default_spring_constant)
#    m.set_maximum_score(r, 100)
    return(r)
    
def get_harmonic_excluded_volume_restraint(mi,ev_spring_constant=default_ev_spring_constant):
    """
    adds an excluded volume restraint to the model
    @param m: the imp Model in which we are working
    @param mi : a ModelInf object
    """
    particles = []
    for subunit_info in mi.itervalues():
        particles.extend( subunit_info.get_particles() )
    evr = IMP.core.ExcludedVolumeRestraint( 
                IMP.container.ListSingletonContainer(particles) , default_ev_spring_constant 
                )
    evr.set_name("Excluded volume restraint")
    return evr
    
def get_LJ_restraint_all_particles(mi):
    """
    Lennard-johnes all protein domains in a model
    """
    sf          = IMP.atom.ForceSwitch(60.0, 70.0)
    LJS         = IMP.atom.LennardJonesPairScore(sf)
    well_depth  = 1
    default_LJ_constant = 1.0
    # In a first approximation we will stick everybody, 
    particles=[]
    for subunit_info in mi.itervalues():
        for p in subunit_info.get_particles() :
            IMP.atom.LennardJones.setup_particle(p,well_depth)
            particles.append(p)
#        particles.extend( p )
    for i in range(1,len(particles)):
        for j in range(i) :
            r = IMP.core.PairRestraint( LJS,
                                        IMP.ParticlePair(particles[j],particles[i])
                                      )
            mi.get_model().add_restraint(r)
            mi.get_model().set_maximum_score(r, default_LJ_constant)
    
    
def get_LJ_restraint(mi):
    """
    Lennard-johnes all protein domains in a model
    """
    sf          = IMP.atom.ForceSwitch(60.0, 70.0)
    LJS         = IMP.atom.LennardJonesPairScore(sf)
    well_depth  = 1.0
    default_LJ_constant = 1.0
    # In a first approximation we will stick everybody, 
    particles=[]
    for subunit_info in mi.itervalues():
        for p in subunit_info.get_particles() :
            IMP.atom.LennardJones.setup_particle(p,well_depth)
            particles.append(p)
    lspc = IMP.container.ListSingletonContainer(particles)
    cpc  = IMP.container.ClosePairContainer(lspc,30.0)
    r=IMP.container.PairsRestraint(LJS,cpc)
    mi.get_model().add_restraint(r)
    mi.get_model().set_maximum_score(r, default_LJ_constant)
    


def get_EM_covering_spheres_restraint(unionSpheres,particles,steepness=EM_coveringSpheres_ubh_steepness):
    """ 
    @param unionSpheres:    a UnionSpheres object
    @param particles:      a list of IMP particles which we want to restrain to the union of spheres
    @param steepness:        steepness of the harmonic score to stick to balls; defaults to EM_coveringSpheres_ubh_steepness
    """
#    restraints = []
#    idx=0
    
#    nbSpheres = unionSpheres.get_size()
    
    rss = IMP.RestraintSet()
    
    for p in particles :
        px = IMP.core.XYZR_decorate_particle(p)
        restraintName = "stickin"+p.get_name()
        scores = []
        for s in unionSpheres :
            offset = s.get_radius() - 2*px.get_radius()
            unaryf = IMP.core.HarmonicUpperBound( offset , steepness )
    #        score  = IMP.core.DistanceToSingletonScore( unaryf , IMP.algebra.Vector3D(*s[0]) )
            score  = IMP.core.SphereDistanceToSingletonScore( unaryf , IMP.algebra.Vector3D(*s.get_center()) )
            scores.append(score)
#        print "restraint ",restraintName,"built on",len(scores),"scores"
#        minScore = IMP.container.MinimumSingletonScore( scores, 1 , "min"+str(idx))
        minScore = IMP.container.MinimumSingletonScore( scores, 1 )
        r= IMP.container.SingletonsRestraint( minScore, IMP.container.ListSingletonContainer( [px] ), restraintName )
        max_out_of_enveloppe_score = EM_coveringSpheres_ubh_steepness_max_score
        r.set_maximum_score( max_out_of_enveloppe_score )
#        idx+=1
        rss.add_restraint(r)
        
    return rss

        
    
#def save_as_pdbCA(pdbFileName, protein_info_dict, differentiate_subunits=False):
#        """
#        saves proteins from protein_info_dict as a Calpha pdb file in file pdbFileName
#        meant to be read by TMscore 
#        @param pdbFileName              : 
#        @param protein_info_dict        : 
#        @param differentiate_subunits   : if True a chain is output per subunit, otherwise, only one chain for the whole complex
#        @precondition:  particles attached to beads should be already set
#        """
##        p = ProteinModelInfo()
##        X = IMP.core.XYZR()
#        
#        chainIDs = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
#        
#        f = open(pdbFileName,"w")
#        subunit_index=0;
#        header_lines        = []
#        atom_lines          = {}
#        connect_lines       = {}
#        
#        header_line = "{0:<6s} {1:<3d} {2:s}\n".format("REMARK",950,"Fake CA PDB file\n")
#        header_lines.append(header_line)
#        atom_index = 0
#        chainID             = "A"
#        for (prot_name,prot_info) in protein_info_dict.iteritems() :
#            if differentiate_subunits == True :
#                chainID = chainIDs[subunit_index]
#            subunit_index+=1;
#            header_line     = "REMARK 951 subunit {0:s} ({1:d} beads) chain {4:1s} ATOMs {2:d} to {3:d}\n".format(
#                          prot_name,
#                          prot_info.get_number_of_beads(),
#                          atom_index+1,
#                          atom_index+prot_info.get_number_of_beads(),
#                          chainID
#                          )
#            header_lines.append(header_line)
#            
#            connect_lines[subunit_index]=[]
#            for link_index in range(prot_info.get_number_of_links()) :
#                (b1,b2) = prot_info.get_link_bead_indices( link_index )
#                connect_line    = "CONECT{0:>5d}{1:>5d}\n".format(atom_index+1+b1,atom_index+1+b2)
#                connect_lines[subunit_index].append( connect_line )
##            
##    TODO : residue number should be updated if diff sub == True
##
##
#            atom_lines[subunit_index]=[]
#            for bead_index in range (prot_info.get_number_of_beads()) :
#                atom_index+=1
#                xyzr        = prot_info.get_bead(bead_index).get_XYZR()
#                x,y,z,r     = xyzr.get_x(),xyzr.get_y(),xyzr.get_z(),xyzr.get_radius()
##                "ATOM     34  CA AARG A  -3      12.353  85.696  94.456  0.50 36.67           C  "
#                atom_line   = "ATOM  {0:>5d}  CA  ARG {5:1s}{0:>4d}    {1:>8.3f}{2:>8.3f}{3:>8.3f} 00.00 {4:>5.2f}           C  \n".format(
#                       atom_index,x,y,z,r,chainID)
#                atom_lines[subunit_index].append(atom_line)
#                
#        for header_line in header_lines :
#            f.write(header_line)
#        
#        if differentiate_subunits == True :
#            # a chain per subunit
#            for subunit_idx in range(1,subunit_index):
#                for atom_line in atom_lines[subunit_idx] :
#                    f.write(atom_line)
#                f.write("TER\n")
#                for connect_line in connect_lines[subunit_idx] :
#                    f.write(connect_line)
#        else :
#            # just one chain
#            for subunit_idx in range(1,subunit_index):
#                for atom_line in atom_lines[subunit_idx] :
#                    f.write(atom_line)
#            f.write("TER\n")
#            for subunit_idx in range(1,subunit_index):
#                for connect_line in connect_lines[subunit_idx] :
#                    f.write(connect_line)
#
#
#        f.close()
        
        
