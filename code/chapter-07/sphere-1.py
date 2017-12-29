# -----------------------------------------------------------------------------
# Python & OpenGL for Scientific Visualization
# www.labri.fr/perso/nrougier/python+opengl
# Copyright (c) 2018, Nicolas P. Rougier
# Distributed under the 2-Clause BSD License.
# -----------------------------------------------------------------------------
import numpy as np
from glumpy import app, gloo, gl

vertex = """
    uniform vec2 resolution;
    attribute vec2 center;
    attribute float radius;
    varying vec2 v_center;
    varying float v_radius;
    void main()
    {
        v_radius = radius;
        v_center = center;
        gl_PointSize = 2.0 + ceil(2.0*radius);
        gl_Position = vec4(2.0*center/resolution-1.0, 0.0, 1.0);
    } """

fragment = """
  varying vec2 v_center;
  varying float v_radius;
  void main()
  {
      vec2 p = gl_FragCoord.xy - v_center;
      float z = 1.0 - length(p)/v_radius;

      if (z > 0.0)
          gl_FragColor = vec4(vec3(0.0), 1.0);
      else
          discard;
  } """


V = np.zeros(1, [("center", np.float32, 2),
                 ("radius", np.float32, 1)])
V["center"] = 256,256
V["radius"] = 250

window = app.Window(512, 512, color=(1,1,1,1))
points = gloo.Program(vertex, fragment)
points.bind(V.view(gloo.VertexBuffer))

@window.event
def on_resize(width, height):
    points["resolution"] = width, height
    
@window.event
def on_draw(dt):
    window.clear()
    points.draw(gl.GL_POINTS)
    
app.run()
