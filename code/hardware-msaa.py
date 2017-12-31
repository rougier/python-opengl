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
  // attribute vec2 position;
  in vec2 position;
  void main()
  { gl_Position = vec4(2.0*position/resolution-1.0, 0.0, 1.0); }
"""

fragment = """
  out vec4 color;
  void main() { color = vec4(vec3(0.0), 1.0); }
  // void main() { gl_FragColor = vec4(vec3(0.0), 1.0); }
"""

config = app.configuration.Configuration()
config.samples = 6
config.major_version = 3
config.minor_version = 2
config.profile = "core"
GLSL_version = "150"
window = app.Window(32, 8, color=(1,1,1,1), config=config)
             
triangle = gloo.Program(vertex, fragment, version=GLSL_version)
V = np.zeros(3, dtype=[("position", np.float32,2)])
V["position"] = (1.,3.), (7.,7.), (30., 1.)
V = V.view(gloo.VertexArray)
triangle.bind(V)
             
@window.event
def on_resize(width, height):
    triangle["resolution"] = width, height

@window.event
def on_init():
    gl.glEnable(gl.GL_MULTISAMPLE)
    pass
    
@window.event
def on_draw(dt):
    window.clear()
    triangle.draw(gl.GL_TRIANGLE_STRIP)


for i in range(window.config.samples):
    print(gl.glGetMultisamplefv(gl.GL_SAMPLE_POSITION, i))

app.run()
