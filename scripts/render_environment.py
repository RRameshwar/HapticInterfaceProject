import pygame as pg
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

from HapticInterfacePoint import *

## The render class handles all the OpenGL stuff that we need to display 3D objects. It also uses pygame to handle taking
## user input.

class render_environment():
	def __init__(self):
		self.display = (1250, 850)
		pg.init()
		screen = pg.display.set_mode(self.display, DOUBLEBUF|OPENGL)
		glMatrixMode(GL_PROJECTION)
		gluPerspective(45, (self.display[0]/self.display[1]), 0.5, 50.0)
		
		glRotatef(90, 0, 0, 0)
		glTranslatef(0.0, 0.0, -20)

		glMatrixMode(GL_MODELVIEW)
		glLoadIdentity()

		glEnable(GL_BLEND);
		glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
		
		self.viewMatrix = glGetFloatv(GL_MODELVIEW_MATRIX)

		self.transf = [0,0,0] # No transf at first
		self.createOrigin()

		# Sets the mouse in the middle of the display so we can use it to rotate views.
		self.displayCenter = [screen.get_size()[i] // 4 for i in range(2)]
		self.mouseMove = [0, 0]
		pg.mouse.set_pos(self.displayCenter)

		self.up_down_angle = 0.0
		self.paused = False
		self.run = True

	## Takes in vertices, edges, and faces and creates a 3D static object.
	def createStaticObj(self,vertices,edges,faces):  # Only for a wireframe display (lines + edges)
		self.staticVerts = vertices
		self.staticEdges = edges
		self.staticFaces = faces

	## Creates a point that will represent both the HIP and the god object
	def createHIP(self,vertex,size=10):
		self.hipVert = vertex
		self.hipSize = size

	## Creates the lines that will display the axes at the origin
	def createOrigin(self):
		self.originVerts = ((0,0,0),(1,0,0),(0,1,0),(0,0,1))
		self.originEdges = ((0,1),(0,2),(0,3))

	## Draws the origin axes
	def drawOrigin(self):
		glBegin(GL_LINES)
		for edge in self.originEdges:
			color = list(self.originVerts[edge[1]]) + [1]
			for vertex in edge:
				glColor4f(*color)
				glVertex3fv(self.originVerts[vertex])
		glEnd()

	## Draws the wire frame around the static object
	def drawWire(self):
		glBegin(GL_LINES)
		glColor4f(0,0,0,1)
		for edge in self.staticEdges:
			for vertex in edge:
				glVertex3fv(self.staticVerts[vertex])
		glEnd()

	## Draws the faces of the static object. Highlights active planes.
	def drawObject(self,prims):
		glBegin(GL_TRIANGLES)
		for i in range(0, len(self.staticFaces)):
			if i in prims:
				glColor4f(0,1,0,1) # Highlight active plane
			else:
				glColor4f(1,0,0,0.5)
			for vertex in self.staticFaces[i]:
				glVertex3fv(self.staticVerts[vertex])
		glEnd()

	## Draws the HIP in white given the current HIP position
	def drawHIP(self, position):
		glPointSize(self.hipSize)
		glBegin(GL_POINTS)
		glColor3f(1,1,1)
		glVertex3f(*position)
		glEnd()

	## Draws the god object in blue given the current god object position
	def drawGod(self, position):
		glPointSize(self.hipSize)
		glBegin(GL_POINTS)
		glColor3f(0,1,1)
		glVertex3f(*position)
		glEnd()

	## Takes in user input.
		# Quit = ESC
		# Pause = 'P'
		# Rotate view = mouse motion
	## Returns a transformation vector that moves the HIP
	def userInput(self, hip):
		for event in pg.event.get():
			if event.type == pg.QUIT:
				self.run = False
			if event.type == pg.KEYDOWN:
				if event.key == pg.K_ESCAPE:
					self.run = False
				if event.key == pg.K_PAUSE or event.key == pg.K_p:
					self.paused = not self.paused
					pg.mouse.set_pos(self.displayCenter)
			if self.paused==False: 
				if event.type == pg.MOUSEMOTION:
					self.mouseMove = [event.pos[i] - self.displayCenter[i] for i in range(2)]
				pg.mouse.set_pos(self.displayCenter)    

		# As long as we haven't paused it, we run this
		if self.paused==False:
			# get keys
			keypress = pg.key.get_pressed()
		
			# init model view matrix
			glLoadIdentity()

			# apply the look up and down
			self.up_down_angle += self.mouseMove[1]*0.1
			glRotatef(self.up_down_angle, 1.0, 0.0, 0.0)

			# init the view matrix
			glPushMatrix()
			glLoadIdentity()

			# apply camera movment  
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

			# multiply the current matrix by the get the new view matrix and store the final view matrix 
			glMultMatrixf(self.viewMatrix)
			self.viewMatrix = glGetFloatv(GL_MODELVIEW_MATRIX)

			# apply view matrix
			glPopMatrix()
			glMultMatrixf(self.viewMatrix)

			# apply hip movement
			if keypress[pg.K_UP]:
				return [0, 0.055, 0]
			if keypress[pg.K_DOWN]:
				return [0, -0.055, 0]
			if keypress[pg.K_LEFT]:
				return [-0.055, 0, 0]
			if keypress[pg.K_RIGHT]:
				return [0.055, 0, 0]
			if keypress[pg.K_RETURN]:
				return [0, 0, 0.055]
			if keypress[pg.K_RSHIFT]:
				return [0, 0, -0.055]
		return [0, 0, 0]			


	## Draws alll the things
	def render(self, prims, hip):  ## Run this inside a loop in the top-level file.
		
		if self.paused == False:	
			glMatrixMode(GL_MODELVIEW)
			glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)  # This must go before we draw our objects

			self.drawObject(prims) 
			self.drawWire()
			# self.drawHIP(hip.current_position)
			self.drawHIP(hip.previous_position)
			self.drawGod(hip.god_pos)
			self.drawOrigin()
		
			pg.display.flip()
			pg.time.wait(10)
		return self.run