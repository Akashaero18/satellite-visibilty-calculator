# Ground Station Visibility Calculator

Predicts satellite visibility passes over Bengaluru ground station using Orekit's topocentric frame transformations.

## Overview
Given a satellite TLE and ground station coordinates, calculates when the satellite is visible (elevation > 10°) and 
provides pass details: start time, end time, duration, and maximum elevation.

## Satellites Included
- **ISS** (Low Earth Orbit, approx.420 km)
- **Tiangong** (Chinese Space Station, approx.390 km)

## Output
Pass predictions for 24 hours with:
- Acquisition of Signal (AOS) time
- Loss of Signal (LOS) time
- Pass duration (minutes)
- Maximum elevation angle (degrees)

## Author
Akash K
