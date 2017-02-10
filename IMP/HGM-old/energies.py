'''

'''
import re
import helpers
import representation



#        fenergies.write(":".join(map(str,energies))+"\n")
#        fstatistics.write("{0:f} {1:f}\n".format(E,s))
class EnergiesForSample :
    """ Stores energies for a given sample """
    
    def __init__(self,cs):
        """ @param cs: sample as a ConfigurationSet """
        self._energies  = helpers.compute_sample_energies(cs)
    
    def get_sample_size(self):
        return len(self._energies)
    
    def get_energies(self):
        return self._energies()
    




class StatisticsForSampleCollection :
    """ Stores statistics for a collection of samples """
    
    def __init__(self):
        self._statistics = {}   # dict { id tag (int) -> stats (float,float) (E,sigma) }

    def read_from_file(self,filePath):
        """ """
        fstatistics = open(filePath)
        fstatistics.readline()  # trash header in a pure pig style
        for line in fstatistics :
#            print ">",line,"<"
            tokens = re.split("\s+",line.strip())
            self._statistics[int(tokens[0])]=(float(tokens[1]),float(tokens[2]))    
        fstatistics.close()
        
    def write_to_file(self,filePath, sorted=False):
        """ write statistics to file
        @param filePath: write statistics 
        @param sorted:"""
        fstatistics = open(filePath,"w")
        #
        fstatistics.write("# sample_id E(mean) s(std_dev)\n")
        #
        linesToWrite=[]
        for k,l in self._statistics.iteritems() :
            token = [k]
            token.extend(l)
            linesToWrite.append( token )
        if sorted :
            linesToWrite.sort(key=lambda x:x[1])
#            linesToWrite.sort(key=lambda x:x[1],reverse=True)
        #
        for line in linesToWrite :
            fstatistics.write("{0:>8d} {1:>15.5f} {2:>15.5f}\n".format(*line))
        fstatistics.close()
        
    def remove(self,sample_id):
        del self._statistics[sample_id]
        
    def remove_all(self):
        self._statistics = {}

        
    def add_statistics(self,sample_index,stats):
        """ add manually statistics in the container """
        self._statistics[sample_index]=stats
    
    def add_statistics_from_ConfigurationSet(self,sample_index,cs):
        """ compute statistics from a ConfigurationSet object and push these in the container
        @param sample_index: an integer to identify the sample
        @param cs: the sample as a ConfigurationSet
        @return: statistics for the sample """
        energies = helpers.compute_sample_energies(cs)
        stats = helpers.compute_list_statistics(energies)
        self._statistics[sample_index] = stats
        return stats
    
    def add_stats_from_EnergiesForSampleCollection(self,efsc):
        """ extracts and stores statistics from an EnergiesForSampleCollection object
        @param efsc:  an EnergiesForSampleCollection
        """
        for k in efsc.get_sample_indices():
            self._statistics[k]=efsc.get_statistics_for_sample(k)
    
    def get_sample_indices(self):
        return self._statistics.keys()
        
    def get_stats(self,sample_index):
        return self._statistics[sample_index]
    
    
    
    
    

class EnergiesForSampleCollection :
    """ Stores energies and statistics for a collection of samples """
    def __init__(self):
        self._energies      = {}
        self._statistics    = {}
        self._global_statistics   = None
        
    def set_energies_for_sample(self,sample_id,cs):
        """ """
        self._energies[sample_id]       = helpers.compute_sample_energies(cs)
        self._statistics[sample_id]     = helpers.compute_list_statistics(self._energies[sample_id])
        self._global_statistics   = None # we must invalidate global statistics
        
    def read_from_file(self,filePath):
        """ """
        fenergies = open(filePath)
        fenergies.readline()  # trash header in a pure pig style
        line=fenergies.readline()
#        print ">",line
        self._global_statistics = re.split("\s+",line.strip())
        fenergies.readline()  # trash header in a pure pig style
        for line in fenergies :
#            print ">>",line
            tokens = re.split("\s+",line.strip())
#            print ">>(",tokens[0],",",tokens[-2],")"
            self._statistics[int(tokens[0])]    = (map(float,tokens[1:3]))
            self._energies[int(tokens[0])]      = (map(float,tokens[3:]))
        fenergies.close()
        
    def write_to_file(self,filePath):
        """ """
        fenergies = open(filePath,'w')
#        fenergies.write("# Global stats : (E,s)=({0:f},{1:f})\n".format(self.global_stats))
        fenergies.write("# Global stats : E s\n")
        if self._global_statistics ==  None :
            self._update_global_statistics()
        fenergies.write("{0:f} {1:f}\n".format(*self._global_statistics))
        fenergies.write("# sample_id   E s e1 .. eN\n")
        for k,l in self._energies.iteritems() :
            fenergies.write( str(k) + " "
                             + " ".join(map(str,self._statistics[k])) + " "
                             + " ".join(map(str,l))
                             + "\n")  
        fenergies.close()
        
    def remove_sample(self,sample_id):
        """ remove information associated with a given sample index """
        del self._energies[sample_id]
        del self._statistics[sample_id]
        self._global_statistics = None
        
    def clear(self):
        """ flush the container """
        self._energies={}
        self._statistics={}
        self._global_statistics = None
        
    def get_sample_indices(self):
        """ return keys to get the samples """
        return self._energies.keys()
    
    def get_sample_indices_with_average_above_threshold(self,t):
        """ returns keys to get samples with an energy average above a given threshold"""
        return [k for (k,v) in self._statistics.items() if v[0] > t]

    def get_sample_indices_with_average_below_threshold(self,t):
        """ returns keys to get samples with an energy average below a given threshold"""
        return [k for (k,v) in self._statistics.items() if v[0] < t]

    def get_sample_energy(self,sample_index):
        return self._energies[sample_index]
    
    def get_statistics_for_sample(self,sample_index):
        """ """
        return self._statistics[sample_index]
    
    def _update_global_statistics(self):
            all_energies = []
            for l in self._energies.values() :
                all_energies.extend(l)
            self._global_statistics = helpers.compute_list_statistics(all_energies)
    
    def get_global_statistics(self):
        if self._global_statistics == None :
            self._update_global_statistics()
        return self._global_statistics
    
    def get_statistics(self):
        """ return a StatisticsForSampleCollection """
        s=StatisticsForSampleCollection()
        s.add_stats_from_EnergiesForSampleCollection(self)
        return s
    
    def get_number_of_samples(self):
        return len(self._energies)
    
    def get_number_of_energies(self):
        size = 0
        for k in self._energies.keys() :
            size += len( self._energies[k] )
        return size
    



class SubsamplesEnergies :
    """ A container to host all configuration energies from a set of samples 
    configurations will be identified by a string key sample_index:subsample_index"""
    
    def __init__(self):
#        self._energies = []
        self._energies = {}
    
#    def read_sample_file(self,sampleFilePath):


    def write_to_file(self,filePath):
        """ save Subsamples energies to file"""
        fenergies = open(filePath,'w')
        fenergies.write("# SubsampleEnergies --- \n")
        fenergies.write("# sample_id:subsample_id e\n")
        for k,e in self._energies.iteritems() :
            fenergies.write( "{0:s} {1:.2f}\n".format(k,e))  
        fenergies.close()
        
    def read_from_file(self,filePath):
        """read Subsamples energies from file"""
        fenergies = open(filePath)
        fenergies.readline()  # trash 1st header in a pure pig style
        fenergies.readline()  # trash 2nd header in a pure pig style
        line=fenergies.readline()
#        print ">",line
        
        for line in fenergies :
#            print ">>",line
            token = re.split("\s+",line.strip())
#            print ">>(",tokens[0],",",tokens[-2],")"
            self._energies[token[0]]=float(token[1])
        fenergies.close()
        
        
    def read_energies(self,e):
        """ reads samples energies from an EnergiesForSampleCollection collection 
         @param e : an EnergiesForSampleCollection object """
        for i in e.get_sample_indices() :
            l = e.get_sample_energy(i)
            j=0
            for se in l :
                index = (str(i)+":"+str(j))
#                self._energies.append( (index,se) )
                self._energies[index]=se
                j+=1
         

    def read_samples_energies_from_file( self , energiesFilePath ):
        """ read and import samples energies from a file"""
        e = EnergiesForSampleCollection()
        e.read_from_file(energiesFilePath)
        self.read_energies(e)

    def get_sorted_subsamples_energies(self):
        """ returns the list of sample indices with energies, sorted in increasing energy 
        @return: a list of pairs (config_identifier, energy)
        @note: config_identifier are formated as sample_index:subsample_index"""
        return sorted (self._energies.items(),key=lambda x:x[1])

