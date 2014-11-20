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



class Point:
	
	#Point = namedtuple('Point', 'x y z')
	# TODO: Extract Point definition (or find pre-existing)

	def __init__(self, x=0, y=0, z=0):
		self.x = x
		self.y = y
		self.z = z

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

	@property
	def within(self, x, y):
		return (self.left <= x <= self.right) and (self.top <= y <= self.bottom)