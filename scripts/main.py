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
	hip = HapticInterfacePoint()
	dod = ModelObject('dodecahedron.obj')
	#pyr = Pyramid(((1,0,0),(2, 2, 0),(1,2,0),(2, 1, 2)))

	coll = CollisionChecker() # From checker.py

	pointVertex = (-2.0, -2.0 ,0)

	gl.createStaticObj(dod.vertices, dod.edges, dod.faces)
	gl.createHIP(pointVertex)

	i = 0.01

	run = gl.render()
	while run == True:
		run = gl.render()
		is_coll, prims = coll.detectCollision(dod,hip) # returns a boolean and a list of primitives (faces)

		if not is_coll:
			T = [i, 1.25, 0]
			hip.updatePos(T) # find new position for HIP
			gl.moveHIP([i,1.25,0])
		else:
			print("Collided!")
				

		# 	else: #we have already collided, this is a second collision
		# 		if prims == hip.entry_point: #we collided with the same primitive that we entered, so it's a clear exit
		# 			hip.has_collided = False
		# 			hip.entry_point = []

		# if hip.has_collided:
		# 	hip.calculateGodObject()
		
		
		# gl.render(god_object=hip.has_collided)

		i += 0.01



