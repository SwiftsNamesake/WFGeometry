#
# WFGeometry.py
# Loading WaveFront OBJ data with Python
#
# Unknown (http://www.pygame.org/wiki/OBJFileLoader)
# October 11 2014
#
# Subsequent edits by Jonatan H Sundqvist
#

# TODO | - Context manager for glBegin/glEnd (with statement) (✓)
#        - Event handlers (✓)
#        - Matrix helper functions (stack?) (cf. numpy)
#        - Platformer, loading maps, triggers
#        - 3D Widgets
#        - Performant 3D vectors (cf. numpy, magic methods, __slots__, namedtuple, type=...)
#
# SPEC | - 
#        - 



import sys, pygame
from pygame.locals import *
from pygame.constants import *
from OpenGL.GL import *
from OpenGL.GLU import *

from models import createBuffers	# 
from collections import namedtuple	# 
from math import sin, cos, radians	# 
from random import choice, random, randint

from SwiftUtils.EventDispatcher import EventDispatcher
from camera import Camera
from utilities import Point, Rect, glDraw



def main():

	'''
	Docstring goes here

	'''

	dispatcher = bindEvents()
	dispatcher.mainloop()



def InitGL():
	
	'''
	Initialize OpenGL

	'''

	pygame.init()

	pygame.display.set_caption('Los Hombres con sombreros')
	pygame.display.set_icon(pygame.image.load('C:/Users/Jonatan/Desktop/Python/resources/images/paintings/mont-sainte-victoire-3.jpg'))

	viewport = (int(720*2), int(480*2))
	hx = viewport[0]/2
	hy = viewport[1]/2
	srf = pygame.display.set_mode(viewport, OPENGL | DOUBLEBUF)

	glLightfv(GL_LIGHT0, GL_POSITION,  (-40, 200, 100, 0.0))
	glLightfv(GL_LIGHT0, GL_AMBIENT, (0.2, 0.2, 0.2, 1.0))
	glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.5, 0.5, 0.5, 1.0))
	glEnable(GL_LIGHT0)
	glEnable(GL_LIGHTING)
	glEnable(GL_COLOR_MATERIAL)
	glEnable(GL_DEPTH_TEST)
	glShadeModel(GL_SMOOTH)           # Most obj files expect to be smooth-shaded

	# Load object after pygame init
	# obj = OBJ(sys.argv[1], swapyz=True)
	# TODO: Fix access violation bug (occurs whenever more than one OBJ is rendered)
	# TODO: Separate context creation and data loading
	# models = [OBJ(fn, swapyz=False) for fn in ('data/villa.obj', 'data/cube.obj', 'data/hombre#2.obj')[-3:-2]]
	models = createBuffers('data/hombre.obj', groups=True)

	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	width, height = viewport
	gluPerspective(90.0, width/height, 1, 100.0)
	glEnable(GL_DEPTH_TEST)
	glMatrixMode(GL_MODELVIEW)

	return models



class Avatar:

	'''
	Docstring goes here

	'''

	def __init__(self, model, x=0, y=0, z=0, rx=0, ry=0, rz=0, dx=0, dy=0, dz=0, drx=0, dry=0, drz=0):
		
		'''
		Docstring goes here

		'''

		# TODO: Nomenclature (dx or vx, ω or dr, etc)
		# TODO: Verify units

		self.pos = Point(x, y, z)		# Meters
		self.rot = Point(rx, ry, rz)	# Degrees

		self.v = Point(dx, dy, dz)		# Meters per second
		self.ω = Point(drx, dry, drz)	# Degrees per second

		self.vf = 0 #  Forward velocity

		self.model = model # Currently an OpenGL list

		self.armRot = Point(0, 0, 0)
		self.darmRot = 2


	def animate(self, dt):

		'''
		Docstring goes here

		'''

		self.pos.x += self.v.x * dt
		self.pos.y += self.v.y * dt
		self.pos.z += self.v.z * dt

		self.rot.x += self.ω.x * dt
		self.rot.y += self.ω.y * dt
		self.rot.z += self.ω.z * dt

		self.forward(self.vf) # Animate forwards

		self.armRot.z += self.darmRot*dt
		self.darmRot *= (-1) * (abs(self.armRot.z) > 15)


	def renderPart(self, part, angle, pivot, vector):
		
		'''
		Docstring goes here

		'''

		# TODO: Comment, explain arguments, write docstring

		# 
		glTranslate(*pivot)
		glRotate(angle, *vector)
		glTranslate(-pivot[0], -pivot[1], -pivot[2])
		glCallList(self.model[part])

		# Reset matrix
		glTranslate(*pivot)
		glRotate(-angle, *vector)
		glTranslate(-pivot[0], -pivot[1], -pivot[2])



	def applyTransformations(self, undo=False):

		'''
		Docstring goes here

		'''

		if not undo:
			glTranslate(self.pos.x, self.pos.y, self.pos.z) # TODO: Get rid of scaling
			glRotate(self.rot.x, 1, 0, 0)
			glRotate(self.rot.y, 0, 1, 0)
			glRotate(self.rot.z, 0, 0, 1)
		else:
			glRotate(-self.rot.z, 0, 0, 1)
			glRotate(-self.rot.y, 0, 1, 0)
			glRotate(-self.rot.x, 1, 0, 0)
			glTranslate(-self.pos.x, -self.pos.y, -self.pos.z) # TODO: Get rid of scaling


	def render(self):

		'''
		Docstring goes here

		'''

		# Apply transformations (relative to modelview matrix)
		self.applyTransformations()

		# Render
		#for part, data in self.model.items():
		#	glCallList(data)
		for part in ('Torso1', 'leg1', 'leg2'):
			glCallList(self.model[part])

		# TODO: Rotate about a pivot (✓)
		# TODO: Arbitrary vector rotations

		self.renderPart('arm1',  self.armRot.z, ( 0.317, 1.76, 0), (0, 0, 1)) # Draw first arm
		self.renderPart('arm2', -self.armRot.z, (-0.317, 1.76, 0), (0, 0, 1)) # Draw second arm

		for part in ('head1', 'eye1', 'eye2', 'mouth1', 'nose1', 'hat1'):
			self.renderPart(part, self.armRot.z, (0.0, 0.0, 0.0), (0, 1, 0))

		# Undo transformations
		self.applyTransformations(undo=True)


	def forward(self, v):
		
		'''
		Docstring goes here

		'''

		if v == 0.0:
			return

		# TODO: Tweak velocity
		dx = sin(radians(self.rot.y))*v
		dz = cos(radians(self.rot.y))*v

		self.set(v=Point(x=dx, z=dz))


	def set(self, **kwargs):

		'''
		Docstring goes here

		'''

		for key, val in kwargs.items():
			setattr(self, key, val)



def createGrid():
	
	'''
	Docstring goes here

	'''

	# TODO: Add options (eg. spacing, colours, origin)

	width, height = 10, 10

	grid = glGenLists(1)
	glNewList(grid, GL_COMPILE)

	# X-axis
	with glDraw(GL_LINES):
		glColor(1.0, 0.0, 0.0, 1.0)
		glVertex(-200.0, 0.0, 0.0)
		glVertex( 200.0, 0.0, 0.0)

	with glDraw(GL_TRIANGLE_STRIP):
		glColor(1.0, 0.0, 0.0, 0.5)
		glVertex(-width, 0.0, -height)
		glVertex(-width, 0.0,  height)
		glVertex( width, 0.0, -height)
		glVertex( width, 0.0,  height)

	# Y-axis
	with glDraw(GL_LINES):
		glColor(0.0, 0.0, 1.0, 1.0)
		glVertex(0.0, -200.0, 0.0)
		glVertex(0.0,  200.0, 0.0)

	with glDraw(GL_TRIANGLE_STRIP):
		glColor(0.0, 1.0, 0.0, 0.5)
		glVertex(0.0, -width, -height)
		glVertex(0.0, -width,  height)
		glVertex(0.0,  width, -height)
		glVertex(0.0,  width,  height)

	# Z-axis
	with glDraw(GL_LINES):
		glColor(0.0, 1.0, 0.0, 1.0)
		glVertex(0.0, 0.0, -200.0)
		glVertex(0.0, 0.0,  200.0)

	with glDraw(GL_TRIANGLE_STRIP):
		glColor(0.0, 0.0, 1.0, 0.5)
		glVertex(-width, -height, 0.0)
		glVertex(-width,  height, 0.0)
		glVertex( width, -height, 0.0)
		glVertex( width,  height, 0.0)

	glEndList()

	return grid



class Widget:

	'''
	OpenGL widgets

	'''

	def __init__(self, box, command):
		
		'''
		Docstring goes here

		'''

		self.box = box
		self.command = command
		self.pressed = False # self.state

		self.vPressed 	= OBJ('data/buttonP.obj')
		self.vReleased 	= OBJ('data/buttonR.obj')
		self.active = self.vPressed if self.pressed else self.vReleased


	def pressIf(self, x, y):
		if self.box.within(x, y):
			self.press()


	def press(self):
		self.pressed = True
		self.active = self.vPressed
		self.command() # TODO: Generate event instead (?)


	def release(self):
		self.pressed = True
		self.active = self.vReleased


	def render(self):

		width, height = (int(720*2), int(480*2)) # TODO: Make more robust
		
		sx = self.box.width()*1/width
		sy = self.box.height()*1/height
		
		# print(self.box.width(), self.box.height())
		
		glLoadIdentity() # Don't apply camera transformations
		glScale(sx, sy, sx)
		glTranslate(-1.5/sx, 1.0/sy, -1.1/sx)
		glCallList(self.active.gl_list)



def bindEvents():

	'''
	Docstring goes here

	'''

	models 		= InitGL()
	camera 		= Camera()
	avatar 		= Avatar(models, x=2.0, z=-2.0)
	grid 		= createGrid()
	dispatcher 	= EventDispatcher()

	scales = [[1+randint(0, 20)*0.05 for y in range(20)] for x in range(10)]
	# button = Widget(Rect(10, 10, 150, 80), lambda: None)


	def AvatarMain(event):

		'''
		Executes on each iteration of the event loop.
		Test code for the Avatar class

		'''

		# print('Pos: ', avatar.pos)
		# TODO: Keep FPS in check

		glEnable (GL_BLEND);
		glBlendFunc (GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);

		camera.animate()
		avatar.animate(1.0) # TODO: Determine dt

		glEnable(GL_BLEND)
		glAlphaFunc(GL_GREATER, 0.5)

		glClearColor(0.4, 0.4, 0.9, 1.0)

		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
		glLoadIdentity()
		camera.apply()

		glCallList(grid)

		for i in range(10):
			glTranslate(2.2, 0.0, 0.0)
			for j in range(10):
				sc = scales[i][j]
				glTranslate(0.0, 0.0, 2.2)
				glScale(sc, sc, sc)
				avatar.render()
				glScale(1/sc, 1/sc, 1/sc)
			glTranslate(0.0, 0.0, -10*2.2)

		# Draw widget
		# button.render()

		pygame.display.flip()


	def bindAvatarEvents():

		# dispatcher.bind({'type': MOUSEBUTTONDOWN, 'button': 1}, lambda event: button.pressIf(*event.pos))
		# dispatcher.bind({'type': MOUSEBUTTONUP, 'button': 1}, lambda event: button.release())

		for pattern, handler in (
			#
			# ({'type': MOUSEMOTION, 'also': (K_RSHIFT,)}, lambda event: camera.set(ry=camera.ry+event.rel[0], rx=camera.rx+event.rel[1])),
			({'type': MOUSEMOTION}, lambda event: camera.set(ry=camera.ry+event.rel[0]*pygame.mouse.get_pressed()[0], rx=camera.rx+event.rel[1]*pygame.mouse.get_pressed()[0])),
			({'type': KEYDOWN, 'key': K_LEFT}, lambda event: avatar.set(ω=Point(y= 5))),
			({'type': KEYDOWN, 'key': K_RIGHT}, lambda event: avatar.set(ω=Point(y=-5))),
			({'type': KEYUP, 'key': K_LEFT}, lambda event: avatar.set(ω=Point(y= 0))),
			({'type': KEYUP, 'key': K_RIGHT}, lambda event: avatar.set(ω=Point(y= 0))),

			#
			({'type': KEYDOWN, 'key': K_UP, 'mod': 0}, lambda event: avatar.set(vf= 0.05)),
			({'type': KEYDOWN, 'key': K_UP, 'mod': 2}, lambda event: avatar.set(vf= 0.1)),
			({'type': KEYDOWN, 'key': K_DOWN}, lambda event: avatar.set(vf=-0.05)),
			({'type': KEYUP, 'key': K_UP}, lambda event: avatar.set(vf= 0)),
			({'type': KEYUP, 'key': K_DOWN}, lambda event: avatar.set(vf= 0)),

			({'type': KEYDOWN, 'key': K_SPACE}, lambda event: avatar.set(v=Point(y=0.1))),
			({'type': KEYUP, 'key': K_SPACE}, lambda event: avatar.set(v=Point(y=-0.1)))):
			dispatcher.bind(pattern, handler)


	def bindEvents():

		# NOTE: K_w is not the scancode for 'w'
		w, a, s, d = 17, 30, 31, 32

		dispatcher.bind({'type': KEYDOWN, 'unicode': 'w'}, 	lambda event: camera.set(dtz=4, translating=True))
		dispatcher.bind({'type': KEYDOWN, 'unicode': 'a'}, 	lambda event: camera.set(dry=5, rotating=True))
		dispatcher.bind({'type': KEYDOWN, 'unicode': 's'}, 	lambda event: camera.set(dtz=-4, translating=True))
		dispatcher.bind({'type': KEYDOWN, 'unicode': 'd'}, 	lambda event: camera.set(dry=-5, rotating=True))

		dispatcher.bind({'type': KEYUP, 'scancode': w}, lambda event: camera.setTranslating(False))
		dispatcher.bind({'type': KEYUP, 'scancode': a}, lambda event: camera.setRotating(False))
		dispatcher.bind({'type': KEYUP, 'scancode': s}, lambda event: camera.setTranslating(False))
		dispatcher.bind({'type': KEYUP, 'scancode': d}, lambda event: camera.setRotating(False))

		dispatcher.bind({'type': MOUSEBUTTONDOWN, 'button': 4}, lambda event: camera.setTranslation(z=camera.tz+1.2))
		dispatcher.bind({'type': MOUSEBUTTONDOWN, 'button': 5}, lambda event: camera.setTranslation(z=camera.tz-1.2))

	dispatcher.always = AvatarMain
	bindAvatarEvents()
	bindEvents()

	return dispatcher



if __name__ == '__main__':
	main()