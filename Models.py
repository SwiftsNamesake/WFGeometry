#
# Models.py
# Loading and managing 3D models
#
# Jonatan H Sundqvist
# November 18 2014
#

# TODO | - Define API
#        - 3D vectors
#        - Handle units (conversion factor)
#        - Splines, bezier curves (advanced, low priority)
#        - Pre-existing parsing modules
#        - Make sure input files are closed properly
#        - Reference official specs, describe formats, ensure correctness
#        - Optimize, comment, refactor
#
# SPEC | - Exports a Model class and parsers for Wavefront MTL and OBJ files
#        - SI units by default



from os.path import abspath, join, dirname, normpath 	# ...
from pygame import image 								# ...
from OpenGL.GL import *									# ...
from collections import defaultdict, OrderedDict 		# ...
# from itertools



def parent(filename):

	'''
	Retrieves parent directory of the specified file

	'''

	return dirname(abspath(filename))



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

	materials = {} 				# TODO: Dict comprehension, itertools, split on "newmtl" (?)
	current = None 				# Name of the current material
	path 	= parent(filename) 	# Path to containing folder

	for line in filter(lambda ln: not (ln.isspace() or ln.startswith('#')), open(filename, 'r')):
		
		# TODO: Decide between abbreviated and full-length keys

		# For each line that is not blank or a comment
		values = line.split() # Split on space

		if values[0] in ('Ka', 'Kd', 'Ks'):
			# Ambient, Diffuse and Specular
			# TODO: Convert to tuple (?)
			materials[current][values[0]] = [float(ch) for ch in values[1:]] # (R, G, B, A) channels
		elif values[0] == 'map_Kd':
			# Texture
			materials[current][values[0]] = loadTexture(join(path, values[1]))
		elif values[0] == 'newmtl':
			# New material definition
			current = values[1]
			materials[current] = {}
		else:
			# Unknown parameter encountered
			raise ValueError('\'{0}\' is not a recognised parameter.'.format(values[0]))

	return materials



def parseOBJ(filename):

	'''
	Parses an OBJ file

	'''

	# TODO: Use namedtuple to pack face data (?)
	# TODO: Difference between groups and objects (?)
	# TODO: Handle multiple groups properly (eg. g group1 group2 group3)

	raise NotImplementedError('Walk along. Nothing to see here.')

	data 	= defaultdict(list)	#
	path 	= parent(filename) 	# Path to containing folder



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
			face = [vertex.split('/') for vertex in values[1:].split()] # Extract indices for each vertex of the face
			data['faces'].append(([data['vertices'][int(vertex[0])+1] for vertex in face], 							# Vertices
								  [data['textures'][int(vertex[0])+1] for vertex in face] if face != '' else None, 	# Texture coordinates
								  [data['normals'][int(vertex[0])+1]  for vertex in face], 							# Normals
								   data['material'])) 																# Material

		elif values[0] == 'g':
			# Group
			# Stores lower and upper bounds (indices) of faces that belong to each group
			# We use an OrderedDict to store the groups since the beginning of a new group
			# determines the upper bound of the previous one.
			data['groups'] = data.get('groups', OrderedDict()) # TODO: Fix extraneous object creation (this is were lazy evaluation comes in handy... Oh well.)
			data['groups'].append()

		elif values[0] == 'o':
			# Object
			pass

		elif values[0] == 's':
			# Smooth shading
			pass

		elif values[0] == 'mtllib':
			# MTL library
			# Load materials defined in an external file
			data['mtl'] = parseMTL(join(path, values[1]))

		elif values[0] == 'usemtl':
			# Use MTL material
			data['material'] = data['mtl'][values[1]] # Current material

		else:
			# Unknown parameter encountered
			raise ValueError('\'{0}\' is not a recognised parameter.'.format(values[0]))

	return data



def createBuffers(filename, groups=True):
	
	'''
	Creates OpenGL buffers (one per group unless groups are disabled)

	'''

	# TODO: Look into all non-deprecated glEnable arguments, make sure they're handled properly

	raise NotImplementedError('Leave me alone. I\'m not ready yet')



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