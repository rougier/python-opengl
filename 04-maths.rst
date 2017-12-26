Basic Mathematics
===============================================================================

.. contents:: .
   :local:
   :depth: 2
   :class: toc chapter-04

.. ----------------------------------------------------------------------------


There is no way around mathematics. If you want to understand computer
geometry, you need to masterize a few mathematical concepts. But not that many
actually. I won't introduce everything since there is already a lot of
tutorials online explaining the core concepts of `linear algrebra
<http://math.hws.edu/graphicsbook/c3/s5.html>`_, `Euclidean geometry
<https://en.wikipedia.org/wiki/Three-dimensional_space>`_, `homogeneous
coordinates
<http://www.tomdalling.com/blog/modern-opengl/explaining-homogenous-coordinates-and-projective-geometry/>`_,
`projective geometry <http://www.songho.ca/opengl/gl_projectionmatrix.html>`_
and quaternions (yes, those are the keywords to enter in your preferred search
engine). The teaser image above comes from the Cyclopaedia, an Universal
Dictionary of Arts and Sciences published by Ephraim Chambers in London in 1728
(sources `History of Geometry <https://en.wikipedia.org/wiki/History_of_geometry>`_).

Projective Geometry
-------------------------------------------------------------------------------

Homogeneous coordinates
+++++++++++++++++++++++

Even though we're dealing with the three-dimensional Euclidean space, three
dimensional coordinates are actually not the best representation we can use and
this is the reason why we will use homogeneous coordinates that describe
coordinates in a four-dimensional projective space (that includes the Euclidean
space). We'll see in the next section that this allows us to express linear
transformations (rotation, scaling), affine transformations (translations) and
projection using 4×4 matrices. Homogeneous coordinatess are tightly linked with
regular 3D coordinates with the noticeable difference that they require a
fourth `w` coordinate that corresponds to the fourth dimension, let's call it
the projective dimension. In order to explain it, we'll use a 1-dimensional
space where point coordinates are single scalars indicating the position of the
points onto the X-axis. This will make everything clearer hopefully.

Let us consider for example a simple set of point `[-1.0, -0.5, 0.0, +0.5,
+1.0]` in this unidimensional space. We want to project onto another segment
`[-2,+2]` that represent the screen (any point projected outside this segment
is discared and won't be visible into the final projection) The question now is
how do we project the points onto the screen?

.. figure:: images/chapter-04/1D-H-Coordinates.png
   :figwidth: 50%
   :figclass: right

   Figure

   5 sets of homogeneous coordinates, each of them corresponding to the set of
   unidimensional Cartesian coordinates `[-1.0, -0.5, 0.0, +0.5, +1.0]`.

To answer this question, we need to know where is the camera (from where do we
look at the scene) and where are the points positioned relatively to the
screen. This is the reason why we introduce a supplementary `w` coordinate in
order to indicate the distance to the screen. To go from our Euclidean
representation to our new homogeneous representation, we'll use a conventional
and default value of 1 for all the `w` such that our new point set is now
`[(-1.0,1.0), -(0.5,1.0), (0.0,1.0), (+0.5,1.0), (+1.0,1.0)]`. Reciprocally, a
point `(x,w)` in projective space corresponds to the point `x/w` (if `w` ≠ 0)
in our unidimensional Euclidean space. From this conversion, we can see
immediately that there exist actually an infinite set of homogenous coordinates
that correspond to a single Cartesian coordinate as illustrated on the figure.

.. figure:: images/chapter-04/1D-Projection.png
   :figwidth: 100%

   Figure

   Different one dimensional projections using homogeneous coordinates.

.. .. note::

      What if `w` is null then? The answer is that this point cannot be
      projected and you can consider it like an infinite point.


Projections
+++++++++++

We are now ready to project our point set onto the screen. As shown on the
figure above, we can use an orthographic (all rays are parallels) or a linear
projection (rays originate from the camera point and hit the screen, passing
through points to be projected). For these two projections, results are similar
but different. In the first case, distances have been exactly conserved while
in the second case, the distance between projected points has increased, but
projected points are still equidistant. The third projection is where
homogenous coordinates make sense. For this (abritraty) projection, we decided
that the further the point is from the origin, and the further away from the
origin its projection will be. To do that, we measure the distance of the point
to the origin and we add this distance to its `w` value before projecting it
(this corresponds to the black circles on the figure) using the linear
projection. It is to be noted that this new projection does not conserve the
distance relationship and if we consider the set of projected points `[P(-1.0),
P(-0.5), P(0.0), P(+0.5), P(+1.0)]`, we have have `║P(-1.0)-P(-0.5)]║ >
║P(-0.5)- P(0.0)║`.


.. note::
   
   **Quaternions are not homogenous coordinates** even though they are usually
   represented in the form of a 4-tuple (a,b,c,d) that is a shortcut for the
   actual representation: a + bi⃗ + cj⃗ + dk⃗, where a, b, c, and d are real
   numbers, and i⃗, j⃗, k⃗ are the fundamental quaternion units.
   
Back to our regular 3D-Euclidean space, the principle remains the same and we have the following relationgship between Cartesian and homogeneous coordinates:
 
.. code::
   :class: math

    (x,y,z,w) → (x/w, y/w, z/w) (for w ≠ 0)
   Homogeneous    Cartesian
   
    (x,y,z)   → (x, y, z, 1)
   Cartesian     Homogeneous
   

If you didn't understood everything, you can stick to the description provided
by Sam Hocevar:

* If w = 1, then the vector (x,y,z,1) is a position in space
* If w = 0, then the vector (x,y,z,0) is a direction




Transformations
-------------------------------------------------------------------------------

.. figure:: images/chapter-04/composition.png
   :figwidth: 50%
   :figclass: right

   Figure

   Transformation are not commutative, hence R*T*V (up) is different from T*R*V
   (bottom). Remember that last transformation is on the left.
   

We'll use now homogeneous coordinates and express all our transformations using
only 4×4 matrices. This will allow us to chain several transformations by
multiplying transformation matrices. However, before diving into the actual
definition of these matrices, we need to decide if we consider a four
coordinates vector to be 4 rows and 1 column or 1 row and 4 columns. Depending
on the answer, the multiplication with a matrix will happen on the left or on
the right side of the vector. To be consistent with OpenGL convention, we'll
consider a vector to be 4 rows and 1 columns, meaning transformations happen on
the left side of vectors. To transform a vertex V by a transformation matrix M,
we write: V' = M*V. To chain two transformations M1 and M2 (first M1, then M2),
we write: V' = M2*M1*V which is different from V' = M1*M2*V because matrix
multiplication is not communative. As clearly illustrated on the right figure,
this means for example that a rotation followed by a translation is not the
same as a translation followed by a rotation.


..
   **Main transformations**

      For the impatient, here are all the main transformations:

      .. code::
         :class: math

               ┌         ┐            ┌          ┐         ┌            ┐
               │ 1 0 0 0 │            │ 1 0 0 tx │         │ sx 0  0  0 │
               │ 0 1 0 0 │            │ 0 1 0 ty │         │ 0  sy 0  0 │
               │ 0 0 1 0 │            │ 0 0 1 tz │         │ 0  0  sz 0 │
               │ 0 0 0 1 │            │ 0 0 0 1  │         │ 0  0  0  1 │
               └         ┘            └          ┘         └            ┘
                Identity               Translate               Scale

         ┌                    ┐ ┌                    ┐ ┌                    ┐
         │   1       0    0 0 │ │  cos(d) 0 sin(d) 0 │ │ cos(d) -sin(d) 0 0 │
         │ cos(d) -sin(d) 0 0 │ │    0    1   0    0 │ │ sin(d)  cos(d) 0 0 │
         │ sin(d)  cos(d) 0 0 │ │ -sin(d) 0 cos(d) 0 │ │   0       0    1 0 │
         │   0       0    0 1 │ │    0    0    0   1 │ │   0       0    0 1 │
         └                    ┘ └                    ┘ └                    ┘
             Rotate X-axis          Rotate Y-axis           Rotate Z-axis

      Let us check they work as expected.


..
   Identity transformation
   +++++++++++++++++++++++

   .. code::
      :class: math

      ┌         ┐   ┌   ┐   ┌                       ┐   ┌   ┐
      │ 1 0 0 0 │ * │ x │ = │ 1*x + 0*0 + 0*0 + 0*0 │ = │ x │
      │ 0 1 0 0 │   │ y │   │ 0*0 + 1*y + 0*0 + 0*0 │   │ y │
      │ 0 0 1 0 │   │ z │   │ 0*0 + 0*0 + 1*z + 0*0 │   │ z │
      │ 0 0 0 1 │   │ 1 │   │ 0*0 + 0*0 + 0*0 + 1*1 │   │ 1 │
      └         ┘   └   ┘   └                       ┘   └   ┘

   
Translation
+++++++++++

Considering a vertex `V = (x, y, z, 1)` and a translation vector `T = (tx, ty,
tz, 0)`, the translation of `V` by `T` is `(x+tx, y+ty, z+tz, 1)`.  The
corresponding matrix is given below:

.. code::
   :class: math

   ┌          ┐   ┌   ┐   ┌                        ┐   ┌      ┐
   │ 1 0 0 tx │ * │ x │ = │ 1*x + 0*y + 0*z + tx*1 │ = │ x+tx │
   │ 0 1 0 ty │   │ y │   │ 0*x + 1*y + 0*z + ty*1 │   │ y+ty │
   │ 0 0 1 tz │   │ z │   │ 0*x + 0*y + 1*z + tz*1 │   │ z+tz │
   │ 0 0 0 1  │   │ 1 │   │ 0*x + 0*y + 0*z +  1*  │   │ 1    │
   └          ┘   └   ┘   └                        ┘   └      ┘

Scaling
+++++++

Considering a vertex `V = (x, y, z, 1)` and a scaling vector `T = (sx, sy, sz,
0)`, the scaling of `V` by `S` is `(sx*x, sy*y, sz*z, 1)`. The corresponding
matrix is given below:

.. code::
   :class: math

   ┌            ┐   ┌   ┐   ┌                          ┐   ┌      ┐
   │ sx 0  0  0 │ * │ x │ = │ sx*x +  0*y +  0*z + 0*1 │ = │ sx*x │
   │ 0  sy 0  0 │   │ y │   │  0*x + sy*y +  0*z + 0*1 │   │ sy*y │
   │ 0  0  sz 0 │   │ z │   │  0*x +  0*y + sz*z + 0*1 │   │ sz*z │
   │ 0  0  0  1 │   │ 1 │   │  0*x +  0*y +  0*z + 1*1 │   │ 1    │
   └            ┘   └   ┘   └                          ┘   └      ┘

Rotation
++++++++

A rotation is defined by an axis of rotation A and an angle of rotation d. We
defined below only the most common rotations, that is, around the X-axis,
Y-axis and Z-axis.



X-axis rotation
~~~~~~~~~~~~~~~

.. code::
   :class: math

   ┌                    ┐   ┌   ┐   ┌                                 ┐
   │   1       0    0 0 │ * │ x │ = │      1*x      + 0*y + 0*z + 0*0 │
   │ cos(d) -sin(d) 0 0 │   │ y │   │ cos(d)*x - sin(d)*y + 0*z + 0*0 │
   │ sin(d)  cos(d) 0 0 │   │ z │   │ sin(d)*x + cos(d)*y + 0*z + 0*0 │
   │   0       0    0 1 │   │ 1 │   │      0*x      + 0*y + 0*z + 1*1 │
   └                    ┘   └   ┘   └                                 ┘
                                    ┌                      ┐
                                  = │ x                    │
                                    │ cos(d)*x - sin(d)*y  │
                                    │ sin(d)*x + cos(d)*y  │
                                    │ 1                    │
                                    └                      ┘

Y-axis rotation
~~~~~~~~~~~~~~~

.. code::
   :class: math


   ┌                    ┐   ┌   ┐   ┌                                  ┐
   │  cos(d) 0 sin(d) 0 │ * │ x │ = │  cos(d)*x + 0*y + sin(d)*z + 0*0 │
   │    0    1   0    0 │   │ y │   │       0*x + 1*y +      0*z + 0*0 │
   │ -sin(d) 0 cos(d) 0 │   │ z │   │ -sin(d)*x + 0*y + cos(d)*z + 0*0 │
   │    0    0    0   1 │   │ 1 │   │       0*x + 0*y      + 0*z + 1*1 │
   └                    ┘   └   ┘   └                                  ┘
                                    ┌                      ┐
                                  = │ cos(d)*x - sin(d)*z  │
                                    │ y                    │
                                    │ -sin(d)*x + cos(d)*z │
                                    │ 1                    │
                                    └                      ┘

Z-axis rotation
~~~~~~~~~~~~~~~
                                    
.. code::
   :class: math

   ┌                    ┐   ┌   ┐   ┌                                  ┐
   │ cos(d) -sin(d) 0 0 │ * │ x │ = │  cos(d)*x - sin(d)*y + 0*z + 0*0 │
   │ sin(d)  cos(d) 0 0 │   │ y │   │  sin(d)*x + cos(d)*y + 0*z + 0*0 │
   │   0       0    1 0 │   │ z │   │       0*x +      0*y + 1*z + 0*0 │
   │   0       0    0 1 │   │ 1 │   │       0*x +      0*y + 0*z + 1*1 │
   └                    ┘   └   ┘   └                                  ┘
                                    ┌                      ┐
                                  = │ cos(d)*x - sin(d)*y  │
                                    │ sin(d)*x + cos(d)*y  │
                                    │ z                    │
                                    │ 1                    │
                                    └                      ┘

A word of caution
+++++++++++++++++

OpenGL uses a `column-major representation
<https://www.opengl.org/archives/resources/faq/technical/transformations.htm>`_
of matrices. This mean that when reading a set of 16 contiguous
values in memory, the first 4 values corresponds to the first column while in
Numpy (using C default layout), this would corresponds to the first row. In
order to stay consistent with most OpenGL tutorials, we'll use a column-major
order in the rest of this book. This means that any glumpy transformations will
appear to be transposed when displayed, but the underlying memory
representation will still be consistent with OpenGL and GLSL. This is all you
need to know at this stage.


Considering a set of 16 contiguous values in memory:

.. code::
   :class: math

   ┌                                  ┐
   │ a b c d e f g h i j k l  m n o p │ 
   └                                  ┘

We get different representations depending on the order convention (column major or row major):
   
.. code::
   :class: math

   column-major                          row-major
     (OpenGL)                             (NumPy)
    ┌         ┐   ┌   ┐   ┌         ┐   ┌         ┐   ┌                   ┐
    │ a b c d │ × │ x │ = │ x y z w │ × │ a e i m │ = │ ax + by + cz + dw │
    │ e f g h │   │ y │   └         ┘   │ b f j n │   │ ex + fy + gz + hw │
    │ i j k l │   │ z │                 │ c g k o │   │ ix + jy + hz + lw │
    │ m n o p │   │ w │                 │ d h l p │   │ mx + ny + oz + pw │
    └         ┘   └   ┘                 └         ┘   └                   ┘


For example, here is a translation matrix as returned by the
`glumpy.glm.translation` function:
    
.. code:: python

   import glumpy
   T = glumpy.glm.translation(1,2,3)
   print(T)
   [[ 1.  0.  0.  0.]
    [ 0.  1.  0.  0.]
    [ 0.  0.  1.  0.]
    [ 1.  2.  3.  1.]]
   print(T.ravel())
   [ 1.  0.  0.  0.  0.  1.  0.  0.  0.  0.  1.  0.  1.  2.  3.  1.]
                                                     ↑   ↑   ↑
                                                     13  14  15

So this means you would use this translation on the left when uploaded to the
GPU, but you would use on the right with Python/NumPy:

.. code:: python

   T = glumpy.glm.translation(1,2,3)
   V = [3,2,1,1]
   print(np.dot(V, T))
   [ 4.  4.  4.  1.]
   
          
                                                     
Projections
-------------------------------------------------------------------------------

In order to define a projection, we need to specify first what what do we want
to view, that is, we need to define a viewing volume such that any object
within the volume (even partially) will be rendered while objects outside
won't. On the image below, the yellow and red spheres are within the volume
while the green one is not and does not appear on the projection.

.. image:: data/projection.png
   :width: 100%

There exist many different ways to project a 3D volume onto a 2D screen but
we'll only use the `perspective projection`_ (distant objects appear smaller)
and the `orthographic projection`_ which is a parallel projection (distant
objects have the same size as closer ones) as illustrated on the image
above. Until now (previous section), we have been using implicitly an
orthographic projection in the z=0 plane.

Depending on the projection we want, we will use one of the two projection
matrices below:

Orthographic
++++++++++++

.. code::
   :class: math

   ┌                                         ┐ n: near  
   │ 2/(r-l)    0       0     -((r+l)/(r-l)) │ f: far   
   │   0     2/(t-b)    0     -((t+b)/(t-b)) │ t: top   
   │   0        0    -2/(f-n) -((f+n)/(f-n)) │ b: bottom
   │   0        0      -1            0       │ l: left  
   └                                         ┘ r: right 
             Orthographic projection


Perspective
+++++++++++

.. code::
   :class: math

   ┌                                               ┐ n: near
   │ 2n/(r-l)    0       (r+l)/(r-l)       0       │ f: far
   │    0     2n/(t-b)   (t+b)/(t-b)       0       │ t: top
   │    0        0     -((f+n)/(f-n)) -(2nf/(f-n)) │ b: bottom
   │    0        0           -1            0       │ l: left
   └                                               ┘ r: right 
               Perspective projection

               
At this point, it is not necessary to understand how these matrices were
built. Suffice it to say they are standard matrices in the 3D world. Both
suppose the viewer (=camera) is located at position (0,0,0) and is looking in
the direction (0,0,1).

There exists a second form of the perpective matrix that might be easier to
manipulate. Instead of specifying the right/left/top/bottom planes, we'll use
field of view in the horizontal and vertical direction:

.. code::
   :class: math

   ┌                                     ┐ n: near
   │ c/aspect  0       0          0      │ f: far
   │    0      c       0          0      │ c : cotangen(fovy)
   │    0      0  (f+n)/(n-f)  2nf/(n-f) │ 
   │    0      0      -1          0      │ 
   └                                     ┘ 
               Perspective projection

               
where `fovy` specifies the field of view angle, in degrees, in the y direction
and `aspect` specifies the aspect ratio that determines the field of view in
the x direction.


Model and view matrices
+++++++++++++++++++++++

We are almost done with matrices. You may have guessed that the above matrices
requires the viewing volume to be in the z direction. We could design our 3D
scene such that all objects are withing this direction but it would not be very
convenient. So instead, we use a view matrix that maps the world space to
camera space. This is pretty much as if we were orienting the camera at a given
position and look toward a given direction. In the meantime, we can further
refine the whole pipeline by providing a model matrix that maps the object's
local coordinate space into world space. For example, this is useful for
rotating an object around its center. To sum up, we need:

* **Model matrix** maps from an object's local coordinate space into world space
* **View matrix** maps from world space to camera space
* **Projection matrix** maps from camera to screen space

This corresponds to the model-view-projection model. If you have read the whole
chapter carefully, you may have guessed the corresponding GLSL shader:

.. code:: glsl

   uniform mat4 view;
   uniform mat4 model;
   uniform mat4 projection;
   attribute vec3 P;
   void main(void)
   {
       gl_Position = projection*view*model*vec4(P, 1.0);
   }

