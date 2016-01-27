#!/usr/bin/python
# The main work of solar estimation from Spokas 2006
# 20160127: First work-able edition. Check with Latitude with 
import math

def SolarDeclinationAng(doy):
  # doy: day of year, starting from 1 to 365/366
  SIN_dsd =  0.39785 * math.sin( 4.869 + 0.0172 * doy + 0.03345 * math.sin (6.2238 + 0.0172 * doy)   )

  COS_dsd = ( 1 - SIN_dsd **2 ) ** 0.5
  dsd =  math.asin(SIN_dsd)
  chk_tmp = SIN_dsd ** 2 + COS_dsd ** 2
  max_sd =  0.13 * math.pi
  min_sd = -0.13 * math.pi
#  print "dsd:       ",SIN_dsd, COS_dsd,dsd, dsd*180/math.pi
#  print "min/max sin",math.sin(min_sd),math.sin(max_sd) 
  return SIN_dsd, COS_dsd, dsd


def ZenithAngle(doy, lati_deg, time_cur, time_noon=12):
  #lati_deg: latitude in degree, but starting from 0 in the south pole
  PHI = lati_deg /180.0 * math.pi
  SIN_dsd, COS_dsd, dsd = SolarDeclinationAng(doy)

  #COS_PSI = math.sin( PHI ) * SIN_dsd + math.cos( PHI ) * COS_dsd * math.cos(15*(time_cur - time_noon) *math.pi/180)
  COS_PSI =  math.sin( PHI ) * math.sin(dsd) + math.cos( PHI ) * math.cos(dsd) * math.cos(15*(time_cur - time_noon)/180.0*math.pi)

  PSI = math.acos(COS_PSI)
#  print "PSI:", PSI,COS_PSI, "in degree:", PSI*180/math.pi 
  return PSI,COS_PSI


def MassNum(ZnAng, Pa=98000, if_ele=False, num_ele=0.0):
  if if_ele:
    num_pa=101300 * math.exp( -1 * (num_ele /8200.0 ))
  else:
    num_pa = Pa
  num_mass = num_pa / ( 101300 * math.cos(ZnAng)  )
  #num_mass = num_pa / ( 101300 * ZnAng  )
#  print "num_mass",num_mass
  return num_mass

def SolarBeamRadia(ZnAng, SP0=1360, TAU=0.7, Pa=98000, if_ele=False, num_ele=0.0):
  num_mass = MassNum(ZnAng, Pa=Pa, if_ele=if_ele, num_ele=num_ele)
  print num_mass, math.cos(ZnAng)
  if num_mass < 0:
    num_SolarBeam = 0
  else:
    num_SolarBeam = SP0 * (TAU ** num_mass) * math.cos(ZnAng)
  return num_SolarBeam,num_mass


def SolarDiffRadia(num_SolarBeam, m, TAU=0.7, ):
  if m < 0:
    return 0
  else:
    return num_SolarBeam * 0.300 * (1-TAU ** m)


def SolarRadiationModel(doy, lati_deg, time_cur, time_noon=12, SP0=1360, TAU=0.7, Pa=98000, if_ele=False, num_ele=0.0):
  #time_cur: current time of a day, starting from 0 to 23
  PSI,COS_PSI= ZenithAngle(doy, lati_deg, time_cur, time_noon=time_noon)
  if PSI > math.pi/2.0 and PSI < 0.0:
    pass
  else:
    print PSI, math.pi/2.0
    num_SolarBeam,num_mass = SolarBeamRadia(PSI, SP0=SP0, TAU=TAU, Pa=Pa, if_ele=if_ele, num_ele=num_ele)
    num_SolarDiff = SolarDiffRadia(num_SolarBeam, m=num_mass, TAU=TAU)
    num_TotalSolarRadia = num_SolarBeam + num_SolarDiff
  return num_TotalSolarRadia, num_SolarBeam, num_SolarDiff, PSI
