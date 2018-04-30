# -----------------------------------------------------------------------------
# Python, OpenGL & Scientific Visualization
# www.labri.fr/perso/nrougier/python+opengl
# Copyright (c) 2018, Nicolas P. Rougier
# Distributed under the 2-Clause BSD License.
# -----------------------------------------------------------------------------
import numpy as np
import scipy.spatial
from glumpy import app, gl, gloo

vertex = """
attribute vec2 position;
void main() { gl_Position = vec4(position, 0.0, 1.0); }
"""

fragment = """
void main() { gl_FragColor = vec4(0.0,0.0,0.0,1.0); }
"""

config = app.configuration.Configuration()
config.stencil_size = 8
window = app.Window(config=config, width=512, height=512, color=(1, 1, 1, 1))

@window.event
def on_draw(dt):
    window.clear()

    gl.glColorMask(gl.GL_FALSE, gl.GL_FALSE, gl.GL_FALSE, gl.GL_FALSE)
    gl.glStencilFunc(gl.GL_ALWAYS, 0x1, 0x1)
    gl.glStencilOp(gl.GL_KEEP, gl.GL_INVERT, gl.GL_INVERT)
    polygon.draw(gl.GL_TRIANGLE_FAN)

    gl.glColorMask(gl.GL_TRUE, gl.GL_TRUE, gl.GL_TRUE, gl.GL_TRUE)
    gl.glStencilFunc(gl.GL_EQUAL, 0x1, 0x1)
    gl.glStencilOp(gl.GL_KEEP, gl.GL_KEEP, gl.GL_KEEP)
    polygon.draw(gl.GL_TRIANGLE_FAN)

@window.event
def on_init():
    gl.glEnable(gl.GL_STENCIL_TEST)

def star(inner=0.35, outer=0.9, n=5):
    R = np.array( [inner,outer]*n)
    T = np.linspace(-0.5*np.pi, 1.5*np.pi, 2*n, endpoint=False)
    P = np.zeros((2+2*n,2))
    P[1:-1,0]= R*np.cos(T)
    P[1:-1,1]= R*np.sin(T)
    P[0] = 0,-1
    P[-1] = P[1]
    return P

P = star()
polygon = gloo.Program(vertex, fragment, count=len(P))
polygon["position"] = P
app.run()
