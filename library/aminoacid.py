"""
Irenaeus Chan
12/13/2016

Amino Acid Class
Used for the BINF6210 Final Project
"""

from atom import Atom

#The 20 Amino Acids
AMINO_ACIDS = {'GLY', 'ALA', 'SER', 'THR', 'CYS', 'VAL', 'LEU', 'ILE', 'MET', 'PRO', 'PHE', 'TYR', 'TRP', 'ASP', 'GLU', 'ASN', 'GLN', 'HIS', 'LYS', 'ARG', 'SEC', 'TER'}
ELEMENTS = {'N':14, 'C':12, 'O':16, 'S':32, 'H':1, 'P':31, 'D':1, 'SE':34}

#A configuration for a single Amino Acid
class AminoAcid(object):
	"""
	Creates a new Amino Acid
	Full argument constructor. 
	Initializes all instance variables based on parameters passed while checking for formatting

	Arguments:
		aminoAcid: The specific Amino Acid
		seqres: Which chain (specified by PDB) does the Amino Acid belong to
		position: The numerical position of the Amino Acid e.g. 239, 240, 241
		backboneAtoms: The backbone atoms
		sidechainAtoms: The sidechain atoms

	Exceptions:
		ValuError: If given any invalid parameters
	"""
	def __init__(self, aminoAcid, seqres, position, backboneAtoms, sidechainAtoms):
		if aminoAcid in AMINO_ACIDS: self.aminoAcid = aminoAcid
		else: raise ValueError('Invalid Amino Acid {0}'.format(aminoAcid))

		if isinstance(seqres, basestring): self.seqres = seqres
		else: raise ValueError('Invalid SEQRES {0}'.format(seqres))

		if isinstance(position, int): self.position = position
		else: raise ValueError('Invalid Position {0}'.format(position))

		#No need to raise Errors for these because when we create an Atom it should check values appropriately
		self.backboneAtoms = backboneAtoms
		self.sidechainAtoms = sidechainAtoms
		self.avgx, self.avgy, self.avgz = weightedAverage(self)

	def __eq__(self, other): return self.__dict__ == other.__dict__
	def __ne__(self, other): return not self.__eq__(other)
	def __repr__(self):
		aminoAcidString = "{0} {1} {2}\n".format(self.aminoAcid, self.seqres, self.position)
		for aa in self.backboneAtoms:
			aminoAcidString += "{0}".format(aa)
		for aa in self.sidechainAtoms:
			aminoAcidString += "{0}".format(aa)
		return aminoAcidString

def weightedAverage(self):
	totalX = 0
	totalY = 0
	totalZ = 0
	totalMass = 0

	for atom in self.backboneAtoms:
		totalX += atom.x * ELEMENTS[atom.element]
		totalY += atom.y * ELEMENTS[atom.element]
		totalZ += atom.z * ELEMENTS[atom.element]
		totalMass += ELEMENTS[atom.element]
	for atom in self.sidechainAtoms:
		totalX += atom.x * ELEMENTS[atom.element]
		totalY += atom.y * ELEMENTS[atom.element]
		totalZ += atom.z * ELEMENTS[atom.element]
		totalMass += ELEMENTS[atom.element]

	totalX = totalX/totalMass
	totalY = totalY/totalMass
	totalZ = totalZ/totalMass

	return totalX, totalY, totalZ