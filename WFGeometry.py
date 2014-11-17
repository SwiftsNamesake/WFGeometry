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
#
#
# SPEC | -
#        -



# Basic OBJ file viewer. needs objloader from:
#  http://www.pygame.org/wiki/OBJFileLoader
# LMB + move: rotate
# RMB + move: pan
# Scroll wheel: zoom in/out
import sys, pygame
from pygame.locals import *
from pygame.constants import *
from OpenGL.GL import *
from OpenGL.GLU import *

# Import object loader
from OBJFileLoader import *
from collections import namedtuple
from math import sin, cos, radians


from SwiftUtils.EventDispatcher import EventDispatcher
from Camera import Camera
from Utilities import Point, Rect



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
	obj = OBJ(['data/villa#2.obj', 'data/square.obj', 'data/cube.obj', 'data/hombre#2.obj'][3], swapyz=False)

	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	width, height = viewport
	gluPerspective(90.0, width/height, 1, 100.0)
	glEnable(GL_DEPTH_TEST)
	glMatrixMode(GL_MODELVIEW)

	return obj




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

		# print('Pos:', self.pos, 'Rot:', self.rot)
		# print('v:', self.v, 'dR:', self.ω)


	def render(self):

		'''
		Docstring goes here

		'''

		# Apply transformations (relative to modelview matrix)
		glTranslate(self.pos.x/20.0, self.pos.y/20.0, self.pos.z/20.0 - 2.5) # TODO: Get rid of scaling
		glRotate(self.rot.x, 1, 0, 0)
		glRotate(self.rot.y, 0, 1, 0)
		glRotate(self.rot.z, 0, 0, 1)

		# Render
		glCallList(self.model)

		# Undo transformations
		glRotate(-self.rot.z, 0, 0, 1)
		glRotate(-self.rot.y, 0, 1, 0)
		glRotate(-self.rot.x, 1, 0, 0)
		glTranslate(-self.pos.x, -self.pos.y, -self.pos.z) # TODO: Get rid of scaling


	def forward(self, v):
		
		'''
		Docstring goes here

		'''

		# TODO: Tweak velocity
		dx = sin(radians(self.rot.y))*v
		dz = cos(radians(self.rot.y))*v

		self.set(v=Point(x=dx, z=dz))


	def set(self, **kwargs):
		for key, val in kwargs.items():
			# print('Setting %s to %s' % (key, val))
			setattr(self, key, val)



def createGrid():
	
	'''
	Docstring goes here

	'''

	# TODO: Add options (eg. spacing, colours, origin)

	grid = glGenLists(1)
	glNewList(grid, GL_COMPILE)

	# X-axis
	with glDraw(GL_LINES):
		glColor(1.0, 0.0, 0.0, 1.0)
		glVertex(-200.0, 0.0, 0.0)
		glVertex( 200.0, 0.0, 0.0)

	with glDraw(GL_TRIANGLE_STRIP):
		glColor(1.0, 0.0, 0.0, 0.5)
		glVertex(-5.0, 0.0, -5.0)
		glVertex(-5.0, 0.0,  5.0)
		glVertex( 5.0, 0.0, -5.0)
		glVertex( 5.0, 0.0,  5.0)

	# Y-axis
	with glDraw(GL_LINES):
		glColor(0.0, 0.0, 1.0, 1.0)
		glVertex(0.0, -200.0, 0.0)
		glVertex(0.0,  200.0, 0.0)

	with glDraw(GL_TRIANGLE_STRIP):
		glColor(0.0, 1.0, 0.0, 0.5)
		glVertex(0.0, -5.0, -5.0)
		glVertex(0.0, -5.0,  5.0)
		glVertex(0.0,  5.0, -5.0)
		glVertex(0.0,  5.0,  5.0)

	# Z-axis
	with glDraw(GL_LINES):
		glColor(0.0, 1.0, 0.0, 1.0)
		glVertex(0.0, 0.0, -200.0)
		glVertex(0.0, 0.0,  200.0)

	with glDraw(GL_TRIANGLE_STRIP):
		glColor(0.0, 0.0, 1.0, 0.5)
		glVertex(-5.0, -5.0, 0.0)
		glVertex(-5.0,  5.0, 0.0)
		glVertex( 5.0, -5.0, 0.0)
		glVertex( 5.0,  5.0, 0.0)

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
		glTranslate(-1.5/(sx), 1.0/sy, -1.1/sx)
		glCallList(self.active.gl_list)



def bindEvents():

	'''
	Docstring goes here

	'''

	obj 		= InitGL()
	camera 		= Camera()
	avatar 		= Avatar(obj.gl_list)
	grid 		= createGrid()
	dispatcher 	= EventDispatcher()

	button = Widget(Rect(10, 10, 150, 80), lambda: None)


	def doAlways(event):

		# TODO: Keep FPS in check

		# camera.animate()
	
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
		glLoadIdentity()

		# Render object
		glTranslate(camera.tx/20.0, camera.ty/20.0, camera.tz/20.0)
		glRotate(camera.rx, 1, 0, 0)
		glRotate(camera.ry, 0, 1, 0)
		glRotate(camera.rz, 0, 0, 1)
		glCallList(obj.gl_list)

		if False:
			glTranslate(1.2, 0.0, 0.0)
			glRotate(-27, 0, 0, 1)
			glCallList(obj.gl_list)
			glRotate(27, 0, 0, 1)
			glTranslate(-1.2, 1.8, 0.0)
			glCallList(obj.gl_list)
			glTranslate(0.0, -2*1.8, 0.0)
			glCallList(obj.gl_list)

		pygame.display.flip()


	def AvatarMain(event):

		'''
		Executes on each iteration of the event loop.
		Test code for the Avatar class

		'''

		# print('Pos: ', avatar.pos)

		glEnable (GL_BLEND);
		glBlendFunc (GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);

		camera.animate()
		avatar.animate(1.0) # TODO: Determine dt

		glEnable(GL_BLEND)
		glAlphaFunc(GL_GREATER, 0.5)
		# glBlendFunc(GL_DST_ALPHA, GL_ONE)

		glClearColor(0.4, 0.4, 0.9, 1.0)

		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
		glLoadIdentity()
		camera.apply()

		glCallList(grid)
		avatar.render()

		# Draw widget
		button.render()

		pygame.display.flip()


	def bindAvatarEvents():

		dispatcher.bind({'type': MOUSEBUTTONDOWN, 'button': 1}, lambda event: button.pressIf(*event.pos))
		dispatcher.bind({'type': MOUSEBUTTONUP, 'button': 1}, lambda event: button.release())

		dispatcher.bind({'type': MOUSEMOTION, 'also': (K_RSHIFT,)}, lambda event: camera.set(ry=camera.ry+event.rel[0], rx=camera.rx+event.rel[1]))

		dispatcher.bind({'type': KEYDOWN, 'key': K_LEFT}, 	lambda event: avatar.set(ω=Point(y= 5)))
		dispatcher.bind({'type': KEYDOWN, 'key': K_RIGHT}, 	lambda event: avatar.set(ω=Point(y=-5)))
		dispatcher.bind({'type': KEYUP, 'key': K_LEFT}, 	lambda event: avatar.set(ω=Point(y= 0)))
		dispatcher.bind({'type': KEYUP, 'key': K_RIGHT}, 	lambda event: avatar.set(ω=Point(y= 0)))

		# dispatcher.bind({'type': KEYDOWN, 'key': K_UP}, 	lambda event: avatar.set(v=Point(z=-3)))
		# dispatcher.bind({'type': KEYDOWN, 'key': K_DOWN}, 	lambda event: avatar.set(v=Point(z= 3)))
		dispatcher.bind({'type': KEYDOWN, 'key': K_UP, 'mod': 0}, lambda event: avatar.set(vf= 1))
		dispatcher.bind({'type': KEYDOWN, 'key': K_UP, 'mod': 2}, lambda event: avatar.set(vf= 2))
		dispatcher.bind({'type': KEYDOWN, 'key': K_DOWN}, 	lambda event: avatar.set(vf=-1))
		dispatcher.bind({'type': KEYUP, 'key': K_UP}, 		lambda event: avatar.set(vf= 0))
		dispatcher.bind({'type': KEYUP, 'key': K_DOWN}, 	lambda event: avatar.set(vf= 0))

		# dispatcher.bind({'type': KEYDOWN, 'key': K_DOWN}, 	lambda event: avatar.set(vf=-1))
		# dispatcher.bind({'type': KEYDOWN, 'key': K_DOWN}, 	lambda event: avatar.set(vf=-1))
		# dispatcher.bind({'type': KEYDOWN, 'key': K_DOWN}, 	lambda event: avatar.set(vf=-1))


	def bindEvents():

		# NOTE: K_w is not the scancode for 'w'
		w, a, s, d = 17, 30, 31, 32

		dispatcher.bind({'type': KEYDOWN, 'unicode': 'w'}, 	lambda event: camera.set(dtz=-4, translating=True))
		dispatcher.bind({'type': KEYDOWN, 'unicode': 'a'}, 	lambda event: camera.set(dry=5, rotating=True))
		dispatcher.bind({'type': KEYDOWN, 'unicode': 's'}, 	lambda event: camera.set(dtz=4, translating=True))
		dispatcher.bind({'type': KEYDOWN, 'unicode': 'd'}, 	lambda event: camera.set(dry=-5, rotating=True))

		dispatcher.bind({'type': KEYUP, 'scancode': w}, lambda event: camera.setTranslating(False))
		dispatcher.bind({'type': KEYUP, 'scancode': a}, lambda event: camera.setRotating(False))
		dispatcher.bind({'type': KEYUP, 'scancode': s}, lambda event: camera.setTranslating(False))
		dispatcher.bind({'type': KEYUP, 'scancode': d}, lambda event: camera.setRotating(False))

		# dispatcher.bind({'type': MOUSEBUTTONDOWN, 'button': 1}, lambda event: camera.set(drz=-4, rotating=True))
		# dispatcher.bind({'type': MOUSEBUTTONDOWN, 'button': 3}, lambda event: camera.set(drz=4, rotating=True))
		# dispatcher.bind({'type': MOUSEBUTTONUP, 'button': 1}, 	lambda event: camera.setRotating(False))
		# dispatcher.bind({'type': MOUSEBUTTONUP, 'button': 3}, 	lambda event: camera.setRotating(False))

		dispatcher.bind({'type': MOUSEBUTTONDOWN, 'button': 4}, lambda event: camera.setTranslation(z=camera.tz+1.2))
		dispatcher.bind({'type': MOUSEBUTTONDOWN, 'button': 5}, lambda event: camera.setTranslation(z=camera.tz-1.2))

	dispatcher.always = [doAlways, AvatarMain][1]
	bindAvatarEvents()
	bindEvents()

	return dispatcher



if __name__ == '__main__':
	main()