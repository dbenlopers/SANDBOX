'''

'''

import math
import pickle

import IMP
import IMP.core, IMP.algebra

import HGM
import HGM.representation

import os, os.path

import glob

import re

import socket








def XYZdecorate(IMP_particle):
    return IMP.core.XYZ_decorate_particle(IMP_particle)

def XYZRdecorate(IMP_particle):
    return IMP.core.XYZR_decorate_particle(IMP_particle)
    

#### sample file names and indices
#
#

def forge_sample_name(savePrefix,index):
    return savePrefix+"--"+str(index)+".txt"

def forge_sample_path(saveDir,savePrefix,index):
    return os.path.join(saveDir,savePrefix+"--"+str(index)+".txt")


def read_all_sample_indices(saveDirSample,savePrefix):
    """
    """
    fileNames = glob.glob(os.path.join(saveDirSample,savePrefix+"--*.txt"))
    indices =[]
    for f in fileNames :
        m = re.search("--(\d+)\.txt$", f)
        try :
            i = int(m.group(1))
            indices.append(i)
        except :
            print "cannot find index in sample file  <<",f,">>"
            pass
    
    return indices

def read_all_sample_indices_in_list(saveDirSample,savePrefix,desired_indices):
    """
    read all sample files in a directory and collect the filename only for those having their index in the indices list 
    """
    fileNames = glob.glob(os.path.join(saveDirSample,savePrefix+"--*.txt"))
    indices =[]
    for f in fileNames :
        m = re.search("--(\d+)\.txt$", f)
        try :
            i = int(m.group(1))
            if i in desired_indices :
                indices.append(i)
        except :
            print "cannot find index in sample file  <<",f,">>"
            pass
    
    return indices

def get_sample_indices_gaps(saveDirSample,savePrefix):
    indices = sorted (read_all_sample_indices(saveDirSample,savePrefix))
#    print (len (indices))
    prev_i =indices[0]
    gaps=[]
    for i in indices :
        if i-prev_i !=1 :
            gaps.append( "range({0},{1})".format(prev_i+1,i) )
        prev_i=i
    return gaps






def get_datadir():
    "get full path to data dir depending on the machine on which I am"
    machine_name = socket.gethostname()
    if machine_name == "MacBook-Pro-de-Benjamin-SCHWARZ.local" :
        dataDir = "/Users/schwarz/Dev/TFIIH/data/"
    else :
        dataDir = "/home/lbm/schwarz/Dev/TFIIH/data/"
    return dataDir




def randomize_particles_in_bbox(bb,particles):
    """ Sets a list of particles randomly in a bbox
    @param bb: the bounding box
    @param particles:  the list of partcles to move
    """
    #
    for p in particles :
        x = IMP.core.XYZ(p)
        x.set_coordinates( IMP.algebra.get_random_vector_in(bb) )


def randomize_xparticles_in_bbox(bb,xparticles):
    """ Sets a list of particles randomly in a bbox
    @param bb: the bounding box
    @param xparticles:  a list of XYZ to move
    """
    #
    for x in xparticles :
        x.set_coordinates( IMP.algebra.get_random_vector_in(bb) )


def show_restraints_names(m):
    """ @param m : IMP model"""
    for r in m.get_restraints():
        print r.get_name()
        
def evaluate_restraints(m):
    """ @param m : IMP model"""
    for r in m.get_restraints():
        print r.get_name(),":",r.evaluate(False)

def compute_sample_energies(mcs,m=None):
    """ returns the series of energies for the configurations hosted in a configurationSet object
     @param mcs: an object of type ConfigurationSet
     @param m:   an IMP.Model object, if NoneType, we hope mcs is a MyConfigurationSet and we can access its model"""
    if m == None :
        m = mcs.get_model()
    energies = []
    
#    mc=HGM.representation.MyConfigurationSet()
    for i in range(mcs.get_number_of_configurations()) :
        mcs.load_configuration(i)
        energies.append(m.evaluate(False))
    return energies

def compute_list_statistics(l):
    """ returns mean and std dev of a list """
    E   = 0
    s   = 0
    for e in l :
        E+=e
        s+=e*e
    n= float(len(l))
    E = E/n
    s = s/n - E*E
    return (E,s)

def check_or_create_dir(dir):
    """ check if directory exists, and if not, tries to create it"""
    if not os.path.exists(dir):
        print "directory <",dir,"> does not exist, I'll create it"
        os.makedirs(dir)


def set_all_restraints_verbosity(m,v):
    for r in m.get_restraints():
        r.set_log_level(v)

def mute_all_restraints(m):
    for r in m.get_restraints():
        r.set_log_level(IMP.SILENT)


#    DIST MATRIX
#
def savePickleDistMatrix(fileName,cdm):
    print "saving matrix to", fileName
    f=open(fileName,"w")
    pickle.dump(cdm,f,protocol=2)
    f.close()
    
def loadPickleDistMatrix(fileName):
    print "loading matrix from",fileName
    f=open(fileName)
    cdm = pickle.load(f)
    f.close()
    return cdm

#def get_list_of_files():

def get_IMP_version_string():
    version_string = ""
    try:
        version_string=IMP.get_module_version_info().get_version()
    except:
        version_string=IMP.get_module_version()
    return version_string






##############################
#
#    HANDLE PDB WRITTING
#
#

def get_current_pause_as_pdbCA_string(protein_info_dict, differentiate_subunits=False):
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
        
        chainIDs = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
        
        subunit_index=0;
        header_lines        = []
        atom_lines          = {}
        connect_lines       = {}
        
        header_line = "{0:<6s} {1:<3d} {2:s}\n".format("REMARK",950,"Fake CA PDB file\n")
        header_lines.append(header_line)
        atom_index = 0
        chainID             = "A"   # if differentiate_subunits == False
        for (prot_name,prot_info) in protein_info_dict.iteritems() :
#            print "TREATING ",prot_name
            if differentiate_subunits == True :
                chainID = chainIDs[subunit_index]
            subunit_index+=1;
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
        
        if differentiate_subunits == True :
            # a chain per subunit
            for subunit_idx in range(1,subunit_index+1):
                for atom_line in atom_lines[subunit_idx] :
                    f+=(atom_line)
                f+=("TER\n")
                for connect_line in connect_lines[subunit_idx] :
                    f+=(connect_line)
        else :
            # just one chain
            for subunit_idx in range(1,subunit_index+1):
                for atom_line in atom_lines[subunit_idx] :
                    f+=(atom_line)
            f+=("TER\n")
            for subunit_idx in range(1,subunit_index+1):
                for connect_line in connect_lines[subunit_idx] :
                    f+=(connect_line)

        return f
        
def write_current_pause_as_pdbCA(filePath,protein_info_dict, differentiate_subunits=False):
    f = open(filePath,"w")
    f.write( get_current_pause_as_pdbCA_string( protein_info_dict, differentiate_subunits ) )
    f.close()

#
#def write_pauses_as_pdbCA(filePath,mcs, differentiate_subunits=False):
#    """
#    output configurations in a configuration set as distinct pdb MDL in a pdb file
#    @param filePath:               path to the pdb file I shall write
#    @param mcs:                    a (My)configurationsSet object : list of configurations
#    @param differentiate_subunits: if true, every subunit is output as different chain in the PDB file 
#    """
#    protein_info_dict       = mcs.get_prot_info_model()
#    f = open(filePath,"w")
#    for i in range( mcs.get_number_of_configurations() ) :
#        f.write("MDL       {0:>4d}".format(i))
#        f.write( get_current_pause_as_pdbCA_string( protein_info_dict, differentiate_subunits ) )
#        f.write("ENDMDL")  
#    f.close()
#
#def make_current_pauses_as_pdbCA(protein_info_dict, differentiate_subunits=False):
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
#        subunit_index=0;
#        header_lines        = []
#        atom_lines          = {}
#        connect_lines       = {}        #unused
#        
#        prot_name           = []        # we'll store the protein names as they are comming
#        subunit_beadsxyzr   = {}        # we'll store the protein XYZR domains as they are comming
#        
#        
#        header_line = "{0:<6s} {1:<3d} {2:s}\n".format("REMARK",950,"Fake CA PDB file\n")
#        header_lines.append(header_line)
#        atom_index = 0
#        chainID             = "A"   # if differentiate_subunits == False
#        for (prot_name,prot_info) in protein_info_dict.iteritems() :
##            print "TREATING ",prot_name
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
##            print "TREATING ",prot_name,"WITH INDEX",subunit_index
#            connect_lines[subunit_index]=[]
#            for link_index in range(prot_info.get_number_of_links()) :
#                (b1,b2) = prot_info.get_link_bead_indices( link_index )
#                connect_line    = "CONECT{0:>5d}{1:>5d}\n".format(atom_index+1+b1,atom_index+1+b2)
#                connect_lines[subunit_index].append( connect_line )
##            
##    TODO : residue number should be updated if diff sub == True
##
##
#            
#            for bead_index in range (prot_info.get_number_of_beads()) :
#                subunit_beadsxyzr[subunit_index]=[]
#                xyzr        = prot_info.get_bead(bead_index).get_XYZR()                
#                subunit_beadsxyzr[subunit_index].append(xyzr)
#                
#        #    def make_atom_lines_for_current_pause():
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
#        f=""
#        
#        for header_line in header_lines :
#            f+=(header_line)
#        
#        if differentiate_subunits == True :
#            # a chain per subunit
#            for subunit_idx in range(1,subunit_index+1):
#                for atom_line in atom_lines[subunit_idx] :
#                    f+=(atom_line)
#                f+=("TER\n")
#                for connect_line in connect_lines[subunit_idx] :
#                    f+=(connect_line)
#        else :
#            # just one chain
#            for subunit_idx in range(1,subunit_index+1):
#                for atom_line in atom_lines[subunit_idx] :
#                    f+=(atom_line)
#            f+=("TER\n")
#            for subunit_idx in range(1,subunit_index+1):
#                for connect_line in connect_lines[subunit_idx] :
#                    f+=(connect_line)
#
#        return f


######## RMSD and such
#
#

def gather_coordinates_for_current_config(xyzl):
    """ provided a list of XYZ particles, returns the concatenated list of the particles coordinates in the current conformation"""
    vect = []
    for X in xyzl :
        vect.extend([X.get_x(),X.get_y(),X.get_z()])
    return vect

def compute_coods_rmsd(coods_1,coods_2):
    """ computes rmsd distance between two 3D vectors stored in flat python lists
    @param coods_1: a list of float representing coordinates
    @param coods_2: a list of float representing coordinates
    @precondition: list lengths for coods_1 and coods_2 should be similar and multiple of 3"""
    rmsd2 = 0
    length = len(coods_1)
    for i in range(length) :
        c=coods_1[i]-coods_2[i]
        rmsd2 += c*c
#    return ( math.sqrt(rmsd2 / length ) )
    return ( math.sqrt(3*(rmsd2 / length ) ) )

def compute_particle_dist_vector(coods_current,coods_solution):
    """ computes """
    rmsd2 = 0
    length = len(coods_current)
    rmsdl = []
    for i in range(length) :
        x = i*3 ; y = i*3+1; z = i*3+2
        cx=coods_current[x]-coods_solution[x]
        cy=coods_current[y]-coods_solution[y]
        cz=coods_current[z]-coods_solution[z]
        c2 = cx*cx+cy*cy+cz*cz
        rmsdl.append(math.sqrt(rmsd2))
    return rmsdl
