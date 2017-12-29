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
    attribute vec3 center;
    attribute float radius;
    varying vec3 v_center;
    varying float v_radius;
    void main()
    {
        v_radius = radius;
        v_center = center;
        gl_PointSize = 2.0 + ceil(2.0*radius);
        gl_Position = vec4(2.0*center.xy/resolution-1.0, v_center.z, 1.0);
    } """

fragment = """
  varying vec3 v_center;
  varying float v_radius;
  void main()
  {
      vec2 p = (gl_FragCoord.xy - v_center.xy)/v_radius;
      float z = 1.0 - length(p);
      if (z < 0.0) discard;

      gl_FragDepth = 0.5*v_center.z + 0.5*(1.0 - z);

      vec3 color = vec3(1.0, 0.0, 0.0);
      vec3 normal = normalize(vec3(p.xy, z));
      vec3 direction = normalize(vec3(1.0, 1.0, 1.0));
      float diffuse = max(0.0, dot(direction, normal));
      float specular = pow(diffuse, 24.0);
      gl_FragColor = vec4(max(diffuse*color, specular*vec3(1.0)), 1.0);
  } """


np.random.seed(1)
V = np.zeros(100, [("center", np.float32, 3),
                   ("radius", np.float32, 1)])
V["center"] = np.random.uniform(50,512-50,(len(V),3))
V["center"][:,2] = np.random.uniform(0,1,len(V))
V["radius"] = np.random.uniform(25,50,len(V))

window = app.Window(512, 512, color=(1,1,1,1))
points = gloo.Program(vertex, fragment)
points.bind(V.view(gloo.VertexBuffer))

@window.event
def on_resize(width, height):
    points["resolution"] = width, height
    
@window.event
def on_draw(dt):
    window.clear()
    gl.glEnable(gl.GL_DEPTH_TEST)
    points.draw(gl.GL_POINTS)
    
app.run()
