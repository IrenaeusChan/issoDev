"""
Irenaeus Chan
12/01/2016 - OLD CODE with edits

Sheets and Strands (that make up Sheets)
Used for the BINF6210 Final Project

 =m1tg<bi(siA
"""

from itertools import tee, islice, chain, izip
import re
import string
import os
import urllib2

#Configuration for a Strand Object
class Strand(object):
	"""
	Creates a new STRAND made up of Amino Acids
	Full argument constructor. 
	Initializes all instance variables based on parameters passed while checking for formatting

	Arguments:
		strandNum: This will be a LETTER representing which SHEET it belongs to and a NUMBER 
					which will correspond to the order of the STRAND in the SHEET
		start: The starting position of the STRAND
		stop: The ending position of the STRAND
		seqres: Which chain does the STRAND belong to
		strandType: The number which determines Parallel (1) or Anti-Parallel (-1) or Starting (0)
		direction: Related to strandType, but assuming --> is 1 and <-- is -1
		aminoAcidList: A list of all the Amino Acids that make up the STRAND

		thisStrand: RESIDUE NUMBER of THIS STRAND that connects to otherStrand
		otherStrand: RESIDUE NUMBER of OTHER STRAND that connects to thisStrand

	Exceptions:
		ValuError: If given any invalid parameters
	"""
	def __init__(self, strandNum, start, stop, seqres, strandType, direction, aminoAcidList, thisStrand, otherStrand):
		if isinstance(strandNum, basestring): self.strandNum = strandNum
		else: raise ValueError('Invalid SEQRES {0}'.format(strandNum))

		if isinstance(start, int): self.start = start
		else: raise ValueError('Invalid Start Position {0}'.format(start))

		if isinstance(stop, int): self.stop = stop
		else: raise ValueError('Invalid Stop Position {0}'.format(stop))

		if isinstance(seqres, basestring): self.seqres = seqres
		else: raise ValueError('Invalid SEQRES {0}'.format(seqres))

		if isinstance(strandType, int): self.strandType = strandType
		else: raise ValueError('Invalid Type {0}'.format(strandType))

		if isinstance(direction, int): self.direction = direction
		else: raise ValueError('Invalid Type {0}'.format(direction))
			
		self.aminoAcidList = aminoAcidList

		if isinstance(thisStrand, int): self.thisStrand = thisStrand
		elif thisStrand == None: self.thisStrand = None
		else: raise ValueError('Invalid Type {0}'.format(thisStrand))

		if isinstance(otherStrand, int): self.otherStrand = otherStrand
		elif otherStrand == None: self.otherStrand = None
		else: raise ValueError('Invalid Type {0}'.format(otherStrand))

	def __eq__(self, other): return self.__dict__ == other.__dict__
	def __ne__(self, other): return not self.__eq__(other)
	def __repr__(self):
		strandSequence = ""
		aarepr = ""
		for aa in self.aminoAcidList:
			if aa.position != self.aminoAcidList[-1].position:
				aarepr = str(aa.position)
				if len(aarepr) == 2: aarepr = "0" + aarepr
				elif len(aarepr) == 1: aarepr = "00" + aarepr
				strandSequence += aarepr + " --- "
			else:
				aarepr = str(aa.position) 
				if len(aarepr) == 2: aarepr = "0" + aarepr
				elif len(aarepr) == 1: aarepr = "00" + aarepr
				strandSequence += aarepr
		return strandSequence

	def strandLength(self):
		return (self.stop - self.start)+1

#Configuration for a Sheet Object
class Sheet(object):
	"""
	Creates a new Sheet made up of Amino Acids
	Full argument constructor. 
	Initializes all instance variables based on parameters passed while checking for formatting

	Arguments:
		PDBFile: Identifies which PDB File the sheet is from
		sheetIden: The identification character of the SHEET
		seqres: Which chain does the SHEET belong to
		totalStrand: The total number of STRANDS that make up the SHEET
		strandList: The list of STRANDS that make up the SHEET

	Exceptions:
		ValuError: If given any invalid parameters
	"""
	def __init__(self, PDBFile, sheetIden, seqres, totalStrand, strandList):
		if isinstance(PDBFile, basestring): self.PDBFile = PDBFile
		else: raise ValueError('Invalid SEQRES {0}'.format(PDBFile))

		if isinstance(sheetIden, basestring): self.sheetIden = sheetIden
		else: raise ValueError('Invalid SEQRES {0}'.format(sheetIden))

		if isinstance(seqres, basestring): self.seqres = seqres
		else: raise ValueError('Invalid SEQRES {0}'.format(seqres))

		if isinstance(totalStrand, int): self.totalStrand = totalStrand
		else: raise ValueError('Invalid SEQRES {0}'.format(totalStrand))
			
		self.strandList = strandList

	def __eq__(self,other): return self.strandList == other.strandList
	def __ne__(self, other): return not self.__eq__(other)
	def __repr__(self):
		sheetRepresent, beforeEditStrand = "", ""#"{0}{1}\n".format(self.seqres, self.sheetIden)
		listOfStrands = []
		nextStrandSpacing = 0
		for prev, currentStrand, nxt in previousAndNext(self.strandList):
			if currentStrand.strandType == 0:
				"""
				Assumption: We must assume the FIRST STRAND (0) in the SHEET goes from LEFT to RIGHT
							From here, ANY successive "Parallel (1)" STRAND will also go LEFT to RIGHT
							AND ANY successive "Anti-Parallel (-1)" STRAND will therefore have to go LEFT to RIGHT
				"""
				beforeEditStrand = "{0}\n".format(currentStrand).replace("---", "-->")
				
				"""
				This is where we check for Parallel and Anti-parallel spacing. Depending on whether or not the next
				strand in the list is Parallel or Anti-parallel, we will have to change the differenceValue in order to
				account for the spacing problem
				"""
				differenceValue = differenceValueCalculations(nxt, currentStrand, "lr")
				if differenceValue > 0: beforeEditStrand = " "*8*differenceValue + beforeEditStrand
				elif differenceValue < 0: nextStrandSpacing += abs(differenceValue)
			elif re.search('-->', beforeEditStrand) and currentStrand.strandType != 0:
				"""
				We want to know which direction the previous strand to this one was facing. Depending on that, it will change
				the way we will change the arrow direction in this set of function
				"""
				if currentStrand.strandType == 1: #-->
					beforeEditStrand = " "*8*nextStrandSpacing + "{0}".format(currentStrand).replace("---", "-->") + "\n"
					if nxt is not None: differenceValue = differenceValueCalculations(nxt, currentStrand, "lr")
					beforeEditStrand, listOfStrands, nextStrandSpacing = applyAndReconfigure(differenceValue, beforeEditStrand, listOfStrands, nextStrandSpacing)
						
				elif currentStrand.strandType == -1: #<--
					beforeEditStrand = " "*8*nextStrandSpacing + reverseDirection("{0}".format(currentStrand).replace("---", "<--")) + "\n"
					if nxt is not None: differenceValue = differenceValueCalculations(nxt, currentStrand, "rl")
					beforeEditStrand, listOfStrands, nextStrandSpacing = applyAndReconfigure(differenceValue, beforeEditStrand, listOfStrands, nextStrandSpacing)						

			elif re.search('<--', beforeEditStrand) and currentStrand.strandType != 0:
				if currentStrand.strandType == 1: #<--
					beforeEditStrand = " "*8*nextStrandSpacing + reverseDirection("{0}".format(currentStrand).replace("---", "<--")) + "\n"
					if nxt is not None: differenceValue = differenceValueCalculations(nxt, currentStrand, "rl")
					beforeEditStrand, listOfStrands, nextStrandSpacing = applyAndReconfigure(differenceValue, beforeEditStrand, listOfStrands, nextStrandSpacing)
				
				elif currentStrand.strandType == -1: #-->
					beforeEditStrand = " "*8*nextStrandSpacing + "{0}".format(currentStrand).replace("---", "-->") + "\n"
					if nxt is not None: differenceValue = differenceValueCalculations(nxt, currentStrand, "lr")
					beforeEditStrand, listOfStrands, nextStrandSpacing = applyAndReconfigure(differenceValue, beforeEditStrand, listOfStrands, nextStrandSpacing)

			listOfStrands.append([currentStrand.strandNum, beforeEditStrand])
			templistOfStrands = []
		sheetRepresent += ''.join(word[0] + " " + word[1] for word in listOfStrands)
		return sheetRepresent

def previousAndNext(some_iterable):
	#http://stackoverflow.com/questions/1011938/python-previous-and-next-values-inside-a-loop
	prevs, items, nexts = tee(some_iterable, 3)
	prevs = chain([None], prevs)
	nexts = chain(islice(nexts, 1, None), [None])
	return izip(prevs, items, nexts)

#Used to calculate the positional difference between the two strands in order to account for spacing
def differenceValueCalculations(nxt, currentStrand, direction):
	differenceValue = 0
	if direction == "rl":
		if nxt.strandType == 1:	#Next Strand is <-- Meaning Stop
			differenceValue = abs(nxt.thisStrand - nxt.stop) - abs(nxt.otherStrand - currentStrand.stop)
		elif nxt.strandType == -1:	#Next Strand is --> Meaning Start
			differenceValue = abs(nxt.thisStrand - nxt.start) - abs(nxt.otherStrand - currentStrand.stop)
		return differenceValue
	elif direction == "lr":
		if nxt.strandType == 1:	#Next Strand is --> Meaning Start
			differenceValue = abs(nxt.thisStrand - nxt.start) - abs(nxt.otherStrand - currentStrand.start)
		elif nxt.strandType == -1:	#Next Strand is <-- Meaning Stop
			differenceValue = abs(nxt.thisStrand - nxt.stop) - abs(nxt.otherStrand - currentStrand.start)
	return differenceValue

#Using the difference value as a reference for position, we can then space the strands out properly and apply the changes
def applyAndReconfigure(differenceValue, beforeEditStrand, listOfStrands, nextStrandSpacing):
	templistOfStrands = []
	if differenceValue > 0:
		beforeEditStrand = " "*8*differenceValue + beforeEditStrand
		for strandString in listOfStrands:
			templistOfStrands.append([strandString[0], " "*8*differenceValue + strandString[1]])
		listOfStrands = []
		listOfStrands = templistOfStrands
	elif differenceValue < 0:
		nextStrandSpacing += abs(differenceValue)
	return beforeEditStrand, listOfStrands, nextStrandSpacing

def reverseDirection(stringOfNumbers):
	toFlip = stringOfNumbers.split(" ")
	return ' '.join(word for word in toFlip[::-1])

def buildSheet(url_target, protein, pdbname):
	strandAminoAcidList, strandList, sheetList = [], [], []
	thisStrand, otherStrand = None, None
	stream = urllib2.urlopen(url_target)
	for line in stream:
		#Reads from the file the information regarding the SHEET structures
		if (line[0:5] == "SHEET"):
			#drive, path_and_file = os.path.splitdrive(filename)
			#path, pdbname = os.path.split(path_and_file)
			PDBFile = str(pdbname)				#The name of the PDB File
			sheetIden = str(line[11:14])		#The PDB Identifier Number
			totalStrand = int(line[14:16])		#The number of Strands in the Sheet
			strandNum = str(line[8:10])			#The current Strand Position in the Sheet
			start = int(line[22:26])			#Start of the Strand
			stop = int(line[33:37])				#End of the Strand
			seqres = str(line[21:22])			#Which SEQRES does the Strand belong to
			strandType = int(line[38:40])		#What type? Parallel(1), Anti-Parallel(-1), Start(0)

			if strandType == 0: direction = 1	#The direction of the strand --> (1) or <-- (-1)
			else:
				if strandType == -1 and direction == 1: direction = -1 		#Anti 		-->			 <--
				elif strandType == -1 and direction == -1: direction = 1 	#Anti 		<-- 		 -->
				elif strandType == 1 and direction == 1: direction = 1 		#Parallel	--> 		 -->
				elif strandType == 1 and direction == -1: direction = -1 	#Parallel   <--			 <--
			#This information is important when we are trying to represent the entire Sheet
			if strandType != 0:
				try:
					thisStrand = int(line[50:55])
					otherStrand = int(line[65:69])
				except ValueError:
					thisStrand = 0
					otherStrand = 0 
				#Looks for the position of the Amino Acid using the already parsed sequence and copies the sequence
			for aa in protein.aminoAcidList:
				if (aa.position >= start and aa.position <= stop and aa.seqres == seqres): strandAminoAcidList.append(aa)
				if (aa.position == stop and aa.seqres == seqres): break

			#Appends the STRAND sequence to a list of other sequences
			strandList.append(Strand(sheetIden.strip() + strandNum.strip(), start, stop, seqres, +
				+ strandType, direction, strandAminoAcidList, thisStrand, otherStrand))
			strandAminoAcidList = []

			if len(strandList) == totalStrand:
				sheetList.append(Sheet(PDBFile, sheetIden, seqres, totalStrand, strandList))
				strandList = []
	return sheetList
