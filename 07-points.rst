
Rendering points
===============================================================================

.. contents:: .
   :local:
   :depth: 2
   :class: toc chapter-07

If you have read the previous chapters, you may have noticed that there exists
actually a `gl.GL_POINTS` drawing primitive and you might have concluded (quite
logically) that displaying points in OpenGL is straightforward. This is partly
true. This primitive can be actually used to display points, but the concept of
point for OpenGL is roughly a non-antialiased, non-rotated, boring and ugly
square. Consequently, if we want to display points like in the teaser image
above , we'll need to take care of pretty much everything.



Dots, discs, circles
-------------------------------------------------------------------------------

We've gone through a lot of theory and we're almost ready to render our first
dots (what? it is not yet finished? no!). We have our signed distance functions
but we need to exploit them in order to do the proper antialiasing. If you
remember that a SDF function gives the distance to the border of the shape, we
still need to compute the right color according to this distance. When we are
fully inside or outside the shape, it is easy: let's say black for the inside
and white for the oustide (or nothing using the transaprency level). The
interesting part is located in the vicinity of the border, it is not fully
black nor fully white but grey. What amount of grey you might ask? Well, it is
directly correlated with the distance to the border. But first, let's have a
look at the figure below that show the different situations:

.. figure:: data/circle-aa.png

   Figure

   For a given shape, we might want to draw only the outline of the shape
   (left), the interior only (left) or both of them (middle).


For all these cases, we need to define the thickness of the antialiased area,
(that is, the area where the estimated coverage will go from 0 (outside) to 1
(inside)) and the line thickness for the stroke and outline cases. This means
that wen we compute the actual size of the circle, we have to take this into
account (2*antialias + linewidth). The antililias area is usually 1.0 pixel.
If it is larger, the shape will appear blurry, and it it is too narrow, the
shape will have hard egdes. The degenerated case being a null area that results
in no antialias at all. Finally, we need to define a function that gives the
coverage according to the distance. As illustrated below, we have the choice
between several solutions (you're free to design your own) and we'll mostly use
the last one for the rest of this book because it appears to be the nicest to
me.
   
.. figure:: data/antialias-function.png

   Figure

   Antialiasing functions: **Left**: None, **Middle**: linear, **Right**:
   exponential.

Ok, we're done with the theory. Let's draw some dots (at last).

We'll use the `gl.GL_POINTS` primitive that actually display a quad whose size
(in pixels) can be specified within the vertex shader` using the `gl_PointSize`
method. If the point is supposed to have a given radius, the quad size must be
slightly larger to take into account the antialias area (1 pixel on each size
in ur case). Futhermore, we can specify a non integer radius and we thus have
to take car of getting the upper bound. So finally, our vertex shader reads:
   
.. code:: glsl

   uniform vec2 resolution;
   
   attribute vec2 center;
   attribute float radius;
   
   varying vec2 v_center;
   varying float v_radius;
   void main()
   {
       v_radius = radius;
       v_center = center;
       gl_PointSize = 2.0 + ceil(2.0*radius);
       gl_Position = vec4(2.0*center/resolution-1.0, 0.0, 1.0);
   }

You may have noticed that we give the window resolution to the shader using a
uniform (that will be updated each time the window size has changed). The goal
is to be able to use window coordinates in python without taking care of the
normalized device coordinate. This transformation will be done inside the
shader. This is important because in the fragment shader, we'll need pixel
coordinates to perform anti-aliasing. This fragment shaders reads:

.. code:: glsl
          
   varying vec2 v_center;
   varying float v_radius;
   void main()
   {
       vec2 p = gl_FragCoord.xy - v_center;
       float a = 1.0;
       float d = length(p) - v_radius + 1.0;
       if(d > 0.0) a = exp(-d*d);
       gl_FragColor = vec4(vec3(0.0), a);
   }

Note that there is a new `gl_FragCoord` variable in this fragment shader. This
variable gives the coordinate of the current fragment in window coordinates
(bottom-left is (0,0)). Without it, the `gl.GL_POINTS` would be useless.

Last, we setup our python program (see `dots-1.py <code/dots-1.py>`_).

.. code:: python

   V = np.zeros(16, [("center", np.float32, 2),
                     ("radius", np.float32, 1)])
   V["center"] = np.dstack([np.linspace(32, 512-32, len(V)),
                            np.linspace(25, 28, len(V))])
   V["radius"] = 15

   window = app.Window(512, 50, color=(1,1,1,1))
   points = gloo.Program(vertex, fragment)
   points.bind(V.view(gloo.VertexBuffer))

   @window.event
   def on_resize(width, height):
       points["resolution"] = width, height

   @window.event
   def on_draw(dt):
       window.clear()
       points.draw(gl.GL_POINTS)

   app.run()


.. figure:: data/dots-1.png
   :figwidth: 50%
   :figclass: right

   Figure

   Discs positionned vertically with a 0.2 pixel increase.

.. figure:: data/dots-2.png
   :figwidth: 50%
   :figclass: right

   Figure

   Circles positionned vertically with a 0.2 pixel increase.

You can see the result on the image on the right. Not only the discs are
properly antialiased, but they are also positionned at the subpixel level. In
the image on the right, each disc is actually vertically shifted upward by 0.2
pixels compared to its left neightbour. However, you cannot see any artefacts
(can you?): the discs are similar and properly aligned.

----

.. figure:: data/triangles.mp4
   :loop:
   :autoplay:
   :controls:
   :figwidth: 30%
   :figclass: right

   Figure

.. figure:: data/ellipses.mp4
   :loop:
   :autoplay:
   :controls:
   :figwidth: 30%
   :figclass: right

   Figure

.. figure:: data/spiral.png
   :figwidth: 30%
   :figclass: right

   Figure


   
Markers
-------------------------------------------------------------------------------


.. figure:: data/CSG-markers.png
   :figwidth: 50%
   :figclass: right

   Figure

   Some example of markers constructed using CSG.


Arrows
-------------------------------------------------------------------------------


Spheres
-------------------------------------------------------------------------------
