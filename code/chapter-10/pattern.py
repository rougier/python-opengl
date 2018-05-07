# -----------------------------------------------------------------------------
# Python, OpenGL & Scientific Visualization
# www.labri.fr/perso/nrougier/python+opengl
# Copyright (c) 2018, Nicolas P. Rougier
# Distributed under the 2-Clause BSD License.
# -----------------------------------------------------------------------------
import numpy as np
from glumpy import app, gl, gloo, data

vertex = """
attribute vec2 position;
varying   vec2 v_texcoord;
void main() {
    v_texcoord = (position+1.0)/2.0;
    gl_Position = vec4(position.xy, 0.0, 1.0);
}
"""

fragment = """
uniform sampler2D u_texture;
varying vec2      v_texcoord;
void main()
{
    gl_FragColor = texture2D(u_texture, v_texcoord);
}
"""

window = app.Window(width=512, height=512, color=(1, 1, 1, 1))

@window.event
def on_draw(dt):
    window.clear()
    polygon.draw(gl.GL_TRIANGLE_FAN)
   
P = np.zeros((1+64,2), dtype=np.float32)
T = np.linspace(0,2*np.pi, len(P)-1, endpoint = True)
P[1:,0], P[1:,1] = 0.95*np.cos(T), 0.95*np.sin(T)
polygon = gloo.Program(vertex, fragment, count=len(P))
polygon["position"] = P
polygon['u_texture'] = data.load("wave.png")
app.run()
