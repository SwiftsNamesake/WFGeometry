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
#        - Instancing
#        - Include OBJ and MTL specs
#
# SPEC | - Exports a Model class and parsers for Wavefront MTL and OBJ files
#        - SI units by default
#        - https://en.wikipedia.org/wiki/Wavefront_.obj_file
#        - http://paulbourke.net/dataformats/mtl/



from OpenGL.GL import *									# ...
from collections import defaultdict, OrderedDict 		# ...
from utilities import parent, loadTexture 				# ...
from os.path import join								# ...
from SwiftUtils.SwiftUtils import Logger
# from itertools



logger = Logger('Models.py')



def parseMTL(filename):

	'''
	Parses an MTL file

	'''

	# TODO: Spec compliance
	# TODO: Blender compliance (MTL properties: Ns, Ni, d, illum)

	# From Wikipedia:
	# 0. Color on and Ambient off
	# 1. Color on and Ambient on
	# 2. Highlight on
	# 3. Reflection on and Ray trace on
	# 4. Transparency: Glass on, Reflection: Ray trace on
	# 5. Reflection: Fresnel on and Ray trace on
	# 6. Transparency: Refraction on, Reflection: Fresnel off and Ray trace on
	# 7. Transparency: Refraction on, Reflection: Fresnel on and Ray trace on
	# 8. Reflection on and Ray trace off
	# 9. Transparency: Glass on, Reflection: Ray trace off
	# 10. Casts shadows onto invisible surfaces

	#raise NotImplementedError('Walk along. Nothing to see here.')

	logger.log('Parsing MTL file: %s\n' % filename, kind='log')
	
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
		elif values[0] in ('Ns', 'Ni', 'd', 'Tr', 'illum'):
			# ?, ?, d(issolved), Tr(ansparent), ?
			# Dissolved and Transparent are synonyms
			logger.log('The valid MTL property \'{0}\' is currently unsupported by this parser and will have no effect.'.format(values[0]))
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
	# TODO: Handle convex polygons correctly

	# TODO: Handle 'off' instruction

	# TODO: Spec compliance
	# TODO: Blender compliance

	#raise NotImplementedError('Walk along. Nothing to see here.')

	logger.log('Parsing OBJ file: %s\n' % filename, kind='log')

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
			# TODO: Handle absent values for normals and texture coords
			# TODO: Handle vertex definitions of varying length (eg. 50/2/1 55/2 60)
			face = [vertex.split('/') for vertex in values[1:]] # Extract indices for each vertex of the face
			assert all(len(vertex) == len(face[0]) for vertex in face)
			# data['faces'].append(data[key][int(vertex[index]-1)] for index, attr in enumerate(('vertices', 'textures', 'normals') if len(face[0])>index) else None)
			# data['faces'].append(data['material'])
			data['faces'].append(([data['vertices'][int(vertex[0])-1] for vertex in face], 								 # Vertices
								  [data['textures'][int(vertex[1])-1] for vertex in face] if len(face[0])>1 else None,   # Texture coordinates
								  [data['normals'][int(vertex[2])-1]  for vertex in face] if len(face[0])>2 else None,   # Normals
								   data['material'])) 																	 # Material

		elif values[0] == 'g':
			# Group
			print('Adding group:', values[2])
			data['groups'].append((values[2], len(data['faces']))) # Group name with its lower bound (index into faces array)

		elif values[0] == 'o':
			# Object
			logger.log('Ignoring OBJ property \'{0}\''.format(values[0]))
			pass

		elif values[0] == 's':
			# Smooth shading
			logger.log('Ignoring OBJ property \'{0}\''.format(values[0]))
			pass

		elif values[0] == 'mtllib':
			# MTL library
			# Load materials defined in an external file
			data['mtl'] = parseMTL(join(path, values[1]))

		elif values[0] == 'usemtl':
			# Use MTL material
			# TODO: Handle usemtl (null)
			data['material'] = data['mtl'][values[1]] # Current material

		elif values[0] in ('l'):
			logger.log('Unsure how to handle property \'{0}\'.'.format(values[0]))
			pass
		else:
			# Unknown parameter encountered
			raise ValueError('\'{0}\' is not a recognised parameter.'.format(values[0]))

	# TODO: Handle data with no group definitions
	print('Groups', data['groups'])
	assert len(data['groups']) == 0 or data['groups'][0][1] == 0, 'All faces must belong to a group. (lowest index is {0})'.format(data['groups'][0][1])
	# Map group names to their lower and upper bounds
	# TODO: Refactor (or atleast explain) this line
	data['groups'] = { group : (low, upp) for (group, low), (_, upp) in zip(data['groups'], data['groups'][1:]+[(None, len(data['faces']))])}
	print('Groups', data['groups'])
	return data



def createBuffer(faces, data):

	'''
	Creates a single OpenGL buffer from the given faces.

	'''

	# TODO: Options (?)
	# TODO: Find a more suitable name (?)
	# TODO: Better documentation
	# TODO: Look into all non-deprecated glEnable arguments, make sure they're handled properly

	# NOTE: Fails unless OpenGL has been initialized

	glBuffer = glGenLists(1)
	glNewList(glBuffer, GL_COMPILE)
	glFrontFace(GL_CCW) # TODO: Cause of the colour bug (?)
	# glDisable(GL_CULL_FACE)
	# glCullFace(GL_BACK)

	for vertices, texcoords, normals, material in faces:

		# TODO: Handle all texture and colour types
		if (texcoords is not None) and ('map_Kd' in material):
			glEnable(GL_TEXTURE_2D)
			glBindTexture(GL_TEXTURE_2D, material['map_Kd']) # Use diffuse texture map if available
			# glColor(material['Ka']) # Use diffuse colour
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

	# TODO: Refactor (if statement looks ugly) (✓)
	# TODO: Should a dictionary be returned even when groups is False (?)
	#raise NotImplementedError('Leave me alone. I\'m not ready yet')

	data = parseOBJ(filename)

	if not groups:
		return {'model': createBuffer(data['faces'], data)}
	else:
		return { group : createBuffer(data['faces'][lower:upper], data) for group, (lower, upper) in data['groups'].items()}



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




if __name__ == '__main__':
	main()