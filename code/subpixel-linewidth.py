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
    attribute vec2 position;
    attribute float radius;
    attribute float linewidth;
    attribute float antialias;

    varying float v_radius;
    varying float v_linewidth;
    varying float v_antialias;
    varying vec2 v_position;
    void main()
    {
        v_radius = radius;
        v_position = position;
        v_linewidth = linewidth;
        v_antialias = antialias;
        gl_PointSize = v_linewidth + 2.0*v_antialias + ceil(2.0*v_radius);
        vec2 ndc = 2.0*position/resolution-1.0;
        gl_Position = vec4(ndc, 0.0, 1.0);
    } """

fragment = """
  float SDF_circle(vec2 p, float radius)
  {
      return length(p) - radius;
  }

  vec4 SDF_color(float distance, float linewidth, float antialias,
                 vec4 fg_color, vec4 bg_color) {
      float t = linewidth/2.0 - antialias;
      float signed_distance = distance;
      float border_distance = abs(signed_distance) - t;
      float alpha = border_distance/antialias;
      alpha = exp(-alpha*alpha);
      if( border_distance < 0.0 ) {
          return fg_color;
      } else if( signed_distance < 0.0 ) {
          return mix(bg_color, fg_color, sqrt(alpha));
      } else {
          if( abs(signed_distance) < (linewidth/2.0 + antialias) ) {
              return vec4(fg_color.rgb, fg_color.a * alpha);
          } else {
              discard;
          }
      }
  }

  varying float v_radius;
  varying float v_linewidth;
  varying float v_antialias;
  varying vec2 v_position;
  void main() {
      vec2 p = gl_FragCoord.xy;
      float d = SDF_circle(p - v_position, v_radius);
      gl_FragColor = SDF_color(d, v_linewidth, v_antialias,
                               vec4(0.0,0.0,0.0,1.0),
                               vec4(0.0,0.0,0.0,0.0));
  } """




n_rows = 5
n_columns = 16
radius = 20
window = app.Window(n_columns*radius*2, n_rows*radius*2, color=(1,1,1,1))
V = np.zeros((n_rows, n_columns), [("position",  np.float32, 2),
                                   ("radius",    np.float32, 1),
                                   ("linewidth", np.float32, 1),
                                   ("antialias", np.float32, 1)])

for i in range(n_rows):
    X = np.linspace(radius, n_columns*radius*2 - radius, n_columns)
    Y = radius + i*radius*2
    V["position"][i,:,0] = X
    V["position"][i,:,1] = Y

V["radius"]       = radius
V["linewidth"]    = 1.0 # np.linspace(0.1, 8, n_columns)
V["antialias"]    = 1.0

# Second row
V["linewidth"][1] = np.linspace(0.1, 8, n_columns)

# Third row
V["linewidth"][2] = 1.0
V["antialias"][2] = np.linspace(0.1, 3, n_columns)

# Fourth row
V["linewidth"][3] = np.linspace(0.1, 8, n_columns)
V["radius"][3] = radius-np.linspace(0.1, 8, n_columns)/2

V = V.ravel()


points = gloo.Program(vertex, fragment)
V = V.view(gloo.VertexBuffer)
points['position'] = V['position']
points['radius'] = V['radius']
points['linewidth'] = V['linewidth']
points['antialias'] = V['antialias']

@window.event
def on_resize(width, height):
    points["resolution"] = width, height
    
@window.event
def on_draw(dt):
    window.clear()
    points.draw(gl.GL_POINTS)
app.run()
