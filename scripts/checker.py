import numpy as np
import time
from myObject import *

class CollisionChecker():
	def __init__(self, object):
		self.modelObject = object
		self.modelObjectFaces = [list(tup) for tup in self.modelObject.faces]
		self.modelObjectVertices = [list(tup) for tup in self.modelObject.vertices]
		self.intersect_point = [0, 0, 0]

	## This function should perform line-plane test, then if True, perform point-triangle test
	## Two types of checks: collision with object and updating plain constraints
	def detectCollision(self, test_faces, hip_position, test_position, constraint_test=False, concave=False):
		# if not constraint_test:
			# print("\n**** PERFORMING COLLISION DETECTION ****")

		collision = False
		colliding_faces = []
		
		# Check each face
		for face in test_faces:
			face = list(face) # These are the indices corresponding to vertices
			triangle_vertices = []
			
			## Assign test face's vertices to list 
			triangle_vertices.append(self.modelObjectVertices[face[0]])
			triangle_vertices.append(self.modelObjectVertices[face[1]])
			triangle_vertices.append(self.modelObjectVertices[face[2]])
			
			## Perform line test, if passes, perform primitive test.
			if self.line_test(triangle_vertices, hip_position, test_position, constraint_test):

				## Perform primitive test. If pass, return the face that passed
				if self.primitive_test(triangle_vertices, self.intersect_point, concave):

					colliding_faces.append(self.modelObjectFaces.index(face))
					collision = True

		return collision, colliding_faces 


	## Perform line test between line segment and a plane
	def line_test(self, tri, hipPos, testPos, constraint_test):

		## Detect collision between line segment and a face (triangle)
		n = np.cross(np.subtract(tri[0], tri[1]), np.subtract(tri[1], tri[2])) # Get face normal vector
		n = n/np.linalg.norm(n)
		
		## If performing a constraint update check, add a fudge factor normal to the face we are checking
		# if constraint_test:
		# 	testPos = testPos - 0.05*n

		## Calculate distance of hip and god from the plane
		hip_dist_to_plane = round(np.dot(np.subtract(hipPos, tri[0]), n), 3)
		test_dist_to_plane = round(np.dot(np.subtract(testPos, tri[0]), n), 3) + 0.005

		# if constraint_test:
		# 	test_dist_to_plane += 0.01 ## Fudge factor

		## If both distances are on the same side of the plane (same sign), LINE TEST FAILS
		if abs(hip_dist_to_plane + test_dist_to_plane) == abs(hip_dist_to_plane) + abs(test_dist_to_plane):
			return False
		else:
			## Calculate the point that falls on the plane
			self.intersect_point = np.subtract(hip_dist_to_plane*testPos , test_dist_to_plane*hipPos)/np.subtract(hip_dist_to_plane , test_dist_to_plane)
			return True


	def primitive_test(self, tri, p, concave):
		## Detect collision between a point and a triangle
		tri = np.array(tri)
		p = np.array(p)
		
		u = np.subtract(tri[1], tri[0])
		v = np.subtract(tri[2], tri[0])
		w = np.subtract(p, tri[0])

		alpha = (np.dot(u,v) * np.dot(w,v) - np.dot(v,v) * np.dot(w,u)) / (np.dot(u,v)**2 - np.dot(u,u) * np.dot(v,v))
		beta = (np.dot(u,v) * np.dot(w,u) - np.dot(u,u) * np.dot(w,v)) / (np.dot(u,v)**2 - np.dot(u,u) * np.dot(v,v))

		
		## Check collision conditions as a boolean list
		if type(self.modelObject) == type(ConcavePrism()):
			check = [alpha>=-0.05, beta>=-0.05, alpha+beta<=1.05]
		else:
			check = [alpha>=0.0, beta>=0.0, alpha+beta<=1.0]


		# if concave:
		# 	check = [alpha>=-0.1, beta>=-0.1, alpha+beta<=1.1]
		# else:
		# 	check = [alpha>=0.0, beta>=0.0, alpha+beta<=1.0]
		return all(check)