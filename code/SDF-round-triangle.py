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
  float SDF_triangle(vec2 p0, vec2 p1, vec2 p2, vec2 p)
  {
      vec2 e0 = p1 - p0;
      vec2 e1 = p2 - p1;
      vec2 e2 = p0 - p2;

      vec2 v0 = p - p0;
      vec2 v1 = p - p1;
      vec2 v2 = p - p2;

      vec2 pq0 = v0 - e0*clamp( dot(v0,e0)/dot(e0,e0), 0.0, 1.0 );
      vec2 pq1 = v1 - e1*clamp( dot(v1,e1)/dot(e1,e1), 0.0, 1.0 );
      vec2 pq2 = v2 - e2*clamp( dot(v2,e2)/dot(e2,e2), 0.0, 1.0 );

      float s = sign( e0.x*e2.y - e0.y*e2.x );
      vec2 d = min( min( vec2( dot( pq0, pq0 ), s*(v0.x*e0.y-v0.y*e0.x) ),
                         vec2( dot( pq1, pq1 ), s*(v1.x*e1.y-v1.y*e1.x) )),
                         vec2( dot( pq2, pq2 ), s*(v2.x*e2.y-v2.y*e2.x) ));
      return -sqrt(d.x)*sign(d.y);
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
  uniform vec2 p1, p2, p3;
  void main()
  {
      float radius = 0.1;

      float d = SDF_triangle(p1, p2, p3, v_position) - radius;
      gl_FragColor = color(d);
  } """


window = app.Window(512, 512)
quad = gloo.Program(vertex, fragment, count=4)
quad['position'] = (-1,+1), (+1,+1), (-1,-1), (+1,-1)


phi = 0
@window.event
def on_draw(dt):
    global phi

    phi1 = np.pi*phi/180.0
    phi2 = np.pi*(phi+120)/180.0
    phi3 = np.pi*(phi+240)/180.0
    rho1 = rho2 = rho3 = 0.75;
    quad["p1"] = rho1*np.cos(phi1), rho1*np.sin(phi1)
    quad["p2"] = rho2*np.cos(phi2), rho2*np.sin(phi2)
    quad["p3"] = rho3*np.cos(phi3), rho3*np.sin(phi3)
    
    window.clear()
    quad.draw(gl.GL_TRIANGLE_STRIP)
    phi += 1.0

app.run(framerate=60, framecount=360)
