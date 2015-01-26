#
# Camera.py
# Utility class for manipulating the OpenGL modelview matrix
#
# Jonatan H Sundqvist
# November 14 2014
#

# TODO | - Units
#        - Coalesce setters and getters, simplify API (?)
#
# SPEC | -
#        -



from OpenGL.GL import *
from SwiftUtils import Console, addLogger
from utilities import Point



@addLogger
class Camera:

	'''
	Animation data
	
	'''
	
	def __init__(self):

		self.pos = Point(0, 0, 0) # Translation
		self.rot = Point(0, 0, 0) # Rotation
		self.v   = Point(0, 0, 0) # Velocity
		self.ω   = Point(0, 0, 0) # Angular velocity
		
		self.rotating 	 = False
		self.translating = False

		self.DEBUG = False


	def set(self, attr, x=None, y=None, z=None):

		'''
		Docstring goes here

		'''

		# TODO: This API method is subject to change

		getattr(self, attr).set(x, y, z) #

		# for key, val in kwargs.items():
			# setattr(self, key, val)


	def nudge(self, attr, x=None, y=None, z=None):

		'''
		Increments a given attribute

		'''

		attr = getattr(self, attr) 
		attr += Point(x or attr.x, y or attr.y, z or attr.z)


	def rotate(self, x=None, y=None, z=None):

		'''
		Rotates the camera from its current orientation

		'''

		self.nudge('rot', x, y, z)
		self.rotating = True # TODO: Is this necessary?


	def setRotation(self, x=None, y=None, z=None):

		'''
		Sets an absolute rotation

		'''

		self.rot.set(x, y, z)


	def setTranslation(self, x=None, y=None, z=None):

		'''
		Sets an absolute translation

		'''

		self.pos.set(x, y, z)



	def translate(self, x=None, y=None, z=None):

		'''
		Translates the camera from its current position

		'''

		self.nudge('pos', x, y, z)
		self.translating = True # TODO: Is this necessary (animation flags in general)?


	def setVelocity(self, x=None, y=None, z=None):

		'''
		Sets an absolute velocity

		'''

		self.set('v', x, y, z)
		self.translating = True



	def accelerate(self, x=None, y=None, z=None):

		'''
		Increases the velocity of the camera

		'''

		self.nudge('v', x, y, z)
		self.translating = True



	def setRotating(self, rotating):
		self.set(rotating=rotating)


	def setTranslating(self, translating):
		self.set(translating=translating)


	def apply(self):
		
		'''
		Apply transformations

		'''

		# TODO: Decide in which order the transformations should be applied
		glTranslate(*self.pos)
		glRotate(self.rot.x, 1, 0, 0)
		glRotate(self.rot.y, 0, 1, 0)
		glRotate(self.rot.z, 0, 0, 1)


	def animate(self, dt=1):

		# TODO: Take time delta into account (?)

		if self.rotating:
			self.rot += self.ω

		if self.translating:
			self.pos += self.v


	def __str__(self):

		'''
		Docstring goes here

		'''

		return 'Camera | rot x={rx} y={ry} z={rz} | pos x={tx} y={ty} z={tz}'.format(rx=self.rx, ry=self.ry, rz=self.rz, tx=self.tx, ty=self.ty, tz=self.tz)



def main():
	
	'''
	Docstring goes here

	'''

	camera = Camera()


if __name__ == '__main__':
	main()