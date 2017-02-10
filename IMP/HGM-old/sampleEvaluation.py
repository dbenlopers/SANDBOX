'''

'''
import math
import re

import helpers
import representation


def _gather_coordinates_for_current_config(xyzl):
    """ outputs the concatenated list of partile coordinates for a given model"""
    vect = []
    for X in xyzl :
        vect.extend([X.get_x(),X.get_y(),X.get_z()])
    return vect

def _compute_vectors_rmsd(coods_current,coods_solution):
    """compute euclidian distance between two 'vectors' of similar size
    @param coods1:
    @param coods2:
    """
    rmsd2 = 0
    for i in range(len(coods_current)) :
        c=coods_current[i]-coods_solution[i]
        rmsd2 += c*c
    return math.sqrt(rmsd2)

class RMSDsToSolutionForSampleCollection :
    """ Stores energies and statistics for a collection of samples """
    def __init__(self,subunitsInfo):
        """
        """
        self._xyzl = map (helpers.XYZdecorate, self._subunitsInfo.get_particles())
        self._rmsds     = {}
        self._solution   = []
        self._subInfos   = subunitsInfo

    def set_solution(self,solution=None):
        """@param solution: the 'vector' to which everything else will be compared to
        it can be any type of python iterables."""
        if solution == None :
            # the solution is the actual 
            self._solution  = _gather_coordinates_for_current_config(self._xyzl)
        else :
            self._solution   = list(solution) # let's store a copy of the solution

        
    def add_sample(self,sample_index,configSet):
        """
        @param configSet: 
        """    
        # should check that subunitInfo is similar
        for i in range(configSet.get_number_of_configurations()) :
            configSet.load_configuration(i)
            coods_current = _gather_coordinates_for_current_config(self._xyzl)
            rmsd    = __compute_vectors_rmsd(coods_current,self._solution)
            self._rmsd[sample_index]=rmsd
    
#        
    def read_from_file(self,filePath):
        """ """
        f = open(filePath)
        f.readline()  # trash header in a pure pig style
        line=f.readline()
#        print ">",line
        self._solution = map(float,list(re.split("\s+",line.strip()))[1:])
        f.readline()  # trash header in a pure pig style
        for line in f :
            tokens = re.split("\s+",line.strip())
            self._rmsds[int(tokens[0])]      = (map(float,tokens[1:]))
        f.close()
        
    def write_to_file(self,filePath):
        """ """
        f = open(filePath,'w')
        f.write("# RMSD to solution\n")
        f.write("solution: \n"+str(self._solution))
        f.write("# rmsds   k rmsd1 .. rmsdN\n")
        for k,l in self._rmsds.iteritems() :
            f.write( str(k) + " "
                             + " ".join(map(str,l))
                             + "\n")  
        f.close()

        
#    def remove_sample(self,sample_id):
#        """ remove information associated with a given sample index """
#        del self._energies[sample_id]
#        del self._statistics[sample_id]
#        self._global_statistics = None
        
#    def clear(self):
#        """ flush the container """
#        self._energies={}
#        self._statistics={}
#        self._global_statistics = None
        
    def get_sample_indices(self):
        """ return keys to get the samples """
        return self._rmsds.keys()
    
    def get_sample_rmsds_to_solution(self,sample_index):
        return self._rmsds[sample_index]
        
    def get_number_of_samples(self):
        return len(self._rmsds)
    
    def get_number_of_entries(self):
        size = 0
        for l in self._rmsds.itervalues() :
            size += len( l )
        return size
    



class RMSDsToSolutionForSubsamples :
    """ A container to host all RMSD from a set of samples to a given solution 
    configurations will be identified by a string key sample_index:subsample_index"""
    
    def __init__(self,subunitsInfo):
        """
        """
        self._xyzl = map (helpers.XYZdecorate, subunitsInfo.get_particles())
        self._rmsds     = {}
        self._solution   = []
        self._subInfos   = subunitsInfo

    def set_solution(self,solution=None):
        """@param solution: the 'vector' to which everything else will be compared to
        it can be any type of python iterables."""
        if solution == None :
            # the solution is the actual 
            self._solution  = _gather_coordinates_for_current_config(self._xyzl)
        else :
            self._solution   = list(solution) # let's store a copy of the solution


    def add_sample(self,sample_index,configSet):
        """
        @param configSet: 
        """    
        # should check that subunitInfo is similar
        for i in range(configSet.get_number_of_configurations()) :
            configSet.load_configuration(i)
            coods_current = _gather_coordinates_for_current_config(self._xyzl)
            rmsd    = _compute_vectors_rmsd(coods_current,self._solution)
            index = (str(sample_index)+":"+str(i))
            self._rmsds[index]=rmsd

    
#    def read_sample_file(self,sampleFilePath):


    def write_to_file(self,filePath):
        """ save Subsamples energies to file"""
        f = open(filePath,'w')
        f.write("# SubsampleRMSDs to solution --- \n")
        f.write("solution: \n"+str(self._solution))
        for k,rmsd in self._rmsds.iteritems() :
            f.write( "{0:s} {1:.2f}\n".format(k,rmsd))  
        f.close()
        
    def read_from_file(self,filePath):
        """read Subsamples energies from file"""
        f = open(filePath)
        f.readline()  # trash header in a pure pig style
        line=f.readline()
#        print ">",line
        self._solution = map(float,list(re.split("\s+",line.strip()))[1:])
        f.readline()  # trash header in a pure pig style
        for line in f :
#            print ">>",line
            token = re.split("\s+",line.strip())
            self._rmsds[token[0]]=float(token[1])
        f.close()
        
    def get_sorted_subsamples_rmsds_to_solution(self):
        """ returns the list of sample indices with rmsd, sorted in increasing energy 
        @return: a list of pairs (config_identifier, energy)
        @note: config_identifier are formated as sample_index:subsample_index"""
        return sorted (self._rmsds.items(),key=lambda x:x[1])

