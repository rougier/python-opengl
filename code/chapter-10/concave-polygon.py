# -----------------------------------------------------------------------------
# Python, OpenGL & Scientific Visualization
# www.labri.fr/perso/nrougier/python+opengl
# Copyright (c) 2018, Nicolas P. Rougier
# Distributed under the 2-Clause BSD License.
# -----------------------------------------------------------------------------
import triangle
import numpy as np
from glumpy import app, gl, gloo

vertex = """
attribute vec2 position;
void main() { gl_Position = vec4(position, 0.0, 1.0); }
"""

fragment = """
uniform vec4 color;
void main() { gl_FragColor = color; }
"""

window = app.Window(width=512, height=512, color=(1, 1, 1, 1))

@window.event
def on_draw(dt):
    window.clear()

    polygon["color"] = 0.95, 0.95, 0.95, 1.00
    gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_FILL)
    polygon.draw(gl.GL_TRIANGLES, I)

    gl.glLineWidth(1.0)
    polygon["color"] = 0.50, 0.50, 0.50, 1.00
    gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_LINE)
    polygon.draw(gl.GL_TRIANGLES, I)

    gl.glLineWidth(3.0)
    polygon["color"] = 0.00, 0.00, 0.00, 1.00
    polygon.draw(gl.GL_LINE_LOOP, O)

def star(inner=0.35, outer=0.9, n=5):
    R = np.array( [inner,outer]*n)
    T = np.linspace(-0.5*np.pi, 1.5*np.pi, 2*n, endpoint=False)
    P = np.zeros((2*n,2))
    P[:,0]= R*np.cos(T)
    P[:,1]= R*np.sin(T)
    return P

def triangulate(vertices):
    n = len(vertices)
    segments = (np.repeat(np.arange(n+1),2)[1:-1]) % n
    T = triangle.triangulate({'vertices': vertices, 'segments': segments}, "p")
    return T["vertices"], T["triangles"]

P, I = triangulate(star())
polygon = gloo.Program(vertex, fragment, count=len(P))
polygon["position"] = P
I = I.astype(np.uint32).view(gloo.IndexBuffer)
O = (np.repeat(np.arange(len(P)+1),2)[1:-1]) % len(P)
O = O.astype(np.uint32).view(gloo.IndexBuffer)
app.run()
