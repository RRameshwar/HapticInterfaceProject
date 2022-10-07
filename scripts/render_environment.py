import pygame as pg
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

class render_environment():
	def __init__(self):
		self.display = (1680, 1050)
		pg.init()
		screen = pg.display.set_mode(self.display, DOUBLEBUF|OPENGL)
		glMatrixMode(GL_PROJECTION)
		gluPerspective(70, (self.display[0]/self.display[1]), 0.5, 50.0)
		
		glRotatef(90, 0, 0, 1)
		glTranslatef(0.0, 0.0, -5)

		glMatrixMode(GL_MODELVIEW)
		glLoadIdentity()

		glEnable(GL_BLEND);
		glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
		
		self.viewMatrix = glGetFloatv(GL_MODELVIEW_MATRIX)

		self.transf = [0,0,0] # No transf at first
		self.createOrigin()

		self.displayCenter = [screen.get_size()[i] // 4 for i in range(2)]
		self.mouseMove = [0, 0]
		pg.mouse.set_pos(self.displayCenter)

		self.up_down_angle = 0.0
		self.paused = False
		self.run = True


	def moveHIP(self,transf):
		self.transf = transf


	def createStaticObj(self,vertices,edges,faces):  # Only for a wireframe display (lines + edges)
		self.staticVerts = vertices
		self.staticEdges = edges
		self.staticFaces = faces


	def createHIP(self,vertex,size=5):
		self.hipVert = vertex
		self.hipSize = size


	def createOrigin(self):
		self.originVerts = ((0,0,0),(1,0,0),(0,1,0),(0,0,1))
		self.originEdges = ((0,1),(0,2),(0,3))


	def drawOrigin(self):
		glBegin(GL_LINES)
		for edge in self.originEdges:
			color = list(self.originVerts[edge[1]]) + [1]
			print(color)
			for vertex in edge:
				glColor4f(*color)
				glVertex3fv(self.originVerts[vertex])
		glEnd()


	def drawStaticObj(self):
		glBegin(GL_LINES)
		glColor4f(1,1,1,1)
		for edge in self.staticEdges:
			for vertex in edge:
				glVertex3fv(self.staticVerts[vertex])
		glEnd()


	def drawStaticObjSolid(self,prims):
		glBegin(GL_TRIANGLES)
		
		for i in range(0, len(self.staticFaces)):
			if i in prims:
				glColor4f(0,1,0,0.3)
			else:
				glColor4f(1,0,0,0.3)
			for vertex in self.staticFaces[i]:
				glVertex3fv(self.staticVerts[vertex])
		glEnd()


	def drawHIP(self, position):
		glPointSize(self.hipSize)
		glBegin(GL_POINTS)
		glColor3f(1,1,1)
		glVertex3f(*position)
		glEnd()

	def drawGodObject(self, position):
		glPointSize(self.hipSize)
		glBegin(GL_POINTS)
		glColor3f(0,1,1)
		glVertex3f(*position)
		glEnd()


	def render(self, prims, hip_position, god_position):  ## Run this inside a loop in the top-level file. Can use move() to move the object inside that loop.
		for event in pg.event.get():
			if event.type == pg.QUIT:
				self.run = False
			if event.type == pg.KEYDOWN:
				if event.key == pg.K_ESCAPE or event.key == pg.K_RETURN:
					self.run = False
				if event.key == pg.K_PAUSE or event.key == pg.K_p:
					self.paused = not self.paused
					pg.mouse.set_pos(self.displayCenter) 
			if self.paused==False: 
				if event.type == pg.MOUSEMOTION:
					self.mouseMove = [event.pos[i] - self.displayCenter[i] for i in range(2)]
				pg.mouse.set_pos(self.displayCenter)    

		if self.paused==False:
			# get keys
			keypress = pg.key.get_pressed()
			#mouseMove = pg.mouse.get_rel()
		
			# init model view matrix
			glLoadIdentity()

			# apply the look up and down
			self.up_down_angle += self.mouseMove[1]*0.1
			glRotatef(self.up_down_angle, 1.0, 0.0, 0.0)

			# init the view matrix
			glPushMatrix()
			glLoadIdentity()

			# apply the movment 
			if keypress[pg.K_w]:
				glTranslatef(0,0,0.1)
			if keypress[pg.K_s]:
				glTranslatef(0,0,-0.1)
			if keypress[pg.K_d]:
				glTranslatef(-0.1,0,0)
			if keypress[pg.K_a]:
				glTranslatef(0.1,0,0)

			# apply the left and right rotation
			glRotatef(self.mouseMove[0]*0.1, 0.0, 1.0, 0.0)

			# multiply the current matrix by the get the new view matrix and store the final vie matrix 
			glMultMatrixf(self.viewMatrix)
			self.viewMatrix = glGetFloatv(GL_MODELVIEW_MATRIX)

			# apply view matrix
			glPopMatrix()
			glMultMatrixf(self.viewMatrix)

			glMatrixMode(GL_MODELVIEW)
			glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)  # This must go before we draw our objects

			self.drawHIP(hip_position)			

			self.drawGodObject(god_position)

			self.drawStaticObjSolid(prims) # Need to draw the object after push/pop 
			self.drawStaticObj()
			self.drawOrigin()
			# glPopMatrix()



		# newVertex = pointVertex + np.array(transMat)
		# print(newVertex)
		# detectCollision(triangleVertices,newVertex)
		
			pg.display.flip()
			pg.time.wait(100)
		return self.run



def main():
	render = render_enviroment()


if __name__ == "__main__":
	main()