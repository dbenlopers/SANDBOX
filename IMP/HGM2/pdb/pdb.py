'''

'''




#rePDBlineATOM       = re.compile("ATOM  ")

#    PDB ATOM/HETATM fields
#
# 1 -  6        Record name   "ATOM  " ( | "HETATM" )
# 7 - 11        Integer       serial       Atom  serial number.
#13 - 16        Atom          name         Atom name.
#17             Character     altLoc       Alternate location indicator.
#18 - 20        Residue name  resName      Residue name.
#22             Character     chainID      Chain identifier.
#23 - 26        Integer       resSeq       Residue sequence number.
#27             AChar         iCode        Code for insertion of residues.
#31 - 38        Real(8.3)     x            Orthogonal coordinates for X in Angstroms.
#39 - 46        Real(8.3)     y            Orthogonal coordinates for Y in Angstroms.
#47 - 54        Real(8.3)     z            Orthogonal coordinates for Z in Angstroms.
#55 - 60        Real(6.2)     occupancy    Occupancy.
#61 - 66        Real(6.2)     tempFactor   Temperature  factor.
#77 - 78        LString(2)    element      Element symbol, right-justified.
#79 - 80        LString(2)    charge       Charge  on the atom.
class MolecInfos():
    """Stores the coordinates field informations of a pdb file, and eases access to these"""
    class Entry(dict):
        """ a dict-like object meant to store the various fields of a pdb ATOM (or HETATM) line """
        def __init__(self,coordinateLine):
            """ 
            @param coordinateLine: a pdb coordinate line string
            @precondition: coordinateLine should be formated as a regular ATOM or HETATM pdb line
            """
#            coordinateLine
#            self.line = coordinateLine
            self["record"]          = coordinateLine[0:6]
            self["serial"]          = coordinateLine[6:11]
            self["name"]            = coordinateLine[12:16]
            self["altLoc"]          = coordinateLine[16]
            self["resName"]         = coordinateLine[17:20]
            self["chainID"]         = coordinateLine[21]
            self["resSeq"]          = coordinateLine[22:26]
            self["iCode"]           = coordinateLine[26]
            self["x"]               = coordinateLine[30:38]
            self["y"]               = coordinateLine[38:46]
            self["z"]               = coordinateLine[46:54]
            self["occupancy"]       = coordinateLine[54:60] 
            self["tempFactor"]      = coordinateLine[60:66]
            self["element"]         = coordinateLine[76:78]
            self["charge"]          = coordinateLine[78:80]        
            
        def __repr__(self):
            return self["record"]       +\
                self["serial"]          +\
                " "                     +\
                self["name"]            +\
                self["altLoc"]          +\
                self["resName"]         +\
                " "                     +\
                self["chainID"]         +\
                self["resSeq"]          +\
                self["iCode"]           +\
                "   "                   +\
                self["x"]               +\
                self["y"]               +\
                self["z"]               +\
                self["occupancy"]       +\
                self["tempFactor"]      +\
                "          "            +\
                self["element"]         +\
                self["charge"]
        
        def getCoods(self):
            """ returns the 3 floats coordinates """
            return [ float(self["x"]), float(self["y"]), float(self["z"]) ]
        
        get_coordinates = getCoods
        
        def getPDBline(self):
            """ returns the corresponding pdb Line string """
            return str(self)
        
        def get_chainID(self):
            return self["chainID"]
        
        def get_resSeq(self):
            return int(self["resSeq"])
        
        get_resNum = get_resSeq
        
        def get_name(self):
            return self["name"].strip()
        
        def get_resName(self):
            return self["resName"].strip()
            
    def __init__(self):
        self._entries               = []
        
    def size(self):
        return len(self._entries)
        
    def read_pdb_file(self,filePath):
        self._entries               = []
        # try to open file
        f = open(filePath)
        
        
        # these internal fields are set only when needed through _initMinMaxIndices(self):
        #self._maxAtomIndex
        #self._minAtomIndex
        #self._maxResidueIndex
        #self._maxResidueIndex
        
        self._chainIDs=set()
        #
        # fill internal fields
        #
        for line in f :
            firstToken = line[0:6].strip()
            if      firstToken == "ATOM" or firstToken == "HETATM":
                e = self.Entry(line)
                self._chainIDs.add(e["chainID"])
                self._entries.append( e )
                
        
    
    
#    def _initMinMaxIndices(self):
#        """ looks for min and max indices for atoms or residues in the structure, and sets internal fiels accordingly """
#        for atom in self._entries:
#            atomIndex       = int(atom["serial"].strip())
#            residueIndex    = int(atom["resSeq"].strip())
#            try :
#                if atomIndex < self._minAtomIndex :
#                    self._minAtomIndex = atomIndex
#            except :
#                self._minAtomIndex = atomIndex
#            try :
#                if atomIndex > self._maxAtomIndex :
#                    self._maxAtomIndex = atomIndex
#            except :
#                self._maxAtomIndex = atomIndex
#            try :
#                if residueIndex < self._minResidueIndex :
#                    self._minResidueIndex = residueIndex
#            except :
#                self._minResidueIndex = residueIndex
#            try :
#                if residueIndex > self._maxResidueIndex :
#                    self._maxResidueIndex = residueIndex
#            except :
#                self._maxResidueIndex = residueIndex                    
    def get_chainIDs(self):
        try :
            return list(self._chainIDs)
        except :
            return None
    
    def iterEntries(self):
        """ """
        return iter(self._entries)
    
    def getEntry(self,index):
        """ """
        return self._entries[index]
    
    def filterChains(self,chains):
        molec = MolecInfos()
        for atom in self._entries :
            if atom["chainID"] in chains :
                molec._entries.append(atom)
        return molec
    
    def filterResidues(self,residueNames):
        molec = MolecInfos()
        for atom in self._entries :
            if atom["resName"] in residueNames :
                molec._entries.append(atom)
        return molec
        
    def filterAllHetatom(self):
        molec = MolecInfos()
        for atom in self._entries :
            if atom["record"] =="HETATM" :
                molec._entries.append(atom)
        return molec

    def filterAllAtom(self):
        molec = MolecInfos()
        for atom in self._entries :
            if atom["record"] =="ATOM  " :
                molec._entries.append(atom)
        return molec
    
#    def getMaxAtomIndex(self):
#        """ returns the greatest atom index encountered in the pdb file """
#        try : 
#            return self._maxAtomIndex
#        except :
#            self._initMinMaxIndices()
#            return self._maxAtomIndex
#    
#    def getMinAtomIndex(self):
#        """  returns the lowest atom index encountered in the pdb file """
#        try : 
#            return self._minAtomIndex
#        except :
#            self._initMinMaxIndices()
#            return self._minAtomIndex
#
#    def getMaxResidueIndex(self):
#        """ returns the greatest atom index encountered in the pdb file """
#        try : 
#            return self._maxResidueIndex
#        except :
#            self._initMinMaxIndices()
#            return self._maxResidueIndex
#    
#    def getMinResidueIndex(self):
#        """  returns the lowest atom index encountered in the pdb file """
#        try : 
#            return self._minResidueIndex
#        except :
#            self._initMinMaxIndices()
#            return self._minResidueIndex

    def saveCoordinates(self, filePath):
        """ writes atom coordinates to a file
        """
        f=open(filePath,"w")
        for atom in self.iterEntries() :
            f.write( atom.getPDBline() +"\n")    
        f.close()
        
    def get_entries_from_chain(self,chainID):
        """
        """
        entries=[]
        for e in self._entries :
            if e["chainID"]==chainID:
                entries.append( self.Entry(str(e)) )
        return entries
    
    def insert_entry(self,e):
        self._entries.append( self.Entry(str(e)) )
        try :
            self._chainIDs.add( e["chainID"] )
        except :
            self._chainIDs=set( [e["chainID"]] )
