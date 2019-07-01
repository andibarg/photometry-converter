import os
import numpy as np
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt

'''
Load CIE 1931 eye sensitivity function,
also known as luminousity function (see Wikipedia).
Output is the interpolated function.
'''
def eye_sensitivity():
    # CIE 1931 data array
    eyedata = np.array([[375, 380, 385, 390, 395, 400, 405, 410, 415, 420, 425,
           430, 435, 440, 445, 450, 455, 460, 465, 470, 475, 480,
           485, 490, 495, 500, 505, 510, 515, 520, 525, 530, 535,
           540, 545, 550, 555, 560, 565, 570, 575, 580, 585, 590,
           595, 600, 605, 610, 615, 620, 625, 630, 635, 640, 645,
           650, 655, 660, 665, 670, 675, 680, 685, 690, 695, 700,
           705, 710, 715, 720, 725, 730, 735, 740, 745, 750, 755,
           760, 765, 770, 775, 780, 785, 790, 795, 800, 805, 810,
           815, 820, 825, 830],
           [2.202000e-05, 3.900000e-05, 6.400000e-05, 1.200000e-04,
           2.170000e-04, 3.960000e-04, 6.400000e-04, 1.210000e-03,
           2.180000e-03, 4.000000e-03, 7.300000e-03, 1.160000e-02,
           1.684000e-02, 2.300000e-02, 2.980000e-02, 3.800000e-02,
           4.800000e-02, 6.000000e-02, 7.390000e-02, 9.098000e-02,
           1.126000e-01, 1.390200e-01, 1.693000e-01, 2.080200e-01,
           2.586000e-01, 3.230000e-01, 4.073000e-01, 5.030000e-01,
           6.082000e-01, 7.100000e-01, 7.932000e-01, 8.620000e-01,
           9.148501e-01, 9.540000e-01, 9.803000e-01, 9.949501e-01,
           1.000000e+00, 9.950000e-01, 9.786000e-01, 9.520000e-01,
           9.154000e-01, 8.700000e-01, 8.163000e-01, 7.570000e-01,
           6.949000e-01, 6.310000e-01, 5.668000e-01, 5.030000e-01,
           4.412000e-01, 3.810000e-01, 3.210000e-01, 2.650000e-01,
           2.170000e-01, 1.750000e-01, 1.382000e-01, 1.070000e-01,
           8.160000e-02, 6.100000e-02, 4.458000e-02, 3.200000e-02,
           2.320000e-02, 1.700000e-02, 1.192000e-02, 8.210000e-03,
           5.723000e-03, 4.102000e-03, 2.929000e-03, 2.091000e-03,
           1.484000e-03, 1.047000e-03, 7.400000e-04, 5.200000e-04,
           3.611000e-04, 2.492000e-04, 1.719000e-04, 1.200000e-04,
           8.480000e-05, 6.000000e-05, 4.240000e-05, 3.000000e-05,
           2.120000e-05, 1.499000e-05, 1.060000e-05, 7.465700e-06,
           5.257800e-06, 3.702900e-06, 2.607800e-06, 1.836600e-06,
           1.293400e-06, 9.109300e-07, 6.415300e-07, 4.518100e-07]])

    # Interpolate eye sensitivity function
    return interp1d(eyedata[0,:],eyedata[1,:],
                      kind='cubic',
                      bounds_error=False,
                      fill_value = (0,0))

'''
Gaussian spectral emission function (e.g. approx for a single color LEDs)
cwvl: center wavelength in nm
SBW: spectral bandwidth in nm
N: number of samples
'''
def gauss_emission(cwvl, sbw=20, N=201):
    # Wavelength array
    wvl = np.linspace(cwvl-6*sbw/2,cwvl+6*sbw/2,N)

    # Calculate sigma from FWHM
    sigma = sbw/(2*np.sqrt(2 * np.log(2)))

    # Calculate gaussian function and return
    return np.column_stack([wvl, np.exp(-(wvl-cwvl)**2/(2*sigma**2))])

'''
Lambert's cosine radiation (e.g. approx for LEDs w/o dome)
'''
def lambert():
    # Angle array in rad
    angle = np.linspace(0,np.pi/2,51)

    # Calcualte cosine and return
    return np.column_stack([angle, np.cos(angle)])


'''
Convert luminous flux (in lm) to power in mW. Returns
value in milliwatt.

Inputs
lm: luminous flux in lumen.
specdata: spectral distribution of light source as array
    where specdata[:,0] is the wavelength and specdata[:,1] the
    spectral flux (in a.u.)
'''
def lm2mW(lm, specdata):
    # Convert spectrum data to numpy array
    specdata = np.array(specdata)
    
    # Normalize spectrum data so area is unity
    A = np.trapz(specdata[:,1], specdata[:,0])
    specdata[:,1] /= A

    # Load CIE 1931 eye sensitivity function
    eyeinterp = eye_sensitivity()

    # Integrate normalized spectral luminous flux (W/nm) and convert
    nSLF = specdata[:,1]*eyeinterp(specdata[:,0])
    mW = lm/(683.002*np.trapz(nSLF, specdata[:,0]))*1e3

    return mW

'''
Convert power in mW to luminous flux (in lm). Returns
value in lumen.

Inputs
mW: optical power in milliwatt.
specdata: spectral distribution of light source as array
    where specdata[:,0] is the wavelength and specdata[:,1] the
    spectral flux (in a.u.)
'''
def mW2lm(mW, specdata):
    # Convert spectrum data to numpy array
    specdata = np.array(specdata)
    
    # Normalize spectrum data
    specdata[:,1] /= max(specdata[:,1])

    # Convert to spectral flux/power (W/nm)
    fac = 1e-3*mW/np.trapz(specdata[:,1], specdata[:,0])
    SF = specdata[:,1]*fac

    # Load CIE 1931 eye sensitivity function
    eyeinterp = eye_sensitivity()

    # Integrate spectral luminous flux (W/nm) and convert to lumen
    SLF = SF*eyeinterp(specdata[:,0])
    lm = 683.002*np.trapz(SLF, specdata[:,0])

    return lm

'''
Convert from luminous intensity (in cd)
to luminous flux (in lm). Returns value in lumen.

Inputs
cd: maximum luminous intensity in candela
beamdata: Data of normalized luminous intensity vs
polar angle (0 <= theta <= pi), where beamdata[:,0] is
the angle and beamdata[:,1] the normalized luminous intensity
(in a.u.).
'''
def cd2lm(cd, beamdata):
    # Convert intensity data to numpy array
    beamdata = np.array(beamdata)
    
    # Normalize intensity data
    beamdata[:,1] /= max(beamdata[:,1])

    # Calculate equivalent solid angle
    effomg = 2*np.pi*np.trapz(beamdata[:,1]*np.sin(beamdata[:,0]),
                          beamdata[:,0])

    # Calculate luminous flux and return
    return effomg*cd

'''
Convert from luminous flux (in lm)
to luminous intensity (in cd). Returns value in candela.

Inputs
lm: luminous flux in lumen.
beamdata: Data of normalized luminous intensity vs
polar angle (0 <= theta <= pi), where beamdata[:,0] is
the angle and beamdata[:,1] the normalized luminous intensity
(in a.u.).
'''
def lm2cd(lm, beamdata):
    # Convert intensity data to numpy array
    beamdata = np.array(beamdata)
    
    # Normalize intensity data
    beamdata[:,1] /= max(beamdata[:,1])

    # Calculate equivalent solid angle
    effomg = 2*np.pi*np.trapz(beamdata[:,1]*np.sin(beamdata[:,0]),
                          beamdata[:,0])

    # Calculate luminous intensity and return
    return lm/effomg
    
'''
Simplified conversion from luminous flux (in lm) to
luminous intensity (in cd). Assumes homogenous intensity
across apex angle. Returns value in candela.

Inputs
cd: maximum luminous intensity in candela at the maximum
apexangle: apex angle in degree (2*theta)
'''
def simple_lm2cd(lm, apexangle=120):
    # Calculate solid angle
    effomg = 2*np.pi*(1-np.cos(apexangle/2*np.pi/180))

    # Calculate luminous flux and return
    return lm/effomg

'''
Simplified conversion from luminous intensity (in cd)
to luminous flux (in lm). Assumes homogenous intensity
across apex angle. Returns value in lumen.

Inputs
cd: maximum luminous intensity in candela at the maximum
apexangle: apex angle in degree (2*theta)
'''
def simple_cd2lm(cd, apexangle=120):
    # Calculate solid angle
    effomg = 2*np.pi*(1-np.cos(apexangle/2*np.pi/180))

    # Calculate luminous flux and return
    return cd*effomg


'''
Class object for light source.
'''
class source:
    def __init__(self, **kwargs):
        # Create class attributes
        self.__dict__.update(kwargs)

    # Transfer conversion functions
    def lm2mW(self):
        self.mW = lm2mW(lm=self.lm, specdata=self.specdata)
        return self.mW

    def mW2lm(self):
        self.lm = mW2lm(mW=self.mW, specdata=self.specdata)
        return self.lm

    def cd2lm(self):
        try:
            self.lm = cd2lm(cd=self.cd, angledata=self.angledata)
        except:
            self.lm = simple_cd2lm(cd=self.cd, apexangle=self.apexangle)
        return self.lm

    def lm2cd(self):
        try:
            self.cd = lm2cd(lm=self.lm, angledata=self.angledata)
        except:
            self.cd = simple_lm2cd(lm=self.lm, apexangle=self.apexangle)
        return self.cd




##########################################################
if __name__ == "__main__":
    # Radiant flux in milliwatt
    mW = 827

    # Emission spectrum
    # specdata = np.loadtxt('filename.csv', skiprows = 1,delimiter=',')
    specdata = gauss_emission(cwvl=457,sbw=27)

    # Find luminous flux
    lm = mW2lm(mW, specdata)

    # Plot
    wvl = np.linspace(min(specdata[:,0]),max(specdata[:,0]),301)
    eyeinterp = eye_sensitivity()
    plt.figure(1)
    plt.plot(specdata[:,0],specdata[:,1],'.-',label='Emission spectrum')
    plt.plot(wvl,eyeinterp(wvl),'-',label='Eye sensitivity')
    plt.fill_between(specdata[:,0],specdata[:,1]*eyeinterp(specdata[:,0]),
                     color='gray',label='Integrated area')
    plt.legend(loc='upper right')
    plt.title('Result: %.2f mW --> %.2f lm' %(mW, lm))
    plt.ylabel('Normalized spectrum')
    plt.xlabel('Wavelength (nm)')

    # Normalized luminous intensity vs polar angle
    # beamdata = np.loadtxt(anglepath, skiprows = 1,delimiter=',')
    beamdata = lambert()

    # Find luminous intensity
    cd = lm2cd(lm, beamdata)

    # Plot
    plt.figure(2)
    plt.plot(beamdata[:,0]*180/np.pi,beamdata[:,1],'.-',label='Beam profile')
    plt.fill_between(beamdata[:,0]*180/np.pi,beamdata[:,1]*np.sin(beamdata[:,0]),
                     color='gray',label='Integrated area')
    plt.title('Result: %.2f lm --> %.2f cd' %(lm, cd))
    plt.legend(loc='upper right')
    plt.ylabel('Relative lumimous intensity')
    plt.xlabel('Angle (degree)')
    plt.show()
