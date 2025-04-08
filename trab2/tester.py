from src.Astrolocator import Astrolocator

A=Astrolocator(lon=-9.142685, lat=38.736946, alt=0)
sir = A.querySimbad("Sirius")
print(sir)
A.getAzAlt(sir,A.getTime())
A.queryBrightObjets(2)