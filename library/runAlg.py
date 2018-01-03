from rango.models import Algorithm, PDB, AlgorithmDetail
import protein, sheet, vector
import os, sys

def testAlgorithm(alg):
	sheetList = []
	url_target = "https://www.rcsb.org/pdb/files/1a1r.pdb"
	p = protein.buildProtein(url_target)
	sheetList += sheet.buildSheet(url_target, p, '1a1r')
	algName = os.path.splitext(os.path.basename(alg.filePath.name))[0]
	sys.path.append(os.path.realpath("media/content/{0}".format(alg.author)))
	new_module = __import__(algName)
	try: 
		new_module.detect(sheetList)
		return True
	except:
		print "Unexpected Error: Probably not proper file format"
		print sys.exc_info()[0]
		return False
	
def runAlgorithm(alg, PDBList, pdb_used_testing, example_information):
	sheetList = []
	returnPDBSheetList = []

	for pdb in PDBList:
		try:
			url_target = "https://www.rcsb.org/pdb/files/{0}.pdb".format(pdb.pdb_iden)
			p = protein.buildProtein(url_target)
			sheetList += sheet.buildSheet(url_target, p, pdb.pdb_iden)
			algName = os.path.splitext(os.path.basename(alg.filePath.name))[0]
			sys.path.append(os.path.realpath("media/content/{0}".format(alg.author)))
			new_module = __import__(algName)
			print "Working... {0}".format(pdb.pdb_iden)
			try:
				returnPDBSheetList += new_module.detect(sheetList)
				sheetList = []
			except:
				print "Unexpected Error: Probably something went wrong with their logic"
				print sys.exc_info()[0]
			for PDBsheet in returnPDBSheetList:
				ad = AlgorithmDetail.objects.get_or_create(algorithm=alg, pdb=pdb, sheet_iden=PDBsheet.sheetIden,test_set=False, example=False)[0] 
				ad.save()
			returnPDBSheetList = []

			pdbDetails = pdb.algorithmdetail_set.all().filter(algorithm=alg)
			for pdbDet in pdbDetails:
				for each_pdb in pdb_used_testing:
					if pdbDet.pdb.pdb_iden == each_pdb.pdb_iden:
						pdbDet.test_set = True
				for example_pdb in example_information:
					if pdbDet.pdb.pdb_iden == example_pdb[0] and pdbDet.pdb.sheet_iden == example_pdb[1]:
						pdbDet.example = True

		except:
			print pdb.pdb_iden
