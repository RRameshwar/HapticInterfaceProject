import numpy as np


class CollisionChecker():
	def __init():
		pass

	def detectCollision(self, object, hip):
		colliding_faces = []
		is_coll = False
		for face in object.faces:
			triangle_vertices = []
			for i in range(0,3): # 0-3 for pyramid (4 faces)
				triangle_vertices.append(object.vertices[face[i]])
			if self.detectCollision_line_test(triangle_vertices, hip):
				colliding_faces.append(face)
				is_coll = True

		return is_coll, colliding_faces 


	def detectCollision_line_test(self, tri, hip):

		## Detect collision between line segment and a face
		n = np.cross(np.subtract(tri[1], tri[0]), np.subtract(tri[2], tri[0]))
		hipPos = hip.current_position
		godPos = hip.god_object_pos

		d_a = np.dot(np.subtract(hipPos, tri[0]), n)
		d_b = np.dot(np.subtract(godPos, tri[0]), n)

		if abs(d_a + d_b) == abs(d_a) + abs(d_b): ## If both distances are on the same side of the plane (same sign)
			lineCollision = False
		else:
			lineCollision = True

		if lineCollision:
			print("lineCollision")
			print(tri)
			intersect_point = (d_a*godPos - d_b*hipPos)/(d_a - d_b)
			print(intersect_point)
			return self.detectCollision_primitive_test(tri, intersect_point)
			
		else:
			return False


	def detectCollision_primitive_test(self, tri, p):
	    ## Detect collision between a point and a triangle
	    tri = np.array(tri)
	    p = np.array(p)

	    u = tri[1] - tri[0]
	    v = tri[2] - tri[0]
	    w = p - tri[0]

	    #alpha = -(np.dot(u,v) * np.dot(w,v) - np.dot(v,v) * np.dot(w,u)) / (np.dot(u,v)**2 - np.dot(u,u) * np.dot(v,v))
	    #beta = -(np.dot(u,v) * np.dot(w,u) - np.dot(u,u) * np.dot(w,v)) / (np.dot(u,v)**2 - np.dot(u,u) * np.dot(v,v))

	    alpha = np.dot(w,v)/np.dot(u,v)
	    beta = np.dot(w,u)/np.dot(u,v)

	    # Check collision conditions as a boolean list
	    check = [alpha>=0, beta>=0, alpha+beta<=1]

	    if alpha>= 0:
	        print("alpha high")

	    if all(check):
	        print("\nCollision Detected!")
	        print(alpha, beta)
	        print(check)
	    else:
	        print('\nNo Detection...')
	        print(alpha, beta)
	        print(check)

	    return all(check)