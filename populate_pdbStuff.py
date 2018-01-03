import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

import django
django.setup()

from django.contrib.auth.models import User
from rango.models import Algorithm, PDB, AlgorithmDetail, UserFollow

def populate():

	irenaeus = User.objects.get(pk=1)
	irenaeus.save()

	twistList = ['1a0h', '1a0i', '1a0r', '1a1r', '1a2c', '1a3k', '1a5u', '1a7n', '1a7o', '1a7p', '1a7q', '1a7r', '1a72', '1ac6', '1adf', '1adg', '1ajo', '1akp', '1aly', '1amy', '1apn', '1apv', '1apw', '1avn', '1ax1', '1ax2', '1ax3', '1axy', '1axz', '1ayo', '1azd', '1azm', '1b0w', '1b8a', '1bbu', '1bbw', '1bcd', '1beb', '1bfs', '1bft', '1bjq', '1bk0', '1bk1', '1bmf', '1bmv', '1bn1', '1bn3', '1bn4', '1bn8', '1bnn', '1bnq', '1bnt', '1bnu', '1bnv', '1bnw', '1br2']
	betabarrelList = ['1a1r', '1a1x', '1a2d', '1a2u', '1a3l', '1a3t', '1a3u', '1a3v', '1a4a', '1a4b', '1a4c', '1a4w', '1a5h', '1a5i', '1a5u', '1a6u', '1a6v', '1a6w', '1a8v', '1a18', '1a61', '1aa6', '1ab0', '1abi', '1ac0', '1acd', '1acz', '1adl', '1aex', '1agj', '1ah9', '1ai1', '1aip', '1aix', '1aiz', '1akj', '1alb', '1amh', '1amy', '1anb', '1anc', '1and', '1ao5', '1aq7', '1aqb', '1aqc', '1awf', '1au8', '1auj', '1aut', '1avd', '1ave', '1avw', '1avx', '1ay6', '1az8', '1b0e', '1b0f', '1b3q', '1b5g', '1b8a', '1b9m', '1b9z', '1b56', '1b90', '1ba8', '1ba9', '1bag', '1bb0', '1bb9', '1bcu', '1bd0', '1bda', '1bf2', '1bg9', '1bio', '1bit', '1bj7', '1bj8', '1bju', '1bjv', '1bm5', '1bma', '1bmf', '1bml', '1bmm', '1bmn', '1bqy', '1brp', '1brq', '1bru', '1btp', '1btu', '1btw', '1btx', '1bty', '1btz', '1bui', '1bwy']

	bridgeList = ['1a5k', '1a5l', '1a5m', '1a5n', '1a5o', '1a8d', '1a8j', '1a42', '1a47', '1adb', '1ajk', '1ajw','1al0', '1as6', '1as7', '1as8', '1asj', '1asp', '1asq', '1at0', '1avg', '1avk', '1avl', '1axk', '1azz', '1b6s', '1b7t', '1bec', '1bm3', '1bmg', '1bml', '1bnm', '1bnn', '1bpv', '1bq5', '1bqu', '1bvz', '1bw8']

	a1 = createAlgorithm("90 Degree Twist", "A series of Beta-Strands that sequentially increases the angle of inclination with the x-axis being the previous Beta-Strand and the line being the next Beta-Strand. This angle of inclination gradually increases until the final Beta-Strand is at an approximate 90 degree or 180 degree angle from the starting strand.", len(twistList), irenaeus)

	a2 = createAlgorithm("Beta Barrel", "The Beta-Barrel is an iconic tertiary structure that is well defined and studied. The Beta-Barrel greatly resembles a barrel or a tube. The barrel structure is unique in the sense that the first Beta-Strand is generally connected via hydrogen bonds to its last Beta-Strand making it a complete circle. This gives rise to the definition of a cylindrical shape with a fully enclosed circumference that follows the relationship of shear value to radius as defined by Murzin et al (1994).", len(betabarrelList), irenaeus)

	a3 = createAlgorithm("Bridge", "Two Beta-Sheets that have connecting or overlapping Beta-Strands that cause the two individual Beta-Sheets to either appear as if they are a larger connected sheet.", len(bridgeList), irenaeus)

	for pdb in twistList:
		createAlgorithmDetail(a1, createPDB(pdb, "http://www.rcsb.org/pdb/explore.do?structureId={0}".format(pdb)), 'A', True, False)

	for pdb in betabarrelList:
		createAlgorithmDetail(a2, createPDB(pdb, "http://www.rcsb.org/pdb/explore.do?structureId={0}".format(pdb)), 'A', True, False)

	for pdb in bridgeList:
		createAlgorithmDetail(a3, createPDB(pdb, "http://www.rcsb.org/pdb/explore.do?structureId={0}".format(pdb)), 'A', True, False)

	for alg in Algorithm.objects.all():
		for p in alg.pdb.all():
			print "{0}: {1}".format(str(alg), str(p))

def createAlgorithm(algorithm_name, gd, pdbFilesUsed, irenaeus):
	a = Algorithm.objects.get_or_create(algorithm_name=algorithm_name, author=irenaeus)[0]
	a.general_description = gd
	a.PDBFilesUsed = pdbFilesUsed
	a.save()
	return a

def createPDB(pdb_iden, url):
	p = PDB.objects.get_or_create(pdb_iden=pdb_iden)[0]
	p.url = url
	p.save()
	return p

def createAlgorithmDetail(algorithm, pdb, sheet_iden, test_set, example):
	ad = AlgorithmDetail.objects.get_or_create(algorithm=algorithm, pdb=pdb, sheet_iden=sheet_iden, test_set=test_set, example=example)[0]
	ad.save()

if __name__ == '__main__':
	print "Starting PDB-Algorithm population script..."
	populate()
