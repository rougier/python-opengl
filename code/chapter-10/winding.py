# -----------------------------------------------------------------------------
# Python, OpenGL & Scientific Visualization
# www.labri.fr/perso/nrougier/python+opengl
# Copyright (c) 2018, Nicolas P. Rougier
# Distributed under the 2-Clause BSD License.
# -----------------------------------------------------------------------------
import numpy as np
import scipy.spatial
from glumpy import app, gl, gloo

vertex = """
attribute vec2 position;
void main() { gl_Position = vec4(position, 0.0, 1.0); }
"""

fragment = """
uniform vec4 color;
void main() { gl_FragColor = color; }
"""

config = app.configuration.Configuration()
config.stencil_size = 8
window = app.Window(config=config, width=512, height=512, color=(1, 1, 1, 1))

@window.event
def on_draw(dt):
    window.clear()

    # Disable color and depth writing
    gl.glColorMask(gl.GL_FALSE, gl.GL_FALSE, gl.GL_FALSE, gl.GL_FALSE)
    gl.glDepthMask(gl.GL_FALSE)
    
    gl.glStencilFunc(gl.GL_ALWAYS, 0, 0)
    # gl.glStencilOp(gl.GL_KEEP, gl.GL_INVERT, gl.GL_INVERT)
    gl.glStencilOpSeparate(gl.GL_FRONT, gl.GL_KEEP, gl.GL_KEEP, gl.GL_INCR)
    gl.glStencilOpSeparate(gl.GL_BACK,  gl.GL_KEEP, gl.GL_KEEP, gl.GL_DECR)
    
    polygon.draw(gl.GL_TRIANGLES, I)

    # glStencilFunc(func, ref, mask):
    #  GL_NEVER:    Always fails
    #  GL_LESS:     Passes if ( ref & mask ) <  ( stencil & mask )
    #  GL_LEQUAL:   Passes if ( ref & mask ) <= ( stencil & mask )
    #  GL_GREATER:  Passes if ( ref & mask ) >  ( stencil & mask )
    #  GL_GEQUAL:   Passes if ( ref & mask ) >= ( stencil & mask )
    #  GL_EQUAL:    Passes if ( ref & mask ) =  ( stencil & mask )
    #  GL_NOTEQUAL: Passes if ( ref & mask ) != ( stencil & mask )
    #  GL_ALWAYS:   Always passes
    
    # Enable color and depth writing
    gl.glColorMask(gl.GL_TRUE, gl.GL_TRUE, gl.GL_TRUE, gl.GL_TRUE)
    gl.glDepthMask(gl.GL_TRUE)

    # odd 
    gl.glStencilFunc(gl.GL_EQUAL, 0x01, 0x1)

    # non zero
    # gl.glStencilFunc(gl.GL_NOTEQUAL, 0x00, 0xff)

    # positive
    # gl.glStencilFunc(gl.GL_LESS, 0x0, 0xff)

    gl.glStencilOp(gl.GL_KEEP, gl.GL_KEEP, gl.GL_KEEP)

    polygon.draw(gl.GL_TRIANGLES, I)

@window.event
def on_init():
    gl.glEnable(gl.GL_STENCIL_TEST)


P = [ (-0.75,-0.75), (+0.75,-0.75), (+0.75,+0.75), (-0.75,+0.75),
      (-0.50,-0.50), (+0.50,-0.50), (+0.50,+0.50), (-0.50,+0.50),
      (-0.25,-0.25), (+0.25,-0.25), (+0.25,+0.25), (-0.25,+0.25) ]
#I = [0, 1, 2,  2, 3, 0, # CCW
#     4, 5, 6,  6, 7, 4, # CCW
#     8, 9,10, 10,11, 8] # CCW
I = [0, 1, 2,  2, 3, 0, # CCW
     6, 5, 4,  4, 7, 6, # CW
     8, 9,10, 10,11, 8] # CCW


polygon = gloo.Program(vertex, fragment, count=len(P))
polygon["position"] = P
polygon["color"] = 0.9, 0.9, 0.9, 1.00
I = np.array(I).astype(np.uint32).view(gloo.IndexBuffer)

app.run()
