# -----------------------------------------------------------------------------
# Python and OpenGL for Scientific Visualization
# www.labri.fr/perso/nrougier/python+opengl
# Copyright (c) 2017, Nicolas P. Rougier
# Distributed under the 2-Clause BSD License.
# -----------------------------------------------------------------------------
import numpy as np
from PIL import Image
from glumpy import app, gl, glm, gloo, data

def cube():
    vtype = [('position', np.float32, 3),
             ('texcoord', np.float32, 2)]
    itype = np.uint32

    # Vertices positions
    p = np.array([[1, 1, 1], [-1, 1, 1], [-1, -1, 1], [1, -1, 1],
                  [1, -1, -1], [1, 1, -1], [-1, 1, -1], [-1, -1, -1]],
                 dtype=float)
    # Texture coords
    t = np.array([[0, 0], [0, 1], [1, 1], [1, 0]])

    faces_p = [0, 1, 2, 3,  0, 3, 4, 5,   0, 5, 6, 1,
               1, 6, 7, 2,  7, 4, 3, 2,   4, 7, 6, 5]
    faces_t = [0, 1, 2, 3,  0, 1, 2, 3,   0, 1, 2, 3,
               3, 2, 1, 0,  0, 1, 2, 3,   0, 1, 2, 3]

    vertices = np.zeros(24, vtype)
    vertices['position'] = p[faces_p]
    vertices['texcoord'] = t[faces_t]

    filled = np.resize(
       np.array([0, 1, 2, 0, 2, 3], dtype=itype), 6 * (2 * 3))
    filled += np.repeat(4 * np.arange(6, dtype=itype), 6)

    vertices = vertices.view(gloo.VertexBuffer)
    filled = filled.view(gloo.IndexBuffer)

    return vertices, filled



vertex = """
uniform mat4   model;      // Model matrix
uniform mat4   view;       // View matrix
uniform mat4   projection; // Projection matrix
attribute vec3 position;   // Vertex position
attribute vec2 texcoord;   // Vertex texture coordinates
varying vec2   v_texcoord;   // Interpolated fragment texture coordinates (out)

void main()
{
    // Assign varying variables
    v_texcoord  = texcoord;

    // Final position
    gl_Position = projection * view * model * vec4(position,1.0);
}
"""

fragment = """
uniform sampler2D texture;    // Texture 
varying vec2      v_texcoord; // Interpolated fragment texture coordinates (in)
void main()
{
    // Final color
    gl_FragColor = texture2D(texture, v_texcoord);
}
"""

window = app.Window(width=512, height=512, color=(1,1,1,1))

@window.event
def on_draw(dt):
    global phi, theta, duration

    window.clear()

    gl.glDisable(gl.GL_BLEND)
    gl.glEnable(gl.GL_DEPTH_TEST)
    cube.draw(gl.GL_TRIANGLES, I)


    # Rotate cube
    theta += 1.0 # degrees
    phi += 1.0 # degrees
    model = np.eye(4, dtype=np.float32)
    glm.rotate(model, theta, 0, 0, 1)
    glm.rotate(model, phi, 0, 1, 0)
    cube['model'] = model

@window.event
def on_resize(width, height):
    cube['projection'] = glm.perspective(45.0, width / float(height), 2.0, 100.0)

@window.event
def on_init():
    gl.glEnable(gl.GL_DEPTH_TEST)


V,I = cube()
cube = gloo.Program(vertex, fragment)
cube.bind(V)

cube['texture'] = np.array(Image.open("./crate.png"))
cube['model'] = np.eye(4, dtype=np.float32)
cube['view'] = glm.translation(0, 0, -5)
phi, theta = 40, 30

app.run(framerate=60, framecount=360)
