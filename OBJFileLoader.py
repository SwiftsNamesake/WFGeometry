#
# OBJFileLoader
# Loads Wavefront OBJ data
#
# Unknown (http://www.pygame.org/wiki/OBJFileLoader)
# October 11 2014
#
# Subsequent edits by Jonatan H Sundqvist
#

# TODO | - BUG: MTL references in the OBJ file are assumed to
#          be relative to the working dir, as opposed to the
#          parent directory of the OBJ file itself (✓)
#        - Entities support (eg. 'g Mesh1 roof1 Model'), possibly by storing slice indices for each object
#        - Units
#        - Properties (textures, colours, sides, area, centre point)
#
# SPEC | -
#        -



import pygame
from OpenGL.GL import *
from contextlib import contextmanager
from os.path import abspath, join, dirname, normpath


debug = False

def DEBUG(*messages):
	if debug:
		DEBUG(*messages)


@contextmanager
def glDraw(mode):

	'''
	Context manager for OpenGL primitive rendering, eg.
	with glDraw(GL_POLYGON):
		# Draw some polygons
		...
	'''
	
	glBegin(mode)
	yield
	glEnd()



def MTL(filename):

	'''
	Docstring goes here

	'''

	# TODO: Spec compliance
	# TODO: Blender compliance (Ns, Ni, illum)

	# TODO: Handle input file properly (close handle)

	contents 	= {}							# 
	mtl 	 	= None							# 
	path 		= dirname(abspath(filename)) 	# 
	
	for line in filter(lambda ln: not (ln.isspace() or ln.startswith('#')), open(filename, 'r')):

		values = line.split()
		
		if values[0] == 'newmtl':
			mtl = contents[values[1]] = {}
		elif mtl is None:
			raise ValueError('MTL file doesn\'t start with newmtl statement')
		elif values[0] == 'map_Kd':
			# load the texture referred to by this declaration
			mtl[values[0]] = values[1]
			surf = pygame.image.load(join(path, normpath(mtl['map_Kd']))) # TODO: Fix path bug (✓)
			image = pygame.image.tostring(surf, 'RGBA', True)
			ix, iy = surf.get_rect().size
			texid = mtl['texture_Kd'] = glGenTextures(1)
			DEBUG('texid', texid)
			glBindTexture(GL_TEXTURE_2D, texid)
			glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
			glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
			glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, ix, iy, 0, GL_RGBA, GL_UNSIGNED_BYTE, image)
		else:
			mtl[values[0]] = [float(v) for v in values[1:]] #map(float, values[1:])

	return contents


 
class OBJ:

	'''
	Docstring goes here

	'''

	def __init__(self, filename, swapyz=True):
		
		'''
		Loads a Wavefront OBJ file.

		'''
		
		self.vertices = []
		self.normals = []
		self.texcoords = []
		self.faces = []
 
		material = None

		self.path = dirname(abspath(filename))
		print(filename)
		for line in open(filename, 'r'):

			# Skip comments
			if line.startswith('#'):
				continue
			
			values = line.split()

			# Skip empty lines
			if not values:
				continue

			# DEBUG(values)

			if values[0] == 'v':
				v = [float(v) for v in values[1:4]] #map(float, values[1:4])
				if swapyz:
					v = v[0], v[2], v[1]
				self.vertices.append(v)
			elif values[0] == 'vn':
				v = [float(v) for v in values[1:4]] #map(float, values[1:4])
				if swapyz:
					v = v[0], v[2], v[1]
				self.normals.append(v)
			elif values[0] == 'vt':
				#self.texcoords.append(map(float, values[1:3]))
				self.texcoords.append([float(v) for v in values[1:3]])
			elif values[0] in ('usemtl', 'usemat'):
				material = values[1]
				DEBUG(material)
			elif values[0] == 'mtllib':
				DEBUG('Values:', values)
				self.mtl = MTL(join(self.path, normpath(values[1]))) # TODO | Fix relative path bug (✓)
			elif values[0] == 'f':
				face = []
				texcoords = []
				norms = []
				for v in values[1:]:
					w = v.split('/')
					face.append(int(w[0]))
					if len(w) >= 2 and len(w[1]) > 0:
						texcoords.append(int(w[1]))
					else:
						texcoords.append(0)
					if len(w) >= 3 and len(w[2]) > 0:
						norms.append(int(w[2]))
					else:
						norms.append(0) # Append 0 if normal index is missing
				self.faces.append((face, norms, texcoords, material))
 
		self.gl_list = glGenLists(1)
		glNewList(self.gl_list, GL_COMPILE)
		glEnable(GL_TEXTURE_2D) # TODO: Determine why this is required (even for diffuse colours)
		glFrontFace(GL_CCW)		# TODO: Determine what this does

		for face in self.faces:
			vertices, normals, texture_coords, material = face
 
			mtl = self.mtl[material]

			if 'texture_Kd' in mtl: # TODO: Possible cause of the texture-bug (?)
				# Use diffuse texmap
				glBindTexture(GL_TEXTURE_2D, mtl['texture_Kd'])
			else:
				# Just use diffuse colour
				glColor(*mtl['Kd'])
 
			glBegin(GL_POLYGON)

			for i, v in enumerate(vertices):
				if normals[i] > 0:
					glNormal3fv(self.normals[normals[i] - 1])
				if texture_coords[i] > 0:
					glTexCoord2fv(self.texcoords[texture_coords[i] - 1])
				glVertex3fv(self.vertices[vertices[i] - 1])

			glEnd()

		glDisable(GL_TEXTURE_2D)
		glEndList()