Rendering a cube
===============================================================================

.. contents:: .
   :local:
   :depth: 2
   :class: toc chapter-05

We now have all the pieces needed to render a simple 3D scene, that is, a
rotating cube as show in the teaser image above. But we first need to create
the cube and to tell OpenGL how we want to actually project it on the screen.


Object creation
-------------------------------------------------------------------------------

We need to define what we mean by a *cube* since there is not such thing as as
cube in OpenGL. A cube, when seen from the outside has 6 faces, each being a
square. We just saw that to render a square, we need two triangles. So, 6
faces, each of them being made of 2 triangles, we need 12 triangles.

How many vertices? 12 triangles × 3 vertices per triangles = 36 vertices might
be a reasonable answer. However, we can also notice that each vertex is part of
3 different faces actually. We'll thus use no more than 8 vertices and tell
explicitly OpenGL how to draw 6 faces with them:

.. code:: python
            
   V = np.zeros(8, [("position", np.float32, 3)])
   V["position"] = [[ 1, 1, 1], [-1, 1, 1], [-1,-1, 1], [ 1,-1, 1],
                    [ 1,-1,-1], [ 1, 1,-1], [-1, 1,-1], [-1,-1,-1]]

These vertice describe a cube centered on (0,0,0) that goes from (-1,-1,-1) to
(+1,+1,+1). Unfortunately, we cannot use `gl.GL_TRIANGLE_STRIP` as we did for
the quad. If your remember how this rendering primitive considers vertices as a
succession of triangles, you should also realize there is no way to organize
our vertices into a triangle strip that wpuld describe our cube. This means we
have to tell OpenGL explicitely what are our triangles, i.e. we need to
describe triangles in terms of vertex indices (relatively to the `V` array we
just defined):

.. code:: python

   I = np.array([0,1,2, 0,2,3,  0,3,4, 0,4,5,  0,5,6, 0,6,1,
                 1,6,7, 1,7,2,  7,4,3, 7,3,2,  4,7,6, 4,6,5], dtype=np.uint32)

This `I` is an `IndexBuffer` that need to be uploaded to the GPU as well.
Using glumpy, the easiest way is to use a `VertexBuffer` for vertices data and
an `IndexBuffer` for indices data:

.. code:: python

   V = V.view(gloo.VertexBuffer)
   I = I.view(gloo.IndexBuffer)

We can now proceed with the actual creation of the cube and upload the
vertices. Note that we do not specify the `count` argument because we'll bind
explicitely our own vertex buffer. The `vertex` and `fragment` shader sources
are given below.
   
.. code:: python
          
   cube = gloo.Program(vertex, fragment)
   cube["position"] = V

And we'll use the indices buffer when actually rendering the cube.
    

Scene setup
-------------------------------------------------------------------------------

The next step is to define the scene. This means we need to say where are our
objects located and oriented in space, where is our camera located, what kind
of camera we want to use and ultimately, where do we look at. In this simple
example, we'll use the model-view-projection model that requires 3 matrices:

* `model:` maps from an object's local coordinate space into world space
* `view:` maps from world space to camera space
* `projection:` maps from camera to screen space

The corresponding vertex shader code is then:

.. code:: glsl

   vertex = """
   uniform mat4   model;
   uniform mat4   view;
   uniform mat4   projection;
   attribute vec3 position; 
   void main()
   {
       gl_Position = projection * view * model * vec4(position,1.0);
   } """

and we'll keep the fragment shader to a minimum for now (red color):

.. code:: glsl
          
   fragment = """
   void main()
   {
       gl_FragColor = vec4(1.0, 0.0, 0.0, 1.0);
   } """


For the projection, we'll use the default perspective camera that is available
from the `glumpy.glm` module (that also defines ortho, frustum and perspective
matrices as well as rotation, translation and scaling operations). This default
perspective matrix is located at the origin and look in the negative z
direction with the up direction pointing toward the positive y-axis. If we
leave our cube at the origin, the camera would be inside the cube and we woudl
not see much. So let first create a view matrix that is a translation along the
z-axis:

.. code:: python

   view = np.eye(4,dtype=np.float32)
   glm.translate(view, 0,0,-5)

Next, we need to define the model matrix and the projection matrix. However,
we'll not setup them right away because the model matrix will be updated in the
`on_draw` function in order to rotate the cube, while the projection matrix
will be updated as soon as the viewport change (which is the case when the
window is first created) in the `on_resize` function.


.. code:: python

   projection = np.eye(4,dtype=np.float32)
   model = np.eye(4,dtype=np.float32)

   cube['model'] = model
   cube['view'] = view
   cube['projection'] = projection
   
In the resize function, we update the projection with a perspective matrix,
taking the window aspect ratio into account. We define the viewing volume
with `near=2.0`, `far=100.0` and field of view of 45°:

.. code:: python
   
   @window.event
   def on_resize(width, height):
      ratio = width / float(height)
      cube['projection'] = glm.perspective(45.0, ratio, 2.0, 100.0)

For the mode matrix, we want the cube to rotate around its center. We do that
by compositing a rotation the z axis (`theta`), then around the y axis (`phi`):

.. code:: python

   phi, theta = 0,0

   @window.event
   def on_draw(dt):
       global phi, theta
       window.clear()
       cube.draw(gl.GL_TRIANGLES, I)

       # Make cube rotate
       theta += 1.0 # degrees
       phi += 1.0 # degrees
       model = np.eye(4, dtype=np.float32)
       glm.rotate(model, theta, 0, 0, 1)
       glm.rotate(model, phi, 0, 1, 0)
       cube['u_model'] = model

   
Actual rendering
-------------------------------------------------------------------------------

.. figure:: movies/chapter-05/solid-cube.mp4
   :loop:
   :autoplay:
   :controls:
   :figwidth: 35%
   :figclass: left
            
   Figure

   A flat shaded rotating cube using Python, OpenGL and glumpy. The 3d aspect
   may be difficult to see because of the flat shading of the cube.


We're now alsmost ready to render the whole scene but we need to modify the
initialization a little bit to enable depth testing:

.. code:: python
            
   @window.event
   def on_init():
       gl.glEnable(gl.GL_DEPTH_TEST)

This is needed because we're now dealing with 3D, meaning some rendered
triangles may be behind some others. OpenGL will take care of that provided we
declared our context with a depth buffer which is the default in glumpy.

As previously, we'll run the program for exactly 360 frames in order to make an
endless animation:

.. code:: python

   app.run(framerate=60, framecount=360)

Complete source code: `<code/chapter-05/solid-cube.py>`_


   
Variations
-------------------------------------------------------------------------------

Colored cube
++++++++++++

The previous cube is not very interesting because we used a single color for
all the faces and this tends to hide the 3d structure. We can fix this by adding
some colors and in the process, we'll discover why glumpy_ is so useful. To add
color per vertex to the cube, we simply define the vertex structure as:

.. code:: python

   V = np.zeros(8, [("position", np.float32, 3),
                    ("color",    np.float32, 4)])
   V["position"] = [[ 1, 1, 1], [-1, 1, 1], [-1,-1, 1], [ 1,-1, 1],
                    [ 1,-1,-1], [ 1, 1,-1], [-1, 1,-1], [-1,-1,-1]]
   V["color"]    = [[0, 1, 1, 1], [0, 0, 1, 1], [0, 0, 0, 1], [0, 1, 0, 1],
                    [1, 1, 0, 1], [1, 1, 1, 1], [1, 0, 1, 1], [1, 0, 0, 1]]

And we're done ! Well, actually, we also need to slightly modify the vertex
shader since color is now an attribute that needs to be passed to the fragment
shader.

.. code:: glsl

   vertex = """
   uniform mat4   model;         // Model matrix
   uniform mat4   view;          // View matrix
   uniform mat4   projection;    // Projection matrix
   attribute vec4 color;         // Vertex color
   attribute vec3 position;      // Vertex position
   varying vec4   v_color;       // Interpolated fragment color (out)
   void main()
   {
       v_color = color;
       gl_Position = projection * view * model * vec4(position,1.0);
   } """

   fragment = """
   varying vec4 v_color;         // Interpolated fragment color (in)
   void main()
   {
       gl_FragColor = v_color;
   } """


.. figure:: movies/chapter-05/color-cube.mp4
   :loop:
   :autoplay:
   :controls:
   :figwidth: 35%
   :figclass: left
            
   Figure

   The RGB rotating cube 
   
   
Furthermore, since our vertex buffer fields corresponds exactly to program
attributes, we can directly bind it:

.. code:: python

   cube = gloo.Program(vertex, fragment)
   cube.bind(V)


But we could also have written

.. code:: python
          
   cube = gloo.Program(vertex, fragment)
   cube["position"] = V["position"]
   cube["color"] = V["color"]

Complete source code: `<code/chapter-05/color-cube.py>`_
   
   

Outlined cube
+++++++++++++

.. figure:: movies/chapter-05/outline-cube.mp4
   :loop:
   :autoplay:
   :controls:
   :figwidth: 35%
   :figclass: left
            
   Figure

   An outlined colored cube using `GL_POLYGON_OFFSET_FILL` that allows to draw
   coincident surfaces properly.

We can make the cube a bit nicer by outlining it using black lines. To outline
the cube, we need to draw lines between couple of vertices on each face. 4
lines for the back and front face and 2 lines for the top and bottom faces. Why
only 2 lines for top and bottom ? Because lines are shared between the
faces. So overall we need 12 lines and we need to compute the corresponding
indices (I did it for you):

.. code:: python

    O = [0,1, 1,2, 2,3, 3,0,
         4,7, 7,6, 6,5, 5,4,
         0,5, 1,6, 2,7, 3,4 ]
    O = O.view(gloo.IndexBuffer)

We then need to draw the cube twice. One time using triangles and the indices
index buffer and one time using lines with the outline index buffer.  We need
also to add some OpenGL black magic to make things nice. It's not very
important to understand it at this point but roughly the idea to make sure lines
are drawn "above" the cube because we paint a line on a surface:

----

.. code:: python

   @window.event
   def on_draw(dt):
       global phi, theta, duration

       window.clear()

       # Filled cube
       gl.glDisable(gl.GL_BLEND)
       gl.glEnable(gl.GL_DEPTH_TEST)
       gl.glEnable(gl.GL_POLYGON_OFFSET_FILL)
       cube['ucolor'] = .75, .75, .75, 1
       cube.draw(gl.GL_TRIANGLES, I)

       # Outlined cube
       gl.glDisable(gl.GL_POLYGON_OFFSET_FILL)
       gl.glEnable(gl.GL_BLEND)
       gl.glDepthMask(gl.GL_FALSE)
       cube['ucolor'] = 0, 0, 0, 1
       cube.draw(gl.GL_LINES, O)
       gl.glDepthMask(gl.GL_TRUE)

       # Rotate cube
       theta += 1.0 # degrees
       phi += 1.0 # degrees
       model = np.eye(4, dtype=np.float32)
       glm.rotate(model, theta, 0, 0, 1)
       glm.rotate(model, phi, 0, 1, 0)
       cube['model'] = model

Complete source code: `<code/chapter-05/outlined-cube.py>`_


Textured cube
+++++++++++++

.. figure:: movies/chapter-05/texture-cube.mp4
   :loop:
   :autoplay:
   :controls:
   :figwidth: 35%
   :figclass: left
            
   Figure

   A textured cube.

For making a textured cube, we need a texture (a.k.a. an image) and some
coordinates to tell OpenGL how to map it to the cube faces. Texture coordinates
are normalized and should be inside the [0,1] range (actually, texture
coordinates can be pretty much anything but for the sake of simplicity, we'll
stick to the [0,1] range). Since we are displaying a cube, we'll use one
texture per side and the texture coordinates are quite easy to define: [0,0],
[0,1], [1,0] and [1,1]. Of course, we have to take care of assigning the right
texture coordinates to the right vertex or you texture will be messed up.

Furthemore, we'll need some extra work because we cannot share anymore our
vertices between faces since they won't share their texture coordinates. We
thus need to have a set of 24 vertices (6 faces × 4 vertices). We'll use the
dedicated function below that will take care of generating the right texture
coordinates.

----

.. code:: python

   def cube():
       vtype = [('position', np.float32, 3),
                ('texcoord', np.float32, 2)]
       itype = np.uint32

       # Vertices positions
       p = np.array([[1, 1, 1], [-1, 1, 1], [-1, -1, 1], [1, -1, 1],
                     [1, -1, -1], [1, 1, -1], [-1, 1, -1], [-1, -1, -1]],
                     dtype=float)

       # Texture coords
       t = np.array([[0, 0], [0, 1], [1, 1], [1, 0]])

       faces_p = [0, 1, 2, 3,  0, 3, 4, 5,   0, 5, 6, 1,
                  1, 6, 7, 2,  7, 4, 3, 2,   4, 7, 6, 5]
       faces_t = [0, 1, 2, 3,  0, 1, 2, 3,   0, 1, 2, 3,
                  3, 2, 1, 0,  0, 1, 2, 3,   0, 1, 2, 3]

       vertices = np.zeros(24, vtype)
       vertices['position'] = p[faces_p]
       vertices['texcoord'] = t[faces_t]

       filled = np.resize(
          np.array([0, 1, 2, 0, 2, 3], dtype=itype), 6 * (2 * 3))
       filled += np.repeat(4 * np.arange(6, dtype=itype), 6)

       vertices = vertices.view(gloo.VertexBuffer)
       filled   = filled.view(gloo.IndexBuffer)

       return vertices, filled


Now, inside the fragment shader, we have access to the texture:

.. code::

   vertex = """
   uniform mat4   model;      // Model matrix
   uniform mat4   view;       // View matrix
   uniform mat4   projection; // Projection matrix
   attribute vec3 position;   // Vertex position
   attribute vec2 texcoord;   // Vertex texture coordinates
   varying vec2   v_texcoord;   // Interpolated fragment texture coordinates (out)

   void main()
   {
       // Assign varying variables
       v_texcoord  = texcoord;

       // Final position
       gl_Position = projection * view * model * vec4(position,1.0);
   } """

   
   fragment = """
   uniform sampler2D texture; // Texture 
   varying vec2 v_texcoord;   // Interpolated fragment texture coordinates (in)
   void main()
   {
       // Get texture color
       gl_FragColor = texture2D(texture, v_texcoord);
   } """


Complete source code: `<code/chapter-05/textured-cube.py>`_

Exercises
-------------------------------------------------------------------------------

.. figure:: movies/chapter-05/color-border-cube-1.mp4
   :loop:
   :autoplay:
   :controls:
   :figwidth: 35%
   :figclass: left
            
   Figure

   An outlined cube where outline is computed from within the shader.


**Shader outline** We've seen in the section `outlined cube`_ how to draw a
thin line around the cube to enhance its shape. For this, we drew the cube
twice, one for the cube itself and a second time for the outline. However, it
is possible to get more or less the same results from within the shader in a
single pass. The trick is to pass the (untransformed) position from the vertex
shader to the fragment shader and to use this information to set the color of
the fragment to either the black color or the v_color. Starting from the `color
cube code <code/chapter-05/color-cube.py>`_, try to modify only the shader code
(both vertex and fragment) to achieve the result on the right.

**Solution**: `<code/chapter-05/border-cube.py>`_

----

.. figure:: movies/chapter-05/color-border-cube-2.mp4
   :loop:
   :autoplay:
   :controls:
   :figwidth: 35%
   :figclass: left
            
   Figure

   An outlined hollow cube computed from within the shader.


**Hollow cube** We can play a bit more with the shader and try to draw only a
thick border surrounded by black outline. For the "transparent" part, you'll
need to use the `discard` instruction from within the fragment shader that
instructs OpenGL to not display the fragment at all and to terminate the
program frot this shader. Since nothing will be rendered, there is no need to
process the rest of program.

**Solution**: `<code/chapter-05/hollow-cube.py>`_

----

.. --- Links ------------------------------------------------------------------
.. _GLUT:   http://freeglut.sourceforge.net 
.. _GLFW:   http://www.glfw.org
.. _GTK:    https://www.gtk.org
.. _QT:     https://www.qt.io
.. _WX:     https://www.wxwidgets.org
.. _TK:     https://docs.python.org/3/library/tk.html
.. _ffmpeg: https://www.ffmpeg.org
.. _glumpy: http://glumpy.github.io
.. _`perspective projection`:
            https://en.wikipedia.org/wiki/Perspective_(graphical)
.. _`orthographic projection`:
            https://en.wikipedia.org/wiki/Orthographic_projection_(geometry)
.. _glFrustum: https://www.opengl.org/sdk/docs/man2/xhtml/glFrustum.xml
.. _glOrtho: https://www.opengl.org/sdk/docs/man2/xhtml/glOrtho.xml
.. ----------------------------------------------------------------------------
