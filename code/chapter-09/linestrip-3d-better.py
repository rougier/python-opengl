# -----------------------------------------------------------------------------
# Python & OpenGL for Scientific Visualization
# www.labri.fr/perso/nrougier/python+opengl
# Copyright (c) 2018, Nicolas P. Rougier
# Distributed under the 2-Clause BSD License.
# -----------------------------------------------------------------------------
import sys
import ctypes
import numpy as np
from glumpy import app, gloo, gl, glm

vertex = """
uniform vec2 viewport;
uniform mat4 model, view, projection;
uniform float antialias, thickness, linelength;
attribute vec3 prev, curr, next;
attribute vec2 uv;
varying vec2 v_uv;
varying vec3 v_normal;
varying float v_thickness;
void main() {

    // Normalized device coordinates
    vec4 NDC_prev = projection * view * model * vec4(prev.xyz, 1.0);
    vec4 NDC_curr = projection * view * model * vec4(curr.xyz, 1.0);
    vec4 NDC_next = projection * view * model * vec4(next.xyz, 1.0);

    // Viewport (screen) coordinates
    vec2 screen_prev = viewport * ((NDC_prev.xy/NDC_prev.w) + 1.0)/2.0;
    vec2 screen_curr = viewport * ((NDC_curr.xy/NDC_curr.w) + 1.0)/2.0;
    vec2 screen_next = viewport * ((NDC_next.xy/NDC_next.w) + 1.0)/2.0;

    // Compute tickness according to line orientation (through surface normal)
    vec4 normal = model*vec4(curr.xyz, 1.0);
    v_normal = normal.xyz;
    if (normal.z < 0)
        v_thickness = thickness/2.0;
    else
        v_thickness = thickness*(pow(normal.z,.5)+1)/2.;
    
    vec2 position;
    float w = thickness/2.0 + antialias;
    vec2 t0 = normalize(screen_curr.xy - screen_prev.xy);
    vec2 n0 = vec2(-t0.y, t0.x);
    vec2 t1 = normalize(screen_next.xy - screen_curr.xy);
    vec2 n1 = vec2(-t1.y, t1.x);
    v_uv = vec2(uv.x, uv.y*w);
    if (prev.xy == curr.xy) {
        v_uv.x = -w;
        position = screen_curr.xy - w*t1 + uv.y*w*n1;
    } else if (curr.xy == next.xy) {
        v_uv.x = linelength+w;
        position = screen_curr.xy + w*t0 + uv.y*w*n0;
    } else {
        vec2 miter = normalize(n0 + n1);
        // The max operator avoid glitches when miter is too large
        float dy = w / max(dot(miter, n1), 1.0);
        position = screen_curr.xy + dy*uv.y*miter;
    }

    // Back to NDC coordinates
    gl_Position = vec4(2.0*position/viewport-1.0, NDC_curr.z/NDC_curr.w, 1.0);
} """

fragment = """
uniform float antialias;
uniform float thickness;
uniform float linelength;
varying float v_thickness;
varying vec2 v_uv;
varying vec3 v_normal;
void main() {
    float d = 0;
    float w = v_thickness/2.0 - antialias;

    vec3 color = vec3(0.0, 0.0, 0.0);
    if (v_normal.z < 0)
        color = 0.75*vec3(pow(abs(v_normal.z),.5)); //*vec3(0.95, 0.75, 0.75);

    // Cap at start
    if (v_uv.x < 0)
        d = length(v_uv) - w;
    // Cap at end
    else if (v_uv.x >= linelength)
        d = length(v_uv - vec2(linelength,0)) - w;
    // Body
    else
        d = abs(v_uv.y) - w;
    if( d < 0) {
        gl_FragColor = vec4(color, 1.0);
    } else {
        d /= antialias;
        gl_FragColor = vec4(color, exp(-d*d));
    }
} """

window = app.Window(2*512, 2*512, color=(1,1,1,1))

@window.event
def on_resize(width, height):
    spiral['projection'] = glm.perspective(30.0, width / float(height), 2.0, 100.0)
    spiral['viewport'] = width, height
    
@window.event
def on_draw(dt):
    global phi, theta, duration
    window.clear()
    spiral.draw(gl.GL_TRIANGLE_STRIP)
    theta += .1 # degrees
    phi += .2 # degrees
    model = np.eye(4, dtype=np.float32)
    glm.rotate(model, theta, 0, 1, 0)
    glm.rotate(model, phi, 1, 0, 0)
    spiral['model'] = model

@window.event
def on_init():
    gl.glEnable( gl.GL_DEPTH_TEST )


def bake(P, closed=False):
    epsilon = 1e-10
    n = len(P)
    if closed and ((P[0]-P[-1])**2).sum() > epsilon:
        P = np.append(P, P[0])
        P = P.reshape(n+1,3)
        n = n+1
    V = np.zeros(((1+n+1),2,3), dtype=np.float32)
    UV = np.zeros((n,2,2), dtype=np.float32)
    V_prev, V_curr, V_next = V[:-2], V[1:-1], V[2:]
    V_curr[...,0] = P[:,np.newaxis,0]
    V_curr[...,1] = P[:,np.newaxis,1]
    V_curr[...,2] = P[:,np.newaxis,2]
    L = np.cumsum(np.sqrt(((P[1:]-P[:-1])**2).sum(axis=-1))).reshape(n-1,1)
    UV[1:,:,0] = L
    UV[...,1] = 1,-1
    if closed:
        V[0], V[-1] = V[-3], V[2]
    else:
        V[0], V[-1] = V[1], V[-2]
    return V_prev, V_curr, V_next, UV, L[-1]

n = 2048
T = np.linspace(0, 20*2*np.pi, n, dtype=np.float32)
R = np.linspace(.1, np.pi-.1, n, dtype=np.float32)
X = np.cos(T)*np.sin(R)
Y = np.sin(T)*np.sin(R)
Z = np.cos(R)
P = np.dstack((X,Y,Z)).squeeze()


V_prev, V_curr, V_next, UV, length = bake(P)
spiral = gloo.Program(vertex, fragment)
spiral["prev"], spiral["curr"], spiral["next"]  = V_prev, V_curr, V_next
spiral["uv"] = UV
spiral["thickness"] = 5.0
spiral["antialias"] = 1.5
spiral["linelength"] = length
spiral['model'] = np.eye(4, dtype=np.float32)
spiral['view'] = glm.translation(0, 0, -5)
phi, theta = 0, 0

app.run() #framerate=60, framecount=360)
