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
  varying vec2 v_position;
  void main()
  {
      v_position = position;
      vec2 p = position;
      // This could be optimized but we don't care here
      p = vec2(p.x*cos(angle+theta) - p.y*sin(angle+theta),
               p.y*cos(angle+theta) + p.x*sin(angle+theta));
      p = p + resolution/2.0;
      gl_Position = vec4(2.0*p/resolution-1.0, 0.0, 1.0);
  } """

fragment = """
  float SDF_fake_ellipse(vec2 p, vec2 size)
  {
    float a = 1.0;
    float b = size.x/size.y;
    float r = 0.5*max(size.x,size.y);
    float f = length(p*vec2(a,b));
    return f*(f-r)/length(p*vec2(a*a,b*b));
  }

  uniform vec2 size;
  varying vec2 v_position;
  void main()
  {
      float d = SDF_fake_ellipse(v_position, size) + 1.0;
      float alpha;
      if (abs(d) < 1.0) alpha = exp(-d*d)/ 4.0;
      else if (d < 0.0) alpha =       1.0/16.0;
      else              alpha = exp(-d*d)/16.0;
      gl_FragColor = vec4(vec3(0.0), alpha);
  } """


n = 30
aa = 1
a, b = 450, 50

x0,x1 = -a/2, +a/2
y0,y1 = -b/2, +b/2

v0 = x0-aa, y0-aa
v1 = x0-aa, y1+aa
v2 = x1+aa, y1+aa
v3 = x1+aa, y0-aa

window = app.Window(512, 512, color=(1,1,1,1))
ellipses = gloo.Program(vertex, fragment)
V = np.zeros((n,4), [("position", np.float32, 2),
                     ("angle",  np.float32, 1)])
V["position"] = [v0, v1, v2, v3]
V["angle"] = np.linspace(0, 2*np.pi, n, endpoint=False).reshape(n,1)

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
    theta += 0.1*np.pi/180.0
    ellipses["theta"] = theta
    window.clear()
    ellipses.draw(gl.GL_TRIANGLES, I)

app.run(framerate=60, framecount = 360/30/0.1)

