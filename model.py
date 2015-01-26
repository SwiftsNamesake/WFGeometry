#
# model.py
# description
#
# Jonatan H Sundqvist
# January 25 2015
#

# TODO | -
#        -
#
# SPEC | -
#        -



import models


class Model(object):

	'''
	Wraps an OpenGL buffer

	'''

	def __init__(self, filename, groups, origin=(0,0,0)):
		
		'''
		Docstring goes here

		'''

		self.vertices = parseOBJ(filename)
		self.buffers  = createBuffers(data=self.vertices, groups=groups)
		self.dirty    = False # Dirty vertices flag


	def render(self):
		
		'''
		Docstring goes here

		'''

		# Apply model view transforms
		# Render
		glCallList(self.buffer)


	def animate(self, dt):
		
		'''
		Docstring goes here

		'''

		pass



def main():
	
	'''
	Docstring goes here

	'''

	pass



if __name__ == '__main__':
	main()