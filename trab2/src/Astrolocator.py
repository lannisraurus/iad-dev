"""
Grupo I, IAD, 2025
João Camacho, Duarte Tavares, Margarida Saraiva, Jorge Costa

This file contains various methods to interface with the astroquery
and astropy libraries, in order to get azimuths and altitude angles
of objects, in order to point at them in the sky.

"""
### Imports

from astroquery.simbad import Simbad
from astroquery.jplhorizons import Horizons

import requests
import os

import astropy
from astropy import coordinates as coord
from astropy import units as u
from astropy.coordinates import EarthLocation, AltAz
from astropy.time import Time
import astropy.table

### Class
class Astrolocator():
    
    # Constructor
    def __init__(self, lat=90, lon=0, alt=0):
        # Using SIMBAD database
        Simbad.TIMEOUT = 500
        self.observer = EarthLocation.from_geodetic(lat=lat, lon=lon, height=alt)

    # Updates observers position on Earth
    def updateObserver(self, lat=90, lon=0, alt=0):
        self.observer = EarthLocation.from_geodetic(lat=lat, lon=lon, height=alt)

    # Returns astropy Time object with current time
    def getTime(self):
        return Time.now()

    # Returns an astropy table of the given object. If fails returns None
    def querySimbad(self, identifier):
        simbadData = Simbad()
        simbadData.add_votable_fields("flux(V)")
        result = simbadData.query_object(identifier)
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
        result = Horizons(id=identifier, location=location)
        try:
            result = result.ephemerides()
        except:
            return None
        result.rename_column("targetname", "Name")
        result["Name"].unit = None
        result["Name"] = result["Name"].astype(str)
        result = result[["Name", "RA", "DEC", "V"]]
        return result
    
    def queryN2YO(self, identifier):
        # Your N2YO API key
        api_key = os.getenv("N2YO_API_KEY")
        if not api_key:
            raise ValueError("Missing N2YO API key in environment variable N2YO_API_KEY")
        
        # Export N2YO_API_KEY="L9NPLA-JM7B6C-DG46RL-5GE8"

        # The NORAD satellite ID
        sat_id = identifier  

        # Observer's latitide in decimal degrees
        lat = str(self.observer.lat.value)

        # Observer's longitude in decimal degrees
        lon = str(self.observer.lon.value)

        # Observer's altitude above sea level in meters
        alt = str(self.observer.height.value)

        # Number of satellite positions to return 
        #(Each position for each further second with limit 300 seconds)
        count = '1' # Return positions for current time only

        # Make the API request
        response = requests.get(url = ("https://api.n2yo.com/rest/v1/satellite/positions/" + sat_id+ '/' + lat + '/' + lon + '/' + alt + '/' + count + '/' + "&apiKey=" + api_key))

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            data = response.json()
            
            # Print the response data (satellite position and other details)
            print(data)
            print(data['positions'][0]['azimuth'], data['positions'][0]['elevation'])
            obj = dict()
            obj["Name"] = [data['info']['satname']]
            obj["RA"] = [data['positions'][0]['ra']]
            obj["DEC"] = [data['positions'][0]['dec']]
            result = astropy.table.Table(obj)
            print(result)
            return result
        else:
            print(f'Error: {response.status_code}')
            return None
            
    # Returns an astropy table of brigthest objects in the sky
    def queryBrightObjects(self, magnitude_threshold=0):
        simbadData = Simbad()
        simbadData.add_votable_fields("flux(V)")
        # ADQL query string with magnitude threshold
        brigthCriteria = f"V < {magnitude_threshold}"

        # Query the GC catalog for the brightest stars
        bright_stars = simbadData.query_catalog("GC", criteria=brigthCriteria)
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