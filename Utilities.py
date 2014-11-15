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


	def width(self):
		return self.right - self.left

	def height(self):
		return self.bottom - self.top

	def within(self, x, y):
		return (self.left <= x <= self.right) and (self.top <= y <= self.bottom)