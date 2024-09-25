## Script Name: ecef_to_sez.py

## Usage: python3 ecef_to_sez.py o_x_km o_y_km o_z_km x_km y_km z_km

## Parameters:
# o_x_km: Origin x-magnitude, in kilometers
# o_y_km: Origin y-magnitude, in kilometers
# o_z_km: Origin z-magnitude, in kilometers
# x_km: X-magnitude, in kilometers
# y_km: Y-magnitude, in kilometers
# z_km: Z-magnitude, in kilometers

## Output: Converts given ECEF-vector into the equivalent SEZ-vector

## Written by Carl Hayden
# Other Contributors: Professor Brad Denby

## Importing Libraries
import math # Importing Mathematics Library
import sys # Importing Argument-Reading Library
import numpy # Importing numpy Library (matrix math!)

## Defining Constants
R_Earth = 6378.1363 # Radius of Earth in km
e_Earth = 0.081819221456 # Eccentricity of Earth

## Defining Other Dependent Functions
def calc_denom(ecc,lat_rad):
    return math.sqrt(1.0 - ecc ** 2.0 * math.sin(lat_rad) ** 2.0)

## Initialize Script Arguments
o_x_km = float('nan') # Original x-magnitude, in kilometers
o_y_km = float('nan') # Original y-magnitude, in kilometers
o_z_km = float('nan') # Original z-magnitude, in kilometers
x_km = float('nan') # X-magnitude, in kilometers
y_km = float('nan') # Y-magnitude, in kilometers
z_km = float('nan') # Z-magnitude, in kilometers

## Parse Script Arguments
if len(sys.argv)==7:
    o_x_km = float(sys.argv[1])
    o_y_km = float(sys.argv[2])
    o_z_km = float(sys.argv[3])
    x_km = float(sys.argv[4])
    y_km = float(sys.argv[5])
    z_km = float(sys.argv[6])

else:
    print(\
        'Usage: '\
        'python3 ecef_to_sez.py o_x_km o_y_km o_z_km x_km y_km z_km'\
    )
    exit()

## Main Script
# Converting to normal vector, not offset because of origin
NewX_km = x_km-o_x_km
NewY_km = y_km-o_y_km
NewZ_km = z_km-o_z_km


# START - Code Utilized from In-Class Example from Professor Denby...
lon_rad = math.atan2(y_km,x_km)
lon_deg = lon_rad*180.0/math.pi

lat_rad = math.asin(z_km/math.sqrt(x_km**2+y_km**2+z_km**2))
r_lon_km = math.sqrt(x_km**2+y_km**2)
prev_lat_rad = float('nan')

c_E = float('nan')
count = 0
while (math.isnan(prev_lat_rad) or abs(lat_rad-prev_lat_rad)>10e-10):
  denom = calc_denom(e_Earth,lat_rad)
  c_E = R_Earth/denom
  prev_lat_rad = lat_rad
  lat_rad = math.atan((z_km+c_E*(e_Earth**2)*math.sin(lat_rad))/r_lon_km)

hae_km = r_lon_km/math.cos(lat_rad)-c_E

# END - Code Utilized from In-Class Example from Professor Denby...

LLH_Vect = numpy.array([[NewX_km], [NewY_km], [NewZ_km]])

Rotation1 = numpy.array([[math.sin(lat_rad), 0, -math.cos(lat_rad)], 
             [0, 1, 0], 
             [math.cos(lat_rad), 0, math.sin(lat_rad)]])
Rotation2 = numpy.array([[math.cos(lon_rad), math.sin(lon_rad), 0],
             [-math.sin(lon_rad), math.cos(lon_rad), 0],
             [0, 0, 1]])

Calc1 = numpy.dot(Rotation2, LLH_Vect)
Calc2 = -numpy.dot(Rotation1, Calc1)

s_km = str(numpy.extract(1,Calc2[[0]]))
e_km = str(numpy.extract(1,Calc2[[1]]))
z_km = str(numpy.extract(1,Calc2[[2]]))

print(s_km)
print(e_km)
print(z_km)