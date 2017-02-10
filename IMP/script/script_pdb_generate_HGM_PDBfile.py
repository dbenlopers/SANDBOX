'''


generate fake CA PDB files for all models
'''

import os

import IMP

import HGM
import HGM.representation
import HGM.helpers
import HGM.energies

from alternate_configs import configs



#config_name_for_this_run    = "fixedGeom_EM_1_2"
config_name_for_this_run    = "arp_EM_0_2"
#config_name_for_this_run    = "arp_EM_0_2aLM"


subunitsRepresentationFileName = configs[config_name_for_this_run][0]
runDir                      = os.path.join("results",config_name_for_this_run)
saveDirSample               = os.path.join(runDir,"samples")
savePrefix                  = "saves"

#pdbDir                      = os.path.join(runDir,"pdb")
#### Alternatives
sample_indexes      = HGM.helpers.read_all_sample_indices(saveDirSample, savePrefix)
#sample_indexes      = [0]
#sample_indexes      = range(100)
#pdbPrefix                   = "pdb"
##
#nb_configs          = 1000

nb_configs          = 10000

#pdbDir                      = os.path.join(runDir,"pdb-low")
#type                        = "low"
#pdbPrefix                   = "pdb-low"

pdbDir                      = os.path.join(runDir,"pdb-high")
type                        = "high"
pdbPrefix                   = "pdb-high"

eDir                        = os.path.join(runDir,"energies")
eFileName           = "sample-energies.txt"
sseFileName         = "subsamples-energies.txt"
energiesFilePath    = os.path.join(eDir,eFileName)
subsampleFilePath   = os.path.join(eDir,sseFileName)








for d in [pdbDir] :
    HGM.helpers.check_or_create_dir(d)

exec ( "from {0:s} import build_subunits_info".format( subunitsRepresentationFileName ) )






def load_configurations_from_sample_index_list(arpInfos,sample_indexes) :
    
    mcs                 = HGM.representation.MyConfigurationSet(arpInfos)
    loop_index=0
    print "loading configurations"
    for sidx in sample_indexes :
        loop_index+=1
        if loop_index % 15 == 0 : print ""
        print sidx,
        sampleFilePath  = os.path.join( saveDirSample, HGM.helpers.forge_sample_name(savePrefix, sidx) )
        mcs.read_all_configs_from_file(sampleFilePath)

    return mcs


def load_configurations_from_subsample_index_list(cplxInfos,subsample_indexes) :
    """
    @param cplxInfo: 
    @param indices:  list of configuration indices ("sid:ssidx")
    @param saveDirSample:  where the configuration files are saved
    @return cs:    a cConfigurationSet object in which I I'll store all  
    """
    sample  = HGM.representation.MyConfigurationSet( cplxInfos )
    loop_index=0
    print "  ... reading specific configurations"
    for cidx in subsample_indexes:
        loop_index+=1
        if loop_index % 1500 == 0 : print ""
        if loop_index % 150 == 0 : print cidx,
        (si,isi)=cidx.split(":")
        (si,isi)=(int(si),int(isi))
        sampleFileName          = savePrefix+"--"+str(si)+".txt"
        filePath                = os.path.join(saveDirSample,sampleFileName)
        sample.read_configs_from_file(filePath, [isi])
    
    return sample

def load_configurations_from_sorted_subsample(cplxInfo,nb_configs,type="low"):
    """ 
    sort out configurations based on E score, and return the nb_configs with (lowest/highest) score
    depending on type argument
    """
    print "  - sorting out",nb_configs,type,"configs for",pdbPrefix
    sse = HGM.energies.SubsamplesEnergies()
    try :
#        raise ValueError()  # force recomputation of subsamples
        sse.read_from_file(subsampleFilePath)
        print " (from subsample energies save file)"
    except :
        sse.read_samples_energies_from_file(energiesFilePath)
        print " (from samples energies save file)"
        sse.write_to_file(subsampleFilePath)
    
    ssel = sse.get_sorted_subsamples_energies()
    
    cfgl=[]
    if type == "low":
        cfgl = map( lambda x:x[0],ssel[0:nb_configs])
    elif type == "high":
        cfgl = map( lambda x:x[0],ssel[-nb_configs:])
    else :
        raise ValueError("exepcted one of 'low' or 'high', got"+str(type))

#    print cfgl
    return load_configurations_from_subsample_index_list(cplxInfo,cfgl)





def get_current_pause_as_pdbCA_string(protein_info_dict, chainMap):
        """
        saves proteins from protein_info_dict as a Calpha pdb file in file pdbFileName
        meant to be read by TMscore 
        @param pdbFileName              : 
        @param protein_info_dict        : 
        @param differentiate_subunits   : if True a chain is output per subunit, otherwise, only one chain for the whole complex
        @precondition:  particles attached to beads should be already set
        """
#        p = ProteinModelInfo()
#        X = IMP.core.XYZR()
        
#        chainIDs = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
        
        subunit_index=0;
        header_lines        = []
        atom_lines          = {}
        connect_lines       = {}
        
        header_line = "{0:<6s} {1:<3d} {2:s}\n".format("REMARK",950,"Fake CA PDB file\n")
        header_lines.append(header_line)
        atom_index = 0
#        chainID             = "A"   # if differentiate_subunits == False
        for (prot_name,prot_info) in protein_info_dict.iteritems() :
            subunit_index+=1
#            print "TREATING ",prot_name
            chainID = chainMap[prot_name]
            header_line     = "REMARK 951 subunit {0:s} ({1:d} beads) chain {4:1s} ATOMs {2:d} to {3:d}\n".format(
                          prot_name,
                          prot_info.get_number_of_beads(),
                          atom_index+1,
                          atom_index+prot_info.get_number_of_beads(),
                          chainID
                          )
            header_lines.append(header_line)
#            print "TREATING ",prot_name,"WITH INDEX",subunit_index
            connect_lines[subunit_index]=[]
            for link_index in range(prot_info.get_number_of_links()) :
                (b1,b2) = prot_info.get_link_bead_indices( link_index )
                connect_line    = "CONECT{0:>5d}{1:>5d}\n".format(atom_index+1+b1,atom_index+1+b2)
                connect_lines[subunit_index].append( connect_line )
#            
#    TODO : residue number should be updated if diff sub == True
#
#
            atom_lines[subunit_index]=[]
            for bead_index in range (prot_info.get_number_of_beads()) :
                atom_index+=1
                xyzr        = prot_info.get_bead(bead_index).get_XYZR()
                x,y,z,r     = xyzr.get_x(),xyzr.get_y(),xyzr.get_z(),xyzr.get_radius()
#                "ATOM     34  CA AARG A  -3      12.353  85.696  94.456  0.50 36.67           C  "
                atom_line   = "ATOM  {0:>5d}  CA  ARG {5:1s}{0:>4d}    {1:>8.3f}{2:>8.3f}{3:>8.3f} 00.00 {4:>5.2f}           C  \n".format(
                       atom_index,x,y,z,r,chainID)
                atom_lines[subunit_index].append(atom_line)
        
            
        f=""
        
        for header_line in header_lines :
            f+=(header_line)
        
        # a chain per subunit
        for subunit_idx in range(1,subunit_index+1):
            for atom_line in atom_lines[subunit_idx] :
                f+=(atom_line)
            f+=("TER\n")
            for connect_line in connect_lines[subunit_idx] :
                f+=(connect_line)
                
        return f
        
def write_current_pause_as_pdbCA_with_chains(filePath,protein_info_dict, chainMap):
    f = open(filePath,"w")
    f.write( get_current_pause_as_pdbCA_string( protein_info_dict, chainMap ) )
    f.close()






def main():
        
    m = IMP.Model()
    m.set_log_level(IMP.SILENT)
    cplxInfos = build_subunits_info(m)
    HGM.helpers.mute_all_restraints(m)
    
#    dataDirSample   = "../../data/ARP"
#    sampleFileName  = "save-1TYQ-HGM.txt"
#    sampleFilePath  = os.path.join(dataDirSample,sampleFileName)
#    index = 0
#    sampleFilePath  = os.path.join( saveDirSample, HGM.helpers.forge_sample_name(savePrefix, index) )

#    mcs.load_configuration(0)
    
#    print "WITH differenciation"
#    print HGM.helpers.get_current_pause_as_pdbCA_string(arpInfos, True)
#    
#    print "\n\nWITHOUT differenciation"
#    print HGM.helpers.get_current_pause_as_pdbCA_string(arpInfos, False)    
    
#    mcs = load_configurations_from_sample_index_list(cplxInfos,sample_indexes)
    mcs = load_configurations_from_sorted_subsample(cplxInfos, nb_configs, type)
    
#    mcs                 = HGM.representation.MyConfigurationSet(arpInfos)
#    loop_index=0
#    print "loading configurations"
#    for sidx in sample_indexes :
#        loop_index+=1
#        if loop_index % 15 == 0 : print ""
#        print sidx,
#        sampleFilePath  = os.path.join( saveDirSample, HGM.helpers.forge_sample_name(savePrefix, sidx) )
#        mcs.read_all_configs_from_file(sampleFilePath)

    print "got",mcs.get_number_of_configurations(),"configurations"
    loop_index=0
    print "writing pdb_files"
    for i in range( mcs.get_number_of_configurations() ) :
        loop_index+=1
        if loop_index % 150 == 0 : print ""
        if loop_index % 15 == 0 : print i,
        mcs.load_configuration(i)
        filePath = os.path.join(pdbDir,pdbPrefix+"--{0:06d}.pdb".format(i))
        
        chainMap={"arp3":"A",
                  "arp2":"B",
                  "arpc1":"C",
                  "arpc2":"D",
                  "arpc3":"E",
                  "arpc4":"F",
                  "arpc5":"G"
                  }
        
#        chainMap={"p8":"A",
#                  "p52":"B",
#                  "p44":"C",
#                  "p34":"D",
#                  "p62":"E",
#                  "XPB":"F",
#                  "XPD":"G",
#                  "MAT1":"H",
#                  "CDK7":"I",
#                  "CyclinH":"J"
#                  }
        
        write_current_pause_as_pdbCA_with_chains(filePath, cplxInfos, chainMap )
    

if __name__ == "__main__" :
    main()
    print "\n...Finished !"
