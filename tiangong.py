import orekit
vm = orekit.initVM()

from orekit.pyhelpers import setup_orekit_curdir
setup_orekit_curdir()

from org.orekit.propagation.analytical.tle import TLE, TLEPropagator
from org.orekit.frames import FramesFactory, TopocentricFrame
from org.orekit.bodies import OneAxisEllipsoid, GeodeticPoint
from org.orekit.utils import IERSConventions, Constants
from math import radians, pi

#Tiangong's TLE (NORAD ID: 48274)
tia1 = "1 48274U 21035A   26171.43213816  .00020661  00000+0  24268-3 0  9990"
tia2 = "2 48274  41.4693 302.2526 0007384 105.8714 254.2939 15.60937952293670"
tiatle = TLE(tia1,tia2)

#Coordinate system        
ITRF = FramesFactory.getITRF(IERSConventions.IERS_2010,True)
earth = OneAxisEllipsoid(Constants.WGS84_EARTH_EQUATORIAL_RADIUS,
                         Constants.WGS84_EARTH_FLATTENING,ITRF)

#Ground Station
lat = radians(12.9716)
long = radians(77.5946)
alt = 920.0  #In m
station = GeodeticPoint(lat,long,alt)
stationframe = TopocentricFrame(earth,station,"Esrange")

#prop the TLE
tia_prop = TLEPropagator.selectExtrapolator(tiatle)

#Duration for Visibility Check
startdate = tiatle.getDate()
enddate = startdate.shiftedBy(24.0 * 60.0 * 60.0 )

print (f"Propagating from '{startdate}' to '{enddate}'")

#Check Visibility
currentdate = startdate
in_pass = False
pos = 0
track_start_time = []
track_end_time = []
max_elev = 0
pass_max_elev = 0
passes = []

while (currentdate.compareTo(enddate)<= 0):
    state = tia_prop.propagate(currentdate)
    pv = state.getPVCoordinates(stationframe)
    pos = pv.getPosition()

    elev_calc = (pos.getDelta()) * (180.0/(pi))
    if elev_calc > 10.0:
        if not in_pass:
            in_pass = True
            pass_start = currentdate
            pass_max_elev =max(pass_max_elev,elev_calc)
    else:
        if in_pass:
            passes.append((pass_start,currentdate,pass_max_elev))
            in_pass = False
            pass_max_elev = 0
    currentdate = currentdate.shiftedBy(10.0)

#Printing No. of passes
print(f"Found {len(passes)} passes over Bengaluru in 24 hrs! \n")

for i, (start,end, max_elev) in enumerate(passes):
    duration_sec = end.durationFrom(start)
    duration_min = duration_sec / 60.0
    print(f"Pass {i+1}: {start} to {end}")
    print(f"  Duration: {duration_min:.f} mins, Max Elevation: {max_elev:.1f}deg\n")
print("COOL")