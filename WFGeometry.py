#
# WFGeometry.py
# Loading WaveFront OBJ data with Python
#
# Unknown (http://www.pygame.org/wiki/OBJFileLoader)
# October 11 2014
#

# TODO | - glBegin/glEnd context manager (with statement)
#        - Event handlers
#
# SPEC | -
#        -



from collections import defaultdict



def main():

	'''
	Docstring goes here

	'''

	pass



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
	# TODO: Nested dicts or objects (?)
	# TODO: Handle polling as well (?)
	# TODO: Annotations, error handling

	def __init__(self):
		
		'''
		Docstring goes here

		'''

		# TODO: Is this the optimal data structure (w.r.t RAM and CPU)
		# TODO: Allow multiple handlers per pattern
		self.handlers = defaultdict(defaultdict(list)) # Maps event types to patterns and their respective handlers


	def handle(self, event):
		
		'''
		Dispatches an event to all matching event handlers.

		'''

		for handler in self.query(event): #getattr(self, event.type)
			handler(event)
			print('Invalid handler type')


	def query(self, event):

		'''
		Retrieves all event handlers whose patterns
		matches that of the incoming event (cf. bind for details).

		'''

		# TODO: Use issubset for comparisons
		# TODO: Determine and - if necessary - improve performance
		match = frozenset({attr: getattr(event, attr) for attr in ['type', 'key', 'button', 'rel'] if hasattr(event, attr) })

		# TODO: Optionally return mapping between matching patterns and their corresponding handlers (?)
		return (handler(event) for handler in handlers for pattern, handlers in self.handlers[event.type].items() if pattern.issubset(match))


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

		key = frozenset(*pattern.items)
		self.handlers[pattern.type][key].append(handler)
		return hash(key), id(handler)



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
glShadeModel(GL_SMOOTH)           # most obj files expect to be smooth-shaded
 
# LOAD OBJECT AFTER PYGAME INIT
# obj = OBJ(sys.argv[1], swapyz=True)
obj = OBJ(['data/villa.obj', 'data/square.obj'][0], swapyz=False)

 
clock = pygame.time.Clock()
 
glMatrixMode(GL_PROJECTION)
glLoadIdentity()
width, height = viewport
gluPerspective(90.0, width/float(height), 1, 100.0)
glEnable(GL_DEPTH_TEST)
glMatrixMode(GL_MODELVIEW)
 
rx, ry = (0,0)
tx, ty = (0,0)
zpos = 5
rotate = move = False

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

if __name__ == '__main__':
	main()