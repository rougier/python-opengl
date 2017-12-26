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

    varying vec2 v_position;
    void main()
    {
        const float epsilon = 0.005;

        float d = distance(v_position, vec2(0.0), 0.5);
        if (d < -epsilon)
            gl_FragColor = vec4(1.0-abs(d), 0.0, 0.0, 1.0);
        else if (d > epsilon)
            gl_FragColor = vec4(0.0, 0.0, 1.0-abs(d), 1.0);
        else 
            gl_FragColor = vec4(1.0, 1.0, 1.0, 1.0);
    } """


window = app.Window(512, 512)
quad = gloo.Program(vertex, fragment, count=4)
quad['position'] = (-1,+1), (+1,+1), (-1,-1), (+1,-1)
@window.event
def on_draw(dt):
    window.clear()
    quad.draw(gl.GL_TRIANGLE_STRIP)
app.run()
