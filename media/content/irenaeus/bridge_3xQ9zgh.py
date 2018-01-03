import sys
import glob
import os
import re
sys.path.append(os.path.realpath("Library"))
import protein
import sheet

MAXVALUE = 500				#Used for cases where there are... like... 1 million files

def detect(listOfSheets):
	listOfBridges = []
	for i, currentSheet in enumerate(listOfSheets):
		for otherSheet in listOfSheets[i+1:len(listOfSheets)]:
			if otherSheet.seqres != currentSheet.seqres:
				continue
			for currentStrand in currentSheet.strandList:
				for otherStrand in otherSheet.strandList:
					#Case 1
					if (((currentStrand.start-1) == otherStrand.stop) or ((currentStrand.stop+1) == otherStrand.start)):
						sheetOne = "{0} {1}".format(currentSheet.seqres, currentStrand.strandNum)
						sheetTwo = "{0} {1}".format(otherSheet.seqres, otherStrand.strandNum)
						listOfBridges.append(("Case 1", sheetOne, sheetTwo, currentSheet, otherSheet))
					#Case 2
					elif ((currentStrand.start >= otherStrand.start and currentStrand.start <= otherStrand.stop) 
						or (currentStrand.stop >= otherStrand.start and currentStrand.stop <= otherStrand.stop)):
						sheetOne = "{0} {1}".format(currentSheet.seqres, currentStrand.strandNum)
						sheetTwo = "{0} {1}".format(otherSheet.seqres, otherStrand.strandNum)
						listOfBridges.append(("Case 2", sheetOne, sheetTwo, currentSheet, otherSheet))
					#Case 3
					elif ((otherStrand.start >= currentStrand.start and otherStrand.start <= currentStrand.stop) 
						or (otherStrand.stop >= currentStrand.start and otherStrand.stop <= currentStrand.stop)):
						sheetOne = "{0} {1}".format(currentSheet.seqres, currentStrand.strandNum)
						sheetTwo = "{0} {1}".format(otherSheet.seqres, otherStrand.strandNum)
						listOfBridges.append(("Case 3", sheetOne, sheetTwo, currentSheet, otherSheet))
	return listOfBridges

def toHTML(listOfBridges, filename):
	with open('bridges.html', 'a') as output:
		if os.stat("bridges.html").st_size == 0:
			output.write("<html>\n<head>\n</head>\n<body>")
		output.write("<pre>" + filename + "</pre>")
		for pairOfSheets in listOfBridges:
			output.write("<pre>" + pairOfSheets[0] + "<br>" + pairOfSheets[1] + "<br>" + pairOfSheets[2] + "</pre>")
			output.write("<pre>")
			sheetOne = int(re.findall(r"(\d+)", pairOfSheets[1])[0])
			for i, line in enumerate(str(pairOfSheets[3]).splitlines()):
				if i == sheetOne-1: output.write("<font color=\"red\">" + line + "</font></br>")
				else: output.write(line + "</br>") 
			output.write("</pre>")
			output.write("<pre>")
			sheetTwo = int(re.findall(r"(\d+)", pairOfSheets[2])[0])
			for i, line in enumerate(str(pairOfSheets[4]).splitlines()):
				if i == sheetTwo-1: output.write("<font color=\"blue\">" + line + "</font></br>")
				else: output.write(line + "</br>")
			output.write("</pre>")

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
			listOfBridges = detectBridge(sheetList)
			if listOfBridges:
				print "{0} is BRIDGE".format(file)
				toHTML(listOfBridges, file)
				count+=1
			else:
				print "{0} is NOT BRIDGE".format(file)
	with open("bridges.html", 'a') as output:						#My quick solution to ending HTML file
		output.write("</body>\n</html>")
	print count
				
def computeOne(filename):
	p = protein.buildProtein(filename)
	sheetList = sheet.buildSheet(filename, p)
	listOfBridges = detectBridge(sheetList)
	if listOfBridges:
		print "{0} is BRIDGE".format(filename)
		toHTML(listOfBridges, filename)
	else:
		print "{0} is NOT BRIDGE".format(filename)
	with open("bridges.html", 'a') as output:						#My quick solution to ending HTML file
		output.write("</body>\n</html>")