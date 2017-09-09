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
        gl_PointSize = linewidth + 2.0*antialias + ceil(2.0*radius);

        vec2 ndc = 2.0*position/resolution-1.0;
        gl_Position = vec4(ndc, 0.0, 1.0);
    } """

fragment = """
  float SDF_circle(vec2 p, float radius)
  {
      return length(p) - radius;
  }

  float SDF_coverage(float d, float antialias)
  {
      d = d + antialias;
      float alpha = d/antialias;
      if( d < 0.0 ) return 1.0;
      return exp(-alpha*alpha);
  }

  varying float v_radius;
  varying float v_linewidth;
  varying float v_antialias;
  varying vec2 v_position;
  void main()
  {
      vec2 p = gl_FragCoord.xy;
      if (v_radius < 1.0) {
          float d = SDF_circle(p - v_position, 1.0);
          gl_FragColor = vec4(vec3(0.0), v_radius*SDF_coverage(d, 1.0));
      } else {
          float d = SDF_circle(p - v_position, v_radius);
          gl_FragColor = vec4(vec3(0.0), SDF_coverage(d, 1.0));
      }
  } """


window = app.Window(1024, 1024, color=(1,1,1,1))

V = np.zeros(512, [("position",  np.float32, 2),
                   ("radius",    np.float32, 1),
                   ("linewidth", np.float32, 1),
                   ("antialias", np.float32, 1)])
R = np.linspace(64, 512, len(V))
T = np.linspace(0, 10.125*2*np.pi, len(V))
V["position"][:,0] = R*np.cos(T)+512
V["position"][:,1] = R*np.sin(T)+512
V["radius"] = np.linspace(0.0, 21.0, len(V))
V["linewidth"] = 1.0
V["antialias"] = 1.0

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
