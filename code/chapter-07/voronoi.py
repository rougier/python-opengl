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
    attribute vec3 color;
    attribute float radius;
    varying vec2 v_center;
    varying vec3 v_color;
    varying float v_radius;
    void main()
    {
        v_radius = radius;
        v_center = center;
        v_color  = color;
        gl_PointSize = 2.0 + ceil(2.0*radius);
        gl_Position = vec4(2.0*center/resolution-1.0, 0.0, 1.0);
    } """

fragment = """
  varying vec2 v_center;
  varying vec3 v_color;
  varying float v_radius;
  void main()
  {
      vec2 p = (gl_FragCoord.xy - v_center.xy)/v_radius;
      float z = 1.0 - length(p);
      if (z < 0.0) discard;
      gl_FragDepth = (1.0 - z);
      gl_FragColor = vec4(v_color, 1.0);
  } """


V = np.zeros(1000, [("center", np.float32, 2),
                    ("color",  np.float32, 3),
                    ("radius", np.float32, 1)])
V["center"] = np.random.uniform(0,1024,(len(V),2))
V["color"] = np.random.uniform(0.25,1.00,(len(V),3))
V["radius"] = 100

window = app.Window(1024, 1024, color=(1,1,1,1))
points = gloo.Program(vertex, fragment)
points.bind(V.view(gloo.VertexBuffer))

@window.event
def on_resize(width, height):
    points["resolution"] = width, height
    
@window.event
def on_draw(dt):
    window.clear()
    points.draw(gl.GL_POINTS)

@window.event
def on_init():
    gl.glEnable(gl.GL_DEPTH_TEST)

app.run()
