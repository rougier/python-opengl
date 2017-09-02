# -----------------------------------------------------------------------------
# Python & OpenGL for Scientific Visualization
# www.labri.fr/perso/nrougier/python+opengl
# Copyright (c) 2017, Nicolas P. Rougier
# Distributed under the 2-Clause BSD License.
# -----------------------------------------------------------------------------
from glumpy import app, gloo, gl

vertex = """
    attribute vec2 position;
    void main(){ gl_Position = vec4(position, 0.0, 1.0); } """

fragment = """
  // This function compute the coverage according to the distance d,
  // the desired linewidth and the antialias area. Usually antialias is 1.
  // Greater value means blurred lines, smaller values means hard lines.
  float coverage(float d, float width, float antialias)
  {
      d -= width/2.0 - antialias;
      float alpha = d/antialias;
      if( d < 0.0 ) return 1.0;
      return exp(-alpha*alpha);
  }

  // Union (A or B)
  float csg_union(float d1, float d2)
  {
      return min(d1,d2);
  }

  // Signed distance to a circle
  float circle(vec2 p, vec2 center, float radius)
  {
      return length(p-center) - radius;
  }

  void main() {
      vec2 p = gl_FragCoord.xy;
      float d1 = circle(p, vec2(256.0-64.0, 256.0), 128.0);
      float d2 = circle(p, vec2(256.0+64.0, 256.0), 128.0);
      float d = csg_union(d1,d2);
      gl_FragColor = mix(vec4(1.,1.,1.,1.),
                         vec4(0.,0.,0.,1.),
                         coverage(abs(d),1.5,1.0));
  } """

# Create a window with a valid GL context
window = app.Window(512, 512, color=(1,1,1,1))

# Build the program and corresponding buffers (with 4 vertices)
quad = gloo.Program(vertex, fragment, count=4)

# Upload data into GPU
quad['position'] = (-1,+1), (+1,+1), (-1,-1), (+1,-1)

# Tell glumpy what needs to be done at each redraw
@window.event
def on_draw(dt):
    window.clear()
    quad.draw(gl.GL_TRIANGLE_STRIP)

# Run the app
app.run()
