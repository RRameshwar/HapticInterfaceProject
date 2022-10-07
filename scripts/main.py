import pygame as pg
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

from HapticInterfacePoint import *
from render_environment import *
from pyramid import *
from checker import *

if __name__ == '__main__':
	gl = render_environment()
	hip = HapticInterfacePoint()
	pyr = Pyramid(((1,0,0),(2, 2, 0),(1,2,0),(2, 1, 2)))
	coll = CollisionChecker() # From checker.py

	pointVertex = (0.25,0.25,0)

	gl.createStaticObj(pyr.vertices, pyr.edges)
	gl.createHIP(pointVertex)

	i = 0.01

	run = gl.render()
	while run==True:
		run = gl.render()

		# if i < 1:
		# 	gl.moveHIP([i,0,0])
		# else:
		# 	gl.moveHIP([0,i,0])
				
		# # #find new position for HIP
		# # hip.updatePos(newPos) #maybe have to rewrite the update function

		# # is_coll, prims = coll.detectCollision(pyr, hip) #returns a boolean and a list of primitives (faces)

		# if is_coll:
		# 	if hip.has_collided = False:  #we have not collided with the object yet
		# 		hip.has_collided = True   #we have now!
		# 		hip.entry_point = prims

		# 	else: #we have already collided, this is a second collision
		# 		if prims == hip.entry_point: #we collided with the same primitive that we entered, so it's a clear exit
		# 			hip.has_collided = False
		# 			hip.entry_point = []

		# if hip.has_collided:
		# 	hip.calculateGodObject()
		
		
		# gl.render(god_object=hip.has_collided)

		# i += 0.01



