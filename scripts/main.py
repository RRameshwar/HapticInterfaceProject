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

if __name__ == '__main__':
	gl = render_environment()

	model = ModelObject('dodecahedron.obj')
	print(model.faces)
	# dod = Pyramid(((1,0,0),(2, 2, 0),(1,2,0),(2, 1, 2)))

	coll_check = CollisionChecker() # From checker.py

	pointVertex = (0.2, 0.2 ,-2.0)

	gl.createStaticObj(model.vertices, model.edges, model.faces)
	gl.createHIP(pointVertex)
	hip = HapticInterfacePoint(model, initial_position = pointVertex)

	collided_faces = []
	# run = gl.render(collided_faces, hip.current_position, hip.god_object_pos)
	run = gl.render(collided_faces, hip)
	
	while run == True:
		T = [0, 0, 0.05]
		is_coll, collided_faces = coll_check.detectCollision(model,hip) # returns a boolean and a list of primitives (indices of the face list)
		
		if is_coll:
			hip.has_collided = not hip.has_collided

		if is_coll and hip.has_collided:
			print("UPDATED ACTIVE PLANE ", collided_faces)
			print("Current hip pos ", hip.current_position)
			hip.active_plane = collided_faces

		# run = gl.render(collided_faces, hip.current_position, hip.god_object_pos)
		run = gl.render(collided_faces, hip)

