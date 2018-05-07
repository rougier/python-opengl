# -----------------------------------------------------------------------------
# Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
import numpy as np
from glumpy import app, gl, glm, gloo


vertex = """
uniform mat4 view, model, projection;
attribute vec3 position;
void main()
{
    gl_Position = projection * view * model * vec4(position, 1.0);
}
"""

fragment = """
uniform vec4 color;
void main()
{
    gl_FragColor = color;
}
"""


window = app.Window(width=512, height=512, color=(1,1,1,1))

@window.event
def on_draw(dt):
    window.clear()
    gl.glDisable(gl.GL_BLEND)
    gl.glEnable(gl.GL_DEPTH_TEST)
    gl.glEnable(gl.GL_POLYGON_OFFSET_FILL)
    program["color"] = 0.75, 0.75, 0.75, 1.0
    program.draw(gl.GL_TRIANGLES, indices)

    gl.glDisable(gl.GL_POLYGON_OFFSET_FILL)
    gl.glEnable(gl.GL_BLEND)
    gl.glDepthMask(gl.GL_FALSE)
    program["color"] = 0.0, 0.0, 0.0, 1.0
    program.draw(gl.GL_LINES, indices)
    gl.glDepthMask(gl.GL_TRUE)
    
@window.event
def on_resize(width, height):
    program['projection'] = glm.perspective(25.0, width / float(height), 2.0, 100.0)

@window.event
def on_init():
    gl.glEnable(gl.GL_DEPTH_TEST)
    gl.glPolygonOffset(1, 1)
    gl.glEnable(gl.GL_LINE_SMOOTH)

def surface(func, umin=0, umax=np.pi, ucount=64,
                  vmin=0, vmax=np.pi, vcount=64):
    vtype = [('position', np.float32, 3)]
    itype = np.uint32
    vcount += 1
    ucount += 1
    n = vcount*ucount
    Un = np.repeat(np.linspace(0, 1, ucount, endpoint=True), vcount)
    Vn = np.tile  (np.linspace(0, 1, vcount, endpoint=True), ucount)
    U = umin+Un*(umax-umin)
    V = vmin+Vn*(vmax-vmin)
    vertices = np.zeros(n, dtype=vtype)
    for i,(u,v) in enumerate(zip(U,V)):
        x,y,z = func(u,v)
        vertices["position"][i] = x,y,z
    indices = []
    for i in range(ucount-1):
        for j in range(vcount-1):
            indices.append(i*(vcount) + j        )
            indices.append(i*(vcount) + j+1      )
            indices.append(i*(vcount) + j+vcount+1)
            indices.append(i*(vcount) + j+vcount  )
            indices.append(i*(vcount) + j+vcount+1)
            indices.append(i*(vcount) + j        )
    indices = np.array(indices, dtype=itype)
    return vertices.view(gloo.VertexBuffer), indices.view(gloo.IndexBuffer)

def boy(u, v):
    from math import cos, sin, sqrt
    s2 = sqrt(2)
    cu, su = cos(u), sin(u)
    cv, sv = cos(v), sin(v)
    c2v, s2v = cos(2*v), sin(2*v)
    s2u, s3v = sin(2*u), sin(3*v)
    x = 2/3 * (cu * c2v + s2*su*cv) * cu/(s2-s2u*s3v)
    y = 2/3 * (cu * s2v - s2*su*sv) * cu/(s2-s2u*s3v)
    z = -s2*cu*cu/(s2-s2u*s3v)
    return x, y, z

vertices, indices = surface(boy)
program = gloo.Program(vertex, fragment)
program.bind(vertices)
view = np.eye(4, dtype=np.float32)
model = np.eye(4, dtype=np.float32)
projection = np.eye(4, dtype=np.float32)
glm.translate(view, 0, 0, -5)
program['model'] = model
program['view'] = view

app.run()
