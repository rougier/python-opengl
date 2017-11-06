import numpy as np
from glumpy.ext import png
from glumpy import app, gloo, gl, data

vertex = """
  uniform vec2 offset;
  attribute vec2 position;
  varying vec2 v_texcoord;
  void main() {
      v_texcoord = (position + 1.0)/2.0;
      gl_Position = vec4(position+offset, 0.0, 1.0);
  } """

scene_fragment = """
  varying vec2 v_texcoord;
   void main() {
       gl_FragColor = vec4(vec3(1.0), 1.0);
   } """

ssaa_fragment = """
  uniform sampler2D texture;
  varying vec2 v_texcoord;
  void main() {
    gl_FragColor = texture2D(texture, v_texcoord);
  } """

final_fragment = """
  uniform sampler2D texture;
  varying vec2 v_texcoord;
  void main() {
    gl_FragColor = vec4(1.0-texture2D(texture, v_texcoord).rgb, 1.0);
  } """


N4 = np.linspace(0,1,9, endpoint=True)[1:-1:2]
G4 = np.dstack(np.meshgrid(N4,N4)).reshape(len(N4)**2,2)
N8 = np.linspace(0,1,17, endpoint=True)[1:-1:2]
G8 = np.dstack(np.meshgrid(N8,N8)).reshape(len(N8)**2,2)
offsets = { "1 sample"   : [(0.5,0.5)],
            "1x2 sample" : [(0.50, 0.25), (0.50, 0.75)],
            "2x1 sample" : [(0.25, 0.50), (0.75, 0.50)],
            "quincux"    : [(.05,.05), (.95,.05), (.05,.95), (.95,.95), (0.5,0.5)],
            "2x2 grid"   : [(0.25,0.25), (0.75,0.25), (0.25,0.75), (0.75,0.75)],
            "2x2 RGSS"   : G4[[2,4,11,13]],
            "4x4 checker": G4[[0,2,5,7,8,10,13,15]],
            "8 rooks"    : G8[[4,10,16,30,33,47,53,59]],
            "4x4 grid"   : G4,
            "8x8 checker": G8[[ 0, 2, 4, 6, 9,11,13,15,16,18,20,22,25,27,29,31,
                               32,34,36,38,41,43,45,47,48,50,52,54,57,59,61,63]],
            "8x8 grid"   : G8 }
offset = offsets["8 rooks"]


width, height, zoom = 32, 16, 20
p0, p1, p2 = (26,3), (10,13), (4,6)

window = app.Window(width=width*zoom, height=height*zoom, color=(0,0,0,1))

scene = gloo.Program(vertex, scene_fragment, count=3)
V = np.array([p0, p1, p2])
scene['position'] = 2*V/(width,height) - 1

tex1 = np.zeros((height,width,4), np.float32).view(gloo.Texture2D)
ssaa = gloo.Program(vertex, ssaa_fragment, count=4)
framebuffer_1 = gloo.FrameBuffer(color=tex1)
ssaa['position'] = (-1,+1), (+1,+1), (-1,-1), (+1,-1)
ssaa['texture'] = tex1
ssaa['offset'] = 0,0

tex2 = np.zeros((height,width,4), np.float32).view(gloo.Texture2D)
final = gloo.Program(vertex, final_fragment, count=4)
framebuffer_2 = gloo.FrameBuffer(color=tex2)
final['position'] = (-1,+1), (+1,+1), (-1,-1), (+1,-1)
final['texture'] = tex2
final['offset'] = 0,0


offset_index = 0
framebuffer = np.zeros((window.height, window.width * 3), dtype=np.uint8)
    
@window.event
def on_draw(dt):
    global framebuffer, offset_index

    offset_name = list(offsets.keys())[offset_index]
    offset = offsets[offset_name]
    
    gl.glViewport(0, 0, width, height)
    framebuffer_2.activate()
    window.clear()
    framebuffer_2.deactivate()
        
    for dx,dy in offset:
        framebuffer_1.activate()
        window.clear()
        scene["offset"] = (2*dx-1)/width, (2*dy-1)/height
        scene.draw(gl.GL_TRIANGLE_STRIP)
        # scene.draw(gl.GL_LINE_LOOP)
        framebuffer_1.deactivate()
        
        framebuffer_2.activate()
        gl.glEnable(gl.GL_BLEND)
        gl.glBlendFunc(gl.GL_CONSTANT_ALPHA, gl.GL_ONE)
        gl.glBlendColor(0, 0, 0, 1/len(offset))
        ssaa.draw(gl.GL_TRIANGLE_STRIP)
        gl.glDisable(gl.GL_BLEND)
        framebuffer_2.deactivate()

    gl.glViewport(0, 0, window.width, window.height)
    window.clear()
    final.draw(gl.GL_TRIANGLE_STRIP)

    gl.glReadPixels(0, 0, window.width, window.height,
                    gl.GL_RGB, gl.GL_UNSIGNED_BYTE, framebuffer)
    framebuffer[...] = framebuffer[::-1,:]
    # filename = "triangle-ssaa-outlined-%s.png" % offset_name
    filename = "triangle-ssaa-filled-%s.png" % offset_name
    png.from_array(framebuffer, 'RGB').save(filename)
    offset_index += 1

app.run(framecount=len(offsets)-1)
