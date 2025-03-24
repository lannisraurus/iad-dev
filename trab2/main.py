##################### User defined classes/functions
from src.Astrolocator import Astrolocator

##################### Main Programme Function

if __name__ == '__main__':
    astrolocator = Astrolocator()
    AzAlt = astrolocator.getAnglesInSky('Sirius', 38.73557900984156, -9.139868411420947, 100.00)
    print(AzAlt)
