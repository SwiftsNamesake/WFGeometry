#
# model.py
# description
#
# Jonatan H Sundqvist
# January 25 2015
#

# TODO | - Manipulating and interacting with vertices
#        - Queries, intersections, etc.
#        - Anaglyph 3D
#
# SPEC | -
#        -



from utilities import Point
from models import parseOBJ, createBuffers

from OpenGL.GL import *
from OpenGL.GLU import *



class Model(object):

	'''
	Wraps an OpenGL buffer

	'''

	def __init__(self, filename, groups, origin=(0,0,0)):
		
		'''
		Docstring goes here

		'''

		#
		self.pos = Point(*origin)
		self.rot = Point(0, 0, 0)

		#
		self.vertices = parseOBJ(filename)
		self.buffers  = createBuffers(data=self.vertices, groups=groups)
		self.dirty    = False # Dirty vertices flag


	def render(self):
		
		'''
		Docstring goes here

		'''

		self.apply() 			# Apply model view transforms

		# Order is not guaranteed
		for group, buff in self.buffers.items():
			glCallList(buff) # Render


	def apply(self):
		
		'''
		Apply matrix transformations
		
		'''

		# TODO: Decide in which order the transformations should be applied
		glTranslate(*self.pos)
		glRotate(self.rot.x, 1, 0, 0)
		glRotate(self.rot.y, 0, 1, 0)
		glRotate(self.rot.z, 0, 0, 1)


	def animate(self, dt):
		
		'''
		Docstring goes here

		'''

		pass



def main():
	
	'''
	Docstring goes here

	'''

	pass



if __name__ == '__main__':
	main()