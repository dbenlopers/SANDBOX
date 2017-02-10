'''
'''
import os
import math
import re

import IMP

import HGM
import HGM.energies
import HGM.helpers

from alternate_configs import configs


#config_name_for_this_run    = "fixedGeom_EM_1_2"
config_name_for_this_run    = "arp_EM_0_2"

#
#    PARAMETERS
#
tfiihRepresentationFileName = configs[config_name_for_this_run][0]
#runDir                      = os.path.join("Users","schwarz","Dev","TFIIH","src","coarse2","results",config_name_for_this_run)
runDir                      = os.path.join("results",config_name_for_this_run)

saveDirSample               = os.path.join(runDir,"samples")
savePrefix                  = "saves"

eDir                        = os.path.join(runDir,"energies")
eFileName                   = "sample-energies.txt"
seFileName                  = "subsamples-energies.txt"

altConfigDir                = os.path.join(runDir,"altConfigs")
lowEconfigsFilePath         = os.path.join(altConfigDir,"lowE-configs-112.txt")
mediumEconfigsFilePath      = os.path.join(altConfigDir,"mediumE-configs-112.txt")
highEconfigsFilePath        = os.path.join(altConfigDir,"highE-configs-112.txt")


for d in [altConfigDir] :
    HGM.helpers.check_or_create_dir(d)

energiesFilePath = os.path.join(eDir,eFileName)
subsamplesEnergyfilePath=os.path.join(eDir,seFileName)


exec ( "from {0:s} import build_subunits_info".format( tfiihRepresentationFileName ) )

class SubsamplesEnergies :
    
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
        e = HGM.energies.EnergiesForSampleCollection()
        e.read_from_file(energiesFilePath)
        self.read_energies(e)

    def get_sorted_subsamples_energies(self):
        """ returns the list of sample indices with energies, sorted in increasing energy 
        @return: a list of pairs (config_identifier, energy)
        @note: config_identifier are formated as sample_index:subsample_index"""
        return sorted (self._energies.items(),key=lambda x:x[1])


    
        
def main ():
    
    m = IMP.Model()
    m.set_log_level(IMP.SILENT)
    tfiihInfos = build_subunits_info(m)
    HGM.helpers.mute_all_restraints(m)
    
    sse = SubsamplesEnergies()
    
#    print "getting subsamples energies from samples energies"
#    sse.read_samples_energies_from_file(energiesFilePath)

    print "getting subsamples energies from subsample energy file"
    sse.read_from_file(subsamplesEnergyfilePath)
    
#    print "saving subsamples energies"
#    sse.write_to_file(subsamplesEnergyfilePath)
    
    sl = sse.get_sorted_subsamples_energies()
    print "fst and lst",sl[0],sl[-1]
    es = []
    for (k,e) in sl :
        es.append(e)
    print "fst and lst",es[0],es[-1]
#    print es
    E,S = HGM.helpers.compute_list_statistics(es)
    Ss2 = math.sqrt(S)/2
    print "E,S",Ss2
    
    def first_index_above(l,t):
        i = 0
        for e in l :
            if e[1]>t :
                return i
            i+=1
        return None
    
    Emin = E - Ss2
    Emax = E + Ss2
    print Emin,">",Emax
    
    print first_index_above(sl,Emin),">",first_index_above(sl,Emax),">",len(sl)
    
    
    def saveConfigs( indices, saveFilePath ):
        samples = {}
        print " ... collecting indices and subindices"
        for i in indices :
            sampleIdx = sl[i][0]
            (si,isi)=sampleIdx.split(":")
            (si,isi)=(int(si),int(isi))
            try :
                samples[si].append(isi)
            except :
                samples[si]=[isi]
#        print samples
        sample  = HGM.representation.MyConfigurationSet( tfiihInfos )
        print "  ... reading specific configurations"
        for si,sisl in samples.iteritems() :
            sampleFileName          = savePrefix+"--"+str(si)+".txt"
            filePath                = os.path.join(saveDirSample,sampleFileName)
            sample.read_configs_from_file(filePath, sisl)
            
        print " ... ",sample.get_number_of_configurations()," configurations in the sample"
        print "  ... saving configurations to",saveFilePath
        sample.save_all_configs_to_file(saveFilePath)
    
    
#    print "create sample with lowest energies"
#    saveConfigs( range(first_index_above(sl,Emin)) ,lowEconfigsFilePath)
#    print "create sample with medium energies"
#    saveConfigs( range(first_index_above(sl,Emin),first_index_above(sl,Emax)) ,mediumEconfigsFilePath)
#    print "create sample with highest energies"
#    saveConfigs( range(first_index_above(sl,Emax),len(sl)) ,highEconfigsFilePath)
    
    nbScores = 200
    print nbScores,"best  scores atteined for :",map(lambda x:x[0],sl[0:nbScores]) 
    print nbScores,"worst scores atteined for :",map(lambda x:x[0],sl[-nbScores-1:-1])
    
    
if (__name__ == "__main__") :
    main()
    print "That's all folks !!!"
