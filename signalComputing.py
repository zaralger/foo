from math import *
import cmath

tau = 2*pi

#
# > Digital Signal Processing
#

# inspired by https://greatscottgadgets.com/sdr/7/
# average of a list of degree angles
def degreeAverage(degreeList):
	base = e**(1j*tau/360)
	total = 0
	for r in degreeList: 
		total += base ** r
	result = total / len(degreeList)
	return cmath.log(result, base).real

print degreeAverage([12,320,54])