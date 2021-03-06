'''
Created on 7 juin 2012

A class to store and access execution time for sampling processes

'''
import re

class Times:
    def __init__(self):
        self._times={}
        
    def reset(self):
        self._times={}
        
    def set_sample_time(self,sample_id,time):
        self._times[sample_id]=time
        
    def get_sample_time(self,sample_id):
        return self._times[sample_id]
    
    def merge(self,times):
        """merges the sample times of this container with those of another
        @param times: a Time object to merge with the current object.
            If intersection is not null, entries in times overrides those of current object."""
        for k,v in times._times.iteritems() :
            self._times[k]=v
        
    def read_from_file(self,filePath):
        """ """
        ftimes = open(filePath)
        ftimes.readline()  # trash header in a pure pig style (grouik)
        line=ftimes.readline()
#        print ">",line
        for line in ftimes :
#            print ">>",line
            tokens = re.split("\s+",line.strip())
#            print ">>(",tokens[0],",",tokens[-2],")"
            self._times[int(tokens[0])]     = float(tokens[1])
        ftimes.close()
        
    def write_to_file(self,filePath,overwrite=False):
        """ """
        timesToWrite = self
        if overwrite==False :
            try :
                existingTimes = Times()
                existingTimes.read_from_file(filePath)
                existingTimes.merge(self)
                timesToWrite = existingTimes
            except :
                pass
        ftimes = open(filePath,'w')
        ftimes.write("# computation times for samples\n")
        
        for k,v in timesToWrite._times.iteritems() :
            ftimes.write("{0:>6d} {1:>8d}\n".format(k,v))
            
        ftimes.close()

                
    def get_sample_indices(self):
        return self._times.keys()
