from src.Astrolocator import Astrolocator

A=Astrolocator(lon=-9.142685, lat=38.736946, alt=0)
test = A.queryN2YO("33591")
print(A.getAzAlt(test,A.getTime()))