# photometry-converter
Converts between photometric and radiometric units. Supports luminous intensity (in candela), lumious flux (in lumen) and radiant flux/optical power (in milliwatt). Takes into account the spectral emission and radiation characteristics of a light source.

### Installation
```
$ git clone https://github.com/andibarg/photometry-converter.git
$ cd photometry-converter
```

### Usage
The following example code converts from milliwatt to lumen to candela. The spectrum is a gaussian peak around 457 nm with a bandwith of 27 nm. The beam profile is according to Lambert's cosing law.
```
import photometry_converter as pc

# Radiant flux in milliwatt
mW = 827

# Emission spectrum and profile
specdata = pc.gauss_emission(cwvl=457,sbw=27)
beamdata = pc.lambert()

# Find luminous flux
lm = pc.mW2lm(mW, specdata)

# Find luminous intensity
cd = pc.lm2cd(lm, beamdata)
```
Alternatively, you can create a class instance. In the following example the beam profile is specified via the apexangle:
```
import photometry_converter as pc

# Create class instance
led = pc.source(name = 'Blue LED',
                mW = 827,
                specdata = pc.gauss_emission(cwvl=457,sbw=27),
                apexangle = 120)
                
# Convert units
led.mW2lm()
led.lm2cd()

# Find luminous flux
led.lm

# Find luminous intensity
led.cd
```
