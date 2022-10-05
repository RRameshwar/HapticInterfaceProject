import pygame as pg
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

import pywavefront


## Bunny model
scene = pywavefront.Wavefront('bunny.obj', collect_faces=True)

scene_box = (scene.vertices[0], scene.vertices[0])
for vertex in scene.vertices:
    min_v = [min(scene_box[0][i], vertex[i]) for i in range(3)]
    max_v = [max(scene_box[1][i], vertex[i]) for i in range(3)]
    scene_box = (min_v, max_v)


scene_trans    = [-(scene_box[1][i]+scene_box[0][i])/2 for i in range(3)]

scaled_size    = 5
scene_size     = [scene_box[1][i]-scene_box[0][i] for i in range(3)]
max_scene_size = max(scene_size)
scene_scale    = [scaled_size/max_scene_size for i in range(3)]

def Model():
    glPushMatrix()
    glScalef(*scene_scale)
    glTranslatef(*scene_trans)

    for mesh in scene.mesh_list:
        glBegin(GL_TRIANGLES)
        for face in mesh.faces:
            for vertex_i in face:
                glVertex3f(*scene.vertices[vertex_i])
        glEnd()

    glPopMatrix()

## Cube model:

cubeVertices = ((1,1,1),(1,1,-1),(1,-1,-1),(1,-1,1),(-1,1,1),(-1,-1,-1),(-1,-1,1),(-1,1,-1))
cubeEdges = ((0,1),(0,3),(0,4),(1,2),(1,7),(2,5),(2,3),(3,6),(4,6),(4,7),(5,6),(5,7))
cubeQuads = ((0,3,6,4),(2,5,6,3),(1,2,5,7),(1,0,4,7),(7,4,6,5),(2,3,0,1))

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
