import numpy as np

L_sun = 3.838*10**(26) # solar luminosity, in Watts
AU = 1.496*10**(11)    # 1 astronomical unit, in meters

stars = []
lums = []

with open("main_sequence_data.csv","r") as f:
    file = f.readlines()
    for line in file:
        line = line.split()
        if line[5] != '...':
            stars.append(line[0])
            lums.append(line[5])
            
f.close()

stars = stars[1:]
lums = lums[1:]

while True:
    star = input("Spectral type: ")
    if star in stars:
        lum = lums[stars.index(star)]
        lum = 10**float(lum)
        break
    else:
        print("Spectral type not recognized.")

while True:
    dist = input("Distance to planet (AU) : ")
    try:
        dist = float(dist)
        break
    except:
        print("Improper syntax. Please enter a number")
        
def flux(L,r):
    flux = L*L_sun/(4*np.pi*(r*AU)**2)
    return flux

print("The flux on the planet is "+str(flux(lum,dist))+" W/m^2.")
