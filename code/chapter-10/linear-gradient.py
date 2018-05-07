# -----------------------------------------------------------------------------
# Python, OpenGL & Scientific Visualization
# www.labri.fr/perso/nrougier/python+opengl
# Copyright (c) 2018, Nicolas P. Rougier
# Distributed under the 2-Clause BSD License.
# -----------------------------------------------------------------------------
import numpy as np
from glumpy import app, gl, gloo

vertex = """
attribute vec2 position;
varying vec2 v_position;
void main() {
    v_position = position;
    gl_Position = vec4(position.xy, 0.0, 1.0);
}
"""

fragment = """
uniform vec2 center;
uniform vec3 color1, color2;
varying vec2 v_position;
void main() {
    float a = (v_position.x+1.0)/2.0;
    gl_FragColor.rgb = mix(color1, color2, a);
    gl_FragColor.a = 1.0;
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
polygon["center"] = 1.0, 0.0
polygon["color1"] = 1,1,1
polygon["color2"] = 0,0,0

app.run()
