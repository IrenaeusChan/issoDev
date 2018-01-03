"""
Irenaeus Chan
12/13/2016

Atom Class
Used for the BINF6210 Final Project
"""

ELEMENTS = {'N', 'C', 'O', 'S', 'H', 'P', 'D', 'SE'}					#Common atomic elements found inside Amino Acids

#Configuration for a single Atom
class Atom (object):

	"""
	Creates a new Atom
	Full argument constructor. 
	Initializes all instance variables based on parameters passed while checking for formatting

	Arguments:
		atom: The specific atom representation defined by the PDB File e.g. C, Ca, N
		x: The X position of the Atom
		y: The Y position of the Atom
		z: The Z position of the Atom
		element: Which element the atom is made of (Important for Side Chain Information)

	Exceptions:
		ValueError: If given any invalid parameters
	"""
	def __init__(self, atom, x, y, z, element):
		self.atom = atom 									#No check because PDB has a variety of Atom definitions

		#Position Checks (Float)
		if isinstance(x, float): self.x = x
		else: raise ValueError('Invalid X {0}'.format(x))
		if isinstance(y, float): self.y = y
		else: raise ValueError('Invalid Y {0}'.format(y))
		if isinstance(z, float): self.z = z
		else: raise ValueError('Invalid Z {0}'.format(z))

		if element in ELEMENTS: self.element = element
		else: raise ValueError('Invalid Element {0} {1}'.format(element, x))

	def __eq__(self, other): return self.__dict__ == other.__dict__
	def __ne__(self, other): return not self.__eq__(other)
	def __repr__(self): return "\n{0} at ({1}, {2}, {3}) \t{4}".format(self.atom, self.x, self.y, self.z, self.element)


