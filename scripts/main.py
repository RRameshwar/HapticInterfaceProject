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
	# model = ModelObject('car.obj')
	# model = ModelObject('tree.obj')
	# model = ModelObject
	
	# model = Cube()
	# model = ConcaveCube()

	model = ConcavePrism()

	# model = ModelObject('actual_cube.obj')
	
	# model = Pyramid(((1,0,0),(2, 2, 0),(1,2,0),(2, 1, 2)))


	coll_check = CollisionChecker(model) # From checker.py

	#pointVertex = (0.5, 2.35, 2)
	pointVertex = (2, 1.3, 6.0)

	gl.createStaticObj(model.vertices, model.edges, model.faces)
	gl.createHIP(pointVertex)
	hip = HapticInterfacePoint(model, initial_position = pointVertex)

	collided_faces = []
	# run = gl.render(collided_faces, hip.current_position, hip.god_object_pos)
	run = gl.render(collided_faces, hip)
	collision_time = 0

	is_coll = False
	
	while run == True:
		
		#print(hip.current_position)
		
		transformation = gl.userInput(hip)
		
		# print("\nCHECKING FOR COLLISION WITH OBJECT!!\n")
		
		# print(hip.god_object_pos)
		if is_coll:
			# print("HAS COLLIDED ", hip.has_collided)
			# if time.time() - collision_time < 0.02:
			# 	collision_time = time.time()
			# else:
			if hip.has_collided == False:
				hip.has_collided = True
				collision_time = time.time()
				# print("TOGGLING COLLISION ", hip.has_collided)
				# hip.god_object_pos = hip.current_position
			else:
				hip.has_collided = False
				collision_time = 0
				hip.active_planes = []
				# hip.god_object_pos = hip.current_position
				# print("TOGGLING COLLISION ", hip.has_collided)

		if is_coll and hip.has_collided:
			#print("UPDATED ACTIVE PLANE ", collided_faces)
			#print("Current hip pos ", hip.current_position)
			hip.active_planes = collided_faces

		hip.updatePos(transformation)

		is_coll, collided_faces = coll_check.detectCollision(model, model.faces,hip.current_position,hip.previous_position, False) # returns a boolean and a list of primitives (indices of the face list)
		# print("COLLISION WITH OBJECT RETURNED ", is_coll, hip.current_position, hip.previous_position, hip.god_object_pos)

		

		run = gl.render(collided_faces, hip)



		# run = gl.render(collided_faces, hip.current_position, hip.god_object_pos)
		

