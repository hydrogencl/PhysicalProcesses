# this is an example of running the Solar Calculation Model, with plot
import SolarCalc_alpha as SDM
import matplotlib.pyplot as PLT

#  print d,h,SDM.SolarRadiationModel(d, 50.0, h )
a = []
for d in range(1,366):
  for h in range(24):
    a .append( SDM.SolarRadiationModel( d,140.0, h, Pa=103100, time_noon=12)[0] )
    

fig = PLT.figure()
ax = fig.add_subplot(111)
ax.plot(a)
PLT.show()
