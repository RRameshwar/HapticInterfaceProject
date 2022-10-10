import numpy as np
import time

class CollisionChecker():
	def __init__(self, object):
		self.modelObject = object
		self.modelObjectFaces = [list(tup) for tup in self.modelObject.faces]
		self.modelObjectVertices = [list(tup) for tup in self.modelObject.vertices]
		self.intersect_point = 0
		# pass

	def detectCollision(self, object, object_faces, hip_position, test_position, is_god):
		
		colliding_faces = []
		is_coll = False
		
		for i in range(0, len(object_faces)): # Loop through possible neighboring faces
			face = list(object_faces[i])
			triangle_vertices = []
			
			for j in range(0,len(face)): # Loop through each point in the face (3 points in triangle)
				triangle_vertices.append(self.modelObjectVertices[face[j]])
			
			if self.line_test(triangle_vertices, hip_position, test_position, is_god): # Run line test and point test
				if self.primitive_test(triangle_vertices, self.intersect_point):
					colliding_faces.append(self.modelObjectFaces.index(face))
					is_coll = True

		#print("FINAL RETURN: ", colliding_faces)
		return is_coll, colliding_faces 


	def line_test(self, tri, hip_position, test_position, is_god):

		## Detect collision between line segment and a face (triangle)
		n = np.cross(np.subtract(tri[0], tri[1]), np.subtract(tri[1], tri[2]))
		n = n/np.linalg.norm(n)
		print("\n LINE COLLISION CHECK BEGIN")
		print("n: ", n)
		
		hipPos = np.array([hip_position])
		test_point = np.array([test_position])
		
		if is_god:
			print("Test position without fudge ", test_position)
			test_point = test_position - 0.02*n   ## ************** SWAP FUDGE FACTOR DEPENDING ON THE NORMAL DIRECTION **********
			print("Test position with fudge ", test_point)

		# print("-----------")
		# print("Triangle Vertices: ", tri)
		# print("Current Position: ", hipPos)
		# print("Previos Position: ", godPos)

		d_a = np.dot(np.subtract(hipPos, tri[0]), n) # Distance of hip from plane
		d_b = np.dot(np.subtract(test_point, tri[0]), n) # Distance of god obj from plane

		print("PLANE TO CHECK ", tri, type(tri))
		print("DA ", d_a, type(d_a))
		print("DB ", d_b, type(d_b))
		print("HIP POS ", hipPos, type(hipPos))
		print("TEST POS ", test_point, type(test_point))

		self.intersect_point = (d_a*test_point - d_b*hipPos)/(d_a - d_b)

		if abs(d_a + d_b) == abs(d_a) + abs(d_b): ## If both distances are on the same side of the plane (same sign)
			if abs(d_b) < 0.0001:
				return True
			return False
		else:
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


## Creating helper function for new primitive test
	def detectCollision_same_side(self, p1, p2, a, b):
		# cp1 = np.cross(np.subtract(b,a), np.subtract(p1,a))
		# cp2 = np.cross(np.subtract(b,a), np.subtract(p2,a))
		# if np.dot(cp1, cp2) >= 0:
		if True:
			return True
		else:
			return False

	def detectCollision_primitive_test2(self, tri, p):
		tri = np.array(tri)
		p = np.array(p)

		if self.detectCollision_same_side(p,tri[0],tri[1],tri[2]) and self.detectCollision_same_side(p,tri[1],tri[0],tri[2]) and self.detectCollision_same_side(p,tri[2],tri[0],tri[1]):
			return True
		else:
			return False


	def primitive_test(self, tri, p):
	    ## Detect collision between a point and a triangle
	    tri = np.array(tri)
	    p = np.array(p)

	    u = np.subtract(tri[1], tri[0])
	    v = np.subtract(tri[2], tri[0])
	    w = np.subtract(p, tri[0])

	    alpha = (np.dot(u,v) * np.dot(w,v) - np.dot(v,v) * np.dot(w,u)) / (np.dot(u,v)**2 - np.dot(u,u) * np.dot(v,v))
	    beta = (np.dot(u,v) * np.dot(w,u) - np.dot(u,u) * np.dot(w,v)) / (np.dot(u,v)**2 - np.dot(u,u) * np.dot(v,v))

	    # Check collision conditions as a boolean list
	    check = [alpha>=0, beta>=0, alpha+beta<=1]

	    if all(check):
	        print("\nPrimitive Collision Detected!")
	        # print(round(alpha,3), round(beta,3))
	        print("Alpha and Beta: ", alpha, beta)
	        print(check)
	    else:
	        print('\nNo Primitive Collision Detected...')
	        # print(round(alpha,3), round(beta,3))
	        print("Alpha and Beta: ", alpha, beta)
	        print(check)

	    return all(check)