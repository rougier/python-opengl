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
    varying vec2 v_position;
    void main(){
        v_position = position;
        gl_Position = vec4(position, 0.0, 1.0);
    } """

fragment = """
  #include "./SDF-palette.glsl"

  float SDF_box(vec2 p, vec2 size)
  {
       vec2 d = abs(p) - size;
       return min(max(d.x,d.y),0.0) + length(max(d,0.0));
  }

  float SDF_round_box(vec2 p, vec2 size, float radius)
  {
       return SDF_box(p, size) - radius;
  }

  varying vec2 v_position;
  uniform vec2 size;
  void main()
  {
      float radius = 0.1;
      float d = SDF_round_box(v_position, size, radius);
      gl_FragColor = color(d);
  } """


window = app.Window(512, 512)
quad = gloo.Program(vertex, fragment, count=4)
quad['position'] = (-1,+1), (+1,+1), (-1,-1), (+1,-1)

phi = 0
@window.event
def on_draw(dt):
    global phi
    
    window.clear()
    phi0 = np.pi*phi/180.0
    quad["size"] = 0.5+0.25*np.cos(phi0), 0.5+0.25*np.sin(2*phi0)
    quad.draw(gl.GL_TRIANGLE_STRIP)
    phi += 1.0

app.run(framerate=60, framecount=360)
