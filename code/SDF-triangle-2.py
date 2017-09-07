# -----------------------------------------------------------------------------
# Python & OpenGL for Scientific Visualization
# www.labri.fr/perso/nrougier/python+opengl
# Copyright (c) 2017, Nicolas P. Rougier
# Distributed under the 2-Clause BSD License.
# -----------------------------------------------------------------------------
from glumpy import app, gloo, gl

vertex = """
    attribute vec2 position;
    varying vec2 v_position;
    void main(){
        v_position = position;
        gl_Position = vec4(position, 0.0, 1.0);
    } """

fragment = """
  float segment_distance(vec2 P1, vec2 P2, vec2 P)
  {
      // Tangent vector to the segment
      vec2 T = P2 - P1;

      // Orthogonal vector to the segment      
      vec2 O = vec2(T.y, -T.x);

      // Squared length of the segment
      float l2 = dot(T,T);

      // Linear coordinate of the projection of P onto P1-P2 
      float u = (P.x-P1.x)*(P2.x-P1.x) + (P.y-P1.y)*(P2.y-P1.y);

      // Bound u between 0 and 1
      u = min(max(u/l2, 0.0), 1.0);

      // Projection of P onto P1-P2 segment
      vec2 U = P1 + u * T;

      return length(U-P) * sign(dot(O, P1-P));
  }

  float line_distance(vec2 P1, vec2 P2, vec2 P)
  {
      // Tangent vector to the segment
      vec2 T = P2 - P1;

      // Orthogonal vector to the segment      
      vec2 O = vec2(T.y, -T.x);

      return dot(normalize(O), P1 - P);
  }

  float SDF_triangle(vec2 P1, vec2 P2, vec2 P3, vec2 P)
  {
//    float d1 = line_distance(P1,P2,P);
//    float d2 = line_distance(P2,P3,P);
//    float d3 = line_distance(P3,P1,P);
    float d1 = segment_distance(P1,P2,P);
    float d2 = segment_distance(P2,P3,P);
    float d3 = segment_distance(P3,P1,P);
    return -min(min(d1,d2),d3);
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

  varying vec2 v_position;
  void main()
  {
      float d = SDF_triangle(vec2(-0.5,-0.5),
                             vec2(+0.5,-0.5),
                             vec2( 0.0, 0.5),
                             v_position);
      gl_FragColor = color(d);
  } """


window = app.Window(512, 512)
quad = gloo.Program(vertex, fragment, count=4)
quad['position'] = (-1,+1), (+1,+1), (-1,-1), (+1,-1)
@window.event
def on_draw(dt):
    window.clear()
    quad.draw(gl.GL_TRIANGLE_STRIP)
app.run()
