"""
Grupo I, IAD, 2025
João Camacho, Duarte Tavares, Margarida Saraiva, Jorge Costa

This file contains various methods to interface with the astroquery
and astropy libraries, in order to get azimuths and altitude angles
of objects, in order to point at them in the sky.

"""
### Imports
from astroquery.simbad import Simbad
from astropy import coordinates as coord
from astropy import units as u
from astropy.coordinates import EarthLocation, AltAz
from astropy.time import Time

### Class
class Astrolocator():
    # Constructor
    def __init__(self):
        # Using SIMBAD database
        Simbad.TIMEOUT = 500
        self.database = Simbad()
    
    # Get (azimuth, altitude) angles in 2tuple.
    def getAnglesInSky(self, name, Lat, Lon, Alt):
        # Get dataframe
        result = self.database.query_object(name)
        # Extract Right Ascension (RA) and Declination (Dec)
        ra = result['ra'][0]
        dec = result['dec'][0]
        # Observer's location
        observer = EarthLocation.from_geodetic(Lon, Lat, Alt)
        # Observation time
        obsTime = Time.now()
        # SkyCoord object
        objectCoords = coord.SkyCoord(ra, dec, unit=(u.hourangle, u.deg), frame='icrs')
        # Convert
        altazFrame = AltAz(obstime=obsTime, location=observer)
        altazCoords = objectCoords.transform_to(altazFrame)
        # Result
        return (float(altazCoords.az.value), float(altazCoords.alt.value))

    # Get a comprehensive list of objects from simbad according to various filters
    def getFilteredObjectList():
        return
