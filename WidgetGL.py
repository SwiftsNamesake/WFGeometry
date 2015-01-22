#
# WidgetGL
# OpenGL widgets
#
# Jonatan H Sundqvist
# November 22 2014
#

# TODO | -
#        -
#
# SPEC | -
#        -



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
		self.active 	= self.vPressed if self.pressed else self.vReleased


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
		
		glLoadIdentity() # Don't apply camera transformations
		glScale(sx, sy, sx)
		glTranslate(-1.5/sx, 1.0/sy, -1.1/sx)
		glCallList(self.active.gl_list)