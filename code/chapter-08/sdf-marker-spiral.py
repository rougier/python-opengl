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
    marker.draw(gl.GL_TRIANGLES, I) 
    orientation += 1.0 * np.pi/180
    marker["orientation"] = orientation
#    marker["size"] = 512*abs(np.cos(orientation))
#    marker["linewidth"] = 0.5+2*abs(np.cos(orientation))
    
@window.event
def on_resize(width, height):
    marker["resolution"] = width, height


n = 150
data = np.zeros((n,4), dtype=[('position',    np.float32, 2),
                              ('size',        np.float32, 1),
                              ('size',        np.float32, 1),
                              ('orientation', np.float32, 1),
                              ('texcoord',    np.float32, 2)])

radius, theta, dtheta = 245.0, 0.0, 10 / 180.0 * np.pi
for i in range(n):
    theta += dtheta
    x = 256 + radius * np.cos(theta)
    y = 256 + radius * np.sin(theta)
    r = 20.1 - i * 0.12
    radius -= 1.25
    data['orientation'][i] = theta + np.pi
    data['position'][i] = x, y
    data['size'][i] = 2 * r
    data["texcoord"][i] = (0,1), (0,0), (1,1), (1,0)
data = data.ravel().view(gloo.VertexBuffer)

texture = np.array(Image.open("firefox.png"))/255.0
compute_sdf(texture)
image = Image.fromarray((texture*255).astype(np.ubyte))
image.save("firefox-sdf.png")


# Generate texture
marker = gloo.Program(vertex, fragment)
marker.bind(data)
marker["texture"] = texture
marker["texture"].interpolation = gl.GL_LINEAR
marker["texture"].wrapping = gl.GL_CLAMP

marker["antialias"] = 2.0
marker["linewidth"] = 1.0

# Generate indices
I = np.zeros((n,6), dtype=np.uint32)
I[:] = [0,1,2,1,2,3]
I += 4*np.arange(n,dtype=np.uint32).reshape(n,1)
I = I.ravel().view(gloo.IndexBuffer)

app.run()


# program["u_texture"] = texture
# program["u_texture"] = texture.shape
# import numpy as np
# from PIL import Image
# from glumpy.ext.sdf import compute_sdf
# Z = np.array(Image.open("firefox.png"))
# print(Z.min(), Z.max())
# Z = 1-Z/255.0
# compute_sdf(Z)
# # print(Z.min(), Z.max())
# Z = ((1-Z)*255).astype(np.ubyte)
# image = Image.fromarray(Z)
# image.save("firefox-sdf.png")
