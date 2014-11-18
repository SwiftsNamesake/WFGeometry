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
from collections import defaultdict 					# ...
# from itertools



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

	raise NotImplementedError('Walk along. Nothing to see here.')

	materials = {} # TODO: Dict comprehension, itertools, split on "newmtl" (?)

	for line in filter(lambda ln: not (ln.isspace() or ln.startswith('#')), open(filename, 'r')):
		
		# For each line that is not blank or a comment
		values = line.split() # Split on space



def parseOBJ(filename):

	'''
	Parses an OBJ file

	'''

	raise NotImplementedError('Walk along. Nothing to see here.')

	model 	= [] 				# Buffer 
	data 	= defaultdict(list)	#

	for line in filter(lambda ln: not (ln.isspace() or ln.startswith('#')), open(filename, 'r')):

		if values[0] == 'v':
			# Vertex coordinates
			data['vertices'].append([float(v) for v in values[1:4]]) # TODO: Handle invalid vertex data
		elif values[0] == 'vn':
			# Vertex normal
			data['normals'].append([float(v) for v in values[1:4]]) # TODO: Handle invalid normal data
		elif values[0] == 'vt':
			# Texture coordinates
			data['textures'].append([float(t) for t in values[1:3]]) # TODO: Handle invalid texture data
		elif values[0] == 'f':
			# Face
			pass
		elif values[0] == 'g':
			# Group
			pass
		elif values[0] == 'o':
			# Object
			pass
		elif values[0] == 's':
			# Smooth shading
			pass
		elif values[0] = 'mtllib':
			#
			pass

	return model


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

	obj = parseOBJ('...')



if __name__ == '__main__':
	main()