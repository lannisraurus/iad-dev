"""
Grupo I, IAD, 2025
João Camacho, Duarte Tavares, Margarida Saraiva, Jorge Costa

This file contains various methods to interface with the astroquery
and astropy libraries, in order to get azimuths and altitude angles
of objects, in order to point at them in the sky.

"""
### Imports
import astropy.table
from astroquery.simbad import Simbad
from astroquery.jplhorizons import Horizons
import astropy
from astropy import coordinates as coord
from astropy import units as u
from astropy.coordinates import EarthLocation, AltAz
from astropy.time import Time

### Class
class Astrolocator():
    
    # Constructor
    def __init__(self, lat=90, lon=0, alt=0):
        # Using SIMBAD database
        Simbad.TIMEOUT = 500
        self.simbadData = Simbad()
        self.simbadData.add_votable_fields("allfluxes")
        self.observer = EarthLocation.from_geodetic(lat=lat, lon=lon, height=alt)

    # Updates observers position on Earth
    def updateObserver(self, lat=90, lon=0, alt=0):
        self.observer = EarthLocation.from_geodetic(lat=lat, lon=lon, height=alt)

    # Returns astropy Time object with current time
    def getTime(self):
        return Time.now()

    # Returns an astropy table of the given object. If fails returns None
    def querySimbad(self, identifier):
        result = self.simbadData.query_object(identifier)
        if result is None or len(result) == 0 or "ra" not in result.colnames or "dec" not in result.colnames:
            return None
        result.rename_column("ra", "RA")
        result.rename_column("dec", "DEC")
        result.rename_column("main_id", "Name")
        result["V"].unit = u.mag 
        result["Name"] = result["Name"].astype(str)
        result = result[["Name", "RA", "DEC", "V"]]

        return result

    def queryHorizons(self,identifier):
        location = {"lon": self.observer.lon.value,
            "lat": self.observer.lat.value,
            "elevation": self.observer.height.value,
            "body": "399"}
        result = Horizons(id=identifier, location=location).ephemerides()
        if result is None or len(result) == 0 or "RA" not in result.colnames or "DEC" not in result.colnames:
            return None
    
        result.rename_column("targetname", "Name")
        result["Name"].unit = None
        result["Name"] = result["Name"].astype(str)
        result = result[["Name", "RA", "DEC", "V"]]
        return result

            
    # Returns an astropy table of brigthest objects in the sky
    def queryBrightObjects(self, magnitude_threshold=0):
        # ADQL query string with magnitude threshold
        brigthCriteria = f"V < {magnitude_threshold}"

        # Query the GC catalog for the brightest stars
        bright_stars = self.simbadData.query_catalog("GC", criteria=brigthCriteria)
        # Clean up table
        bright_stars.rename_column("ra", "RA")
        bright_stars.rename_column("dec", "DEC")
        bright_stars.rename_column("main_id", "Name")
        bright_stars["V"].unit = u.mag 
        bright_stars["Name"] = bright_stars["Name"].astype(str)
        bright_stars = bright_stars[["Name", "RA", "DEC", "V"]]
        
        bright_objects = bright_stars
        planetsIdsHorizons = ["199","299","499","599","699","799","899","999"]
        location = {"lon": self.observer.lon.value,
            "lat": self.observer.lat.value,
            "elevation": self.observer.height.value,
            "body": "399"}
        for id in planetsIdsHorizons:
            planet = Horizons(id=id, location=location).ephemerides()
            planet.rename_column("targetname", "Name")
            planet["Name"].unit = None
            planet["Name"] = planet["Name"].astype(str)
            planet = planet[["Name", "RA", "DEC", "V"]]
            if planet["V"] < magnitude_threshold: 
                bright_objects = astropy.table.vstack([bright_objects, planet])

        bright_objects = bright_objects.group_by("V")

        bright_objects_in_sky = None
        for obj in bright_objects:
            objectCoords = coord.SkyCoord(ra=obj["RA"], dec=obj["DEC"], unit="deg", frame="icrs")
            # Convert to AltAz frame of self.observer
            altazFrame = AltAz(obstime=self.getTime(), location=self.observer)
            altazCoords = objectCoords.transform_to(altazFrame)
            if altazCoords.alt.value > 0:
                if bright_objects_in_sky is None:
                    bright_objects_in_sky = astropy.table.Table(obj)
                else:
                    bright_objects_in_sky.add_row(obj)
            
        return bright_objects_in_sky

    
    # Get 2tuple (azimuth, altitude) angles 
    def getAzAlt(self, object, time):
        # Extract Right Ascension (RA) and Declination (Dec)
        ra = object["RA"]
        dec = object["DEC"]
        # SkyCoord object
        objectCoords = coord.SkyCoord(ra, dec, unit="deg", frame="icrs")
        # Convert to AltAz frame of self.observer
        altazFrame = AltAz(obstime=time, location=self.observer)
        altazCoords = objectCoords.transform_to(altazFrame)
        # Result
        return (float(altazCoords.az.value), float(altazCoords.alt.value))

