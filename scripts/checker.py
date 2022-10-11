import numpy as np
import time

class CollisionChecker():
	def __init__(self, object):
		self.modelObject = object
		self.modelObjectFaces = [list(tup) for tup in self.modelObject.faces]
		self.modelObjectVertices = [list(tup) for tup in self.modelObject.vertices]
		self.intersect_point = [0, 0, 0]

	## This function should perform line-plane test, then if True, perform point-triangle test
	## Two types of checks: collision with object and updating plain constraints
	def detectCollision(self, test_faces, hip_position, test_position, constraint_test=False):
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
			
			# if constraint_test:
				# print("\nCHECKING PLANE", self.modelObjectFaces.index(face), triangle_vertices)
			
			## Perform line test, if passes, perform primitive test.
			if self.line_test(triangle_vertices, hip_position, test_position, constraint_test):
				# print("\nLINE TEST PASSED!! Performing prim test...")
				## Perform primitive test. If pass, return the face that passed
				if self.primitive_test(triangle_vertices, self.intersect_point, constraint_test):
					# print("PRIM TEST PASSED!! Returning collided face:", self.modelObjectFaces.index(face),"\n")
					colliding_faces.append(self.modelObjectFaces.index(face))
					collision = True
				# else:
					# print("PRIM TEST FAILED\n")

		return collision, colliding_faces 


	## Perform line test between line segment and a plane
	def line_test(self, tri, hipPos, testPos, constraint_test):

		## Detect collision between line segment and a face (triangle)
		n = np.cross(np.subtract(tri[0], tri[1]), np.subtract(tri[1], tri[2])) # Get face normal vector
		n = n/np.linalg.norm(n)
		
		## If performing a constraint update check, add a fudge factor normal to the face we are checking
		if constraint_test:
			testPos = testPos + 0.05*n

		## Calculate distance of hip and god from the plane
		hip_dist_to_plane = round(np.dot(np.subtract(hipPos, tri[0]), n), 3)
		test_dist_to_plane = round(np.dot(np.subtract(testPos, tri[0]), n), 3)
	
		# if constraint_test:
			# print("HIP TO PLANE", hip_dist_to_plane, "TEST TO PLANE", test_dist_to_plane)
			# print("HIP POS", hipPos, "TEST POS", testPos)

		## If both distances are on the same side of the plane (same sign), LINE TEST FAILS
		if abs(hip_dist_to_plane + test_dist_to_plane) == abs(hip_dist_to_plane) + abs(test_dist_to_plane):
			return False
							## Check if negligible distance to plane (when we are constrained)
							# if abs(test_dist_to_plane) < 0.001:
							# 	self.intersect_point = (hip_dist_to_plane*testPos - test_dist_to_plane*hipPos)/(hip_dist_to_plane - test_dist_to_plane)
							# 	return True
		else:
			## Calculate the point that falls on the plane
			self.intersect_point = (hip_dist_to_plane*testPos - test_dist_to_plane*hipPos)/(hip_dist_to_plane - test_dist_to_plane)
			return True


	def detectCollision_primitive_test_2(self,tri,p):
		tri_translated = []
		for point in tri:
			tri_translated.append(np.subtract(point, p))

		u = np.cross(tri_translated[0], tri_translated[1])
		v = np.cross(tri_translated[0], tri_translated[2])
		w = np.cross(tri_translated[1], tri_translated[2])

		if np.dot(u,v) < 0:
			return False
		if np.dot(u,w) < 0:
			return False

		#print("Primitive Collision Detected!")

		return True


	def primitive_test(self, tri, p, constraint_test):
		## Detect collision between a point and a triangle
		tri = np.array(tri)
		p = np.array(p)

		
		u = np.subtract(tri[1], tri[0])
		v = np.subtract(tri[2], tri[0])
		w = np.subtract(p, tri[0])

		alpha = (np.dot(u,v) * np.dot(w,v) - np.dot(v,v) * np.dot(w,u)) / (np.dot(u,v)**2 - np.dot(u,u) * np.dot(v,v))
		beta = (np.dot(u,v) * np.dot(w,u) - np.dot(u,u) * np.dot(w,v)) / (np.dot(u,v)**2 - np.dot(u,u) * np.dot(v,v))

		# Check collision conditions as a boolean list
		if constraint_test:
			check = [alpha>=-0.1, beta>=-0.1, alpha+beta<=1.1]

		else:
			check = [alpha>=0.0, beta>=0.0, alpha+beta<=1.0]

		return all(check)