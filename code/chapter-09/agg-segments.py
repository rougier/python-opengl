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
  uniform float antialias;

  attribute float thickness;
  attribute vec2 p0, p1, uv;

  varying float v_alpha, v_thickness;
  varying vec2 v_p0, v_p1, v_p;

  void main() {

      if( abs(thickness) < 1.0 ) {
         v_thickness = 1.0;
         v_alpha = abs(thickness);
      } else {
         v_thickness = abs(thickness);
         v_alpha = 1.0;
      } 

      float t = v_thickness/2.0 + antialias;
      float l = length(p1-p0);
      float u = 2.0*uv.x - 1.0;
      float v = 2.0*uv.y - 1.0;

      // Screen space
      vec2 T = normalize(p1-p0);
      vec2 O = vec2(-T.y , T.x);
      vec2 p = p0 + vec2(0.5,0.5) + uv.x*T*l + u*T*t + v*O*t;
      gl_Position = vec4(2.0*p/resolution-1.0, 0.0, 1.0);

      // Local space
      T = vec2(1.0, 0.0);
      O = vec2(0.0, 1.0);
      p = uv.x*T*l + u*T*t + v*O*t;

      v_p0 = vec2(0.0, 0.0);
      v_p1 = vec2(  l, 0.0);
      v_p  = p;
  } """

fragment = """
  uniform float antialias;
  varying float v_alpha, v_thickness;
  varying vec2 v_p0, v_p1, v_p;
  void main() {
      float d = 0;
      if( v_p.x < 0 )
          d = length(v_p - v_p0) - v_thickness/2.0 + antialias/2.0;
      else if ( v_p.x > length(v_p1-v_p0) )
          d = length(v_p - v_p1) - v_thickness/2.0 + antialias/2.0;
      else
          d = abs(v_p.y) - v_thickness/2.0 + antialias/2.0;
      if( d < 0)
          gl_FragColor = vec4(0.0, 0.0, 0.0, v_alpha);
      else if (d < antialias) {
          d = exp(-d*d);
          gl_FragColor = vec4(0.0, 0.0, 0.0, d*v_alpha);
      } 
      else {
          gl_FragColor = vec4(0.0, 0.0, 0.0, 0.0);
      }
  } """

window = app.Window(1200, 400, color=(1,1,1,1))

n = 100
V = np.zeros((n,4), dtype=[('p0', np.float32, 2),
                           ('p1', np.float32, 2),
                           ('uv', np.float32, 2),
                           ('thickness', np.float32, 1)])
V["p0"] = np.dstack((np.linspace(100,1100,n),np.ones(n)* 50)).reshape(n,1,2)
V["p1"] = np.dstack((np.linspace(110,1110,n),np.ones(n)*350)).reshape(n,1,2)
V["uv"] = (0,0), (0,1), (1,0), (1,1)
V["thickness"] = np.linspace(0.1, 8.0, n).reshape(n,1)

segments = gloo.Program(vertex, fragment, count=4*n)
segments.bind(V.ravel().view(gloo.VertexBuffer))
segments["antialias"] = 2.0

I = np.zeros((n,6), dtype=np.uint32)
I[:] = [0,1,2,1,2,3]
I += 4*np.arange(n,dtype=np.uint32).reshape(n,1)
I = I.ravel().view(gloo.IndexBuffer)

@window.event
def on_resize(width, height):
    segments["resolution"] = width, height

@window.event
def on_draw(dt):
    window.clear()
    segments.draw(gl.GL_TRIANGLES, I)
    
app.run()
