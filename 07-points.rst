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

Raw points
++++++++++


.. figure:: images/chapter-07/points.png
   :figwidth: 30%
   :figclass: right

   Figure

   "Point" as drawn by OpenGL
   (see `points.py <code/chapter-07/points.py>`_).
   
The most straightforward way to display points is to use the `gl.GL_POINTS`
primitive that displays a quad that is always facing the camera
(i.e. billboard).  This is very convenient because a mathematical point has no
dimension, even though we'll use this primitive to draw discs and circles in
the next section. The size of the quad must be specified within the vertex
shader using the `gl_PointSize` variable (note that the size is expressed in
pixels). As shown on the figure, the result is quite ugly.

.. code:: python

   import numpy as np
   from glumpy import app, gloo, gl

   vertex = """
     attribute vec2 position;
     void main() {
         gl_PointSize = 5.0;
         gl_Position = vec4(position, 0.0, 1.0);
     } """

   fragment = """
     void main() {
          gl_FragColor = vec4(vec3(0.0), 1.0);
     } """

   window = app.Window(512, 512, color=(1,1,1,1))
   points = gloo.Program(vertex, fragment, count=1000)
   points["position"] = np.random.uniform(-1,1,(len(points),2))

   @window.event
   def on_draw(dt):
       window.clear()
       points.draw(gl.GL_POINTS)

   app.run()


Antialiased points
++++++++++++++++++

For drawing antialiased point, the size of the quad must be slighlty larger
than the actual diameter of the point because we need some extra space for the
antialias area. Considering a point with a radius `r`, the size of the quad is
thus `2+ceil(2*r)` if we consider using 1 pixel for the antalias area. Finally,
considering a point centered at `center` with radius `radius`, our vertex
shader reads (see also previous chapter on signed distance field):
   
.. code:: glsl

   // Screen resolution as (width, height)
   uniform vec2 resolution;

   // Point center (in pixel coordinates)
   attribute vec2 center;

   // Point radius (in pixels)
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

You may have noticed that we gave the window resolution to the shader using a
uniform (that will be updated each time the window size has changed). The goal
is to be able to use window coordinates (i.e. pixels) from within Python
without taking care of the normalized device coordinate (this transformation
has been done in the vertex shader above). We now have one problem to solve. A
GL point is made from a single vertex and the apparent size of the resulting
quad is controlled by the `gl_PointSize` variable resulting in several
fragments. How things are interpolated between vertices knowing there is ony
one vertex? The answer is that there is no interpolation. If we want to know
the position of a fragment relatively to the center, we have to find it
ourself. Luckily, there is one interesting variable `gl_FragCoord` that gives
us the absolute coordinate of the fragment in window coordinates (bottom-left
is (0,0)). Subtracting the center from this coordinate will give us the
relative position of the fragment from which we can compute the distance to the
outer border of the point. Finally, our fragment shader reads:

.. code:: glsl
          
   varying vec2 v_center;
   varying float v_radius;
   void main()
   {
       vec2 p = gl_FragCoord.xy - v_center;
       float a = 1.0;
       float d = length(p) - v_radius;
       if(d > 0.0) a = exp(-d*d);
       gl_FragColor = vec4(vec3(0.0), a);
   }

Last, we setup our python program to display some discs:

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


.. figure:: images/chapter-07/dots-1.png
   :figwidth: 50%
   :figclass: right

   Figure

   Discs positionned vertically with a 0.2 pixel increase.
   See `discs-aligned.py <code/chapter-07/discs-aligned.py>`_

.. figure:: images/chapter-07/dots-2.png
   :figwidth: 50%
   :figclass: right

   Figure

   Circles positionned vertically with a 0.2 pixel increase.
   See `circles-aligned.py <code/chapter-07/circles-aligned.py>`_
   
You can see the result on the image on the right. Not only the discs are
properly antialiased, but they are also positionned at the subpixel level. In
the image on the right, each disc is actually vertically shifted upward by 0.2
pixels compared to its left neightbour. However, you cannot see any artefacts
(can you?): the discs are similar and properly aligned. For the disc outlines,
we simply have to get the absolute distance instead of the signed distance.

.. code:: glsl
          
   varying vec2 v_center;
   varying float v_radius;
   void main()
   {
       vec2 p = gl_FragCoord.xy - v_center;
       float a = 1.0;
       float d = length(p) - v_radius;
       if(abs(d) > 0.0) a = exp(-d*d);
       gl_FragColor = vec4(vec3(0.0), a);
   }


Ellipses
-------------------------------------------------------------------------------


.. figure:: movies/chapter-07/ellipses.mp4
   :loop:
   :autoplay:
   :controls:
   :figwidth: 30%
   :figclass: right

   Figure

   Perfectly antialiases ellipse made of two triangles
   (`ellipses.py  <code/chapter-07/ellipses.py>`_)
   

Rendering ellipses is harder than it seems because, as we've explained in a
previous chapter, computing the distance from an arbitrary point to an ellipse
is surprinsingly difficult if you compare it to the distance to a circle. The
second difficulty for us is the fact that an ellipse can be very "flat" and if
we use the gl.GL_POINTS primitive, a lot of useless fragment will be
generated. This is the reason why we need to compute the bounding box
(including thickness and antialias area) and use two triangles to actually
display the ellipse. Last difficulty is that we cannot take advantage of the
`gl_FragCoord` but we can now take advantage of the four vertices to have local
coordinate interpolation in the fragment shader.

.. code:: glsl

   uniform vec2 resolution;
   uniform float theta;
   attribute vec2 position;
   attribute float angle;
   varying vec2 v_position;
   void main() {
       v_position = position;
       vec2 p = position;
       p = vec2(p.x*cos(angle+theta) - p.y*sin(angle+theta),
                p.y*cos(angle+theta) + p.x*sin(angle+theta));
       p = p + resolution/2.0;
       gl_Position = vec4(2.0*p/resolution-1.0, 0.0, 1.0);
   }

Note that in the vertex shader above, we pass the non-rotated coordinates to
the fragment shader. It makes things much simpler in the fragment shader that
reads:
   
.. code:: glsl

   float SDF_fake_ellipse(vec2 p, vec2 size) {
     float a = 1.0;
     float b = size.x/size.y;
     float r = 0.5*max(size.x,size.y);
     float f = length(p*vec2(a,b));
     return f*(f-r)/length(p*vec2(a*a,b*b));
   }

   uniform vec2 size;
   varying vec2 v_position;
   void main() {
       float d = SDF_fake_ellipse(v_position, size) + 1.0;
       float alpha;
       if (abs(d) < 1.0) alpha = exp(-d*d)/ 4.0;
       else if (d < 0.0) alpha =       1.0/16.0;
       else              alpha = exp(-d*d)/16.0;
       gl_FragColor = vec4(vec3(0.0), alpha);
   }          

 


Spheres
-------------------------------------------------------------------------------

Flat sphere
+++++++++++

.. figure:: images/chapter-07/sphere.png
   :figwidth: 30%
   :figclass: right

   Figure

   A lit sphere
   
If you look closely at a sphere, you'll see that that the projected shape on
screen is actualy as disc as shown on the figure on the right. This is actually
true independently of the viewpoint and we can take advantage of it. A long
time ago (with the fixed pipeline), rendering a sphere meant tesselating the
sphere with a large number of triangles. The larger the number of triangles,
the higher the quality of the sphere and the slower the rendering. However,
with the advent of shaders, things have changeg dramatically and we can use
fake spheres, i.e. discs thar are painted such as to appear as spheres. This is
known as "impostors". If you look again at the image, you might realize that
the appeareance of the sphere is given by the shading that is not uniform and
suggests instead a specific lighting that seems to come from the upper right
corner. Let's seen if can reproduce this.

.. figure:: images/chapter-07/sphere-1.png
   :figwidth: 20%
   :figclass: right

   Figure

   A black disc (`sphere-1.py  <code/chapter-07/sphere-1.py>`_)

First thing first, Let's setup a scene in order to display a single and large
disc. To do that, we simply test if a fragment is inside or outside the circle:

.. code:: glsl

   varying vec2 v_center;
   varying float v_radius;
   void main()
   {
       vec2 p = gl_FragCoord.xy - v_center;
       float z = 1.0 - length(p)/v_radius;
       if (z < 0.0) discard;
       gl_FragColor = vec4(vec3(0.0), 1.0);
   }

----

.. figure:: images/chapter-07/sphere-normals.png
   :figwidth: 20%
   :figclass: right

   Figure

   Sphere normals view on the xz plane.

To simulate lighting on the disc, we need to compute normal vectors over the
surface of the sphere (i.e. disc). Luckily enough for us, computing the normal
for a sphere is very easy. We can simply use the `p=(x,y)` coordinates inside the
fragment shader and compute the `z` coordinate. How? you might ask
yourself. This is actually correlated to the distance `d` to the center such
that `z = 1-d`. If you want to convice yourself, just look at the figure on
the right that show a side view of half a sphere on the xz plane. The z
coordinate is maximal in the center and null on the border.

We're ready to simulate lighting on our disc using the `Phong model
<https://en.wikipedia.org/wiki/Phong_reflection_model>`_. I won't give all the
detail now because we'll see that later. However, as you can see on the source
below, this is quite easy and the result is flawless.

.. figure:: images/chapter-07/sphere-3.png
   :figwidth: 20%
   :figclass: right

   Figure

   A fake lit sphere (`sphere-3.py  <code/chapter-07/sphere-3.py>`_)


.. code:: glsl

   varying vec2 v_center;
   varying float v_radius;
   void main()
   {
       vec2 p = (gl_FragCoord.xy - v_center)/v_radius;
       float z = 1.0 - length(p);
       if (z < 0.0) discard;

       vec3 color = vec3(1.0, 0.0, 0.0);
       vec3 normal = normalize(vec3(p.xy, z));
       vec3 direction = normalize(vec3(1.0, 1.0, 1.0));
       float diffuse = max(0.0, dot(direction, normal));
       float specular = pow(diffuse, 24.0);
       gl_FragColor = vec4(max(diffuse*color, specular*vec3(1.0)), 1.0);
   }
   
----

True sphere
+++++++++++

.. figure:: images/chapter-07/spheres-no-depth.png
   :figwidth: 30%
   :figclass: right

   Figure

   A bunch of fake spheres.

We can use this technique to display several "spheres" having different sizes
and positions as shown on the figure on the right. This can be used to
represent molecules for examples. Howewer, we have a problem with sphere
intersecting each other. If you look closely the figure, you might have notices
that no sphere intersect any sphere. This is due to the depth testing of the
unique vertex (remember gl.GL_POINTS) that is used to generate the quad
fragments. Each of these fragments share the same `z` coordinate resulting in
having sphre fully in front of another of fully behind another. For accurate
rendering, we thus have to tell OpenGL what is the depth of each fragment using
the `gl_FragDepth` variable (that must be between 0 and 1):

.. figure:: images/chapter-07/spheres.png
   :figwidth: 30%
   :figclass: right

   Figure

   A bunch of fake spheres with correct intersections
   (`spheres.py  <code/chapter-07/spheres.py>`_).

.. code:: glsl
          
   varying vec3 v_center;
   varying float v_radius;
   void main()
   {
       vec2 p = (gl_FragCoord.xy - v_center.xy)/v_radius;
       float z = 1.0 - length(p);
       if (z < 0.0) discard;

       gl_FragDepth = 0.5*v_center.z + 0.5*(1.0 - z);

       vec3 color = vec3(1.0, 0.0, 0.0);
       vec3 normal = normalize(vec3(p.xy, z));
       vec3 direction = normalize(vec3(1.0, 1.0, 1.0));
       float diffuse = max(0.0, dot(direction, normal));
       float specular = pow(diffuse, 24.0);
       gl_FragColor = vec4(max(diffuse*color, specular*vec3(1.0)), 1.0);
   }

You can see on the figures that the spheres now intersect each other correctly.
   

Exercises
-------------------------------------------------------------------------------


.. figure:: images/chapter-07/spiral.png
   :figwidth: 25%
   :figclass: right

   Figure

   Disc spiral

Adapting the shader from the "Dots, discs, circles" section, try to write a
script to draw discs on a spiral as displayed on the figure on the right. Be
careful with small discs, especially when the radius is less than one pixel. In
such case, you'll have to find a convincing way to suggest the size of the
disc...

Solution: `spiral.py <code/chapter-07/spiral.py>`_


----

.. figure:: movies/chapter-07/triangles.mp4
   :loop:
   :autoplay:
   :controls:
   :figwidth: 30%
   :figclass: right

   Antialiased triangles

Try to adapt the code from the ellipses section to remake the animation on the
right. Be careful with the computation of the bouding box.

Solution: `triangles.py <code/chapter-07/triangles.py>`_

----

.. figure:: images/chapter-07/voronoi.png
   :figwidth: 25%
   :figclass: right

   Figure

   A voronoi diagram computed on the GPU.


We've seen when rendering sphere that the individual depth of each fragment can
be controled withing the fragment shader and we computed this depth by taking
the distance to the center of each disc/sphere. The goal of this exercise is
thus to adapt this method to render a Voronoi diagram as shown on the right.

Solution: `voronoi.py <code/chapter-07/voronoi.py>`_
