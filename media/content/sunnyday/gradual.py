def detectGradual(listOfSheets):
	listOfGradual = []
	isGradual = True
	for everySheet in listOfSheets:
		caseOne, caseTwo = 100, 0
	#Two Cases
		#First Case is if the starting STRAND is the LONGEST and steadily DECREASES
		for everyStrand in everySheet.strandList:
			if everyStrand.strandLength() < caseOne: caseOne = everyStrand.strandLength()
			else: 
				isGradual = False
				break
		if isGradual: listOfGradual.append(everySheet)
		isGradual = True
		#Second Case is if the starting STRAND is the SHORTEST and steadily INCREASES
		for everyStrand in everySheet.strandList:
			if everyStrand.strandLength() > caseTwo: caseTwo = everyStrand.strandLength()
			else: 
				isGradual = False
				break
		if isGradual: listOfGradual.append(everySheet)
		isGradual = True
	return listOfGradual