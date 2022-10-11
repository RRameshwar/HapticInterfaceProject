import pygame as pg
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

from checker import *

import numpy as np
from myObject import *

class HapticInterfacePoint():
	def __init__(self, modelObject, initial_position=[0, 0, 0]):
		self.initial_position = initial_position
		self.current_position = initial_position
		self.previous_position = initial_position

		self.inside_object = False
		self.god_object_pos = initial_position
		self.god_object_pos_prev = initial_position

		self.active_planes = []
		self.possible_planes = []
		self.rendered_force = [0, 0, 0]

		self.modelObject = modelObject
		self.modelObject_faces = [list(tup) for tup in self.modelObject.faces]

		self.checker = CollisionChecker(self.modelObject)

	## This function should move the HIP and (if colliding) the God object positions
	def updatePos(self, transformation):

		self.previous_position = self.current_position
		
		if self.inside_object:
			## If inside object, let's update our plane constraints recursively
			self.updatePlaneConstraints()
		else:
			## If NOT inside object, let's just update our previous positions
			self.god_object_pos_prev = self.god_object_pos
			self.god_object_pos = self.current_position

		self.current_position = np.add(self.current_position, transformation)				
		print("HIP PREV ", self.previous_position, " HIP NOW ", self.current_position, " GOD PREV ", self.god_object_pos_prev, " GOD NOW ", self.god_object_pos, " ACTIVE PLANES ", self.active_planes)
		

	def updatePlaneConstraints(self):
		# print("PLANE CONSTRAINT FIRST UPDATE")
		self.updatePossiblePlanes()

		old_constraints = []
		new_constraints = []

		god_obj_pos_temp = self.god_object_pos

		# print("PLANES TO CHECK: ", self.possible_planes)
		# print("LINE SEGMENT POINTS", self.current_position, self.god_object_pos)

		is_coll, new_constraints = self.checker.detectCollision(self.possible_planes, self.current_position, self.god_object_pos_prev, True) # Collision check based on old god object position

		# print("NEW CONSTRAINTS ", new_constraints)
		# if new_constraints == []:
			# print("\nNEW CONSTRAINTS IS EMPTY WTF\n")
		

		count = 1
		# print("FIRST GO CALC IS DONE ")

		while not (old_constraints == new_constraints):
			count = count + 1
			# print("CHECKING GO AGAIN ", count, new_constraints)
			old_constraints = new_constraints
			is_coll, new_constraints = self.checker.detectCollision(self.possible_planes, self.current_position, self.god_object_pos_prev, True) # Collision check based on old god object position

			god_obj_pos_temp = self.calculateGodObject(new_constraints)

		# print("TEMP GOD OBJECT AFTER UPDATING PLANE CONSTRAINTS IS ", god_obj_pos_temp)

		self.god_object_pos_prev = self.god_object_pos
		

		if len(new_constraints) > 4:
			self.active_planes = self.active_planes
			print("TRUNCED ACTIVE PLANES")
		else:
			self.active_planes = new_constraints

		self.god_object_pos = self.calculateGodObject(self.active_planes)

	## Optimization - check neighboring triangles (planes) that share two points with active triangle
	def updatePossiblePlanes(self):
		self.possible_planes = []
		# print("\nList of active planes ", self.active_planes)

		## For each active plane, find neighbors
		for active_plane in self.active_planes:
			active_plane_points = self.modelObject_faces[active_plane]
			# print("Current active plane ", active_plane, active_plane_points, [self.modelObject.vertices[active_plane_points[0]], self.modelObject.vertices[active_plane_points[1]], self.modelObject.vertices[active_plane_points[2]]])
			
			## For each object face (must check all faces EVERY time)
			for face in self.modelObject_faces:
				## If a single point is shared, continue
				if (any(point in face for point in active_plane_points)):
					# if not face in self.possible_planes: ## THIS DOESNT DO ANYTHING?
					self.possible_planes.append(face)


	def calcPlaneFromPrim(self, prim):
		#prim = [[x1, y1, z1], [x2, y2, z2], [x3, y3, z3]]
		x1 = prim[0][0]; y1 = prim[0][1]; z1 = prim[0][2]
		x2 = prim[1][0]; y2 = prim[1][1]; z2 = prim[1][2]
		x3 = prim[2][0]; y3 = prim[2][1]; z3 = prim[2][2]

		# edge1 = [x2-x1, y2-y1, z2-z1]
		# edge2 = [x3-x1, y3-y1, z3-z1]

		edge1 = [np.subtract(x2,x1), np.subtract(y2,y1), np.subtract(z2,z1)]
		edge2 = [np.subtract(x3,x1), np.subtract(y3,y1), np.subtract(z3,z1)]

		#print(edge1, edge2)

		cross_product = np.cross(edge1, edge2)

		#print(cross_product)            

		a = cross_product[0]
		b = cross_product[1]
		c = cross_product[2]

		d = -1 * (a * x1 + b * y1 + c * z1)

		return a, b, c, d


	def isCoplanar(self, tri1, tri2):
		# print(tri1)
		# print(tri2)
		cross1 = np.cross(np.subtract(self.modelObject.vertices[tri1[0]], self.modelObject.vertices[tri1[1]]), np.subtract(self.modelObject.vertices[tri1[1]], self.modelObject.vertices[tri1[2]]))
		cross2 = np.cross(np.subtract(self.modelObject.vertices[tri2[0]], self.modelObject.vertices[tri2[1]]), np.subtract(self.modelObject.vertices[tri2[1]], self.modelObject.vertices[tri2[2]]))

		cross1 = cross1/np.linalg.norm(cross1)
		cross2 = cross2/np.linalg.norm(cross2)

		check_cross = np.cross(cross1, cross2)
		
		if abs(np.linalg.norm(check_cross)) == 0.0:
			return True

	def calculateGodObject(self, prim_list):

		consts = np.zeros([3,4])
		prim_list_trimmed = []

		#Trim the primitive list to delete coplanar primitives

		if len(prim_list) == 2:
			if self.isCoplanar(self.modelObject.faces[prim_list[0]], self.modelObject.faces[prim_list[1]]):
				print("removed a coplanar")
				prim_list.remove(prim_list[1])

		if len(prim_list) == 3:
			to_remove = []
			if self.isCoplanar(self.modelObject.faces[prim_list[0]], self.modelObject.faces[prim_list[1]]):
				to_remove.append(1)
			if self.isCoplanar(self.modelObject.faces[prim_list[0]], self.modelObject.faces[prim_list[2]]):
				to_remove.append(2)
			if self.isCoplanar(self.modelObject.faces[prim_list[1]], self.modelObject.faces[prim_list[2]]):
				to_remove.append(2)

			prim_list_trimmed = prim_list
			for i in to_remove:
				prim_list_trimmed.remove(prim_list[i])

			print("removed some coplanars ", len(to_remove))

		if len(prim_list_trimmed) > 0:
			prim_list = prim_list_trimmed

			
		for i in range(0, 3):
			try:
				# print("TRYING SOME SHIT")
				triangle = self.modelObject.faces[prim_list[i]]
				# print("Triangle ", i, " is ", triangle)
				triangle_points = (self.modelObject.vertices[triangle[0]], 
					self.modelObject.vertices[triangle[1]], self.modelObject.vertices[triangle[2]]) 
				
				consts[i] = self.calcPlaneFromPrim(triangle_points)
			except:
				# print("NO MORE PRIMS")
				pass
		
		# consts = [a1 b1 c1 d1
		#           a2 b2 c2 d2
		#           a3 b3 c3 d3]

		print("OG prim list (len, list)", len(prim_list), prim_list)


			
		# print("plane consts, ", consts)

		# A = [
		# 	[1, 0, 0, consts[0][0], consts[1][0], consts[2][0]],
		# 	[0, 1, 0, consts[0][1], consts[1][1], consts[2][1]],
		# 	[0, 0, 1, consts[0][2], consts[1][2], consts[2][2]],
		# 	[consts[0][0], consts[0][1], consts[0][2], 0, 0, 0],
		# 	[consts[1][0], consts[1][1], consts[1][2], 0, 0, 0],
		# 	[consts[2][0], consts[2][1], consts[2][2], 0, 0, 0]]

		if len(prim_list) == 1:
			A = [
				[1, 0, 0, consts[0][0]],
				[0, 1, 0, consts[0][1]],
				[0, 0, 1, consts[0][2]],
				[consts[0][0], consts[0][1], consts[0][2], 0]]

			#B = np.array([self.previous_position[0], self.previous_position[1], self.previous_position[2], consts[0][3]*-1])
			B = np.array([self.current_position[0], self.current_position[1], self.current_position[2], consts[0][3]*-1])

			# print("A = ", A)

		if len(prim_list) == 2:
			A = [
				[1, 0, 0, consts[0][0], consts[1][0]],
				[0, 1, 0, consts[0][1], consts[1][1]],
				[0, 0, 1, consts[0][2], consts[1][2]],
				[consts[0][0], consts[0][1], consts[0][2], 0, 0],
				[consts[1][0], consts[1][1], consts[1][2], 0, 0]
				]

			#B = np.array([self.previous_position[0], self.previous_position[1], self.previous_position[2], consts[0][3]*-1, consts[1][3]*-1])
			B = np.array([self.current_position[0], self.current_position[1], self.current_position[2], consts[0][3]*-1, consts[1][3]*-1])
		
		if len(prim_list) >= 3:
			A = [
				[1, 0, 0, consts[0][0], consts[1][0], consts[2][0]],
				[0, 1, 0, consts[0][1], consts[1][1], consts[2][1]],
				[0, 0, 1, consts[0][2], consts[1][2], consts[2][2]],
				[consts[0][0], consts[0][1], consts[0][2], 0, 0, 0],
				[consts[1][0], consts[1][1], consts[1][2], 0, 0, 0],
				[consts[2][0], consts[2][1], consts[2][2], 0, 0, 0]]

			#B = np.array([self.previous_position[0], self.previous_position[1], self.previous_position[2], consts[0][3]*-1, consts[1][3]*-1, consts[2][3]*-1])
			B = np.array([self.current_position[0], self.current_position[1], self.current_position[2], consts[0][3]*-1, consts[1][3]*-1, consts[2][3]*-1])


		# print("B = ", B)

		# print("A -1 = ", np.linalg.inv(A))

		# A = 
		# [1  0  0  a1 a2 a3
		#  0  1  0  b1 b2 b3
		#  0  0  1  c1 c2 c3
		#  a1 b1 c1  0 0  0
		#  a2 b2 c2  0 0  0
		#  a3 b3 c3  0 0  0 ]

		x_godobj = np.dot(np.linalg.inv(A), B)

		#print("HIP POSITION ", self.current_position)
		# print("GO POSITION ", x_godobj)

		return np.array([x_godobj[0], x_godobj[1], x_godobj[2]])

	def calculateForce():
		k = [17, 17, 17]
		
		for i in range(0, 3):
			self.rendered_force[i] = [k[i]*(self.god_object_pos[i] - self.current_position[i])]




if __name__ == '__main__':
	model = ConcaveCube()
	hip = HapticInterfacePoint(model)
	hip.active_planes =[1,2]
	# hip.previous_position = [0.08, 1.27, 2.12]
	# hip.previous_position = [0.08, 1.3, 2.12]
	# hip.previous_position = [0.08, 1.24, 2.12]
	# hip.current_position = [0.08, 1.27, 2.12]
	hip.previous_position = [0.0, 0.0, 0.0]
	hip.current_position = [0.68, 1.63, 2.3]

	go = hip.calculateGodObject(hip.active_planes)
	print(go)





