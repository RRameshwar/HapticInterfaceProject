import pygame as pg
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

import numpy as np

## Triangle model:

triangleVertices = ((0,0,0),(1,0,0),(0,1,0))
triangleEdges = ((0,1),(0,2),(1,2))
triangleSurfaces = ((0,1,2))

pointVertex = (0.25,0.25,0)


def triangle():
    glBegin(GL_LINES)
    for edge in triangleEdges:
        for vertex in edge:
            glVertex3fv(triangleVertices[vertex])
    glEnd()


def point():
    glPointSize(5)
    glBegin(GL_POINTS)
    glVertex3f(*pointVertex)
    glEnd()



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


def main():
    pg.init()
    display = (1680, 1050)
    pg.display.set_mode(display, DOUBLEBUF|OPENGL)

    glMatrixMode(GL_PROJECTION)
    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)

    # glTranslatef(0.0, 0.0, -5)
    glTranslatef(0.0, 0.0, -10)

    i = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT) # This must go before we draw our objects

        # glMatrixMode(GL_MODELVIEW)
        
        # glPushMatrix()
        
        # triangle()

        # i += 0.05
        # transMat = [-i,0,0]
        # glTranslatef(*transMat)
        point()
        # glPopMatrix()
        
        # newVertex = pointVertex + np.array(transMat)
        # print(newVertex)
        # detectCollision(triangleVertices,newVertex)
        

        pg.display.flip()
        pg.time.wait(10)


if __name__ == "__main__":
    main()
