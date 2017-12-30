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
  void main() {
      gl_PointSize = 5.0;
      gl_Position = vec4(position, 0.0, 1.0);
  } """

fragment = """
  void main() {
       gl_FragColor = vec4(vec3(0.0), 1.0);
  } """

window = app.Window(512, 512, color=(1,1,1,1))
points = gloo.Program(vertex, fragment, count=1000)
points["position"] = np.random.uniform(-1,1,(len(points),2))
    
@window.event
def on_draw(dt):
    window.clear()
    points.draw(gl.GL_POINTS)
    
app.run()
