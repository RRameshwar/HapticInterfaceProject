import pygame as pg
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

from render_environment import *

rd = render_environment()

# rd.test()

pointVertex = (0.25,0.25,0)
triangleVertices = ((0,0,0),(1,0,0),(0,1,0))
triangleEdges = ((0,1),(0,2),(1,2))
triangleSurfaces = ((0,1,2))


rd.createHIP(pointVertex)
rd.createStaticObj(triangleVertices,triangleEdges)	

for i in range(1,1000):
	rd.render()
	rd.moveHIP([0.01, 0, 0])
