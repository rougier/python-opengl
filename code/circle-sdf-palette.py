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
    float distance(vec2 P, vec2 center, float radius)
    {
        return length(P-center) - radius;
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
        const float epsilon = 0.005;

        float d = distance(v_position, vec2(0.0), 0.5);
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
