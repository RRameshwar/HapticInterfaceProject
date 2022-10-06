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
	pyr = Pyramid(((0,0,0),(1, 2, 0),(0,2,0),(1, 1, 2)))
	coll = CollisionChecker() # From checker.py

	pointVertex = (0.25,0.25,0)

	gl.createStaticObj(pyr.vertices, pyr.edges)
	gl.createHIP(pointVertex)

	i = 0.01
	while True:

		if i < 1:
			gl.moveHIP([i,0,0])
		else:
			gl.moveHIP([0,i,0])
				
		# #find new position for HIP
		# hip.updatePos(newPos) #maybe have to rewrite the update function
		# is_coll = coll.detectCollision(pyr, hip)

		
		gl.render()

		i += 0.01



