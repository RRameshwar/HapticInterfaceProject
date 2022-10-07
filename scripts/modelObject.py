import numpy as np
import pywavefront

class ModelObject():
	def __init__(self, obj_file):

		self.obj_file = obj_file

		self.vertices = ()
		self.edges = ()
		self.faces = ()

		self.getGeometry()

	def getGeometry(self):
		scene = pywavefront.Wavefront(self.obj_file, collect_faces=True)
		self.vertices = scene.vertices
		self.faces = scene.mesh_list[0].faces
		self.generateEdges()

	def generateEdges(self):
		edge_list = []
		for face in self.faces:
			edge_list.append([face[0], face[1]])
			edge_list.append([face[0], face[2]])
			edge_list.append([face[1], face[2]])

		self.edges = edge_list



if __name__ == '__main__':

	o = ModelObject('dodecahedron.obj')

	print(o.vertices)
	print(o.faces)
	print(o.edges)




