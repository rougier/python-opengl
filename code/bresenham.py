# -----------------------------------------------------------------------------
# Python & OpenGL for Scientific Visualization
# www.labri.fr/perso/nrougier/python+opengl
# Copyright (c) 2017, Nicolas P. Rougier
# Distributed under the 2-Clause BSD License.
# -----------------------------------------------------------------------------
import numpy as np
from glumpy import app, gloo, gl

vertex = """
    attribute vec2 position;
    void main(){ gl_Position = vec4(position, 0.0, 1.0); } """

fragment = """
  void main() { gl_FragColor = vec4(0.0, 0.0, 0.0, 1.0); } """

window = app.Window(128, 128, color=(1,1,1,1))
lines = gloo.Program(vertex, fragment, count=2)

P = np.array([ [ 1, 1],
               [12, 3.4]], dtype=np.float32)
P += (10,10)
P = 2*(P/128) - 1
lines['position'] = P

@window.event
def on_draw(dt):
    window.clear()
    lines.draw(gl.GL_LINES)
app.run()
