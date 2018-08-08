import numpy as np
import matplotlib.cm as cm
import matplotlib.pyplot as plt

# solar luminosity
L_sun = 3.838*10**(26)

stars = []
lums = []

# parsing the file containing stellar parameters for main sequence stars
with open("main_sequence_data.csv","r") as f:
    file = f.readlines()
    for line in file:
        line = line.split()
        if line[5] != '...':
            stars.append(line[0]) # spectral type
            lums.append(line[5])  # luminosity of spectral type

f.close()

# remove headings
stars = stars[1:]
lums = lums[1:]

star_lum = []

# For spectral types, use "V" at the end to indicate that the star
# is on the main sequence. For instance, use "G2V", not "G2". More
# choices may be added in the future.
while True:
    star_1 = input("Spectral type of component A: ")
    if star_1 in stars:
        star_lum.append(lums[stars.index(star_1)])
        break
    else:
        print("Spectral type not recognized.")
while True:
    star_2 = input("Spectral type of component B: ")
    if star_2 in stars:
        star_lum.append(lums[stars.index(star_2)])
        break
    else:
        print("Spectral type not recognized.")
while True:
    separation = input("Binary separation (AU): ")
    try:
        separation = float(separation)
        break
    except:
        print("Improper syntax. Please enter a number.")
while True:
    albedo = input("Planetary albedo: ")
    try:
        albedo = float(albedo)
        if 0 <= albedo and albedo <= 1:
            break
        else:
            print("Albedo should be between 0 and 1.")
    except:
        print("Improper syntax. Please enter a number.")

star_lum = [10**(float(lum))*L_sun for lum in star_lum]

def temp(i,j,mode=None):
    """Calculates the effective temperature of a planet at particular coordinates.
    
    Inputs:
    i (float) - x-coordinate of planet
    j (float) - y-coordinate of planet
    
    Outputs:
    T (float)
    
    Notes:
    If no argument is given for mode, the function determines whether or not the
    planet is in the circumstellar habitable zone of the system. If mode is set
    to 'temperature', the function explicitly returns the temperature at that point.
    
    """
    star_x = [0, 0]
    star_y = [-float(separation)/2,float(separation)/2]
    
    flux = 0
    
    for m in range(0,2):
        # scale coordinates in AU
        x = i*1.496*10**(11)
        y = j*1.496*10**(11)
        x_star = star_x[m]
        y_star = star_y[m]*1.496*10**(11)
        
        # distance from each star to the point
        diff_x = np.abs(x_star - x)
        diff_y = np.abs(y_star - y)
        dist = np.sqrt(diff_x**2 + diff_y**2)

        L = star_lum[m]
        
        # the flux from a given star
        flux += L/(4*np.pi*dist**2)
        
    sig = 5.67*10**(-8) # stefan-boltzmann constant
    
    # effective temperature
    T = (flux*(1-albedo)/(4*sig))**(1/4)
    T[T>1000] = 1000 # cut this off to avoid singularities
    
    if mode == None:
        # 2 if habitable, 0 if uninhabitable 
        return np.sign(T-273.15)*np.sign(373.13-T) + 1
    elif mode == 'temperature':
        return T

# default grid is 10 AU x 10 AU
x = np.arange(-5, 5, 0.01)
y = np.arange(-5, 5, 0.01)
X, Y = np.meshgrid(x, y)
Z = temp(X, Y)

# cmap=cm.RdYlGn
plt.imshow(Z, interpolation='bilinear', cmap=cm.Greys, origin='center',
                vmax=abs(Z).max(), vmin=-abs(Z).max())
plt.xlabel("$x$ ($10^{-4}$ AU)")
plt.ylabel("$y$ ($10^{-4}$ AU)")
plt.title(str(star_1) + " + " + str(star_2) + ", " + str(separation) + " AU separation")
plt.show()