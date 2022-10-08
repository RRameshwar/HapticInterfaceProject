import pygame as pg
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

import numpy as np

class HapticInterfacePoint():
	def __init__(self, modelObject, initial_position=[0, 0, 0]):
		self.initial_position = initial_position
		self.current_position = initial_position
		self.previous_position = initial_position

		self.has_collided = False
		self.god_object_pos = [0, 0, 0]

		self.active_plane = []

		self.rendered_force = [0, 0, 0]

		self.modelObject = modelObject


	# def updatePos(self, velocity, timestep):
	# 	newx = self.current_position[0] + velocity * timestep
	# 	newy = self.current_position[1] + velocity * timestep

	# 	self.previous_position = self.current_position
	# 	self.current_position = [newx, newy]

	def updatePos(self, transformation): ## Update hip and god position | this is passed to the render function in main.py

		self.previous_position = self.current_position

		self.current_position = np.add(self.current_position, transformation)
				
		if not self.has_collided:
			print("default pos")
			self.god_object_pos = self.current_position ## *************** IF NO COLLISION (ASSUMED FOR NOW Friday 12:35pm) ********************
		if self.has_collided:
			print("calculated pos")
			self.god_object_pos = self.calculateGodObject(self.active_plane)


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

		d = a*-1*x1 + b*-1*x2 + c*-1*x3

		return a, b, c, d


	def calculateGodObject(self, prim_list):
		#for each primitive:
		#calculate plane from primitive
		#build large matrix A and solution vector b --> Ax = b (case for 1, 2, and 3 planes)
		#self.god_object_pos =  A-1 * b


		#Keep track of old god object position
		# Check if we need to update primitive list 
				# test for line segment collision with each triangle in possible list
				# if true, update active primitive list
				   # and find new adjacent triangles for possible list (yikes)
				# update plane constraints with active list
				#calculate new god object position

		consts = np.zeros([3,4])

		#print("prim_list ", prim_list)

		triangle = self.modelObject.faces[prim_list[0]]
		#print("Triangle ", prim_list[0], " is ", triangle)
		
		triangle_points = (self.modelObject.vertices[triangle[0]], 
			self.modelObject.vertices[triangle[1]], self.modelObject.vertices[triangle[2]])

		# print("Triangle Points are ", triangle_points)
		consts[0] = self.calcPlaneFromPrim(triangle_points)

		# for i in range(0, 3):
		# 	try:
		# 		triangle = self.model.faces[prim_list[i]] 
		# 		print("Triangle ", i, " is ", triangle)
		# 		consts[i] = self.calcPlaneFromPrim(triangle)
		# 	except:
		# 		pass
		
		# consts = [a1 b1 c1 d1
		#           a2 b2 c2 d2
		#           a3 b3 c3 d3]

		# print("plane consts, ", consts)

		# A = [
		# 	[1, 0, 0, consts[0][0], consts[1][0], consts[2][0]],
		# 	[0, 1, 0, consts[0][1], consts[1][1], consts[2][1]],
		# 	[0, 0, 1, consts[0][2], consts[1][2], consts[2][2]],
		# 	[consts[0][0], consts[0][1], consts[0][2], 0, 0, 0],
		# 	[consts[1][0], consts[1][1], consts[1][2], 0, 0, 0],
		# 	[consts[2][0], consts[2][1], consts[2][2], 0, 0, 0]]

		A = [
			[1, 0, 0, consts[0][0]],
			[0, 1, 0, consts[0][1]],
			[0, 0, 1, consts[0][2]],
			[consts[0][0], consts[0][1], consts[0][2], 0]]

		# print(A)
		

		B = np.array([self.current_position[0], self.current_position[1], self.current_position[2], consts[0][0]])

		# A = 
		# [1  0  0  a1 a2 a3
		#  0  1  0  b1 b2 b3
		#  0  0  1  c1 c2 c3
		#  a1 b1 c1  0 0  0
		#  a2 b2 c2  0 0  0
		#  a3 b3 c3  0 0  0 ]

		x_godobj = np.dot(np.linalg.inv(A), B)

		#print(x_godobj)

		return [x_godobj[0], x_godobj[1], x_godobj[2]]

	def calculateForce():
		k = [17, 17, 17]
		
		for i in range(0, 3):
			self.rendered_force[i] = [k[i]*(self.god_object_pos[i] - self.current_position[i])]



