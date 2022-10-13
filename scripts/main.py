import pygame as pg
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

from HapticInterfacePoint import *
from render_environment import *
from myObject import *
from checker import *
from modelObject import *

import pywavefront
import time

## This is the main function that sets up the whole simulation. We create a rendering object, model object, a HIP object, 
## and a checker object that we will use inside our while loop.


if __name__ == '__main__':

	#We tested a lot of objects. The bunny and tree were both poorly formed, and the bunny took a really long time to 
	# render.

	# model = ModelObject('../objects/dodecahedron.obj')
	# model = ModelObject('../objects/bunny.obj')
	# model = ModelObject('../objects/tree.obj')
	# model = ModelObject('../objects/actual_cube.obj')
	# model = ModelObject('../objects/hex_prism.obj')

	# model = Cube()
	# model = ConcaveCube()
	# model = Pyramid(((1,0,0),(2, 2, 0),(1,2,0),(2, 1, 2)))

	#2 model objects we used for the demo

	model = ModelObject('../objects/icosahedron.obj')
	# model = ConcavePrism() ######## THIS OUR GUY


	# starting points for each object so we don't start inside the object
	## Convex Vertex:
	pointVertex = (0.5, 1.35, 0)
	## Concave Vertex:
	# pointVertex = (2, 1.3, 6.0)
	
	# Creating the rendering environment object and creating a rigid model as well as the haptic interface point to render
	gl = render_environment()
	gl.createStaticObj(model.vertices, model.edges, model.faces)
	gl.createHIP(pointVertex)

	# Creating a HIP and checker object
	hip = HapticInterfacePoint(model, initial_position = pointVertex)
	checker = CollisionChecker(model) # From checker.py


	run = True
	collision_time = 0
	collided_faces = []
	penetrated = False

	# The major while loop where we do all the work, as long as we haven't paused the render environment (by hitting 'p' or 'esc')
	while run == True:
		
		# Get user input (arrow keys)
		transformation = gl.userInput(hip)
		
		# Creating "toggle" whether we are inside object or not
		if penetrated:									
			## If colliding for the second time, we are NOT IN THE OBJECT
			if hip.inside_object == True:
				hip.inside_object = False
				hip.active_planes = []
				print("\n**** EXITED OBJECT ****\n")

			## If colliding for first time, we are IN THE OBJECT
			else:
				hip.inside_object = True
				hip.active_planes = collided_faces
				print("\n**** ENTERED OBJECT ****\n")

		# Updating both the HIP and the god object positions (major calculations here)
		hip.updatePos(transformation)

		# After calculations, checking if we are penetrating the object
		penetrated, collided_faces = checker.detectCollision(model.faces, hip.current_position, hip.previous_position, False) # returns a boolean and a list of primitives (indices of the face list)
	
		# Render all the things we have to render, now with updating information
		run = gl.render(hip.active_planes, hip) # Now keeping active plane highlighted
