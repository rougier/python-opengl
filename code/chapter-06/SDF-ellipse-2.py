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
  const float M_PI = 3.14159265358979323846264338327950288;
  const float M_PI_2 = 1.57079632679489661923132169163975144;

  float SDF_ellipse(vec2 p, vec2 ab)
  {
     float t = M_PI / 4.0;
     float a = ab.x;
     float b = ab.y;
     float x, y;
     int i;

     for(i=0; i<3; i++) {
         x = a * cos(t);
         y = b * sin(t);

         float ex = (a*a - b*b) * pow(cos(t),3) / a;
         float ey = (b*b - a*a) * pow(sin(t),3) / b;

         float rx = x - ex;
         float ry = y - ey;

         float qx = abs(p.x) - ex;
         float qy = abs(p.y) - ey;

         float r = length(vec2(ry, rx));
         float q = length(vec2(qy, qx));

         float delta_c = r * asin((rx*qy - ry*qx)/(r*q));
         float delta_t = delta_c / sqrt(a*a + b*b - x*x - y*y);

         t += delta_t;
         t = min(M_PI_2, max(0., t));
     }
     return length(vec2(p.x - x*sign(p.x), p.y - y*sign(p.y)));
  }

  vec4 color(float d)
  {
      vec3 white = vec3(1.0, 1.0, 1.0);
      vec3 blue  = vec3(0.1, 0.4, 0.7);
      vec3 color = white - sign(d)*blue;
      color *= (1.0 - exp(-4.0*abs(d))) * (0.8 + 0.2*cos(140.0*d));
      color = mix(color, white, 1.0-smoothstep(0.0,0.02,abs(d)) );
      return vec4(color, 1.0);
  }

  varying vec2 v_position;
  uniform vec2 size;
  void main()
  {
      float d = SDF_ellipse(v_position, size);
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
