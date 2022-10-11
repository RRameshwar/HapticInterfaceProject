import numpy as np
import time

class CollisionChecker():
	def __init__(self, object):
		self.modelObject = object
		self.modelObjectFaces = [list(tup) for tup in self.modelObject.faces]
		self.modelObjectVertices = [list(tup) for tup in self.modelObject.vertices]
		# pass

	def detectCollision(self, object, object_faces, hip_position, test_position, is_god):
		
		colliding_faces = []
		is_coll = False
		
		for i in range(0, len(object_faces)): # Loop through possible neighboring faces
			face = list(object_faces[i])
			triangle_vertices = []
			
			for j in range(0,len(face)): # Loop through each point in the face (3 points in triangle)
				triangle_vertices.append(self.modelObjectVertices[face[j]])
			
			if is_god:
				print("\nPLANE TO CHECK ", self.modelObjectFaces.index(face), "IS GOD = ", is_god)
			
			if self.detectCollision_line_test(triangle_vertices, hip_position, test_position, is_god): # Run line test and point test
				colliding_faces.append(self.modelObjectFaces.index(face))
				is_coll = True

		#print("FINAL RETURN: ", colliding_faces)
		# print("finished checking all faces, these are colliding: ", colliding_faces)
		return is_coll, colliding_faces 


	def detectCollision_line_test(self, tri, hip_position, test_position, is_god):

		## Detect collision between line segment and a face (triangle)
		n = np.cross(np.subtract(tri[0], tri[1]), np.subtract(tri[1], tri[2]))
		n = n/np.linalg.norm(n)
		# print("LINE COLLISION CHECK BEGIN")
		
		hipPos = hip_position
		test_point = test_position
		
		if is_god:
			# print("Test position without fudge ", test_position)
			# print("FUDGE ", n)
			# print("Hip position to test against ", hipPos)
			test_point = test_position - 0.02*n
		else:
			test_point = test_position

		# print("-----------")
		#print("Triangle Vertices: ", tri)
		# print("Current Position: ", hipPos)
		# print("Previos Position: ", godPos)

		d_a = np.dot(np.subtract(hipPos, tri[0]), n) # Distance of hip from plane
		d_b = np.dot(np.subtract(test_point, tri[0]), n) # Distance of god obj from plane


		if abs(d_a + d_b) == abs(d_a) + abs(d_b): ## If both distances are on the same side of the plane (same sign)
			if abs(d_b) < 0.001:
				# print("Line Collision! Checking if point intersects a face...", is_god)

				if is_god:
					print("DA ", d_a)
					print("DB ", d_b)
					print("HIP POS ", hipPos)
					print("TEST POS ", test_point)

				intersect_point = (d_a*test_point - d_b*hipPos)/(d_a - d_b)
				tempPrimTest = self.detectCollision_primitive_test(tri, intersect_point, is_god)
				print("RESULT OF PRIM TEST:", tempPrimTest)
				return tempPrimTest
			return False
		else:
			#print()
			# print("Line Collision! Checking if point intersects a face...", is_god)

			if is_god:
				print("DA ", d_a)
				print("DB ", d_b)
				print("HIP POS ", hipPos)
				print("TEST POS ", test_point)

			intersect_point = (d_a*test_point - d_b*hipPos)/(d_a - d_b)
			#print("intersection point: ", intersect_point)
			tempPrimTest = self.detectCollision_primitive_test(tri, intersect_point, is_god)
			print("RESULT OF PRIM TEST:", tempPrimTest)
			return tempPrimTest


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


	def detectCollision_primitive_test(self, tri, p, is_god):
		## Detect collision between a point and a triangle
		tri = np.array(tri)
		p = np.array(p)

		
		u = np.subtract(tri[1], tri[0])
		v = np.subtract(tri[2], tri[0])
		w = np.subtract(p, tri[0])

		alpha = (np.dot(u,v) * np.dot(w,v) - np.dot(v,v) * np.dot(w,u)) / (np.dot(u,v)**2 - np.dot(u,u) * np.dot(v,v))
		beta = (np.dot(u,v) * np.dot(w,u) - np.dot(u,u) * np.dot(w,v)) / (np.dot(u,v)**2 - np.dot(u,u) * np.dot(v,v))

		# Check collision conditions as a boolean list
		if is_god:
			check = [alpha>=-0.1, beta>=-0.1, alpha+beta<=1.1]

		else:
			check = [alpha>=0.0, beta>=0.0, alpha+beta<=1.0]

		# if alpha>= 0:
		#     print("alpha high")

		# if all(check):
		# 	# print("\nPrimitive Collision Detected!")
		# 	print(round(alpha,3), round(beta,3), alpha+beta)
		# 	print(check)
		# else:
		# 	# print('\nNo Primitive Collision Detected...')
		# 	print(round(alpha,3), round(beta,3), alpha+beta)
		# 	print(check)

		return all(check)