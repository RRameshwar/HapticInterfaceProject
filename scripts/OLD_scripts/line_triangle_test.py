import pygame as pg
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

## Triangle model:

triangleVertices = ((0,0,0),(1,0,0),(0,1,0),(0,0,1))
triangleEdges = ((0,1),(0,2),(1,0),(1,2),(2,0),(2,1),(3,1),())
triangleSurfaces = ((0,1))

newVertex = [];
cubeVertices2 = [];

for vertex in cubeVertices:
    for n, i in enumerate(vertex):
        newVertex.append(i+5)
    cubeVertices2.append(tuple(newVertex))
    newVertex = [];

print(cubeVertices2)



# def wireCube():
#     glBegin(GL_LINES) 
#     for cubeEdge in cubeEdges:
#         for cubeVertex in cubeEdge:
#             glVertex3fv(cubeVertices[cubeVertex])
#     glEnd()

def solidCube():
    glBegin(GL_QUADS)
    for cubeQuad in cubeQuads:
        for cubeVertex in cubeQuad:
            glVertex3fv(cubeVertices[cubeVertex])
    glEnd()

def shiftedCube():
    glBegin(GL_QUADS)
    for cubeQuad in cubeQuads:
        for cubeVertex in cubeQuad:
            glVertex3fv(cubeVertices2[cubeVertex])
    glEnd()

def main():
    pg.init()
    display = (1680, 1050)
    pg.display.set_mode(display, DOUBLEBUF|OPENGL)

    gluPerspective(120, (display[0]/display[1]), 0.1, 50.0)

    # glTranslatef(0.0, 0.0, -5)
    glTranslatef(0.0, 0.0, -10)

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
        glTranslatef(0, 0, 0)
        glRotatef(1, 1, 1, 1)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        shiftedCube()
        #wireCube()
        Model()
        pg.display.flip()
        pg.time.wait(10)

if __name__ == "__main__":
    main()
