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

  uniform float theta;
  attribute vec2 position;
  attribute float angle;
  attribute vec2 center;
  varying vec2 v_position;
  void main()
  {
      v_position = position;
      vec2 p = position;

      p = vec2(p.x*cos(theta) - p.y*sin(theta),
               p.y*cos(theta) + p.x*sin(theta));
      p += center;
      p = vec2(p.x*cos(angle) - p.y*sin(angle),
               p.y*cos(angle) + p.x*sin(angle));

      p = p + resolution/2.0;
      gl_Position = vec4(2.0*p/resolution-1.0, 0.0, 1.0);
  } """

fragment = """
  float SDF_fake_box(vec2 p, vec2 size)
  {
       return max(abs(p.x)-size.x, abs(p.y)-size.y);
  }

  uniform vec2 size;
  varying vec2 v_position;
  void main()
  {
      float d = SDF_fake_box(v_position, size) + 1.0;
      d = abs(d); // Outline, comment for filled shape
      float a = 1.0;
      if(d > 0.0) a = exp(-d*d);
      gl_FragColor = vec4(vec3(0.0), a);
  } """


n = 20
aa = 1
a, b = 24, 24

x0,x1 = -a/2, +a/2
y0,y1 = -b/2, +b/2

v0 = 2*x0-aa, 2*y0-aa
v1 = 2*x0-aa, 2*y1+aa
v2 = 2*x1+aa, 2*y1+aa
v3 = 2*x1+aa, 2*y0-aa

window = app.Window(512, 512, color=(1,1,1,1))
ellipses = gloo.Program(vertex, fragment)
V = np.zeros((n,4), [("position", np.float32, 2),
                     ("center", np.float32, 2),
                     ("angle", np.float32, 1)])
V["position"] = [v0, v1, v2, v3]
V["angle"] = np.linspace(0, 2*np.pi, n, endpoint=False).reshape(n,1)
V["center"] = 0.0, +200.0

V = V.ravel()
ellipses.bind(V.view(gloo.VertexBuffer))
ellipses["size"] = a, b

I = np.zeros((n,6), dtype=np.uint32)
I[:] = 0,1,2, 0,2,3
I += 4*np.arange(0,n,dtype=np.uint32).reshape(n,1)
I = I.ravel()
I = I.view(gloo.IndexBuffer)

@window.event
def on_resize(width, height):
    ellipses["resolution"] = width, height

theta = 0
@window.event
def on_draw(dt):
    global theta
    theta += 0.5*np.pi/180.0
    ellipses["theta"] = theta
    window.clear()
    ellipses.draw(gl.GL_TRIANGLES, I)

app.run() #framerate=60, framecount = 360/30/0.1)

