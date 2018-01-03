import sys
import os
sys.path.append(os.path.realpath("Library"))
import vector

ELEMENTS = {'N':14, 'C':12, 'O':16, 'S':32, 'H':1, 'P':31, 'D':1}

def detect(listOfSheets):
	#Adapted from Shear number of protein B-barrels; Definition refinements and statistics by Wei-Min Liu
	listOfCylindrical = []
	isCylindrical = False
	for everySheet in listOfSheets:
		#We need to find the centroids of the strands and the weighted center of the beta sheet
		center, centroids = centerOfSheet(everySheet) #These are returned as vectors in 3D space
		roughRadius = roughRadiusCalculations(center, centroids)	#Calculate the average radius from each centroid
		for centroid in centroids:
			distance = vector.vectorMagnitude(vector.vectorCalculation(center, centroid))	#Find distance
			#This is a rough guess, but generally speaking, if the sheet is organized as a cylinder then the
			# centroids to the center position should be relatively the same. However, if there are certain 
			# centroids that are smaller or larger, this would indicate a flat sheet rather than a round one
			if (distance < roughRadius + 2 and distance > roughRadius - 2): isCylindrical = True
			else: 
				isCylindrical = False
				break
		if isCylindrical and everySheet.totalStrand >= 4:	#We use 4 here because the smallest possible beta barrels
			listOfCylindrical.append(everySheet)			# have 4 strands minimal, and we want to avoid small sheets
	return listOfCylindrical

def centerOfSheet(sheet):
	totalX, totalY, totalZ, totalMass = 0, 0, 0, 0
	listOfStrandCentroids = []

	for everyStrand in sheet.strandList:
		for everyAminoAcid in everyStrand.aminoAcidList:
			for everyAtom in everyAminoAcid.backboneAtoms:
				totalX += everyAtom.x * ELEMENTS[everyAtom.element]
				totalY += everyAtom.y * ELEMENTS[everyAtom.element]
				totalZ += everyAtom.z * ELEMENTS[everyAtom.element]
				totalMass += ELEMENTS[everyAtom.element]
		totalX = totalX/totalMass
		totalY = totalY/totalMass
		totalZ = totalZ/totalMass
		listOfStrandCentroids.append((totalX, totalY, totalZ))
		totalX, totalY, totalZ, totalMass = 0, 0, 0, 0					#Forgot to make TotalMass 0...
	for centroids in listOfStrandCentroids:
		totalX += centroids[0]
		totalY += centroids[1]
		totalZ += centroids[2]
	totalX = totalX/len(listOfStrandCentroids)
	totalY = totalY/len(listOfStrandCentroids)
	totalZ = totalZ/len(listOfStrandCentroids)
	center = (totalX, totalY, totalZ)
	return center, listOfStrandCentroids

def roughRadiusCalculations(center, centroids):
	sumOfMagnitudes = 0
	for centroid in centroids:
		sumOfMagnitudes += vector.vectorMagnitude(vector.vectorCalculation(center, centroid))
	return sumOfMagnitudes/len(centroids)