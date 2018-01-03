import vector
import time

def detectGeneric(listOfSheets):
	listOfGeneric= []
	isBulge = True
	for everySheet in listOfSheets:
		if everySheet.totalStrand % 2 != 0:	#The Sheet is odd
			middlePos = (everySheet.totalStrand/2)
			middle = everySheet.strandList[middlePos]
			goingLeftAndRight(middlePos, middle, everySheet)
		"""else:
			middlePos = len(everySheet.strandList)/2
			if (everySheet.strandList[middlePos].strandLength()) < (everySheet.strandList[middlePos-1].strandLength()):
				middle = everySheet.strandList[middlePos-1]
				middlePos -= 1
			else: middle = everySheet.strandList[middlePos]
			goingLeftAndRight(middlePos, middle, everySheet)"""
	return listOfGeneric 


#Algorithm
#---------
#Assume the middle strand or strands (same case as Bulge) to be the starting plane
# every consecutive plane afterwards will be reflected along the same axis
# or at least "should" explore the angles of change

def twistAlgorithm(strandOne, strandTwo):
	listOfCoords, sheetStrandVectors = [], []
	for everyAminoAcid in strandOne.aminoAcidList:
		for everyAtom in everyAminoAcid.backboneAtoms:
			#We want to get the coordinates of the backbone atoms in order to form our cloud
			listOfCoords.append([everyAtom.x, everyAtom.y, everyAtom.z])
			#Calculate the ODR using the backbone atoms. This is because we know the backbone atoms will most
			# likely follow the parallelism of the strand. Or follow it "close" enough to generate a rough
			# vector to represent the strand itself.
	strandOneVector, pointsOnLine = vector.orthogonalDistanceRegression(listOfCoords)
	listOfCoords = []
	for everyAminoAcid in strandTwo.aminoAcidList:
		for everyAtom in everyAminoAcid.backboneAtoms:
			listOfCoords.append([everyAtom.x, everyAtom.y, everyAtom.z])
	strandTwoVector, pointsOnLine = vector.orthogonalDistanceRegression(listOfCoords)
	#There is a problem of direction again. Vectors at first had very large angles around 165 degrees
	#However, this was because the strands themselves were anti-parallel, which caused the direction
	# of vectors to be opposite. So we want to normalize it if the strands are anti-parallel
	if (strandOne.direction - strandTwo.direction) != 0: strandOneVector = [strandOneVector[0]*-1, strandOneVector[1]*-1, strandOneVector[2]*-1]
	#This One - Two != 0 works because if they were the same direction, then it would always be 0.
	# but we are considering when they aren't in the same direction, cuz if they aren't in the same direction
	# then we would have to normalize their values to make the angles not dependent on direction
	print strandOne
	print strandTwo

	angleBetweenStrands = vector.dihedralAngle(strandTwoVector, strandOneVector)
	return angleBetweenStrands

def goingLeftAndRight(middlePos, middle, sheet):
	time.sleep(2)
	left, right = middle, middle
	for i, j in zip(range(middlePos-1,-1,-1), range(middlePos+1,len(sheet.strandList))):
		print twistAlgorithm(left, sheet.strandList[i])
		left = sheet.strandList[i]
		print twistAlgorithm(right, sheet.strandList[j])
		right = sheet.strandList[j]