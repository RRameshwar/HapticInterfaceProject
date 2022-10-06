import pygame as pg
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

import numpy as np

class HapticInterfacePoint():
	def __init__(self, initial_position=[0, 0, 0]):
		self.current_position = initial_position
		self.previous_position = initial_position

		self.has_collided = False
		self.god_object_pos = [0, 0, 0]

		self.entry_point = []

		self.rendered_force = [0, 0, 0]

	def updatePos(self, velocity, timestep):
		newx = self.current_position[0] + velocity * timestep
		newy = self.current_position[1] + velocity * timestep

		self.previous_position = self.current_position
		self.current_position = [newx, newy]

	def calcPlaneFromPrim(self, prim):
		#prim = [[x1, y1, z1], [x2, y2, z2], [x3, y3, z3]]
		x1 = prim[0][0]; y1 = prim[0][1]; z1 = prim[0][2]
		x2 = prim[1][0]; y2 = prim[1][1]; z2 = prim[1][2]
		x3 = prim[2][0]; y3 = prim[2][1]; z3 = prim[2][2]

		edge1 = [x2-x1, y2-y1, z2-z1]
		edge2 = [x3-x1, y3-y1, z3-z1]

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

		consts = np.zeros([3,4])

		for i in range(0, 3):
			try: 
				consts[i] = self.calcPlaneFromPrim(prim_list[i])
			except:
				pass
		
		# consts = [a1 b1 c1 d1
		#           a2 b2 c2 d2
		#           a3 b3 c3 d3]

		print(consts)

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
			[consts[0][0], consts[0][1], consts[0][2], 1]]

		print(A)
		

		B = np.array([self.current_position[0], self.current_position[1], self.current_position[2], consts[0][0]])

		# A = 
		# [1  0  0  a1 a2 a3
		#  0  1  0  b1 b2 b3
		#  0  0  1  c1 c2 c3
		#  a1 b1 c1  0 0  0
		#  a2 b2 c2  0 0  0
		#  a3 b3 c3  0 0  0 ]

		x_godobj = np.dot(np.linalg.inv(A), B)

		print(x_godobj)

		self.god_object_pos = [x_godobj[0], x_godobj[1], x_godobj[2]]

	def calculateForce():
		k = [17, 17, 17]
		
		for i in range(0, 3):
			self.rendered_force[i] = [k[i]*(self.god_object_pos[i] - self.current_position[i])]


def main():
	hip = HapticInterfacePoint(initial_position = [2, 2, 2])

	triangleVertices = ((0,0,0),(10,0,0),(0,10,0))

	triangleVertices = [list(tup) for tup in triangleVertices]

	hip.calculateGodObject([triangleVertices])

	print(hip.god_object_pos)



if __name__ == '__main__':
	main()

	


