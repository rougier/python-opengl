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
  attribute vec2 center;
  attribute float angle;
  varying vec2 v_position;
  void main()
  {
      v_position = position;
      vec2 p = position + center;
      // This could be optimized but we don't care here
      p = vec2(p.x*cos(angle+theta) - p.y*sin(angle+theta),
               p.y*cos(angle+theta) + p.x*sin(angle+theta));
      p = p + resolution/2.0;
      gl_Position = vec4(2.0*p/resolution-1.0, 0.0, 1.0);
  } """

fragment = """
  float SDF_fake_triangle(vec2 p, vec2 p0, vec2 p1, vec2 p2)
  {
    vec2 e0 = p1 - p0;
    vec2 e1 = p2 - p1;
    vec2 e2 = p0 - p2;
    vec2 v0 = p - p0;
    vec2 v1 = p - p1;
    vec2 v2 = p - p2;
    vec2 o0 = normalize(vec2(e0.y, -e0.x));
    vec2 o1 = normalize(vec2(e1.y, -e1.x));
    vec2 o2 = normalize(vec2(e2.y, -e2.x));
    return max(max(dot(o0,v0), dot(o1,v1)), dot(o2,v2));
  }

  uniform vec2 p0, p1, p2;
  varying vec2 v_position;
  varying vec4 v_color;
  void main()
  {
      float d = SDF_fake_triangle(v_position, p0, p1, p2) + 1.0;
      d = abs(d); // Outline, comment for filled shape
      float a = 1.0;
      if(d > 0.0) a = exp(-d*d);
      gl_FragColor = vec4(vec3(0.0), a);
  } """



x0, x1 = -8, +8
y0, y1 = 0, 3*32

p0 = x0, y0
p1 = x1, y0
p2 = (x0+x1)/2, y1

aa = 1
v0 = x0-aa, y0-aa
v1 = x1+aa, y0-aa
v2 = (x0+x1)/2, y1+8+aa


window = app.Window(512, 512, color=(1,1,1,1))

triangles = gloo.Program(vertex, fragment)

n = 2*30
V = np.zeros((n,3), [("position", np.float32, 2),
                     ("center", np.float32, 2),
                     ("angle",  np.float32, 1)])
V["position"] = [v0, v1, v2]
V["angle"] = np.linspace(0, 4*np.pi, n, endpoint=False).reshape(n,1)
V["center"][:n//2] = 0.0, +128.0 + 3
V["center"][n//2:] = 0.0, -128.0 + 3

V = V.ravel()
triangles.bind(V.view(gloo.VertexBuffer))
I = np.arange(0,3*n,dtype=np.uint32)
I = I.view(gloo.IndexBuffer)

triangles["p0"] = p0
triangles["p1"] = p1
triangles["p2"] = p2

@window.event
def on_resize(width, height):
    triangles["resolution"] = width, height

theta = 0
triangles["theta"] = theta
    
@window.event
def on_draw(dt):
    global theta
    
    window.clear()
    triangles.draw(gl.GL_TRIANGLES, I)

    theta += 0.1*np.pi/180.0
    triangles["theta"] = theta
    
app.run(framerate=60, framecount = 360/30/0.1)
