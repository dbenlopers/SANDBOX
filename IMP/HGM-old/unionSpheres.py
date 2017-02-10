'''
Created on 9 oct. 2012

'''
import xml.dom.minidom
#from xml.dom.minidom import Node

import IMP, IMP.algebra

class UnionSpheres(list):
    """ a simple container of IMP spheres
    """
    
    def __init__(self):
        """ """
        pass

#    def read_spheres_chimera_xml(self, filename):
#        """ read spheres form a marker xml chimera file (.cmm)
#        @param filename: the path to the file to read
#        @return: the number of spheres extracted 
#        """
#        doc = xml.dom.minidom.parse( filename )
#        ms = doc.getElementsByTagName("marker")
#        idx=0
#        for m in ms :
#            idx+=1
#            s=map(lambda x:float(m.getAttribute(x)),["x","y","z","radius"])
#            self.append( IMP.algebra.Sphere3D( IMP.algebra.Vector3D(s[0:3]),s[3]) )
#        return idx

    def compute_bbox(self):
        """ compute the bounding box of the pack of spheres 
        """
        bb = IMP.algebra.get_bounding_box( self[0] )
        xM,yM,zM = bb.get_corner(1)
        xm,ym,zm = bb.get_corner(0)
        for s in self[1:] :
            bb = IMP.algebra.get_bounding_box( s )
            xsM,ysM,zsM = bb.get_corner(1)
            xsm,ysm,zsm = bb.get_corner(0)
            if xsM > xM : xM = xsM
            if ysM > yM : yM = ysM
            if zsM > zM : zM = zsM
            if xsm < xm : xm = xsm
            if ysm < ym : ym = ysm
            if zsm < zm : zm = zsm
        return IMP.algebra.BoundingBox3D( IMP.algebra.Vector3D(xm,ym,zm) , IMP.algebra.Vector3D(xM,yM,zM) )
    
    def get_size(self):
        """ return the number of spheres in the container """
        return len(self)
    
    def add_sphere_IMP(self, sphere):
        """
        @param sphere: add an IMP sphere in the container
        """
        self.append( sphere )
        
    def add_sphere_coods(self, quadruplet):
        """
        @param quadruplet: transforms [x,y,z,r] in an IMP sphere and pile up in the container 
        """
        self.append( IMP.algebra.Sphere3D( IMP.algebra.Vector3D(quadruplet[0:3]),quadruplet[3]) )
        
    def merge(self, unionSpheres ):
        """
        append all spheres contained in an other UnionSpheres object
        @param unionSpheres: the union of spheres that we wich to import
        """
        self.extend(unionSpheres)





def read_unionSpheres_in_chimera_xml( filename ):
    """ read input from a marker xml chimera file (.cmm)
        and returns a dictionnary containing attaching 
        the name of a marker_set to a UnionSphere object containing the markers 
    @param filename: the path to the file to read
    @return: a dictionnary of UnionSpheres objects 
    """
    doc = xml.dom.minidom.parse( filename )
    msl = doc.getElementsByTagName("marker_set")
    usd={}
    for ms in msl :
        ms_name = ms.getAttribute("name")
        ml = ms.getElementsByTagName("marker")
        us = UnionSpheres(); 
        for m in ml :
            s=map(lambda x:float(m.getAttribute(x)),["x","y","z","radius"])
            us.add_sphere_coods(s)
        usd[ms_name]=us
    return usd
