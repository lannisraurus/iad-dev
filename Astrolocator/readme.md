
# IAD - Project II - Astrolocator

**Duarte Tavares [105920], João Camacho [106224], Jorge Costa [106891], Margarida Saraiva [106994]**  
**2025**

---

## 1. Introduction

This project’s main goal is to read data transmitted by satellites broadcasting HRPTs (High Resolution Picture Transmission), such as NOAA-15, NOAA-19, Metop-C, or Meteor-M N2-3 [6], using a tracking system (which could also be used to follow celestial bodies like stars and planets). The work is divided into three main parts: the tracking system and protocol, the data acquisition and reading system, and the user interface required to access these features.

---

## 2. Tracking System

The tracking system setup (created using Tinkercad [7]) consists of a support platform with gear wheels [8] driven by RB-Moto2 Joy-IT stepper motors [9]. These were designed to allow finer angular movements (gear ratio of 32), which is especially useful for tracking celestial objects. These motors are controlled by a Raspberry Pi, accessed remotely via a connected computer. The Raspberry Pi also contains the user interface, motor control system, and camera data reading module (an optional accessory) [10].

The base supports a primary axis with full angular rotation and can be fitted with two accessories:

- A Raspberry Pi Camera Module 2 with a crosshair, mainly for easier initial alignment using celestial object positions [10].
- A laser pointer mount [11] for real-time satellite tracking, helping the operator keep the data source in sight.

Tracking is handled using two Python libraries:

- `astroquery` [12] to retrieve planetary positions from JPL Horizons and star data from Simbad,
- `N2YO API` [13] to get satellite positions.

To align the system with the angular map of celestial object positions, the user selects an alignment option (1-point or N-points, N ≥ 3). The program requires system coordinates (latitude, longitude, altitude) and suggests the 10 brightest visible celestial bodies for alignment. Users may select another object if necessary (e.g., due to atmospheric conditions). After manual selection using movement controls, the system is aligned and ready for tracking (it's recommended to switch from the camera to the laser accessory).

There’s also a routine that limits the apparatus’ angles to prevent cable breakage or mechanical constraints.

---

## 3. Data Acquisition System

For data acquisition, we built a satellite antenna setup based on [14] to receive meteorological satellite transmissions.

The antenna is connected via an improvised coaxial cable to an RTL-SDR module [15], which converts the antenna’s analog signal into a digital one using a Fourier transform. This digital signal can be converted into an image according to each satellite’s communication protocol.

For simplicity, the RTL-SDR was connected to another computer using open-source software [16], freeing up the Raspberry Pi’s resources and making analysis faster (since programming signal conversion for each satellite would be time-consuming).

Files are often large (approx. 8 GB for 4 minutes), so it is more practical to perform acquisition on the same laptop that controls the Raspberry Pi remotely.

---

## 4. User Interface

The interface includes a main window and several secondary windows:

**Main window components:**

- Presentation image
- Log box to notify users of current processes, keep records, and communicate with the user
- Text input line for user commands (mainly for alignment, tracking, and angle limitation)
- Buttons to control the laser and move motors, plus a slider to adjust the motor step delay
- Buttons to start alignment, tracking, and angle-limiting routines
- Button to open the camera image viewer
- Buttons to open configuration windows for:
  - Steppers
  - Other settings (laser)
  - Location (system coordinates)

**Stepper configuration window**:  
Allows changing the stepper model, gear ratio, and Raspberry Pi pin sequence [9].

**Other settings window**:  
Allows selecting the Raspberry Pi pin used to control the laser [11].

**Coordinates window**:  
Allows editing latitude, longitude, and altitude, and updating these values.

**Camera window**:  
Displays the camera feed, includes a button to capture an exposure image, and a slider for exposure time.

---

## 5. Problems and Suggestions

The original plan was to mount a Newtonian telescope instead of a camera or laser. However, we couldn’t find a primary mirror with a focal length suitable for the structure. So we reused the camera for alignment and the laser for pointing during tracking.

The data acquisition antenna was also intended to be mounted on the tracking system. However, the 3D-printed support was too fragile (one of the main axes broke during testing). While the motors could move the antenna, structural issues and lack of time led us to abandon that plan.

The code was written to be as general as possible to allow quick adaptation to different setups, especially the originally intended one.

**Suggestions for future improvements:**

- **Antenna**:  
  - Joints were taped due to potential disassembly needs; future versions should glue them.
  - Add a low-noise amplifier and signal filter for cleaner signal/image extraction (not done due to budget) [14].

- **Telescope**:  
  - Use a concave mirror with a 15–30 cm focal length and a small flat mirror to build a Newtonian telescope accessory.

- **Support Structure**:  
  - Reprinting a sturdier support would allow mounting the antenna directly on the tracking system.

---

## 6. Conclusions

We conclude that the Raspberry Pi is a strong candidate for building instrumentation systems for amateur astronomers. This project provided a solid software base applicable to multiple data acquisition projects.

---

## References

1. [PyQt documentation](https://doc.qt.io/qtforpython-5/contents.html)  
2. [pyqtgraph documentation](https://pyqtgraph.readthedocs.io/en/latest/index.html)  
3. [pyserial documentation](https://pyserial.readthedocs.io/en/latest/)  
4. [Arduino language reference](https://docs.arduino.cc/language-reference/)  
5. [KiCad EDA Suite](https://www.kicad.org/)  
6. [High Resolution Picture Transmission (HRPT)](https://www.noaasis.noaa.gov/POLAR/HRPT/hrpt.html)  
7. [TinkerCad](https://www.tinkercad.com/)  
8. [Gear generator](https://www.stlgears.com/)  
9. [RB-Moto2 Steppers + Controllers](https://joy-it.net/en/products/RB-Moto2)  
10. [Raspberry Pi Camera Module 2](https://www.raspberrypi.com/products/camera-module-v2/)  
11. [Laser module](https://mauser.pt/catalog/product_info.php?products_id=096-7909)  
12. A. Ginsburg et al. "astroquery: An Astronomical Web-querying Package in Python". *Astronomical Journal*, vol. 157, p. 98, Mar. 2019. [DOI:10.3847/1538-3881/aafc33](https://doi.org/10.3847/1538-3881/aafc33), [arXiv:1901.04520](https://arxiv.org/abs/1901.04520)  
13. [N2YO API](https://www.n2yo.com/api/)  
14. [1.7 GHz HRPT Helicone Antenna by t0nito](https://www.thingiverse.com/thing:6436342)  
15. [RTL-SDR](https://www.rtl-sdr.com/)  
16. [SDR++ Software](https://www.sdrpp.org/)
