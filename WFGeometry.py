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
#        - 
#
# SPEC | -
#        -



from collections import defaultdict



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


	def DEBUG(self, *messages):

		'''
		Docstring goes here

		'''

		if self.debug: print(*messages)


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
				self.handle(event)
			self.always(event)



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

# IMPORT OBJECT LOADER
from OBJFileLoader import *



def InitGL():
	
	'''
	Initialize OpenGL

	'''

	pygame.init()
	viewport = (800,600)
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
	obj = OBJ(['data/villa.obj', 'data/square.obj', 'data/cube.obj', 'data/hombre#2.obj'][3], swapyz=False)

	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	width, height = viewport
	gluPerspective(90.0, width/height, 1, 100.0)
	glEnable(GL_DEPTH_TEST)
	glMatrixMode(GL_MODELVIEW)

	return obj



def mainloop():

	clock = pygame.time.Clock()
	 
	rx, ry = (0,0)
	tx, ty = (0,0)
	zpos = 5
	rotate = move = False
	
	obj = InitGL()

	while 1:
		clock.tick(30)
		for e in pygame.event.get():
			if e.type == QUIT:
				sys.exit()
			elif e.type == KEYDOWN:
				if e.key == K_ESCAPE:
					sys.exit()
				elif e.key in (K_LEFT, K_RIGHT):
					print('Key rotation')
					rotate = True
					i, j = (2 if e.key == K_LEFT else -2, 0)
			elif e.type == KEYUP:
				if e.key in (K_LEFT, K_RIGHT):
					rotate = False
			elif e.type == MOUSEBUTTONDOWN:
				if e.button == 4: zpos = max(1, zpos-1)
				elif e.button == 5: zpos += 1
				elif e.button == 1: rotate = True
				elif e.button == 3: move = True
			elif e.type == MOUSEBUTTONUP:
				if e.button == 1: rotate = False
				elif e.button == 3: move = False
			elif e.type == MOUSEMOTION:
				i, j = e.rel
				if rotate:
					rx += i
					ry += j
				if move:
					tx += i
					ty -= j

		if rotate:
			rx += i
			ry += j

		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
		glLoadIdentity()

		# RENDER OBJECT
		glTranslate(tx/20., ty/20., - zpos)
		glRotate(ry, 1, 0, 0)
		glRotate(rx, 0, 1, 0)
		glCallList(obj.gl_list)

		pygame.display.flip()



class Camera:

	'''
	Animation data
	
	'''
	
	def __init__(self):

		self.rx, self.ry, self.rz 		= 0, 0,  0 # Rotation
		self.tx, self.ty, self.tz 		= 0, 0, -5 # Translation
		self.drx, self.dry, self.drz 	= 0, 0,  0 # Rotation delta
		self.dtx, self.dty, self.dtz 	= 0, 0,  0 # Translation delta
		
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


	def doAlways(event):

		camera.animate()

		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
		glLoadIdentity()

		# Render object
		glTranslate(camera.tx/20.0, camera.ty/20.0, camera.tz/20.0)
		glRotate(camera.ry, 0, 1, 0)
		glRotate(camera.rx, 1, 0, 0)
		glRotate(camera.rz, 0, 0, 1)
		glCallList(obj.gl_list)

		if True:
			glTranslate(1.2, 0.0, 0.0)
			glRotate(-27, 0, 0, 1)
			glCallList(obj.gl_list)
			glRotate(27, 0, 0, 1)
			glTranslate(-1.2, 1.8, 0.0)
			glCallList(obj.gl_list)
			glTranslate(0.0, -2*1.8, 0.0)
			glCallList(obj.gl_list)

		pygame.display.flip()


	dispatcher.bind({'type': KEYDOWN, 'key': K_LEFT}, lambda event: camera.rotate(4, 0))
	dispatcher.bind({'type': KEYUP, 'key': K_LEFT}, lambda event: camera.setRotating(False))

	dispatcher.bind({'type': KEYDOWN, 'key': K_RIGHT}, lambda event: camera.rotate(-4, 0))

	dispatcher.bind({'type': KEYUP, 'key': K_RIGHT}, lambda event: camera.setRotating(False))

	dispatcher.bind({'type': KEYDOWN, 'key': K_UP}, lambda event: camera.translate(z=4))
	dispatcher.bind({'type': KEYUP, 'key': K_UP}, lambda event: camera.setTranslating(False))
	dispatcher.bind({'type': KEYDOWN, 'key': K_DOWN}, lambda event: camera.translate(z=-4))
	dispatcher.bind({'type': KEYUP, 'key': K_DOWN}, lambda event: camera.setTranslating(False))

	dispatcher.bind({'type': MOUSEBUTTONDOWN, 'button': 1}, lambda event: camera.rotate(z=-4))
	dispatcher.bind({'type': MOUSEBUTTONUP, 'button': 1}, lambda event: camera.setRotating(False))

	dispatcher.bind({'type': MOUSEBUTTONDOWN, 'button': 3}, lambda event: camera.rotate(z=4))
	dispatcher.bind({'type': MOUSEBUTTONUP, 'button': 3}, lambda event: camera.setRotating(False))

	dispatcher.bind({'type': MOUSEBUTTONDOWN, 'button': 4}, lambda event: camera.setTranslation(z=camera.tz+1.2))
	dispatcher.bind({'type': MOUSEBUTTONDOWN, 'button': 5}, lambda event: camera.setTranslation(z=camera.tz-1.2))
	
	dispatcher.always = doAlways

	return dispatcher



if __name__ == '__main__':
	main()