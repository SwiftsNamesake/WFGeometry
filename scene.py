#
# scene.py
# description
#
# Jonatan H Sundqvist
# January 25 2015
#

# TODO | - Managing a matrix stack and 'connected' meshes
#        -
#
# SPEC | -
#        -



import camera
import model

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


	def animate(self):

		'''
		Docstring goes here

		'''

		self.camera.animate()

		for mesh in self.meshes:
			mesh.animate()