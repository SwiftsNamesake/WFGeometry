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
from collections import defaultdict, namedtuple
from math import sin, cos, radians



def main():

	'''
	Docstring goes here

	'''

	dispatcher = bindEvents()
	dispatcher.mainloop()



class EventDispatcher:

	'''
	Introduces dynamic event binding to Pygame.

	Add, replace and query event handlers

	'''

	# TODO: Normalize event data (?)
	# TODO: Event aliases, tkinter-style event definitions (?)
	# eg. type=KEYDOWN key=LEFT
	# TODO: Hierachies of events, multiple handlers, replace or add
	# TODO: Pattern or Event class implementing aliases, comparisons, etc.
	# TODO: Queries
	# TODO: Composite events, control keys (eg. Ctrl+Alt+A, Mousemotion+Left mouse button)
	# TODO: Nested dicts or objects (?)
	# TODO: Handle polling as well (?)
	# TODO: Annotations, error handling

	def __init__(self):
		
		'''
		Docstring goes here

		'''

		# TODO: Is this the optimal data structure (w.r.t RAM and CPU)
		# TODO: Allow multiple handlers per pattern
		self.handlers 	= defaultdict(lambda: defaultdict(list)) # Maps event types to patterns and their respective handlers
		self.always 	= lambda event: None # Runs on each iteration of the main loop (configurable)
		self.debug 		= False

		self.keys = defaultdict(bool) # TODO: Use class with default __getattr__ instead (?)


	def DEBUG(self, *messages):

		'''
		Docstring goes here

		'''

		if self.debug: print(*messages)


	def setKey(self, event):

		'''
		Updates internal key state dictionary

		'''

		# TODO: Implement
		# TODO: Rename (?)

		self.keys[0] = event.type in (MOUSEBUTTONDOWN, KEYUP)


	def handle(self, event):
		
		'''
		Dispatches an event to all matching event handlers.

		'''

		for handler in self.query(event): #getattr(self, event.type)
			handler(event)
			self.DEBUG('Invalid handler type')


	def query(self, event):

		'''
		Retrieves all event handlers whose pattern
		matches that of the incoming event (cf. bind for details).

		'''

		# TODO: Use issubset for comparisons
		# TODO: Determine and - if necessary - improve performance
		# TODO: Complete overview of event types and related data
		match = frozenset((attr, getattr(event, attr)) for attr in ['type', 'key', 'button', 'rel'] if hasattr(event, attr))
		self.DEBUG(match)

		# TODO: Optionally return mapping between matching patterns and their corresponding handlers (?)
		return (handler for pattern, handlers in self.handlers[event.type].items() for handler in handlers if pattern.issubset(match))


	def bind(self, pattern, handler, replace=False):

		'''
		Binds a handler to an event pattern, optionally
		replacing any pre-existing handlers.

		A pattern is defined as a set of properties which an event must have
		to be considered a match (eg. event.type is KEYDOWN and event.key is K_LEFT)
		

		Returns an ID associated with the particular handler.

		'''

		# TODO: Implement replace option
		# TODO: Use issubset for comparisons
		# TDOO: Should the type property be mandatory (?)

		key = frozenset(pattern.items())
		self.DEBUG('Bound pattern:', key)
		self.handlers[pattern['type']][key].append(handler)
		return hash(key), id(handler)


	def mainloop(self):
		
		'''
		Docstring goes here

		'''

		self.clock = pygame.time.Clock()
		self.bind({'type': QUIT}, sys.exit)
		self.bind({'type': KEYDOWN, 'key': K_ESCAPE}, sys.exit)

		while True:
			self.clock.tick(30)
			for event in pygame.event.get():
				self.DEBUG(event)
				self.setKey(event)
				self.handle(event)
			self.always(event)



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



class Point:
	
	#Point = namedtuple('Point', 'x y z')
	# TODO: Extract Point definition (or find pre-existing)

	def __init__(self, x=0, y=0, z=0):
		self.x = x
		self.y = y
		self.z = z

	def __str__(self):
		return 'Point(x=%f, y=%f, z=%f)' % (self.x, self.y, self.z)



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
		print(model)


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
		# print('Rendering')
		
		# Undo transformations
		# glRotate(-self.rot.z, 0, 0, 1)
		# glRotate(-self.rot.y, 0, 1, 0)
		# glRotate(-self.rot.x, 1, 0, 0)
		# glTranslate(-self.pos.x, -self.pos.y, -self.pos.z) # TODO: Get rid of scaling


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



class Camera:

	'''
	Animation data
	
	'''
	
	def __init__(self):

		self.rx, self.ry, self.rz 		= 0, 0,   0 # Rotation
		self.tx, self.ty, self.tz 		= 0, 0, -55 # Translation
		self.drx, self.dry, self.drz 	= 0, 5,   0 # Rotation delta
		self.dtx, self.dty, self.dtz 	= 0, 0,   0 # Translation delta
		
		self.rotating 	 = False
		self.translating = False


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


	def animate(self):
		if self.rotating:
			self.rx += self.drx
			self.ry += self.dry
			self.rz += self.drz

		if self.translating:
			self.tx += self.dtx
			self.ty += self.dty
			self.tz += self.dtz



def bindEvents():

	'''
	Docstring goes here

	'''

	obj = InitGL()
	dispatcher = EventDispatcher()
	camera = Camera()
	avatar = Avatar(obj.gl_list)

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

		print('Pos: ', avatar.pos)

		camera.animate()
		avatar.animate(1.0) # TODO: Determine dt

		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
		glLoadIdentity()

		avatar.render()

		pygame.display.flip()


	def bindAvatarEvents():

		dispatcher.bind({'type': KEYDOWN, 'key': K_LEFT}, 	lambda event: avatar.set(ω=Point(y=5)))
		dispatcher.bind({'type': KEYDOWN, 'key': K_RIGHT}, 	lambda event: avatar.set(ω=Point(y=-5)))
		dispatcher.bind({'type': KEYUP, 'key': K_LEFT}, 	lambda event: avatar.set(ω=Point(y=0)))
		dispatcher.bind({'type': KEYUP, 'key': K_RIGHT}, 	lambda event: avatar.set(ω=Point(y=0)))

		# dispatcher.bind({'type': KEYDOWN, 'key': K_UP}, 	lambda event: avatar.set(v=Point(z=-3)))
		# dispatcher.bind({'type': KEYDOWN, 'key': K_DOWN}, 	lambda event: avatar.set(v=Point(z= 3)))
		dispatcher.bind({'type': KEYDOWN, 'key': K_DOWN}, 	lambda event: avatar.set(vf=-1))
		dispatcher.bind({'type': KEYDOWN, 'key': K_UP}, 	lambda event: avatar.set(vf= 1))
		dispatcher.bind({'type': KEYUP, 'key': K_DOWN}, 	lambda event: avatar.set(vf= 0))
		dispatcher.bind({'type': KEYUP, 'key': K_UP}, 		lambda event: avatar.set(vf= 0))


	def bindEvents():

		dispatcher.bind({'type': KEYDOWN, 'key': K_LEFT}, 	lambda event: camera.set(dry=5, rotating=True))
		dispatcher.bind({'type': KEYDOWN, 'key': K_RIGHT}, 	lambda event: camera.set(dry=-5, rotating=True))
		dispatcher.bind({'type': KEYUP, 'key': K_LEFT}, 	lambda event: camera.setRotating(False))
		dispatcher.bind({'type': KEYUP, 'key': K_RIGHT}, 	lambda event: camera.setRotating(False))

		dispatcher.bind({'type': KEYDOWN, 'key': K_UP}, 	lambda event: camera.set(dtz=-4, translating=True))
		dispatcher.bind({'type': KEYDOWN, 'key': K_DOWN}, 	lambda event: camera.set(dtz=4, translating=True))
		dispatcher.bind({'type': KEYUP, 'key': K_UP}, 		lambda event: camera.setTranslating(False))
		dispatcher.bind({'type': KEYUP, 'key': K_DOWN}, 	lambda event: camera.setTranslating(False))

		dispatcher.bind({'type': MOUSEBUTTONDOWN, 'button': 1}, lambda event: camera.set(drz=-4, rotating=True))
		dispatcher.bind({'type': MOUSEBUTTONDOWN, 'button': 3}, lambda event: camera.set(drz=4, rotating=True))
		dispatcher.bind({'type': MOUSEBUTTONUP, 'button': 1}, 	lambda event: camera.setRotating(False))
		dispatcher.bind({'type': MOUSEBUTTONUP, 'button': 3}, 	lambda event: camera.setRotating(False))

		dispatcher.bind({'type': MOUSEBUTTONDOWN, 'button': 4}, lambda event: camera.setTranslation(z=camera.tz+1.2))
		dispatcher.bind({'type': MOUSEBUTTONDOWN, 'button': 5}, lambda event: camera.setTranslation(z=camera.tz-1.2))

	dispatcher.always = [doAlways, AvatarMain][1]
	bindAvatarEvents()
	# bindEvents()

	return dispatcher



if __name__ == '__main__':
	main()