import orekit
vm = orekit.initVM()

from orekit.pyhelpers import setup_orekit_curdir
setup_orekit_curdir()

from org.orekit.frames import FramesFactory, TopocentricFrame
from org.orekit.bodies import OneAxisEllipsoid, GeodeticPoint
from org.orekit.time import TimeScalesFactory, AbsoluteDate, DateComponents, TimeComponents
from org.orekit.utils import IERSConventions, Constants
from org.orekit.propagation.analytical.tle import TLE, TLEPropagator
from math import radians, pi

#Earth Coordinatee System
ITRF = FramesFactory.getITRF(IERSConventions.IERS_2010, True)
earth = OneAxisEllipsoid(Constants.WGS84_EARTH_EQUATORIAL_RADIUS, Constants.WGS84_EARTH_FLATTENING, ITRF)

#Ground Station (Bengaluru)
lat = radians(12.9716)
long = radians(77.5946)
alt = 920.0
station = GeodeticPoint(lat, long, alt)
sta1Frame = TopocentricFrame(earth, station, "Bengaluru")

#International Space Station's TLE
iss_tle1 = "1 25544U 98067A   26169.80206885  .00008155  00000+0  15439-3 0  9994"
iss_tle2 = "2 25544  51.6331 292.1003 0004667 202.2920 157.7867 15.49302471572009"

#Propagating the TLE
ISS_tle = TLE(iss_tle1,iss_tle2)
ISS_prop = TLEPropagator.selectExtrapolator(ISS_tle)

#No. Of Days
startdate = ISS_tle.getDate()
enddate = startdate.shiftedBy(24.0 * 3600.0) #24 hours

print(f"Propagating from {startdate} to {enddate}")

currentdate = startdate
pos = []
max_elev = 0
in_pass = False
pass_max_elev = 0
passes = []

while (currentdate.compareTo(enddate)<=0) :
    
    state = ISS_prop.propagate(currentdate)
    pv = state.getPVCoordinates(sta1Frame)
    pos = pv.getPosition()


    elev_calc = (pos.getDelta()) * (180.0 / (pi))
    if elev_calc > 10.0:
        if not in_pass:
            in_pass = True
            pass_start = currentdate
        pass_max_elev = max(pass_max_elev, elev_calc)
    else:
        if in_pass:
            passes.append((pass_start, currentdate, pass_max_elev))
            in_pass = False
            pass_max_elev = 0
    currentdate = currentdate.shiftedBy(60.0)

print(f"\nFound {len(passes)} passes over Bengaluru in 24 hours\n")
for i, (start, end, max_elev) in enumerate(passes):
    duration_sec = end.durationFrom(start)
    duration_min = duration_sec / 60.0
    print(f"Pass {i+1}: {start} to {end}")
    print(f"  Duration: {duration_min:.1f} mins, Max Elevation: {max_elev:.1f}deg\n")