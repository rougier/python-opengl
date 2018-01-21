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
varying float v_alpha;
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
    v_alpha = curr.w / linelength;
} """

fragment = """
uniform float antialias;
uniform float thickness;
uniform float linelength;
uniform float phase;
varying vec2 v_uv;
varying float v_alpha;

void main() {
    float d = 0;
    float w = thickness/2.0 - antialias;

    float spacing = 1.5;
    float center = v_uv.x + spacing/2.0*thickness
                 - mod(v_uv.x + phase + spacing/2.0*thickness, spacing*thickness);
    if (linelength - center < thickness/2.0)
        discard;
    else if (center < thickness/2.0)
        discard;
    else
        d = length(v_uv - vec2(center,0.0)) - w;

    if( d < 0) {
        gl_FragColor = vec4(0.0, 0.0, 0.0, 1.0);
    } else {
        d /= antialias;
        gl_FragColor = vec4(0.0, 0.0, 0.0, exp(-d*d));
    }
} """

window = app.Window(512, 512, color=(1,1,1,1))
phase = 0
@window.event
def on_resize(width, height):
    line["resolution"] = width, height

@window.event
def on_draw(dt):
    global phase
    window.clear()
    phase -= 0.01*12
    line["phase"] = phase
    line.draw(gl.GL_TRIANGLE_STRIP)

def bake(P):
    n = len(P)
    V = np.zeros(((1+n+1),2,4), dtype=np.float32)
    V_prev, V_curr, V_next = V[:-2], V[1:-1], V[2:]
    V_curr[...,0] = P[:,np.newaxis,0]
    V_curr[...,1] = P[:,np.newaxis,1]
    V_curr[...,2] = 1,-1
    L = np.cumsum(np.sqrt(((P[1:]-P[:-1])**2).sum(axis=-1))).reshape(n-1,1)
    V_curr[1:,:,3] = L
    V[0], V[-1] = V[1], V[-2]
    return V_prev, V_curr, V_next, L[-1]

n = 512
T = np.linspace(0, 10*2*np.pi, n, dtype=np.float32)
R = np.linspace(64, 250, n, dtype=np.float32)
P = np.dstack((256+np.cos(T)*R, 256+np.sin(T)*R)).squeeze()
V_prev, V_curr, V_next, length = bake(P)

line = gloo.Program(vertex, fragment)
line["prev"], line["curr"], line["next"]  = V_prev, V_curr, V_next
line["thickness"] = 12.0
line["antialias"] = 1.5
line["linelength"] = length

app.run()
