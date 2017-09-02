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
   // Merge A with B
  float csg_merge(float d1, float d2, float k)
  {
      float h = clamp(0.5 + 0.5*(d2 - d1)/k, 0.0, 1.0);
      return mix(d2, d1, h) - k * h * (1.0-h);
  }

  // Signed distance to a circle
  float circle(vec2 p, vec2 center, float radius)
  {
      float d = length(p-center) - radius;
      return d;
  }

  vec4 color(float d)
  {
      vec3 white = vec3(1.0, 1.0, 1.0);
      vec3 blue  = vec3(0.1, 0.4, 0.7);
      vec3 color = white - sign(d)*blue;
      color *= (1.0 - exp(-4.0*abs(d))) * (0.8 + 0.2*cos(140.0*d));
      color = mix(color, white, 1.0-smoothstep(0.0,0.02,abs(d)) );
      return vec4(color, 1.0);
  
  }

  void main() {
      vec2 p = gl_FragCoord.xy;
      float d1 = circle(p, vec2(256.0-64.0, 256.0), 128.0/2.);
      float d2 = circle(p, vec2(256.0+64.0, 256.0), 128.0);
      float d = csg_merge(d1,d2,32.0);
      gl_FragColor = color(-d/128.0);
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
