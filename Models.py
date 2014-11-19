#
# Models.py
# Loading and managing 3D models
#
# Jonatan H Sundqvist
# November 18 2014
#

# TODO | - Define API (cf __all__)
#        - 3D vectors
#        - Handle units (conversion factor)
#        - Splines, bezier curves (advanced, low priority)
#        - Pre-existing parsing modules
#        - Make sure input files are closed properly
#        - Reference official specs, describe formats, ensure correctness
#        - Optimize, comment, refactor
#        - Use optional logger (cf. SwiftUtils.)
#
# SPEC | - Exports a Model class and parsers for Wavefront MTL and OBJ files
#        - SI units by default



from OpenGL.GL import *									# ...
from collections import defaultdict, OrderedDict 		# ...
from Utilities import parent, loadTexture 				# ...
from os.path import join								# ...
# from itertools



def parseMTL(filename):

	'''
	Parses an MTL file

	'''

	#raise NotImplementedError('Walk along. Nothing to see here.')

	print('Parsing OBJ file:', filename)
	
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

	#raise NotImplementedError('Walk along. Nothing to see here.')

	print('Parsing OBJ file:', filename)

	data 	= defaultdict(list)	#
	path 	= parent(filename) 	# Path to containing folder

	for line in filter(lambda ln: not (ln.isspace() or ln.startswith('#')), open(filename, 'r')):

		values = line.split()

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
			# TODO: Save indices instead (would probably save memory) (?)
			# TODO: Refactor (?)
			face = [vertex.split('/') for vertex in values[1:]] # Extract indices for each vertex of the face
			data['faces'].append(([data['vertices'][int(vertex[0])-1] for vertex in face], 								 # Vertices
								  [data['textures'][int(vertex[1])-1] for vertex in face] if face[0][1] != '' else None, # Texture coordinates
								  [data['normals'][int(vertex[2])-1]  for vertex in face] if face[0][2] != '' else None, # Normals
								   data['material'])) 																	 # Material

		elif values[0] == 'g':
			# Group
			data['groups'].append((values[1], len(data['faces']))) # Group name with its lower bound (index into faces array)

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
			# TODO: Handle usemtl (null)
			data['material'] = data['mtl'][values[1]] # Current material

		else:
			# Unknown parameter encountered
			raise ValueError('\'{0}\' is not a recognised parameter.'.format(values[0]))

	assert data['groups'][0][1] == 0, 'All faces must belong to a group. (lowest index is {0})'.format(data['groups'][0][1])
	data['groups'] = { group : (lower, upper) for (group, lower), (_, upper) in zip(data['groups'], data['groups'][1:])} # Map group names to their lower and upper bounds
	return data



def createBuffer(faces, data):

	'''
	Creates a single OpenGL buffer from the given faces.

	'''

	# TODO: Options (?)
	# TODO: Find a more suitable name (?)
	# TODO: Better documentation

	# NOTE: Fails unless OpenGL has been initialized

	glBuffer = glGenLists(1)
	glNewList(glBuffer, GL_COMPILE)
	glFrontFace(GL_CCW)

	for vertices, texcoords, normals, material in faces:

		# TODO: Handle all texture and colour types
		if (texcoords is not None) and ('map_Kd' in material):
			glEnable(GL_TEXTURE_2D)
			glBindTexture(GL_TEXTURE_2D, material['map_Kd']) # Use diffuse texture map if available
		else:
			glDisable(GL_TEXTURE_2D)
			glColor(material['Kd']) # Use diffuse colour

		glBegin(GL_POLYGON)

		for i, v in enumerate(vertices):
			if normals is not None:
				glNormal3fv(normals[i])
			if texcoords is not None:
				glTexCoord2fv(texcoords[i])
			glVertex3fv(v)

		glEnd()

	glDisable(GL_TEXTURE_2D)
	glEndList()

	return glBuffer



def createBuffers(filename, groups=True):
	
	'''
	Creates OpenGL buffers (one per group unless groups are disabled)

	'''

	# TODO: Look into all non-deprecated glEnable arguments, make sure they're handled properly
	# TODO: Refactor (if statement looks ugly)
	#raise NotImplementedError('Leave me alone. I\'m not ready yet')

	buffers = {}
	data 	= parseOBJ(filename)

	print(data['groups'])

	if groups:
		for group, (lower, upper) in data['groups']:
			buffers[group] = createBuffer(data['faces'][lower:upper], data)
	else:
		return createBuffer(data['faces'], data)

	return buffers



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

	from WFGeometry import InitGL
	
	hombre = createBuffers('data/hombre#2.obj', groups=False)
	# groups = createBuffers('data/hombre.obj', groups=False)

	# print(groups)
	print(hombre)




if __name__ == '__main__':
	main()