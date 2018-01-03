import sys
import glob
import os
import re
from itertools import tee, islice, chain, izip
sys.path.append(os.path.realpath("Library"))
import protein
import sheet
import vector

MAXVALUE = 500				#Used for cases where there are... like... 1 million files

def previousAndNext(some_iterable):
#http://stackoverflow.com/questions/1011938/python-previous-and-next-values-inside-a-loop
	prevs, items, nexts = tee(some_iterable, 3)
	prevs = chain([None], prevs)
	nexts = chain(islice(nexts, 1, None), [None])
	return izip(prevs, items, nexts)

def detectTwist(listOfSheets):
	listOfTwist, listOfCoords, sheetStrandVectors = [], [], []
	totalAngleBetweenStrands = 0
	for everySheet in listOfSheets:
		#print everySheet.sheetIden
		for everyStrand in everySheet.strandList:
			for everyAminoAcid in everyStrand.aminoAcidList:
				for everyAtom in everyAminoAcid.backboneAtoms:
					#We want to get the coordinates of the backbone atoms in order to form our cloud
					listOfCoords.append([everyAtom.x, everyAtom.y, everyAtom.z])
			#Calculate the ODR using the backbone atoms. This is because we know the backbone atoms will most
			# likely follow the parallelism of the strand. Or follow it "close" enough to generate a rough
			# vector to represent the strand itself.
			regressionVector, pointsOnLine = vector.orthogonalDistanceRegression(listOfCoords)
			sheetStrandVectors.append([regressionVector, everyStrand.strandType])
			listOfCoords = []
		#Once we have all of the strands and their representative vectors, we want to start calculating the
		# angles between the two of them. However...
		for prev, cur, nxt in previousAndNext(sheetStrandVectors):
			if nxt is not None:
				#There is a problem of direction again. Vectors at first had very large angles around 165 degrees
				#However, this was because the strands themselves were anti-parallel, which caused the direction
				# of vectors to be opposite. So we want to normalize it if the strands are anti-parallel
				if nxt[1] == -1: nextStrand = [nxt[0][0]*-1,nxt[0][1]*-1,nxt[0][2]*-1]
				else: nextStrand = nxt[0]		#If the strands aren't parallel, the direction will be the same
				angleBetweenStrands = vector.dihedralAngle(cur[0], nextStrand)
				#angleBetweenStrands = vector.signedAngle(cur[0], nextStrand)
				#This is here arbitrarily, I still haven't figured out why sometimes, angles just seem to be massive
				# good examples being 1a0i and 1a6t where a single angle that "looks" small ends up being like 150+
				if angleBetweenStrands > 100:
					angleBetweenStrands = vector.dihedralAngle(cur[0], nxt[0])
					#angleBetweenStrands = vector.signedAngle(cur[0], nxt[0])
				totalAngleBetweenStrands += angleBetweenStrands
				#print cur[0]
				#print nextStrand
				#print angleBetweenStrands
		if totalAngleBetweenStrands >= 80 and totalAngleBetweenStrands <= 170: 
			#listOfTwist.append([str(everySheet), str(totalAngleBetweenStrands)])
			listOfTwist.append([everySheet, totalAngleBetweenStrands])
		#print ""
		#print totalAngleBetweenStrands
		#print ""
		totalAngleBetweenStrands = 0
		sheetStrandVectors = []
	return listOfTwist

def computeAll(path):
	only100 = 0
	count = 0
	for filename in glob.glob(os.path.join(path, '*.pdb')):
		drive, pathAndFile = os.path.splitdrive(filename)			#http://stackoverflow.com/questions/3167154/how-to-split-a-dos-path-into-its-components-in-python
		filePath, file = os.path.split(pathAndFile)
		if (only100 == MAXVALUE):
			break
		else:
			only100+=1
			p = protein.buildProtein(filename)
			sheetList = sheet.buildSheet(filename, p)
			print "{0} files completed...".format(only100)
			listOfTwist = detectTwist(sheetList)
			if listOfTwist:
				print "{0} has a Twist".format(file)
				toHTML(listOfTwist, file)
				count+=1
			else:
				print "{0} is NOT a Twist".format(file)
	with open("twist.html", 'a') as output:						#My quick solution to ending HTML file
		output.write("</body>\n</html>")
	print count
				
def computeOne(filename):
	p = protein.buildProtein(filename)
	sheetList = sheet.buildSheet(filename, p)
	listOfTwist = detectTwist(sheetList)
	if listOfTwist:
		print "{0} has a Twist".format(filename)
		toHTML(listOfTwist, filename)
	else:
		print "{0} is NOT a Twist".format(filename)
	with open("twist.html", 'a') as output:						#My quick solution to ending HTML file
		output.write("</body>\n</html>")

def toHTML(listOfTwist, filename):
	with open('twist.html', 'a') as output:
		if os.stat("twist.html").st_size == 0:
			output.write("<html>\n<head>\n</head>\n<body>")
		output.write("<pre>" + filename + "</pre>")
		for theSheet in listOfTwist:
			output.write("<pre>" + str(theSheet[1]) + "</pre>")
			output.write("<pre>")
			for i, line in enumerate(str(theSheet[0]).splitlines()):
				output.write(line + "</br>") 
			output.write("</pre>")