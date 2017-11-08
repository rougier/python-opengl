import numpy as np
from glumpy import app, gloo, gl, data

vertex = """
  attribute vec2 position;
  void main() { gl_Position = vec4(position, 0.0, 1.0); } """

fragment = """
  void main() { gl_FragColor = vec4(vec3(0.0), 1.0); } """

config = app.configuration.Configuration()
config.samples = 8
window = app.Window(32, 16, color=(1,1,1,1), config=config)

scene = gloo.Program(vertex, fragment, count=3)
p0, p1, p2 = (26,3), (10,13), (4,6)
V = np.array([p0, p1, p2])
scene['position'] = 2*V/(32,16) - 1

@window.event
def on_draw(dt):
    window.clear()
    # scene.draw(gl.GL_TRIANGLE_STRIP)
    scene.draw(gl.GL_LINE_LOOP)

@window.event
def on_init():
    gl.glEnable(gl.GL_MULTISAMPLE)

app.run()
