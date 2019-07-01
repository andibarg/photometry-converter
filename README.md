# photometry-converter
Converts between photometric and radiometric units. Supports luminous intensity (in candela), lumious flux (in lumen) and radiant flux/optical power (in milliwatt). Takes into account the spectral emission and radiation characteristics of a light source.

### Installation
```
$ git clone https://github.com/andibarg/photometry-converter.git
$ cd photometry-converter
```

### Usage
The following example code converts from milliwatt to lumen to candela. The spectrum is a gaussian peak around 457nm with a bandwith of 27nm. The beam profile is according to Lambert's cosing law.
```
import photometry_converter as pc

# Emission spectrum and profile
specdata = pc.gaus_emission(cwvl=457,sbw=27)
beamdata = lambert()

# Find luminous flux
lm = mW2lm(mW, specdata)

# Find luminous intensity
cd = lm2cd(lm, angledata)
```
