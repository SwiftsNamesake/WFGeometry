#
# App.py
# 
#
# Jonatan H Sundqvist
# January 26 2015
#

# TODO | - Model view controller, over-arching capabilities
#        - Loading worlds from external files (perhaps JSON with filenames and initial positions for now)
#        - Study carefully: http://gamedev.stackexchange.com/questions/92845/why-do-tutorials-use-different-approaches-to-opengl-rendering

# SPEC | -
#        -



from scene import Scene
from model import Model

from SwiftUtils.EventDispatcher import EventDispatcher

from pygame.locals import *
from pygame.constants import *
from OpenGL.GL import *
from OpenGL.GLU import *

import pygame



class App(object):

	'''
	Docstring goes here

	'''


	def __init__(self):

		'''
		Docstring goes here

		'''

		# Configuration
		# TODO: Make sure these never go out of sync
		self.size = 720*2, 480*2
		self.width, self.height = self.size

		# Context
		self.OpenGL(self.width, self.height)
		pygame.display.set_caption('Los Hombres con sombreros')
		# pygame.display.set_icon(pygame.image.load('C:/Users/Jonatan/Desktop/Python/resources/images/paintings/mont-sainte-victoire-3.jpg'))

		# World
		self.scene = Scene()
		self.createWorld()

		# Events
		self.dispatcher = EventDispatcher()
		self.dispatcher.always = lambda event: self.update() #
		self.bindEvents()



	def bindEvents(self):
		
		'''
		Docstring goes here

		'''

		# TODO: Simplify
		bind = self.dispatcher.bind
		camera = self.scene.camera

		def pan(pattern, event):
			pressed = pygame.mouse.get_pressed()[0]
			camera.rotate(x=event.rel[1]*pressed, y=event.rel[0]*pressed)

		bind({'type': MOUSEMOTION}, pan),
		bind({'type': MOUSEMOTION, 'also': (K_RSHIFT,)}, lambda pt, event: camera.translate(x=event.rel[0]*0.2, z=event.rel[1]*0.2)), # TODO: 
		bind({'type': MOUSEBUTTONDOWN, 'button': 4}, lambda pt, event: camera.translate(z= 1.2))
		bind({'type': MOUSEBUTTONDOWN, 'button': 5}, lambda pt, event: camera.translate(z=-1.2))




	def createMenus(self):

		'''
		Docstring goes here

		'''

		pass


	def createWorld(self):
		
		'''
		Initialize OpenGL

		'''

		for n, piece in enumerate(('king', 'Queen', 'Pawn', 'Rook')):
			self.scene.add(Model(filename='data/{0}.obj'.format(piece), groups=False, origin=(8.5*n, 0.0, 0.0))) # TODO: Managing resources and paths


	def OpenGL(self, width, height):
		
		'''
		Initialize OpenGL

		'''

		# TODO: Look closer at the various OpenGL propertiess
		# TODO: Legacy API or clean and modern (?)

		pygame.init()


		viewport = (width, height)
		hx = viewport[0]/2
		hy = viewport[1]/2
		srf = pygame.display.set_mode(viewport, OPENGL | DOUBLEBUF)

		# # TODO: Many of these should probably not be hard-coded...
		glLightfv(GL_LIGHT0, GL_POSITION,  (-40, 200, 100, 0.0))
		glLightfv(GL_LIGHT0, GL_AMBIENT, (0.2, 0.2, 0.2, 1.0))
		glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.5, 0.5, 0.5, 1.0))
		glEnable(GL_LIGHT0)
		glEnable(GL_LIGHTING)
		glEnable(GL_COLOR_MATERIAL)
		glEnable(GL_DEPTH_TEST)
		glShadeModel(GL_SMOOTH)           # Most obj files expect to be smooth-shaded

		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()
		gluPerspective(90.0, width/height, 1, 100.0) # TODO: Aspect ratio should not be hard-coded
		glEnable(GL_DEPTH_TEST)
		glMatrixMode(GL_MODELVIEW)


	def update(self):
		
		'''
		Docstring goes here

		'''

		self.scene.render()


	def run(self):
		
		'''
		Docstring goes here

		'''

		self.dispatcher.mainloop()



def main():
	
	'''
	Docstring goes here

	'''

	app = App()
	app.run()



if __name__ == '__main__':
	main()