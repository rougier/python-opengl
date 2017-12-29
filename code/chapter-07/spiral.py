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
    attribute float size;
    varying vec2 center;
    varying float radius;
    void main() {
        gl_Position = vec4(position, 0.0, 1.0);
        gl_PointSize = 2.0+ceil(size);
        center = 512.0 + position*512.0;
        radius = size/2.0;
    } """

fragment = """
  float coverage(float d, float antialias)
  {
      d = d + antialias;
      float alpha = d/antialias;
      if( d < 0.0 ) return 1.0;
      return exp(-alpha*alpha);
  }

  float circle(vec2 p, vec2 center, float radius)
  {
      return length(p - center) - radius;
  }

  varying vec2 center;
  varying float radius;
  void main()
  {
      vec2 p = gl_FragCoord.xy;
      float antialias = 1.0;
      if (radius < 1.0) {
          float d = circle(p, center, 1.0);
          gl_FragColor = vec4(vec3(0.0), radius*coverage(d, 1.0));
      } else {
          float d = circle(p, center, radius);
          gl_FragColor = vec4(vec3(0.0), coverage(d, 1.0));
      }
  } """


window = app.Window(1024, 1024, color=(1,1,1,1))

V = np.zeros(600, [("position", np.float32, 2),
                   ("size",     np.float32, 1)])
R = np.linspace(0.05, 0.95, len(V))
T = np.linspace(0, 10.125*2*np.pi, len(V))
S = np.linspace(0.0, 42.0, len(V))
V["position"][:,0] = R*np.cos(T)
V["position"][:,1] = R*np.sin(T)
V["size"]          = S

points = gloo.Program(vertex, fragment)
V = V.view(gloo.VertexBuffer)
points['position'] = V['position']
points['size'] = V['size']

@window.event
def on_draw(dt):
    window.clear()
    points.draw(gl.GL_POINTS)
app.run()
