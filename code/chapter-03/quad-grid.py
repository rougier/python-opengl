# -----------------------------------------------------------------------------
# Python, OpenGL & Scientific Visualization
# Copyright (c) 2017, Nicolas P. Rougier
# Distributed under the 2-Clause BSD License.
# -----------------------------------------------------------------------------
import math
from glumpy import app, gloo, gl

vertex = """
  attribute vec2 position;
  varying vec2 v_position;
  void main()
  {
    gl_Position = vec4(position, 0.0, 1.0);

    // We know the window size is 512x512 pixels, here we transform the
    // normalized position into a pixel position (from -256 to +256)
    v_position = 256.0*position;
} """

fragment = """
  varying vec2 v_position;
  uniform float major_scale;
  uniform float minor_scale;

  // This function compute the transparency level (alpha) according
  // to the distance d, the desired linewidth and the antialias area.
  // Usually antialias is 1. Greater value means blurred lines, smaller
  // values means hard lines.
  float compute_alpha(float d, float width, float antialias)
  {
      d -= width/2.0 - antialias;
      float alpha = d/antialias;
      if( d < 0.0 ) return 1.0;
      else          return exp(-alpha*alpha);
  }

  void main()
  {
      vec2 d;
      vec4 black = vec4(0,0,0,1);
      vec4 white = vec4(1,1,1,1);

      // Computer distance to the nearest major line
      d = min(mod(                 v_position, major_scale),
                   mod(major_scale-v_position, major_scale));
      float Ax = compute_alpha(d.x, 2.5, 1.0);
      float Ay = compute_alpha(d.y, 2.5, 1.0);

      // Computer distance to the nearest minor line
      d = min(mod(                 v_position, minor_scale),
                   mod(minor_scale-v_position, minor_scale));
      float ax = compute_alpha(d.x, 1.0, 1.0);
      float ay = compute_alpha(d.y, 1.0, 1.0);

      // Assign color to the fragment by mixing black and white
      // according to the alpha level
      gl_FragColor = mix(white, black, max(max(Ax, Ay), max(ax,ay)));
  } """

quad = gloo.Program(vertex, fragment, count=4)
quad['position'] = [(-1,-1), (-1,+1), (+1,-1), (+1,+1)]
quad['major_scale'] = 128.0
quad['minor_scale'] = quad['major_scale']/10.0
window = app.Window(width=512, height=512)

time = 0

@window.event
def on_draw(dt):
    global time
    time += math.pi/180.0
    scale = 3 + 2*math.cos(time)
    quad['major_scale'] = 128.0*scale
    quad['minor_scale'] = 12.8*scale

    window.clear()
    quad.draw(gl.GL_TRIANGLE_STRIP)

app.run(framerate=60, framecount=360)
