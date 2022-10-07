
import numpy as np


class Pyramid():
	def __init__(self, vertices):
		self.vertices = vertices

		self.edges = ((0,1), (0,2), (1,2), (0,3), (1,3), (2,3))
		self.faces = ((0,1,2), (0,3,1), (0,3,2), (1,2,3))

