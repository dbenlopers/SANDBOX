'''

'''

import IMP
import IMP.core
import helpers
    
class ParticlesPairDistanceMatrix:
    """ """
    def __init__(self,particles_list):
        """ @param particles_list: a list of IMP.core.XYZR particles"""
        nb_particles = len (particles_list) 
        if (nb_particles < 2) :
            raise ValueError("won't store pair distances for less than two beads")
#
#        self._max_index             = nb_particles - 2 # we start at index 0, and we won't store distance i to i
#        self._nb_row                = nb_particles - 1
#        self._number_of_values      = (nb_particles - 1)*(nb_particles - 2) / 2
#        self._values                = [0.0] * self._number_of_values
        self._values=[]
        
        dist = lambda x1,x2 : (x1.get_coordinates()-x2.get_coordinates()).get_magnitude() - x1.get_radius() - x2.get_radius()
#        def dist(x1,x2):
#            return (x1.get_coordinates()-x2.get_coordinates()).get_magnitude() - x1.get_radius() - x2.get_radius()
        
#        for i in range(1,self._max_index + 1):
        for i in range(1,nb_particles):
            l = []
            for j in range(0,i) :
#                self._set_value(i,j,dist(particles_list[i],particles_list[j]))
                l.append( dist(particles_list[i],particles_list[j]) )
            self._values.append(l)
            
    def __repr__(self):
        return str(self._values)
#       
#    def _get_index(self,i,j):
##        if (i<0 or i>self._max_bead_index_beads or j<0 or j>self._max_bead_index_beads) :
##            raise ValueError("wrong acces indices")
#        i,j = sorted([i,j])
#        index = i*(self._nb_beads - 1) + j
#        return index
#       
    def get_value(self,i,j):
        """ """
        j,i = sorted([i,j])
#        return self._values[ self._get_index(self,i,j) ]
        try :
            return self._values[i-1][j]
        except :
            print "get_value crashes with ",i,j
            print self
            raise
#                
#    def _set_value(self,i,j,v):
#        """ """
#        self._values[ self._get_index(self,i,j) ] = v
        
    
        
class ParticlesPairDistanceMatrixSet:
    """ """      
    def __init__(self,cs):
        """ @param cs: an object of class MyConfigurationSet"""
        self._cs                = cs
        self._XYZRparticles     = [ IMP.core.XYZR_decorate_particle(p) for p in cs.get_particles() ]
        self._matrices          = []
        for config_num in range(0,cs.get_number_of_configurations()) :
            cs.load_configuration(config_num)
            m=ParticlesPairDistanceMatrix(self._XYZRparticles)
            self._matrices.append(m)
        self._nb_config=len(self._matrices)
    def get_number_of_configurations(self):
        return self._nb_config
    def get_configuration_set(self):
        return self._cs
    def get_matrix(self,config_index):
        return self._matrices[config_index]
    def iter_matrices(self):
        return (mat for mat in self._matrices)
    def get_distance(self,config_index,i,j):
        return self._matrices[config_index].get_value(i,j)
    def get_distances(self,i,j):
        return [ self._matrices[config_index].get_value(i,j)\
                for config_index in range(0,self.get_number_of_configurations()) ]
    def get_particle_index(self,p):
        return self._cs.get_particles().index(p)
    def save_pickled(self,filePath):
        helpers.savePickleDistMatrix(filePath, self._matrices)
    def load_pickled(self,filePath):
        self._matrices=helpers.loadPickleDistMatrix(filePath)
        self._nb_config = len(self._matrices)
    def get_particles(self):
        return self._cs.get_particles()
        
    
class SubunitsPairDistanceMatrix:
    """ """
    def __init__(self,keyPairsToIndices,dist_matrix):
        """ @param keyPairsToIndices : a 2 level dict {subunit_name1 -> {subunit_name2 -> [ list of pairs of particle indices ]
            @param dist_matrix : a particlesPairDistanceMatrix object
        """
        self._values={}
        #
        def dist(a,b):
            
#            try :
                return min( [ dist_matrix.get_value(*pair) for pair in keyPairsToIndices[a][b] ] )
#            except :
#                print "get value crashes"
#                print keyPairsToIndices[a][b]
#                print a,b,pair
#                raise
#                return 0.0
        #
        names   = keyPairsToIndices.keys()
        self._nb_names = len(names)
        for i1 in range(0,self._nb_names):
            name1=names[i1]
            self._values[name1]={}
            for i2 in range(0,i1):
                name2=names[i2]
                self._values[name1][name2]=dist(name1,name2)
        #
    def get_value(self,name1,name2):
        try:
            return self._values[name1][name2]
        except :
            return self._values[name2][name1]
    


class SubunitsPairDistanceMatrixSet:
    """ """
    def __init__(self,prot_info_mdl,ppdms):
        """
        @param prot_info_mdl: 
        @param ppdms : an object of type ParticlePairDistanceMatrixSet"""
#        self._pim                       = prot_info_mdl
        _pim                       = prot_info_mdl
        #
        self._subunit_index             = {}
        self._subunit_names             = []
        i=0
#        for k in self._pim.keys() :
        for k in _pim.keys() :
            self._subunit_names.append(k)
            self._subunit_index[k]=i
            i+=1
        self._nb_subunits               = i
        #
        subunit_particle_indices = {}
        for name in self.get_subunit_names():
#            subunit_particle_indices[name] = [ ppdms.get_particle_index(p) for p in self._pim[name].get_particles() ]
            subunit_particle_indices[name] = [ ppdms.get_particle_index(p) for p in _pim[name].get_particles() ]
        spppids = {} # subunit pair to particle pair ids
        for name1 in self.get_subunit_names():
            spppids[name1]={}
            for name2 in self.get_subunit_names():
                if name1 == name2 :
                    continue
                else :
                    spppids[name1][name2]=[]
                    try :
                        spppids[name1][name2]=spppids[name2][name1]
                    except :
#                        spppids[name1][name2]=[ (p1,p2) for p1 in subunit_particle_indices[name1] 
#                                                  for p2 in subunit_particle_indices[name2] ]
                        for p1 in subunit_particle_indices[name1] :
                            for p2 in subunit_particle_indices[name2] :
                                spppids[name1][name2].append( (p1,p2) )
        #
        self._matrices                  = []
        for mat in ppdms.iter_matrices() :
            self._matrices.append(SubunitsPairDistanceMatrix(spppids,mat))
        self._nb_configs    = len(self._matrices)       
 
    def get_subunit_names(self):
#        return self._pim.keys()
        return self._subunit_names
    def get_number_of_configurations(self):
        return self._nb_configs
    def get_matrix(self,config_index):
        return self._matrices[config_index]
    def get_distance(self,config_index,sn1,sn2):
        """@param config_index:
           @param s1:            subunit name 1
           @param s2:            subunit name 2"""
        return self._matrices[config_index].get_value(sn1,sn2)
    
    def get_distances(self,sn1,sn2):
        return [ self._matrices[config_index].get_value(sn1,sn2) for config_index in range(0,self._nb_configs) ]




class EdgeOccurenceAccumulator:
    """ 
    Keeps count of the occurrences of each edges as seen in a sample
    The notion of edge is based on a distance critera, selected by the user
    """
    def __init__(self,sdms,threshold=3.0,nodes_sublist=[]):
        """
        @param sdms:            an object of type SubunitsPairDistanceMatrixSet
        @param nodes_sublist:   a list of nodes (subunit names) on which we want to restrict the study
        @param threshold:       maximal distance to consider an edge (i.e. subunits are connected if dist under threshold)
        """
        self._nb_per_edge_accum         = {}
        self._nb_configs                = sdms.get_number_of_configurations()
        self._nodes = (sdms.get_subunit_names()) if (nodes_sublist == []) else (nodes_sublist)
        self._threshold                 = threshold
        # init accumulator
        for i in range(1,len(self._nodes)):
            node_i = self._nodes[i]
            self._nb_per_edge_accum[node_i] = {}
            for j in range(0,i) :
                node_j = self._nodes[j]
                self._nb_per_edge_accum[node_i][node_j] = 0
                
        for config_index in range(0,sdms.get_number_of_configurations()):
            sdm                          = sdms.get_matrix(config_index)
            for i in range(1,len(self._nodes)):
                node_i = self._nodes[i]
                for j in range(0,i) :
                    node_j = self._nodes[j]
                    if sdm.get_value(node_i,node_j) <= self._threshold :                    
                        self._nb_per_edge_accum[node_i][node_j] += 1
            
            
    def get_number_of_configurations(self):
        return self._nb_configs    
    
    def get_edge_count(self,node_1,node_2):
        try :
            return self._nb_per_edge_accum[node_1][node_2]
        except :
            return self._nb_per_edge_accum[node_2][node_1]
        
    def get_threshold(self):
        return self._threshold
    
    def get_nodes(self):
        return self._nodes
    
    def get_sorted_edges(self):
        sorted_edges = []
        for i in range(1,len(self._nodes)):
            node_i = self._nodes[i]
            for j in range(0,i) :
                node_j = self._nodes[j]
                sorted_edges.append((node_i,node_j,self._nb_per_edge_accum[node_i][node_j]))
        sorted_edges.sort(key=lambda x:x[2])
        return sorted_edges

