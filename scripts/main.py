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





if __name__ == '__main__':

	gl = render_environment()

	# model = ModelObject('dodecahedron.obj')
	# model = ModelObject('bunny.obj')
	# model = ModelObject('tree.obj')
	# model = ModelObject('actual_cube.obj')
	# model = ModelObject('hex_prism.obj')
	model = ModelObject('icosahedron.obj')

	# model = Cube()
	# model = ConcaveCube()
	# model = ConcavePrism() ######## THIS OUR GUY
	# model = Pyramid(((1,0,0),(2, 2, 0),(1,2,0),(2, 1, 2)))


	checker = CollisionChecker(model) # From checker.py

	#pointVertex = (0.5, 1.35, 2)
	pointVertex = (2, 1.3, 6.0)

	gl.createStaticObj(model.vertices, model.edges, model.faces)
	gl.createHIP(pointVertex)
	hip = HapticInterfacePoint(model, initial_position = pointVertex)

	# run = gl.render(collided_faces, hip) # WE DON'T NEED THIS ANYMORE???

	run = True
	collision_time = 0
	collided_faces = []

	penetrated = False
	
	while run == True:
		
		# Get user input (arrow keys)
		transformation = gl.userInput(hip)
		
		# Creating "toggle" whether we are inside object or not
		if penetrated:
									# print("HAS COLLIDED ", hip.has_collided)
									# if time.time() - collision_time < 0.02:
									# 	collision_time = time.time()
									# else:
			## If colliding for the second time, we are NOT IN THE OBJECT
			if hip.inside_object == True:
				hip.inside_object = False
				hip.active_planes = []
				print("\n**** EXITED OBJECT ****\n")
				# collision_time = 0
			## If colliding for first time, we are IN THE OBJECT
			else:
				hip.inside_object = True
				hip.active_planes = collided_faces
				print("\n**** ENTERED OBJECT ****\n")
				# collision_time = time.time()

		hip.updatePos(transformation)

		penetrated, collided_faces = checker.detectCollision(model.faces, hip.current_position, hip.previous_position, False) # returns a boolean and a list of primitives (indices of the face list)
		# print("COLLISION WITH OBJECT RETURNED ", is_coll, hip.current_position, hip.previous_position, hip.god_object_pos)

		

		# run = gl.render(collided_faces, hip)
		run = gl.render(hip.active_planes, hip) # Now keeping active plane highlighted
		

