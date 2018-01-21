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
from curves import curve4_bezier


point_vertex = """
  uniform vec2 resolution;
    attribute vec2 center;
    attribute float radius;
    varying vec2 v_center;
    varying float v_radius;
    void main() {
        v_radius = radius;
        v_center = center;
        gl_PointSize = 2.0 + ceil(2.0*radius);
        gl_Position = vec4(2.0*center/resolution-1.0, 0.0, 1.0);
    } """
point_fragment = """
vec4 outline(float distance, float linewidth, float antialias,
             vec4 fg_color, vec4 bg_color)
{
    vec4 frag_color;
    float t = linewidth/2.0 - antialias;
    float signed_distance = distance;
    float border_distance = abs(signed_distance) - t;
    float alpha = border_distance/antialias;
    alpha = exp(-alpha*alpha);

    if( border_distance < 0.0 )
        frag_color = fg_color;
    else if( signed_distance < 0.0 )
        frag_color = mix(bg_color, fg_color, sqrt(alpha));
    else {
        if( abs(signed_distance) < (linewidth/2.0 + antialias) ) {
            frag_color = vec4(fg_color.rgb, fg_color.a * alpha);
        } else {
            discard;
        }
    }
    return frag_color;
}


  varying vec2 v_center;
  varying float v_radius;
  void main() {
      vec2 p = gl_FragCoord.xy - v_center;

      gl_FragColor = outline(length(p)-v_radius, 1.0, 1.0,
                             vec4(0,0,0,1),  vec4(1,1,1,1));
/*
      float a = 1.0;
      float d = length(p) - v_radius + 1.0;
      if(d > 0.0) a = exp(-d*d);
      gl_FragColor = vec4(vec3(0.0), a);
*/
  } """



line_vertex = """
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

line_fragment = """
uniform vec3 color;
uniform float antialias, thickness, linelength;
varying vec2 v_uv;

void main() {
    float d = 0;
    float w = thickness/2.0 - antialias;

    // Cap at start (square)
    if (v_uv.x < 0)
        d = max(abs(v_uv.x),abs(v_uv.y)) - w;

    // Cap at end (square)
    else if (v_uv.x >= linelength)
        d = max(abs(v_uv.x-linelength),abs(v_uv.y)) - w;

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

window = app.Window(512, 512, color=(1,1,1,1))

@window.event
def on_resize(width, height):
    curve["resolution"] = width, height
    points["resolution"] = width, height

@window.event
def on_draw(dt):
    window.clear()
    gl.glDepthMask(gl.GL_FALSE)
    
    curve["color"] = 0.75, 0.75, 0.75
    curve["thickness"] = 64
    curve.draw(gl.GL_TRIANGLE_STRIP)

    curve["color"] = 0.0, 0.0, 0.0
    curve["thickness"] = 1.5
    curve.draw(gl.GL_TRIANGLE_STRIP)

    points.draw(gl.GL_POINTS)
    
    gl.glDepthMask(gl.GL_TRUE)
    
    
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


d = 64
# P = curve4_bezier((d, 3*d), (512+d, 512+d), (512+d, -d), (d, 512-3*d))
# P = curve4_bezier((d, d),  (0,512) , (512,0), (512-d,512-d))
P = curve4_bezier((d, d),  (d,512) , (512-d,512), (512-d,d))


print(len(P))
V_prev, V_curr, V_next, length = bake(P)
curve = gloo.Program(line_vertex, line_fragment)
curve["prev"], curve["curr"], curve["next"]  = V_prev, V_curr, V_next
curve["antialias"] = 1.5
curve["linelength"] = length

points = gloo.Program(point_vertex, point_fragment, count=len(P))
points["center"] = P
points["radius"] = 3.5
points["radius"][0] = 5
points["radius"][-1] = 5

app.run()
