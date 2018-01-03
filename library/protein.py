"""
Irenaeus Chan
12/13/2016

Protein Class
Used for the BINF6210 Final Project
"""

#The PDB symbols for Backbone Atoms
BACKBONE_ATOMS = {'N', 'CA', 'C'}

from atom import Atom
from aminoacid import AminoAcid
import urllib2

#A configuration for an entire Protein
class Protein(object):
	"""
	Creates a new Protein
	Full argument constructor. 
	Initializes all instance variables based on parameters passed while checking for formatting

	Arguments:
		aminoAcidList: A list of all the Amino Acids that make up the Protein
	"""
	def __init__(self, aminoAcidList): self.aminoAcidList = aminoAcidList
	def __eq__(self, other): return self.__dict__ == other.__dict__
	def __ne__(self, other): return not self.__eq__(other)
	def __repr__(self):
		proteinSequence = ""
		for aa in self.aminoAcidList:
			proteinSequence += "{0}\n".format(aa)
		return proteinSequence

def buildProtein(url_target):
	backboneList, sidechainList, proteinList = [], [], []
	currentPos = 0
	currentAminoAcid, currentSeq = "", ""
	stream = urllib2.urlopen(url_target)
	for line in stream:
		#All Lines Indexes are found: https://www.cgl.ucsf.edu/chimera/docs/UsersGuide/tutorials/pdbintro.html
		if (line[0:4] == "ATOM"):
			"""
			This check is in here because, PDB Files do not necessarily have to start their amino acid count
			at 0. Most proteins will have non-amino acid residues before the start of their chain which is
			why the position differs. Additionally, each PDB File defines their amino acids as a single number
			representing the residue number. Which is why we can use that number as a way to detect when the
			start of a new amino acid occurs.

			Therefore, everytime the amino acid residue number changes (and that change is not from 0 to residue
			number) we can assume it is the start of a new amino acid residue.
			"""
			if((currentPos != int(line[22:26])) and currentPos != 0):
				#When a new amino acid is started, append the completed one
				#Amino Acid, SEQRES, Position, Backbone Atoms [N][Ca][C], Sidechain Atoms [1]...[n]
				proteinList.append(AminoAcid(currentAminoAcid, currentSeq, currentPos, list(backboneList), list(sidechainList)))
				backboneList, sidechainList = [], []		#Reset the lists to empty
			
			#The index is defined by looking at the PDB Files, they are consistent across all PDB Files
			currentAminoAcid = str(line[17:20])
			currentSeq = str(line[21:22])
			currentPos = int(line[22:26])

			atomName = line[12:16].strip()
			if(atomName in BACKBONE_ATOMS): backboneList.append(Atom(atomName, float(line[31:38]), float(line[39:46]), float(line[47:54]), str(line[76:78].replace(" ", ""))))
			else: sidechainList.append(Atom(atomName, float(line[31:38]), float(line[39:46]), float(line[47:54]), str(line[76:78].replace(" ", ""))))
	"""
	Because we always add the completed Atom after we detect its completion by examining whether or not the 
	residue number changed, we need to do one more append for the LAST amino acid, since there won't be a
	residue change after the last amino acid has been completed
	"""
	proteinList.append(AminoAcid(currentAminoAcid, currentSeq, currentPos, list(backboneList), list(sidechainList)))
	return Protein(list(proteinList))

def weightedAverage(protein):
	totalX = 0
	totalY = 0
	totalZ = 0
	totalMass = 0

	for AA in protein.amino_acids:
		for atom in AA.backbone:
			totalX += atom.x * ELEMENTS[atom.element]
			totalY += atom.y * ELEMENTS[atom.element]
			totalZ += atom.z * ELEMENTS[atom.element]
			totalMass += ELEMENTS[atom.element]
		for atom in AA.sidechain:
			totalX += atom.x * ELEMENTS[atom.element]
			totalY += atom.y * ELEMENTS[atom.element]
			totalZ += atom.z * ELEMENTS[atom.element]
			totalMass += ELEMENTS[atom.element]

	totalX = totalX/totalMass
	totalY = totalY/totalMass
	totalZ = totalZ/totalMass

	return totalX, totalY, totalZ

def relativeToCenter(protein, center):
	write = 'w'
	if (sys.argv[1] == "all" and len(sys.argv) > 2):
		write = 'a'
	with open("distances.txt", write) as output:
		for AA in protein.amino_acids:
			aminoacid = [AA.avgx, AA.avgy, AA.avgz]
			extraInfo = AA.amino_acid
			d = vector.vectorMagnitude(vector.vectorCalculation(center, aminoacid))
			output.write(extraInfo + ' ' + str(d) + '\n')
