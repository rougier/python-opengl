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
      // Normalize & relative coordinates 
      vec2 p = (gl_FragCoord.xy - v_center) / v_radius;

      // Normalized distance to center
      float d  = length(p);

      // Normal vector to the shere
      vec3 normal = normalize(vec3(p, 1-d));

//      float a = 1.0;
//      float d = abs(length(p) - v_radius + 3.0) - 3.0;
//      if (d > 0.0) a = exp(-d*d);
//      gl_FragColor = vec4(vec3(0.0), a);

      vec3 direction = normalize(vec3(1.0, 1.0, 2.0));
      float diffuse = max(0.0, dot(direction, normal));

      vec3 red = vec3(1.0, 0.0, 0.0);
      float ambient = 0.15;

      if (d > 1.0) discard;
      gl_FragColor.rgb = red*diffuse;
      gl_FragColor.a = 1.0;

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
