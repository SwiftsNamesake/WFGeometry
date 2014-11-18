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



from os.path import abspath, join, dirname, normpath 	# ...
from pygame import image 								# ...
from OpenGL.GL import *									# ...



def loadTexture(filename):

	'''
	Loads an OpenGL texture

	'''

	surface = pygame.image.load(filename)
	image 	= pygame.image.tostring(surface, 'RGBA', True)
	w, h 	= surf.get_rect().size

	ID = glGenTextures(1)

	glBindTexture(GL_TEXTURE_2D, ID)
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
	glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, w, h, 0, GL_RGBA, GL_UNSIGNED_BYTE, image)

	return ID



def parseMTL(filename):

	'''
	Parses an MTL file

	'''

	materials = {}

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