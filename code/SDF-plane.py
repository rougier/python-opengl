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
  float SDF_plane(vec2 p0, vec2 p1, vec2 p)
  {
    vec2 T = p1 - p0;
    vec2 O = normalize(vec2(T.y, -T.x));
    return dot(O, p0 - p);
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
  uniform vec2 p0, p1;
  void main()
  {
      float d = SDF_plane(p0, p1, v_position);
      gl_FragColor = color(d);
  } """


window = app.Window(512, 512)
quad = gloo.Program(vertex, fragment, count=4)
quad['position'] = (-1,+1), (+1,+1), (-1,-1), (+1,-1)

phi = 0
@window.event
def on_draw(dt):
    global phi

    phi0 = np.pi*phi/180
    phi1 = np.pi*(phi+180)/180
    rho = 0.5
    quad["p0"] = rho*np.cos(phi0), rho*np.sin(phi0)
    quad["p1"] = rho*np.cos(phi1), rho*np.sin(phi1)
    
    window.clear()
    quad.draw(gl.GL_TRIANGLE_STRIP)
    phi += 1.0

app.run(framerate=60, framecount=360)
