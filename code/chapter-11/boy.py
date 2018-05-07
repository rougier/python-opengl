# -----------------------------------------------------------------------------
# Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
import numpy as np
from glumpy import app, gl, glm, gloo


vertex = """
uniform mat4 view, model, projection;
attribute vec3 position;
attribute vec2 uv;
varying vec2 v_uv;
void main()
{
    v_uv = uv;
    gl_Position = projection * view * model * vec4(position, 1.0);
}
"""

fragment = """
#include "math/constants.glsl"

// Viridis approximation, Jerome Liard, August 2016
// https://www.shadertoy.com/view/XtGGzG
vec3 viridis_quintic( float x )
{
    x = clamp(x, 0.0, 1.0);
    vec4 x1 = vec4(1.0, x, x*x, x*x*x); // 1 x x2 x3
    vec4 x2 = x1 * x1.w * x; // x4 x5 x6 x7
    return vec3(
      dot( x1.xyzw, vec4(+0.280268003, -0.143510503, +2.225793877, -14.815088879))
    + dot( x2.xy,   vec2(+25.212752309, -11.772589584)),
      dot( x1.xyzw, vec4(-0.002117546, +1.617109353, -1.909305070, +2.701152864))
    + dot( x2.xy,   vec2(-1.685288385, +0.178738871)),
      dot( x1.xyzw, vec4(+0.300805501, +2.614650302, -12.019139090, +28.933559110))
    + dot( x2.xy,   vec2(-33.491294770, +13.762053843)));
}
varying vec2 v_uv;
void main()
{
    float x = 1 - sin(v_uv.x);
    vec4 color = vec4(viridis_quintic(x), 1.0);
    vec4 black = vec4(vec3(0.0), 1.0);

    vec2 d = fract((v_uv/M_PI)*64.0);
    vec2 f = fwidth(d);
    vec2 a = smoothstep(0.99-f, 0.99+f, d);
    gl_FragColor =  mix(color, black, max(a.x,a.y));
}
"""

def surface(func, umin=0, umax=np.pi, ucount=128,
                  vmin=0, vmax=np.pi, vcount=128):
    vtype = [('position', np.float32, 3),
             ('uv',       np.float32, 2)]
    itype = np.uint32
    vcount += 1
    ucount += 1
    n = vcount*ucount
    Un = np.repeat(np.linspace(0, 1, ucount, endpoint=True), vcount)
    Vn = np.tile  (np.linspace(0, 1, vcount, endpoint=True), ucount)
    U = umin+Un*(umax-umin)
    V = vmin+Vn*(vmax-vmin)
    vertices = np.zeros(n, dtype=vtype)
    for i,(u,v) in enumerate(zip(U,V)):
        x,y,z = func(u,v)
        vertices["position"][i] = x,y,z
        vertices["uv"][i] = u,v
    indices = []
    for i in range(ucount-1):
        for j in range(vcount-1):
            indices.append(i*(vcount) + j        )
            indices.append(i*(vcount) + j+1      )
            indices.append(i*(vcount) + j+vcount+1)
            indices.append(i*(vcount) + j+vcount  )
            indices.append(i*(vcount) + j+vcount+1)
            indices.append(i*(vcount) + j        )
    indices = np.array(indices, dtype=itype)
    return vertices.view(gloo.VertexBuffer), indices.view(gloo.IndexBuffer)

def boy(u, v):
    from math import cos, sin, sqrt

    s2 = sqrt(2)
    cu, su = cos(u), sin(u)
    cv, sv = cos(v), sin(v)
    c2v, s2v = cos(2*v), sin(2*v)
    s2u, s3v = sin(2*u), sin(3*v)
    
    x = 2/3 * (cu * c2v + s2*su*cv) * cu/(s2-s2u*s3v)
    y = 2/3 * (cu * s2v - s2*su*sv) * cu/(s2-s2u*s3v)
    z = -s2*cu*cu/(s2-s2u*s3v)
    return x, y, z+1.75


window = app.Window(width=512, height=512, color=(1,1,1,1))

@window.event
def on_draw(dt):
    global phi, theta, duration

    window.clear()
    program.draw(gl.GL_TRIANGLES, indices)
    theta += 1.0 # degree 
    phi += 1.0 # degree
    model = np.eye(4, dtype=np.float32)
    glm.rotate(model, theta, 0, 0, 1)
    glm.rotate(model, phi, 0, 1, 0)
    program['model'] = model


@window.event
def on_resize(width, height):
    program['projection'] = glm.perspective(25.0, width / float(height), 2.0, 100.0)

@window.event
def on_init():
    gl.glEnable(gl.GL_DEPTH_TEST)



vertices, indices = surface(boy)
program = gloo.Program(vertex, fragment)
program.bind(vertices)
view = np.eye(4, dtype=np.float32)
model = np.eye(4, dtype=np.float32)
projection = np.eye(4, dtype=np.float32)
glm.translate(view, 0, 0, -10)
program['model'] = model
program['view'] = view
phi, theta = 30, 40

app.run(framerate=60, framecount=360)
