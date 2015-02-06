#
# Utilities.py
# Utilities for WaveFront geometry project
#
# Jonatan H Sundqvist
# November 14 2014
#

# TODO | -
#        -
#
# SPEC | -
#        -



from pygame import image 					# ...
from contextlib import contextmanager 		# ...
from os.path import abspath, join, dirname 	# ...
from OpenGL.GL import *						# ...
from math import sqrt



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



def parent(filename):

	'''
	Retrieves parent directory of the specified file

	'''

	return dirname(abspath(filename))



def loadTexture(filename):

	'''
	Loads an OpenGL texture

	'''

	surface = image.load(filename)
	texture = image.tostring(surface, 'RGBA', True)
	w, h 	= surface.get_rect().size

	ID = glGenTextures(1)

	glBindTexture(GL_TEXTURE_2D, ID)
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
	glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, w, h, 0, GL_RGBA, GL_UNSIGNED_BYTE, texture)

	return ID



class MatrixStack:

	'''
	Docstring goes here

	'''

	def __init__(self, matrices=[]):
		
		'''
		Docstring goes here

		'''

		self.stack = matrices


	def apply(self):
		
		'''
		Docstring goes here

		'''

		pass


	def pop(self):

		'''
		Docstring goes here

		'''

		pass


	def push(self):

		'''
		Docstring goes here

		'''

		pass



class Point(object):
	
	#Point = namedtuple('Point', 'x y z')
	# TODO: Extract Point definition (or find pre-existing)
	# TODO: Optimise (cf __slots__)
	# TODO: Conversions (eg. asTuple) (?)

	def __init__(self, x=0, y=0, z=0):
		self.x = x
		self.y = y
		self.z = z


	def set(self, x=None, y=None, z=None):

		'''
		Docstring goes here

		'''

		self.x = x or self.x # 
		self.y = y or self.y # 
		self.z = z or self.z # 


	def euclidean(self, other):

		'''
		Euclidean distance between two points (dot-product)

		'''

		return sqrt((other.x-self.x)**2 + (other.y-self.y)**2 + (other.z-self.z)**2)


	def rotate(self, x, y, z):

		'''
		Rotation

		'''

		raise NotImplementedError


	def __mult__(self, other):

		'''
		Scalar multiplication

		'''

		# TODO: Optimise, separate scalar and vector multiplication
		# TODO: Find proper mathematical terms
		# TODO: Correctness

		return Point(self.x*other, self.y*other, self.z*other)


	def __add__(self, other):

		'''
		Adds two vectors (Points) component-wise

		'''

		return Point(self.x+other.x, self.y+other.y, self.z+other.z)


	def __iadd__(self, other):

		'''
		Increments each component by the value of the corresponding component of the right-hand operand
		(destructive addition, cf. self.__add__)

		'''

		self.x += other.x
		self.y += other.y
		self.z += other.z

		return self


	def __iter__(self):

		'''
		Docstring goes here

		'''

		for c in (self.x, self.y, self.z):
			yield c


	def __str__(self):

		return 'Point(x=%f, y=%f, z=%f)' % (self.x, self.y, self.z)



class Rect:

	'''
	Docstring goes here

	'''

	def __init__(self, left=0, top=0, right=0, bottom=0):
		
		'''
		Docstring goes here

		'''

		self.left	= left
		self.top	= top
		self.right	= right
		self.bottom	= bottom

	@property
	def width(self):
		return self.right - self.left

	@property
	def height(self):
		return self.bottom - self.top

	def within(self, x, y):
		return (self.left <= x <= self.right) and (self.top <= y <= self.bottom)



def plot(f, domain, resolution, scale):
	
	'''
	Plots a mathematical function in 3D space

	'''

	# TODO: Options, complex numbers, 3D plots, plot lines

	pass



def visualize(vector):

	'''
	Docstring goes here

	'''

	pass


class Vector(object):

	'''
	Docstring goes here.

	'''

	# TODO: Numpy, matrix operations, performance
	# TODO: Magic method helpers
	# TODO: __slots__
	# TODO: Sigma value to prevent floating-point errors (?)

	# type = float

	def __init__(self, x=0, y=0, z=0):
		
		'''
		Docstring goes here.

		'''

		self.x = x
		self.y = y
		self.z = z


	def __repr__(self):
		pass


	def __str__(self):
		pass


	def __eq__(self, other):
		
		'''
		Docstring goes here

		'''

		# TODO: Sigma value to prevent floating-point errors (?)
		return (self.x == other.x) and (self.y == other.y) and (self.z == other.z)


	def __add__(self, other):

		'''
		Docstring goes here

		'''

		# super(self)
		return Vector(self.x + other.x, self.y + other.y, self.z + other.z)


	def __sub__(self, other):

		'''
		Docstring goes here

		'''

		return Vector(self.x - other.x, self.y - other.y, self.z - other.z)


	def __abs__(self):
		
		'''
		Docstring goes here

		'''

		return None


	def __mul__(self):
		
		'''
		Docstring goes here

		'''

		return None
