from astroquery.simbad import Simbad
from astroquery.jplhorizons import Horizons
from astropy.time import Time

simbad = Simbad()
horizons = Horizons()
simbad.add_votable_fields('allfluxes')
simbad.ROW_LIMIT = 100

result = simbad.query_catalog("GSC")
# Querying without a specific epoch, just to get default data for Mars
obj = horizons(id='499', location='500@10', epochs=Time.now().jd)
ephemerides = obj.ephemerides()
print(ephemerides["V"])



from src.Astrolocator import Astrolocator

A=Astrolocator(lon=-9.142685, lat=38.736946, alt=0)

A.queryBrightObjets()