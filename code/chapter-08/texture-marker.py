# -----------------------------------------------------------------------------
# Python & OpenGL for Scientific Visualization
# www.labri.fr/perso/nrougier/python+opengl
# Copyright (c) 2017, Nicolas P. Rougier
# Distributed under the 2-Clause BSD License.
# -----------------------------------------------------------------------------
import numpy as np
from PIL import Image
from glumpy import app, gl, gloo, data
from glumpy.ext.sdf import compute_sdf


vertex = """
  uniform vec2 resolution;
  uniform float linewidth;
  uniform float antialias;
  attribute float size;
  attribute float orientation;
  attribute vec2 position;
  attribute vec2 texcoord;
  varying float v_size;
  varying vec2 v_texcoord;
  void main() {
      float s = size + linewidth + 2.0*antialias;
      vec2 p = ((2.0*texcoord - 1.0)*s)/resolution;
      p =  vec2(p.x*cos(orientation) - p.y*sin(orientation),
                p.y*cos(orientation) + p.x*sin(orientation));
      p += 2.0*position/resolution - 1.0;
      gl_Position = vec4(p, 0.0, 1.0);
      v_texcoord = texcoord;
      v_size = size;
  } """

fragment = """
  varying float v_size;
  varying vec2 v_texcoord;
  uniform float linewidth;
  uniform float antialias;
  uniform sampler2D texture;
  void main() {
      float size = v_size + linewidth + 2.0*antialias;
      float signed_distance = size*(texture2D(texture, v_texcoord).r - 0.5);
      float border_distance = abs(signed_distance) - linewidth/2.0 + antialias;
      float alpha = border_distance/antialias;
      alpha = exp(-alpha*alpha);
      if (border_distance < 0)
          gl_FragColor = vec4(0.0, 0.0, 0.0, 1.0);
      else if (border_distance < (linewidth/2.0 + 2.0*antialias))
          gl_FragColor = vec4(0.0, 0.0, 0.0, alpha);
      else
          discard;
  } """

window = app.Window(width=512, height=512, color=(1,1,1,1))
orientation = 0

@window.event
def on_draw(dt):
    global orientation
    
    window.clear()
    marker.draw(gl.GL_TRIANGLE_STRIP) #, I) 
    orientation += 0.5*np.pi/180
    marker["orientation"] = orientation
    marker["size"] = 512*abs(np.cos(orientation))
    marker["linewidth"] = 2+2*abs(np.cos(orientation))
    
@window.event
def on_resize(width, height):
    marker["resolution"] = width, height

marker = gloo.Program(vertex, fragment, count=4)
marker["position"] = 256,256
marker["size"]     = 512
marker["orientation"] = 0
marker["texcoord"] = (0,1), (0,0), (1,1), (1,0), 
marker["antialias"] = 2.0
marker["linewidth"] = 3.0

texture = np.array(Image.open("firefox.png"))/255.0
compute_sdf(texture)
image = Image.fromarray((texture*255).astype(np.ubyte))
image.save("firefox-sdf.png")
marker["texture"] = texture[::-1,:]
marker["texture"].interpolation = gl.GL_LINEAR
marker["texture"].wrapping = gl.GL_CLAMP

app.run(framecount=720)

