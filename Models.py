#
# Models.py
# Loading and managing 3D models
#
# Jonatan H Sundqvist
# November 18 2014
#

# TODO | - Define API
#        - 3D vectors
#        - Handle units
#        - Splines, bezier curves (advanced, low priority)
#        - Pre-existing parsing modules
#
# SPEC | - Exports a Model class and parsers for Wavefront MTL and OBJ files
#        -



def parseMTL(filename):

	'''
	Parses an MTL file

	'''

	raise NotImplementedError



def parseOBJ(filename):

	'''
	Parses an OBJ file

	'''

	raise NotImplementedError



class Model(object):

	'''
	Wraps an OpenGL buffer

	'''

	def __init__(self, filename, origin=(0,0,0)):
		
		'''
		Docstring goes here

		'''

		pass


	def render(self):
		
		'''
		Docstring goes here

		'''

		pass



def main():
	
	'''
	Test suite

	'''

	pass



if __name__ == '__main__':
	main()