import pygame as pg
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

from checker import *

import numpy as np
from myObject import *

import datetime as dt
import time

## The HIP class keeps track of everything to do with the HIP, including the god object and the force output.
## This is where we update the HIP position and also make all the calculations to update the god object position and
## output forces. 

class HapticInterfacePoint():
	def __init__(self, model, initial_position=[0, 0, 0]):
		self.current_position = initial_position
		self.previous_position = initial_position

		self.inside_object = False
		self.god_pos = initial_position
		self.god_pos_prev = initial_position

		self.active_planes = []
		self.active_planes_prev = []
		self.possible_planes = []
		self.rendered_force = [0, 0, 0]

		self.model = model
		self.model_faces = [list(tup) for tup in self.model.faces]

		self.checker = CollisionChecker(self.model)

		self.isConcave = False

	## This function should move the HIP and (if colliding) the God object positions
	def updatePos(self, transformation):			

		time_start = time.time()

		## Update previous hip position
		self.previous_position = self.current_position
		self.current_position = np.add(self.current_position, transformation)	

		## If inside object, let's update our plane constraints iteratively. This also calculates a 
		## new god object position
		if self.inside_object:
			self.updatePlaneConstraints()
		else:
			## If NOT inside object, let's just update our god object with the transformation
			self.god_pos_prev = self.god_pos
			self.god_pos = self.previous_position
			
		# Calculate and print output force		 
		self.calculateForce()
		print("CURRENT FORCE = ", round(np.linalg.norm(self.rendered_force),3))
		
		# Calculate and print refresh rate
		time_end = time.time()
		print("REFRESH RATE", 1/(time_end - time_start))

	## Iteratively update plane constraints. Find new constraints between hip and old god, and update god object
	## THEN check constraints between new and old god and update god object AGAIN.
	def updatePlaneConstraints(self):

		## Get neighboring faces sharing a single point ........... MIGHT WANT TO CHANGE THIS TO JUST CHECK THOSE THAT SHARE AN EDGE .............
		self.updatePossiblePlanes()

		self.active_planes_prev = []

		## Iterate both checks until there are no constraint updates		
		while self.active_planes != self.active_planes_prev:

			## Check neighbors to see if they are a new constraint - USING OLD GOD OBJ AND HIP
			__, old_constraints = self.checker.detectCollision(self.possible_planes, self.current_position, self.god_pos_prev, True, self.isConcave)
			old_constraints = [*set(old_constraints)] # This removes duplicates
			
			## ****** IMPORTANT ****** 
			## When we are adding concave constraints, we only pass the point test if we add a constant.
			## self.isConcave checks whether we are adding a constraint or simply rolling around a convex surface
			# if old_constraints in self.active_planes:
			# 	self.isConcave = True
			# else:
			# 	self.isConcave = False
		
			## Calculate temporary god position just to find new constraints, if any
			temp_god_pos = self.calculateGod(old_constraints)


			## Check neighbors to see if new constraint - USING OLD GOD OBJ AND NEW GOD OBJ
			## This might be where extra active planes get discovered
			__, new_constraints = self.checker.detectCollision(self.possible_planes, temp_god_pos, self.god_pos_prev, True, self.isConcave)
			new_constraints = [*set(new_constraints)] # This removes duplicates


			## Combine all of our current constraints
			self.active_planes_prev = self.active_planes
			self.active_planes = new_constraints + old_constraints
			self.active_planes = [*set(self.active_planes)]

			## Update god object for the SECOND TIME
			self.god_pos_prev = self.god_pos
			self.god_pos = self.calculateGod(self.active_planes)


	## Returns new calculated god object position minimizing distance b/w hip and god while maintaining constraint
	def calculateGod(self, prim_list):

		## Step 1 is to trim the list of active planes if any of them are coplanar. Coplanar primitives will
		## give us a singular matrix A and inverting it will cause an error.

		prim_list_trimmed = []

		# If we only have 2, we can do a simple check with no for loops
		if len(prim_list) == 2:
			if self.isCoplanar(self.model.faces[prim_list[0]], self.model.faces[prim_list[1]]):
				# print("removed a coplanar")
				prim_list.remove(prim_list[1])

		# For more than 2, we need to check all planes against all other planes (but no duplicate checking!)
		# We keep track of all the coplanar planes we need to remove
		if len(prim_list) >= 3:
			to_remove = []
			for num, prim in enumerate(prim_list):
				for num2, prim2 in enumerate(prim_list[num+1:-1]):
					if self.isCoplanar(self.model_faces[prim], self.model_faces[prim2]):
						to_remove.append(num2)

			## And remove the coplanar plaes
			prim_list_trimmed = prim_list
			for i in to_remove:
				prim_list_trimmed.remove(prim_list[i])


		if len(prim_list_trimmed) > 0:
			prim_list = prim_list_trimmed

		# We use the trimmed primitive list (all our legitimate active planes) to calculate plane constants
		# We will have a minimum of 1, a maximum of 3.
		
		consts = np.zeros([3,4])
		for i in range(0, len(prim_list)):			
			triangle = self.model.faces[prim_list[i]]
			triangle_points = (self.model.vertices[triangle[0]], 
				self.model.vertices[triangle[1]], self.model.vertices[triangle[2]]) 
			
			# Use the vertices of the primitive to calculate the plane constants and update "consts"
			consts[i] = self.calcPlaneFromPrim(triangle_points)
		
			# consts = [a1 b1 c1 d1
			#           a2 b2 c2 d2
			#           a3 b3 c3 d3]


		# Calculate A and B
		# B is the current position of the HIP

		# A = 
		# [1  0  0  a1 a2 a3
		#  0  1  0  b1 b2 b3
		#  0  0  1  c1 c2 c3
		#  a1 b1 c1  0 0  0
		#  a2 b2 c2  0 0  0
		#  a3 b3 c3  0 0  0 ]

		# A will be 4x4 if we only have 1 constraint, 5x5 if we have 2, 6x6 if we have 3

		## A failsafe for testing purposes, we should never get to this point
		if len(prim_list) == 0:
			A = np.eye(3)
			B = np.array([self.current_position[0], self.current_position[1], self.current_position[2]])

		## 1 plane constraint
		if len(prim_list) == 1:
			A = [
				[1, 0, 0, consts[0][0]],
				[0, 1, 0, consts[0][1]],
				[0, 0, 1, consts[0][2]],
				[consts[0][0], consts[0][1], consts[0][2], 0]]

			B = np.array([self.current_position[0], self.current_position[1], self.current_position[2], consts[0][3]*-1])

		## 2 plane constraints
		if len(prim_list) == 2:
			A = [
				[1, 0, 0, consts[0][0], consts[1][0]],
				[0, 1, 0, consts[0][1], consts[1][1]],
				[0, 0, 1, consts[0][2], consts[1][2]],
				[consts[0][0], consts[0][1], consts[0][2], 0, 0],
				[consts[1][0], consts[1][1], consts[1][2], 0, 0]
				]

			B = np.array([self.current_position[0], self.current_position[1], self.current_position[2], consts[0][3]*-1, consts[1][3]*-1])
		
		## 3 plane constraints
		if len(prim_list) >= 3:
			A = [
				[1, 0, 0, consts[0][0], consts[1][0], consts[2][0]],
				[0, 1, 0, consts[0][1], consts[1][1], consts[2][1]],
				[0, 0, 1, consts[0][2], consts[1][2], consts[2][2]],
				[consts[0][0], consts[0][1], consts[0][2], 0, 0, 0],
				[consts[1][0], consts[1][1], consts[1][2], 0, 0, 0],
				[consts[2][0], consts[2][1], consts[2][2], 0, 0, 0]]

			B = np.array([self.current_position[0], self.current_position[1], self.current_position[2], consts[0][3]*-1, consts[1][3]*-1, consts[2][3]*-1])


		#FINALLY calculate the god object position using A and B.

		x_godobj = np.dot(np.linalg.inv(A), B)
		return np.array([x_godobj[0], x_godobj[1], x_godobj[2]])

	# Returns an output force based on current HIP and god object positions
	def calculateForce(self):
		k = [17, 17, 17]
		
		for i in range(0, 3):
			self.rendered_force[i] = [k[i]*(self.god_pos[i] - self.current_position[i])]


	## HELPER FUNCTIONS ##

	## Check neighboring triangles (planes) that share a single point with active triangle. We need to check
	## these planes later to see if the god object has switched constraint planes.
	def updatePossiblePlanes(self):
		self.possible_planes = []

		## For each active plane, find neighbors
		for active_plane in self.active_planes:
			active_plane_points = self.model_faces[active_plane]
			
			## For each object face (must check all faces EVERY time)
			for face in self.model_faces:
				if (any(point in face for point in active_plane_points)):
					self.possible_planes.append(face) # This will include our active plane as well

	## Takes a triangle of 3 vertices and outputs the plane equation of that triangle. Calculates 2 edges of the
	## triangle, and takes a cross product.
	def calcPlaneFromPrim(self, prim):

		x1 = prim[0][0]; y1 = prim[0][1]; z1 = prim[0][2]
		x2 = prim[1][0]; y2 = prim[1][1]; z2 = prim[1][2]
		x3 = prim[2][0]; y3 = prim[2][1]; z3 = prim[2][2]

		edge1 = [np.subtract(x2,x1), np.subtract(y2,y1), np.subtract(z2,z1)]
		edge2 = [np.subtract(x3,x1), np.subtract(y3,y1), np.subtract(z3,z1)]

		cross_product = np.cross(edge1, edge2)

		a = cross_product[0]
		b = cross_product[1]
		c = cross_product[2]

		d = -1 * (a * x1 + b * y1 + c * z1)

		return a, b, c, d


	## Takes 2 triangles and returns True if they are coplanar, and False if they are not. Calculates the normal
	## to each triangle and checks if the normals are parallel or not.
	def isCoplanar(self, tri1, tri2):

		cross1 = np.cross(np.subtract(self.model.vertices[tri1[0]], self.model.vertices[tri1[1]]), np.subtract(self.model.vertices[tri1[1]], self.model.vertices[tri1[2]]))
		cross2 = np.cross(np.subtract(self.model.vertices[tri2[0]], self.model.vertices[tri2[1]]), np.subtract(self.model.vertices[tri2[1]], self.model.vertices[tri2[2]]))

		cross1 = cross1/np.linalg.norm(cross1)
		cross2 = cross2/np.linalg.norm(cross2)

		check_cross = np.cross(cross1, cross2)
		
		if abs(np.linalg.norm(check_cross)) == 0.0:
			return True