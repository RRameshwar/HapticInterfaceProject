import pygame as pg
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

from HapticInterfacePoint import *
from render_environment import *
from pyramid import *
from checker import *
from modelObject import *

import pywavefront
import time

if __name__ == '__main__':
	gl = render_environment()

	#model = ModelObject('dodecahedron.obj')

	model = Cube()
	
	#model = Pyramid(((1,0,0),(2, 2, 0),(1,2,0),(2, 1, 2)))

	print(model.faces)

	coll_check = CollisionChecker() # From checker.py

	pointVertex = (0.5, 2.0, 0.5)

	gl.createStaticObj(model.vertices, model.edges, model.faces)
	gl.createHIP(pointVertex)
	hip = HapticInterfacePoint(model, initial_position = pointVertex)

	collided_faces = []
	# run = gl.render(collided_faces, hip.current_position, hip.god_object_pos)
	run = gl.render(collided_faces, hip)
	collision_time = 0
	
	while run == True:
		run = gl.render(collided_faces, hip)
		#print(hip.current_position)
		T = [0, 0, 0.05]
		is_coll, collided_faces = coll_check.detectCollision(model,hip) # returns a boolean and a list of primitives (indices of the face list)

		if is_coll:
			if time.time() - collision_time < 0.02:
				collision_time = time.time()
			else:
				if hip.has_collided == False:
					hip.has_collided = True
					collision_time = time.time()
					print("TOGGLING COLLISION ", hip.has_collided)
				else:
					hip.has_collided = False
					collision_time = 0
					print("TOGGLING COLLISION ", hip.has_collided)
	

		if is_coll and hip.has_collided:
			#print("UPDATED ACTIVE PLANE ", collided_faces)
			#print("Current hip pos ", hip.current_position)
			hip.active_plane = collided_faces

		# run = gl.render(collided_faces, hip.current_position, hip.god_object_pos)
		

