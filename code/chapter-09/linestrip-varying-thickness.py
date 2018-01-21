# -----------------------------------------------------------------------------
# Python & OpenGL for Scientific Visualization
# www.labri.fr/perso/nrougier/python+opengl
# Copyright (c) 2018, Nicolas P. Rougier
# Distributed under the 2-Clause BSD License.
# -----------------------------------------------------------------------------
import sys
import ctypes
import numpy as np
from glumpy import app, gloo, gl

vertex = """
uniform vec2 resolution;
uniform float antialias;
uniform float thickness;
uniform float linelength;
attribute vec4 prev, curr, next;
varying vec2 v_uv;
void main() {
    float w = thickness/2.0 + antialias;
    vec2 p;
    if (prev.xy == curr.xy) {
        vec2 t1 = normalize(next.xy - curr.xy);
        vec2 n1 = vec2(-t1.y, t1.x);
        v_uv = vec2(-w, curr.z*w);
        p = curr.xy - w*t1 + curr.z*w*n1;
    } else if (curr.xy == next.xy) {
        vec2 t0 = normalize(curr.xy - prev.xy);
        vec2 n0 = vec2(-t0.y, t0.x);
        v_uv = vec2(linelength+w, curr.z*w);
        p = curr.xy + w*t0 + curr.z*w*n0;
    } else {
        vec2 t0 = normalize(curr.xy - prev.xy);
        vec2 t1 = normalize(next.xy - curr.xy);
        vec2 n0 = vec2(-t0.y, t0.x);
        vec2 n1 = vec2(-t1.y, t1.x);
        vec2 miter = normalize(n0 + n1);
        float dy = w / dot(miter, n1);
        v_uv = vec2(curr.w, curr.z*w);
        p = curr.xy + dy*curr.z*miter;
    }
    gl_Position = vec4(2.0*p/resolution-1.0, 0.0, 1.0);
} """

fragment = """
uniform float antialias;
uniform float thickness;
uniform float linelength;
varying vec2 v_uv;

void main() {
    float d = 0;

    float s = 0.75 + 0.25*cos(0.1*v_uv.x);

    float w = s*thickness/2.0 - antialias;

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
        gl_FragColor = vec4(0.0, 0.0, 0.0, 1.0);
    } else {
        d /= antialias;
        gl_FragColor = vec4(0.0, 0.0, 0.0, exp(-d*d));
    }
} """

window = app.Window(512, 512, color=(1,1,1,1))

@window.event
def on_resize(width, height):
    spiral["resolution"] = width, height

@window.event
def on_draw(dt):
    window.clear()
    spiral.draw(gl.GL_TRIANGLE_STRIP)

def bake(P, closed=False):
    epsilon = 1e-10
    n = len(P)
    if closed and ((P[0]-P[-1])**2).sum() > epsilon:
        P = np.append(P, P[0])
        P = P.reshape(n+1,2)
        n = n+1
    V = np.zeros(((1+n+1),2,4), dtype=np.float32)
    V_prev, V_curr, V_next = V[:-2], V[1:-1], V[2:]
    V_curr[...,0] = P[:,np.newaxis,0]
    V_curr[...,1] = P[:,np.newaxis,1]
    V_curr[...,2] = 1,-1
    L = np.cumsum(np.sqrt(((P[1:]-P[:-1])**2).sum(axis=-1))).reshape(n-1,1)
    V_curr[1:,:,3] = L
    if closed:
        V[0], V[-1] = V[-3], V[2]
    else:
        V[0], V[-1] = V[1], V[-2]
    return V_prev, V_curr, V_next, L[-1]

n = 512
T = np.linspace(0, 4*2*np.pi, n, dtype=np.float32)
R = np.linspace(64, 256-32, n, dtype=np.float32)
P = np.dstack((256+np.cos(T)*R, 256+np.sin(T)*R)).squeeze()
V_prev, V_curr, V_next, length = bake(P)
spiral = gloo.Program(vertex, fragment)
spiral["prev"], spiral["curr"], spiral["next"]  = V_prev, V_curr, V_next
spiral["thickness"] = 32.0
spiral["antialias"] = 1.5
spiral["linelength"] = length

app.run()
