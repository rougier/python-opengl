# -----------------------------------------------------------------------------
# Python, OpenGL & Scientific Visualization
# www.labri.fr/perso/nrougier/python+opengl
# Copyright (c) 2018, Nicolas P. Rougier
# Distributed under the 2-Clause BSD License.
# -----------------------------------------------------------------------------
import numpy as np
import scipy.spatial
from glumpy import app, gl, gloo
from glumpy.graphics.collections import MarkerCollection

vertex = """
attribute vec3 position;
void main() { gl_Position = vec4(position.xy, 0.0, 1.0); }
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

    points.draw()

np.random.seed(1)
P = 0.95 * np.random.uniform(-1, 1, (50,3))
# P = P[scipy.spatial.ConvexHull(P).vertices]

polygon = gloo.Program(vertex, fragment, count=len(P))
polygon["position"] = P
I = scipy.spatial.Delaunay(P[:,:2]).simplices
I = I.astype(np.uint32).view(gloo.IndexBuffer)
O = scipy.spatial.ConvexHull(P[:,:2]).vertices
O = O.astype(np.uint32).view(gloo.IndexBuffer)

H = P[scipy.spatial.ConvexHull(P[:,:2]).vertices]
points = MarkerCollection(marker="disc")
points.append(H, bg_color=(1,1,1,1), size=16)
points.append(P, bg_color=(0,0,0,1), size=4)

app.run()
