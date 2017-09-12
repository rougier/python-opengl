# -----------------------------------------------------------------------------
# Python & OpenGL for Scientific Visualization
# www.labri.fr/perso/nrougier/python+opengl
# Copyright (c) 2017, Nicolas P. Rougier
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
      float a = 1.0;
      float d = length(p) - v_radius + 1.0;
      if(d > 0.0) a = exp(-d*d);
      gl_FragColor = vec4(vec3(0.0), a);
  } """


V = np.zeros(16, [("center", np.float32, 2),
                  ("radius", np.float32, 1)])
V["center"] = np.dstack([np.linspace(32, 512-32, len(V)),
                         np.linspace(25, 28, len(V))])
V["radius"] = 15

window = app.Window(512, 50, color=(1,1,1,1))
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
