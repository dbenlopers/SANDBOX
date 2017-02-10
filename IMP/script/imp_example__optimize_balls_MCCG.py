import IMP.core
import IMP.display
import IMP.container
import IMP.algebra
#import IMP.rmf
bb=IMP.algebra.BoundingBox3D(IMP.algebra.Vector3D(0,0,0),
IMP.algebra.Vector3D(10,10,10));
# in fast do 10,10,10, for the purposes of testing we reduce it
ni=2
nj=3
np=6
radius=.45
k=100

nb_opti_loops = 1
#nb_opti_loops = 10

mc_use_incrental = False
#mc_use_incrental = True
#mc_alternate_moves = False
mc_alternate_moves = True
# using a HarmonicDistancePairScore for fixed length links is more
# efficient than using a HarmonicSphereDistnacePairScore and works
# better with the optimizer
lps= IMP.core.HarmonicDistancePairScore(1.5*radius, k)
sps= IMP.core.SoftSpherePairScore(k)
m= IMP.Model()
IMP.set_log_level(IMP.SILENT)
aps=[]
filters=[]
movers=[]
#rss= IMP.RestraintSet(m, 1.0, "bonds")
rss= IMP.RestraintSet(1.0, "bonds")
m.add_restraint(rss)

for i in range(0,ni):
    for j in range(0,nj):
        base=IMP.algebra.Vector3D(i,j,0)
        chain=[]
        for k in range(0,np):
            p= IMP.Particle(m)
            p.set_name("P"+str(i)+" "+str(j)+" "+str(k))
            s=IMP.algebra.Sphere3D(IMP.algebra.get_random_vector_in(bb), radius)
            d= IMP.core.XYZR.setup_particle(p,s)
            movers.append(IMP.core.BallMover([p], radius*2))
            movers[-1].set_was_used(True)
            IMP.display.Colored.setup_particle(p, IMP.display.get_display_color(i*nj+j))
            if k==0:
                d.set_coordinates(base)
            else:
                d.set_coordinates_are_optimized(True)
            chain.append(p)
            aps.append(p)
        # set up a chain of bonds
#        cpc= IMP.container.ExclusiveConsecutivePairContainer(chain)
        cpc= IMP.container.ConsecutivePairContainer(chain)
        r= IMP.container.PairsRestraint(lps, cpc)
        rss.add_restraint(r)
# cheat
filters.append(IMP.container.InContainerPairFilter(cpc))
filters[-1].set_was_used(True)
ibss= IMP.core.BoundingBox3DSingletonScore(IMP.core.HarmonicUpperBound(0,k), bb)
bbr= IMP.container.SingletonsRestraint(ibss, aps)
rss.add_restraint(bbr)

cg= IMP.core.ConjugateGradients(m)
mc=IMP.core.MonteCarlo(m)
if mc_alternate_moves :
    sm= IMP.core.SerialMover(movers)
    mc.add_mover(sm)
else :
    for mo in movers : 
        mc.add_mover(mo)
        
# we are special casing the nbl term
isf= IMP.core.IncrementalScoringFunction(aps, [rss])
# use special incremental support for the non-bonded part
# apply the pair score sps to all touching ball pairs from the list of particles
# aps, using the filters to remove undersired pairs
# this is equivalent to the nbl construction above but optimized for incremental
isf.add_close_pair_score(sps, 0, aps, filters)

# create a scoring function for conjugate gradients that includes the
# ExcludedVolumeRestraint
nbl= IMP.core.ExcludedVolumeRestraint(aps, k, 1)
nbl.set_pair_filters(filters)
sf= IMP.core.RestraintsScoringFunction([rss, nbl])

if mc_use_incrental:
    mc.set_incremental_scoring_function(isf)
else:
    # we could, instead do non-incremental scoring
    mc.set_scoring_function(sf)

# first relax the bonds a bit
rs=[]
#for p in aps:
#    rs.append(IMP.ScopedSetFloatAttribute(p, IMP.core.XYZR.get_radius_key(),
##                                          IMP.core.XYZR_decorate_particle(p).get_radius()/2.))
#                                          0))
#cg.set_scoring_function(sf)
#cg.optimize(1000)
print "collisions", nbl.evaluate(False), "bonds", rss.evaluate(False), bbr.evaluate(False)
#
# shrink each of the particles, relax the configuration, repeat

print "evaluate model :",m.evaluate(False)
m.set_maximum_score(10)
mccgs =  IMP.core.MCCGSampler(m)
mccgs.set_bounding_box(bb)
mccgs.set_is_refining(True)
mccgs.set_number_of_conjugate_gradient_steps(50)
mccgs.set_number_of_monte_carlo_steps(100)
mccgs.set_number_of_attempts(1)
mccgs.set_save_rejected_configurations(True)

cs      = mccgs.get_sample()
if cs.get_number_of_configurations() == 0 :
    print "no configuration output, let's get the rejected one"
    cs      = mccgs.get_rejected_configurations()
else :
    print "got a good configuration"

print "load config" 
cs.load_configuration(0)
print "evaluate model :",m.evaluate(False)
print "collisions", nbl.evaluate(False), "bonds", rss.evaluate(False), "bounding box", bbr.evaluate(False)

#for i in range(1,nb_opti_loops+1):
#    rs=[]
#    factor=.1*i
#    for p in aps:
#        rs.append(IMP.ScopedSetFloatAttribute(p, IMP.core.XYZR.get_radius_key(),
#                                         IMP.core.XYZR(p).get_radius()*factor))
#    # move each particle 100 times
#    print factor
#    for j in range(0,5):
#        mc.set_kt(100.0/(3*j+1))
#        print "mc", mc.optimize(ni*nj*np*(j+1)*100), m.evaluate(False), cg.optimize(10)
##    del rs
#    print "collisions", nbl.evaluate(False), "bonds", rss.evaluate(False), "bounding box", bbr.evaluate(False)
#    del rs
#    print "collisions", nbl.evaluate(False), "bonds", rss.evaluate(False), "bounding box", bbr.evaluate(False)


w= IMP.display.PymolWriter("bouboules-mccg-final.pym")
#w= IMP.display.PymolWriter("final.pym")
for p in aps:
    g= IMP.core.XYZRGeometry(p)
    w.add_geometry(g)
g= IMP.display.BoundingBoxGeometry(bb)
g.set_name("bb")
w.add_geometry(g)
