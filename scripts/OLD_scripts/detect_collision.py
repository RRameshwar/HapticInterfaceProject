def detectCollision(tri, p):

    ## Detect collision between a point and a triangle
    tri = np.array(tri)
    p = np.array(p)

    u = tri[1] - tri[0]
    v = tri[2] - tri[0]
    w = p - tri[0]

    alpha = -(np.dot(u,v) * np.dot(w,v) - np.dot(v,v) * np.dot(w,u)) / (np.dot(u,v)^2 - np.dot(u,u) * np.dot(v,v))
    beta = -(np.dot(u,v) * np.dot(w,u) - np.dot(u,u) * np.dot(w,v)) / (np.dot(u,v)^2 - np.dot(u,u) * np.dot(v,v))

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