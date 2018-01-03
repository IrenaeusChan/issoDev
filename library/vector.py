"""
Irenaeus Chan
11/27/2015

Math Calculations Required for Protein Analysis
"""

from __future__ import division
import numpy as np
import math
from decimal import *

def vectorCalculation(coord1, coord2):
#Converts the coordinates for the atoms into a vector between the two atoms representing the "bond"
	return [coord2[0]-coord1[0], coord2[1]-coord1[1], coord2[2]-coord1[2]]

def crossProduct(vector1, vector2):
	x = vector1[1]*vector2[2] - vector1[2]*vector2[1]
	y = vector1[2]*vector2[0] - vector1[0]*vector2[2]
	z = vector1[0]*vector2[1] - vector1[1]*vector2[0]
	return [x,y,z]

def dotProduct(vector1, vector2):
	return vector1[0] * vector2[0] + vector1[1] * vector2[1] + vector1[2] * vector2[2]

def vectorMagnitude(vector):
	return ((vector[0])**2 + (vector[1])**2 + (vector[2])**2)**0.5

def normalize(vector):
	return [vector[0]/vectorMagnitude(vector), vector[1]/vectorMagnitude(vector), vector[2]/vectorMagnitude(vector)]

def dihedralAngle(normalVector1, normalVector2):
	return math.degrees(math.acos(dotProduct(normalVector1, normalVector2)/(vectorMagnitude(normalVector1) * vectorMagnitude(normalVector2))))

def signedAngle(vector1, vector2):
	return math.degrees(math.atan2(vectorMagnitude(crossProduct(vector1, vector2)), dotProduct(vector1, vector2)))
	
def orthogonalDistanceRegression(listOfCoord):
#Original code by @dwf from http://stackoverflow.com/questions/2298390/fitting-a-line-in-3d
#Edited and changed accordingly by Irenaeus Chan
	data = np.array(listOfCoord)			#As long as the list of coordinates is [[x, y, z], [x, y, z], [x, y, z]]
	mean = data.mean(axis=0)				#Calculate the mean of the points, i.e. the "center" of the cloud
	uu, dd, vv = np.linalg.svd(data-mean)	#Do an SVD on the mean-centered data

	#According to @dwf
	#vv[0] contains the first principal component, i.e. the direction vector of the "best fit" line
	#Therefore in order to generate two points on the line, we will take the vector and extrapolate
	# a set amount of distance ahead and behind the vector (vector projection)
	# ---------------------------------------------------------------------------------------------
	#This means np.mgrid creates a matrix that contains the distance away from the central cloud
	# we reorganize that matrix into a single vertical array using the np.newaxis function on the
	# whole array
	pointsOnLine = vv[0] * np.mgrid[-50:50:2j][:, np.newaxis]	
	#The -50:50 accounts for a rough spread of how far the start and stop atoms are from each 
	# other, the distance was eyeballed using R statistical software and is arbitrary
	pointsOnLine += mean
	pointsOnLine = pointsOnLine.tolist()
	regressionVector = vectorCalculation(pointsOnLine[0], pointsOnLine[1])
	#regressionVector = vectorCalculation([decimal.Decimal(pointsOnLine[0][0]), decimal.Decimal(pointsOnLine[0][1]), decimal.Decimal(pointsOnLine[0][2])], 
	#	[decimal.Decimal(pointsOnLine[1][0]), decimal.Decimal(pointsOnLine[1][1]), decimal.Decimal(pointsOnLine[1][2])])
	#regressionVector = (round(Decimal(regressionVector[0]), 3), round(Decimal(regressionVector[1]), 3), round(Decimal(regressionVector[2]), 3))
	#pointsOnLine[0] = [round(Decimal(pointsOnLine[0][0]), 3), round(Decimal(pointsOnLine[0][1]), 3), round(Decimal(pointsOnLine[0][2]), 3)]
	return regressionVector, pointsOnLine		#2/22/2017 Changed pointsOnLine[0] to pointsOnLine

def orthogonalVectorCalculation(pointOnLine, vectorOfLine, point):
	#Vector V defined as (x, y, z), a point on the line A defined as (l, m, n) and point P defined as (a, b, c).
	#Any point along vector V can be represented by A + kV or (l+xk, m+yk, n+zk)
	#Let us assume that (l+xk-a, m+xk-b, n+xk-c) is a NEW vector, O from the point, P to the point A on the vector
	# that is also orthogonal to vector V
	#To find the values of the orthogonal vector, O, the dot product between the orthogonal
	# vector, O and vector V must be equivalent to 0
	#Therefore, (l+xk-a, m+xk-b, n+xk-c) . (x, y, z) = 0 would yeild the appropriate orthogonal vector, L
	#As such, k = (ax - lx + by - my + cz - nz)/(x^2 + y^2 + z^2)
	numerator = ((point[0]*vectorOfLine[0]) - (pointOnLine[0]*vectorOfLine[0])) + ((point[1]*vectorOfLine[1]) - (pointOnLine[1]*vectorOfLine[1])) + ((point[2]*vectorOfLine[2]) - (pointOnLine[2]*vectorOfLine[2]))
	denominator = ((vectorOfLine[0]**2) + (vectorOfLine[1]**2) + (vectorOfLine[2]**2))
	k = numerator/denominator
	newPoint = (k*vectorOfLine[0]+pointOnLine[0],k*vectorOfLine[1]+pointOnLine[1],k*vectorOfLine[2]+pointOnLine[2])
	return vectorCalculation(newPoint,point)

#R Code
#data<-read.csv(choose.files(), header=T)
#s<-scatterplot3d(data$x, data$y, data$z)
#p1<-s$xyz.convert(data$xpoints[1], data$ypoints[1], data$zpoints[1])
#p2<-s$xyz.convert(data$xpoints[2], data$ypoints[2], data$zpoints[2])
#segments(p1$x, p1$y, p2$x, p2$y, lwd=2, col=2)