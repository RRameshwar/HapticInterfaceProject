import pygame as pg
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

class render_environment():
	def __init__(self):
		self.display = (1680, 1050)
		pg.init()
		pg.display.set_mode(self.display, DOUBLEBUF|OPENGL)
		glMatrixMode(GL_PROJECTION)
		gluPerspective(70, (self.display[0]/self.display[1]), 0.5, 50.0)
		glTranslatef(0.0, 0.0, -10)

		glMatrixMode(GL_MODELVIEW)
		self.transf = [0,0,0]


	def moveHIP(self,transf):
		self.transf = transf


	def createStaticObj(self,vertices,edges):  # Only for a wireframe display (lines + edges)
		self.staticVerts = vertices
		self.staticEdges = edges


	def createHIP(self,vertex,size=5):
		self.hipVert = vertex
		self.hipSize = size


	def drawStaticObj(self):
		glBegin(GL_LINES)
		for edge in self.staticEdges:
			for vertex in edge:
				glVertex3fv(self.staticVerts[vertex])
		glEnd()	


	def drawHIP(self):
		glPointSize(self.hipSize)
		glBegin(GL_POINTS)
		glVertex3f(*self.hipVert)
		glEnd()


	def render(self,t=0,transf=[0,0,0]):  ## Run this inside a loop in the top-level file. Can use move() to move the object inside that loop.
		
		for event in pg.event.get():
			if event.type == pg.QUIT:
				pg.quit()
				quit()

		glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)  # This must go before we draw our objects

		# glPushMatrix()
		
		
		
		self.drawStaticObj()
		glTranslatef(*self.transf)

		# transMat = move
		# [-i,0,0]
		# glTranslatef(*transMat)

		self.drawHIP()

		# glPopMatrix()
		
		# newVertex = pointVertex + np.array(transMat)
		# print(newVertex)
		# detectCollision(triangleVertices,newVertex)
		
		pg.display.flip()
		pg.time.wait(10)


def main():
	render = render_enviroment()


if __name__ == "__main__":
	main()