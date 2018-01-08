# -----------------------------------------------------------------------------
# Python & OpenGL for Scientific Visualization
# www.labri.fr/perso/nrougier/python+opengl
# Copyright (c) 2018, Nicolas P. Rougier
# Distributed under the 2-Clause BSD License.
# -----------------------------------------------------------------------------
import numpy as np
from glumpy import app, gloo, gl

vertex = """
    attribute vec2 position;
    void main() { gl_Position = vec4(position, 0.0, 1.0); } """

fragment = """
  void main() { gl_FragColor = vec4(0.0, 0.0, 0.0, 1.0); } """

window = app.Window(512, 512, color=(1,1,1,1))

n = 100
segments = gloo.Program(vertex, fragment, count=2*n)
T = np.linspace(0,2*np.pi,n)
segments["position"][1::2,0] = np.cos(T)
segments["position"][1::2,1] = np.sin(T)


@window.event
def on_draw(dt):
    window.clear()
    segments.draw(gl.GL_LINES)
    
app.run()
