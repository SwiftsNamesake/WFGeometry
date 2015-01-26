#
# scene.py
# description
#
# Jonatan H Sundqvist
# January 25 2015
#

# TODO | - Managing a matrix stack and 'connected' meshes
#        - Should scenes manage events, contexts or windows, or simply encapsulate geometry data?
#
# SPEC | -
#        -



import camera
import model

import pygame

from OpenGL.GL import *
from OpenGL.GLU import *



class Scene(object):

	'''
	Docstring goes here

	'''

	def __init__(self):

		'''
		Docstring goes here

		'''

		self.fill = 0.4, 0.4, 0.9, 1.0
		self.camera = camera.Camera()
		self.meshes = [] # TODO: Mesh queries


	def render(self):

		'''
		Docstring goes here

		'''

		self.prepare()
		self.camera.apply()

		for mesh in self.meshes:
			mesh.render()

		pygame.display.flip()


	def add(self, mesh):
		
		'''
		Add a mesh object to the scene

		'''

		self.meshes.append(mesh)


	def prepare(self):
		
		'''
		Prepare for rendering a new frame (set the Scene)

		'''

		glEnable(GL_BLEND)
		glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

		glEnable(GL_BLEND)
		glAlphaFunc(GL_GREATER, 0.5)

		glClearColor(*self.fill)

		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
		glLoadIdentity()


	def animate(self, dt):

		'''
		Animates the camera and each mesh belonging to the scene

		'''

		self.camera.animate()

		for mesh in self.meshes:
			mesh.animate()



def main():
	
	'''
	Docstring goes here

	'''

	pass



if __name__ == '__main__':
	main()