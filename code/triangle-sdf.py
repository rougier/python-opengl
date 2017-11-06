import numpy as np
from glumpy.ext import png
from glumpy import app, gloo, gl

vertex_scene = """
  attribute vec2 position;
  void main() {
      gl_Position = vec4(position, 0.0, 1.0);
  } """

fragment_scene = """
  float SDF_fake_triangle(vec2 p, vec2 p0, vec2 p1, vec2 p2) {
    vec2 e0 = p1 - p0;
    vec2 e1 = p2 - p1;
    vec2 e2 = p0 - p2;
    vec2 v0 = p - p0;
    vec2 v1 = p - p1;
    vec2 v2 = p - p2;
    vec2 o0 = normalize(vec2(e0.y, -e0.x));
    vec2 o1 = normalize(vec2(e1.y, -e1.x));
    vec2 o2 = normalize(vec2(e2.y, -e2.x));
    return max(max(dot(o0,v0), dot(o1,v1)), dot(o2,v2));
  }

  uniform vec2 p0, p1, p2;
  void main() {
      vec2 p = gl_FragCoord.xy;
      float d = SDF_fake_triangle(p, p0, p1, p2);
      d = abs(d) + 0.125;
      float a = 1.0;
      if(d > 0.0) a = exp(-d*d);
      gl_FragColor = vec4(vec3(0.0), a);
  } """


vertex_output = """
  attribute vec2 position;
  varying vec2 v_texcoord;
  void main() {
      v_texcoord = (position + 1.0)/2.0;
      gl_Position = vec4(position, 0.0, 1.0);
  } """

fragment_output = """
  uniform sampler2D texture;
  varying vec2 v_texcoord;
  void main() {
    gl_FragColor = texture2D(texture, v_texcoord);
  } """


w, h, zoom = 32, 16, 20
window = app.Window(w*zoom, h*zoom, color=(1,1,1,1))
texture = np.zeros((h,w,4), np.float32).view(gloo.TextureFloat2D)
framebuffer = gloo.FrameBuffer(color=texture)

scene = gloo.Program(vertex_scene, fragment_scene, count=4)
scene["position"] = (-1,+1), (+1,+1), (-1,-1), (+1,-1)
scene["p0"] = (26, 3)
scene["p1"] = (10,13)
scene["p2"] = ( 4, 6)

output = gloo.Program(vertex_output, fragment_output, count=4)
output["position"] = (-1,+1), (+1,+1), (-1,-1), (+1,-1)
output["texture"] = texture


@window.event
def on_draw(dt):

    framebuffer.activate()
    gl.glViewport(0, 0, w, h)
    window.clear()
    scene.draw(gl.GL_TRIANGLE_STRIP)
    framebuffer.deactivate()

    gl.glViewport(0, 0, zoom*w, zoom*h)
    window.clear()
    output.draw(gl.GL_TRIANGLE_STRIP)

    image = np.zeros((window.height, window.width * 3), dtype=np.uint8)
    gl.glReadPixels(0, 0, window.width, window.height,
                    gl.GL_RGB, gl.GL_UNSIGNED_BYTE, image)
    image[...] = image[::-1,:]
    # filename = "triangle-sdf-filled.png"
    filename = "triangle-sdf-outlined.png"
    png.from_array(image, 'RGB').save(filename)

app.run(framecount=1)

