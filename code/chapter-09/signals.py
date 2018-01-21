# -----------------------------------------------------------------------------
# Python & OpenGL for Scientific Visualization
# www.labri.fr/perso/nrougier/python+opengl
# Copyright (c) 2018, Nicolas P. Rougier
# Distributed under the 2-Clause BSD License.
# -----------------------------------------------------------------------------
import numpy as np
from glumpy import app, gloo, gl

vertex = """
    uniform vec2 shape;
    attribute float xdata, ydata, index;
    varying float v_index;
    void main() {
        float rows = shape.x;
        float cols = shape.y;
        float i = mod(index,cols);
        float j = index/cols - fract(index/cols);
        float x = -1.0 + (0.025 + i + 0.95*xdata)*(2.0/cols);
        float y = -1.0 + (0.025 + j + 0.95*ydata)*(2.0/rows);
        gl_Position = vec4(vec2(x, y), 0.0, 1.0);
        v_index = index;
    } """

fragment = """
  varying float v_index;
  void main() {
      if (fract(v_index) == 0)
          gl_FragColor = vec4(vec3(0.5), 1.0);
  } """

window = app.Window(2*512, 512, color=(1,1,1,1))

rows, cols, size = 15, 20, 100
ydata = np.random.uniform(0, 1, (rows, cols, size)).astype(np.float32)
xdata = np.zeros((rows*cols, size), dtype=np.float32)
xdata[:] = np.linspace(0, 1, size, endpoint=True)
index = np.zeros((rows*cols, size), dtype=np.float32)
index[:] = np.arange(rows*cols)[:,np.newaxis]

signals = gloo.Program(vertex, fragment, count=rows*cols*size)
signals["xdata"] = xdata.ravel()
signals["ydata"] = ydata.ravel()
signals["index"] = index.ravel()
signals["shape"] = rows, cols

@window.event
def on_draw(dt):
    window.clear()
    signals.draw(gl.GL_LINE_STRIP)
    ydata = signals["ydata"].reshape(rows, cols, size)
    ydata[:,:,:-1] = ydata[:,:,1:]
    ydata[:,:,-1] = np.random.uniform(0, 1, (rows, cols))
    
app.run()
