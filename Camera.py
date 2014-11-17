#
# Camera.py
# Utility class for manipulating the OpenGL modelview matrix
#
# Jonatan H Sundqvist
# November 14 2014
#

# TODO | -
#        -
#
# SPEC | -
#        -



from OpenGL.GL import *
from SwiftUtils import Console, addLogger



@addLogger
class Camera:

	'''
	Animation data
	
	'''
	
	def __init__(self):

		self.rx, self.ry, self.rz 		= 0, 0, 0 # Rotation
		self.tx, self.ty, self.tz 		= 0, 0, 0 # Translation
		self.drx, self.dry, self.drz 	= 0, 0, 0 # Rotation delta
		self.dtx, self.dty, self.dtz 	= 0, 0, 0 # Translation delta
		
		self.rotating 	 = False
		self.translating = False

		self.DEBUG = False


	def set(self, **kwargs):
		for key, val in kwargs.items():
			setattr(self, key, val)


	def rotate(self, x=0, y=0, z=0):
		self.set(drx=x, dry=y, drz=z, rotating=True)


	def setRotation(self, x=0, y=0, z=0):
		self.set(rx=x, ry=y, rz=z)


	def setTranslation(self, x=0, y=0, z=0):
		self.set(tx=x, ty=y, tz=z)


	def translate(self, x=0, y=0, z=0):
		self.set(dtx=x, dty=y, dtz=z, translating=True)


	def setRotating(self, rotating):
		self.set(rotating=rotating)


	def setTranslating(self, translating):
		self.set(translating=translating)


	def apply(self):
		
		'''
		Apply transformations

		'''

		glTranslate(self.tx, self.ty, self.tz)
		glRotate(self.rx, 1, 0, 0)
		glRotate(self.ry, 0, 1, 0)
		glRotate(self.rz, 0, 0, 1)


	def animate(self):

		if self.rotating:
			self.rx += self.drx
			self.ry += self.dry
			self.rz += self.drz

		if self.translating:
			self.tx += self.dtx
			self.ty += self.dty
			self.tz += self.dtz


	def __str__(self):

		'''
		Docstring goes here

		'''

		return 'Camera | rot x={rx} y={ry} z={rz} | pos x={tx} y={ty} z={tz}'.format(rx=self.rx, ry=self.ry, rz=self.rz, tx=self.tx, ty=self.ty, tz=self.tz)