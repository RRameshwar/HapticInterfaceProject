import numpy as np


class Pyramid():
	def __init__(self, vertices):
		self.vertices = vertices

		self.edges = ((0,1), (0,2), (1,2), (0,3), (1,3), (2,3))
		self.faces = ((0,1,2), (0,3,1), (0,3,2), (1,2,3))


class Cube():
	def __init__(self):
		self.vertices = ((0,0,0), (1,0,0), (1,2,0), (0,2,0), (0,2,3), (1,2,3), (0,0,3), (1,0,3))
		self.edges = ((0,1), (1,2), (2,3), (3,0), (0,6), (6,4), (4,3), (4,5), (5,7), (7,6), (7,1), (5,2), (0,2), (0,4), 
			(6,5), (1,5), (3,5), (0,7))
		self.faces = ((0,2,1), (0,3,2), (0,6,4), (0,4,3), (6,7,5), (6,5,4), (1,5,7), (1,2,5), (3,5,2), (3,4,5), (0,1,7), (0,7,6))


class ConcaveCube():
	def __init__(self):
		self.vertices = ((0,0,0), (1,0,0), (1,2,0), (0,2,0), (0,2,3), (1,2,3), (0,0,3), (1,0,3), (0.5, 1, 1.5))
		self.edges = ( (0,8), (3,8), (1,8), (2,8), (0,1), (1,2), (2,3), (3,0), (3,4), (4,5), (5,2), (5,7), (7,1), (0,6), (6,7))
		#self.faces = ((0,1,8), (1,8,2), (8,3,2), (0,8,3), (0,6,4), (0,4,3), (7,6,5), (6,4,5), (1,7,5), (1,5,2), (2,5,3), (5,4,3), (0,1,7), (0,7,6))
		self.faces = ((0,1,8), (1,2,8), (8,2,3), (0,8,3), (0,4,6), (0,3,4), (6,5,7), (6,4,5), (1,7,5), (1,5,2), (3,2,5), (3,5,4), (0,7,1), (0,6,7))

		