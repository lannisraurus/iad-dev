from src.Astrolocator import Astrolocator

A=Astrolocator(lon=-9.142685, lat=38.736946, alt=0)
sir = A.querySimbad("Sirius")
print(sir,'\n')
print(A.getAzAlt(sir,A.getTime()),'\n')
#A.queryBrightObjects(2)
maam = A.querySimbad("* alf Ori")
print(maam,'\n')

maam = A.querySimbad("Sirius")
print(maam,'\n')