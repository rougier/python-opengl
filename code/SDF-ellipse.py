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
  float SDF_ellipse(vec2 p, vec2 ab)
  {
      // The function does not like circles
      if (ab.x == ab.y) ab.x = ab.x*0.9999;

      p = abs( p ); if( p.x > p.y ){ p=p.yx; ab=ab.yx; }
      float l = ab.y*ab.y - ab.x*ab.x;
      float m = ab.x*p.x/l; 
      float n = ab.y*p.y/l; 
      float m2 = m*m;
      float n2 = n*n;
      float c = (m2 + n2 - 1.0)/3.0; 
      float c3 = c*c*c;
      float q = c3 + m2*n2*2.0;
      float d = c3 + m2*n2;
      float g = m + m*n2;
      float co;

      if( d<0.0 ) {
          float p = acos(q/c3)/3.0;
          float s = cos(p);
          float t = sin(p)*sqrt(3.0);
          float rx = sqrt( -c*(s + t + 2.0) + m2 );
          float ry = sqrt( -c*(s - t + 2.0) + m2 );
          co = ( ry + sign(l)*rx + abs(g)/(rx*ry) - m)/2.0;
      } else {
          float h = 2.0*m*n*sqrt( d );
          float s = sign(q+h)*pow( abs(q+h), 1.0/3.0 );
          float u = sign(q-h)*pow( abs(q-h), 1.0/3.0 );
          float rx = -s - u - c*4.0 + 2.0*m2;
          float ry = (s - u)*sqrt(3.0);
          float rm = sqrt( rx*rx + ry*ry );
          float p = ry/sqrt(rm-rx);
          co = (p + 2.0*g/rm - m)/2.0;
      }
      float si = sqrt( 1.0 - co*co );
      vec2 r = vec2( ab.x*co, ab.y*si );
      return length(r - p ) * sign(p.y-r.y);
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
