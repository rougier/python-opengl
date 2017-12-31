Rendering markers
===============================================================================

.. contents:: .
   :local:
   :depth: 2
   :class: toc chapter-08



Constructive Solid Geometry
-------------------------------------------------------------------------------


.. figure:: images/chapter-08/CSG.png
   :figwidth: 50%
   :figclass: right
              
   Figure

   Constructive solid geometry (CSG) allows a to create a complex object by using
   Boolean operators to combine simpler objects.


Constructive solid geometry (CSG) is a technique used for modeling in order to
create a complex object by using Boolean operators to combine simpler objects
(primitives). Resulting objects appear visually complex but are actually a
cleverly combined or decombined objects. The teaser image in the `GLSL
References`_ chapter is the result of `complex constructive geometry in 3D
<http://iquilezles.org/www/articles/distfunctions/distfunctions.htm>`_. See
also the Wikipedia entry on `Truth function
<https://en.wikipedia.org/wiki/Truth_function>`_.

This is the reason we did not bother to try to render complex shapes in the
previous section. Using constructive solid geometry, we are free to model
pretty much anything and we'll see that in the markers section below. In the
meantime, we need to define our CSG operations in glsl. The good news is that
it is incredibly simple, just read:

.. code:: glsl

   // Union (A or B)
   float csg_union(float d1, float d2)
   { return min(d1,d2); }

   // Difference (A not B)
   float csg_difference(float d1, float d2)
   { return max(d1,-d2); }

   // Intersection (A and B)
   float csg_intersection(float d1, float d2)
   {  return max(d1,d2); }

   // Exclusion (A xor B)
   float csg_exclusion(float d1, float d2) 
   { return min(max(d1,-d2), max(-d1,d2)); }


And we can check for the result using two circles (the shadertoy link for each
example allows you to play online with them):

   
.. figure:: images/chapter-08/CSG-intersection.png
   :figwidth: 30%
   :figclass: right

   Figure

   | Intersection (A and B)
   | `CSG-intersection.py <code/chapter-08/csg-intersection.py>`_ / `Shadertoy`__

__  https://www.shadertoy.com/view/XllyWn

.. figure:: images/chapter-08/CSG-union.png
   :figwidth: 30%
   :figclass: right

   Figure

   | Union (A or B)
   | `CSG-union.py <code/chapter-08/csg-union.py>`_ / `Shadertoy`__

__  https://www.shadertoy.com/view/4tlyWn

.. figure:: images/chapter-08/CSG-mix.png
   :figwidth: 30%
   :figclass: right

   Figure

   | Two SDF circles (A, B)
   | `CSG-mix.py <code/chapter-08/csg-mix.py>`_ / `Shadertoy`__

__  https://www.shadertoy.com/view/MtfcDr

----

.. figure:: images/chapter-08/CSG-exclusion.png
   :figwidth: 30%
   :figclass: right

   Figure

   | Exclusion (A xor B)
   | `CSG-exclusion.py <code/chapter-08/csg-exclusion.py>`_ / `Shadertoy`__

__  https://www.shadertoy.com/view/4tsyWn
   

.. figure:: images/chapter-08/CSG-difference-2.png
   :figwidth: 30%
   :figclass: right

   Figure

   | Difference (A not B)
   | `CSG-difference-2.py <code/chapter-08/csg-difference-2.py>`_ / `Shadertoy`__

__  https://www.shadertoy.com/view/XtsyWn

.. figure:: images/chapter-08/CSG-difference-1.png
   :figwidth: 30%
   :figclass: right

   Figure

   | Difference (B not A)
   | `CSG-difference-1.py <code/chapter-08/csg-difference-1.py>`_ / `Shadertoy`__

__  https://www.shadertoy.com/view/4llyWn



Markers
-------------------------------------------------------------------------------

.. figure:: images/chapter-08/CSG-markers.png
   :figwidth: 50%
   :figclass: right
   :label: csg-markers

   Figure

   Some example of markers constructed using CSG. See below for corresponding
   GLSL code.

As illustrated on the right figure creating markers is merely a matter of
imagination. Try to think of a precise shape and see how you can decompose it
in terms of constructive solid geometry. I've put a collection of such markers
in the (open access) article `Antialiased 2D Grid, Marker, and Arrow Shaders
<http://jcgt.org/published/0003/04/01/>`_. You'll find the relevant code for
the markers below.

All these markers are also defined in the glumpy library. Have a look at the
`marker.py <code/chapter-08/marker.py>`_ example where you experiment with the
different markers and the different rendering option. Note that all the markers
are defined "vertically" since their orientation can be computed very easily
from within the shader.


Arrow
+++++

.. figure:: images/chapter-08/marker-arrow.png
   :figwidth: 20%

   Figure

   Marker "arrow"

.. code:: glsl

   float marker_arrow(vec2 P, float size)
   {
       float r1 = abs(P.x) + abs(P.y) - size/2;
       float r2 = max(abs(P.x+size/2), abs(P.y)) - size/2;
       float r3 = max(abs(P.x-size/6)-size/4, abs(P.y)- size/4);
       return min(r3,max(.75*r1,r2));
   }


----

Asterisk
++++++++

.. figure:: images/chapter-08/marker-asterisk.png
   :figwidth: 20%

   Figure

   Marker "asterisk"

.. code:: glsl

   float marker_asterisk(vec2 P, float size)
   {
       float x = M_SQRT2/2 * (P.x - P.y);
       float y = M_SQRT2/2 * (P.x + P.y);
       float r1 = max(abs(x)- size/2, abs(y)- size/10);
       float r2 = max(abs(y)- size/2, abs(x)- size/10);
       float r3 = max(abs(P.x)- size/2, abs(P.y)- size/10);
       float r4 = max(abs(P.y)- size/2, abs(P.x)- size/10);
       return min( min(r1,r2), min(r3,r4));
   }

----

Bar
++++

.. figure:: images/chapter-08/marker-bar.png
   :figwidth: 20%

   Figure

   Marker "bar"


.. code:: glsl

   float marker_bar(vec2 P, float size)
   {
       return max(abs(P.x)- size/6.0, abs(P.y)- size/2.0);
   }

----

Chevron
+++++++

.. figure:: images/chapter-08/marker-chevron.png
   :figwidth: 20%

   Figure

   Marker "chevron"

.. code:: glsl

   float marker_chevron(vec2 P, float size)
   {
       float x = 1.0/M_SQRT2 * ((P.x-size/6) - P.y);
       float y = 1.0/M_SQRT2 * ((P.x-size/6) + P.y);
       float r1 = max(abs(x),          abs(y))          - size/3.0;
       float r2 = max(abs(x-size/3.0), abs(y-size/3.0)) - size/3.0;
       return max(r1,-r2);
   }

----

Clover
++++++

.. figure:: images/chapter-08/marker-clover.png
   :figwidth: 20%

   Figure

   Marker "clover"

.. code:: glsl

   float marker_clover(vec2 P, float size)
   {
       const float t1 = -M_PI/2;
       const vec2  c1 = 0.25*vec2(cos(t1),sin(t1));
       const float t2 = t1+2*M_PI/3;
       const vec2  c2 = 0.25*vec2(cos(t2),sin(t2));
       const float t3 = t2+2*M_PI/3;
       const vec2  c3 = 0.25*vec2(cos(t3),sin(t3));

       float r1 = length( P - c1*size) - size/3.5;
       float r2 = length( P - c2*size) - size/3.5;
       float r3 = length( P - c3*size) - size/3.5;
       return min(min(r1,r2),r3);
   }
   
----

Club
++++

.. figure:: images/chapter-08/marker-club.png
   :figwidth: 20%

   Figure

   Marker "club"

.. code:: glsl

   float marker_club(vec2 P, float size)
   {
       // clover (3 discs)
       const float t1 = -M_PI/2.0;
       const vec2  c1 = 0.225*vec2(cos(t1),sin(t1));
       const float t2 = t1+2*M_PI/3.0;
       const vec2  c2 = 0.225*vec2(cos(t2),sin(t2));
       const float t3 = t2+2*M_PI/3.0;
       const vec2  c3 = 0.225*vec2(cos(t3),sin(t3));
       float r1 = length( P - c1*size) - size/4.25;
       float r2 = length( P - c2*size) - size/4.25;
       float r3 = length( P - c3*size) - size/4.25;
       float r4 =  min(min(r1,r2),r3);

       // Root (2 circles and 2 planes)
       const vec2 c4 = vec2(+0.65, 0.125);
       const vec2 c5 = vec2(-0.65, 0.125);
       float r5 = length(P-c4*size) - size/1.6;
       float r6 = length(P-c5*size) - size/1.6;
       float r7 = P.y - 0.5*size;
       float r8 = 0.2*size - P.y;
       float r9 = max(-min(r5,r6), max(r7,r8));

       return min(r4,r9);
   }

----
   
Cross
+++++

.. figure:: images/chapter-08/marker-cross.png
   :figwidth: 20%

   Figure

   Marker "cross"

.. code:: glsl

   float marker_cross(vec2 P, float size)
   {
       float x = M_SQRT2/2.0 * (P.x - P.y);
       float y = M_SQRT2/2.0 * (P.x + P.y);
       float r1 = max(abs(x - size/3.0), abs(x + size/3.0));
       float r2 = max(abs(y - size/3.0), abs(y + size/3.0));
       float r3 = max(abs(x), abs(y));
       float r = max(min(r1,r2),r3);
       r -= size/2;
       return r;
   }
          
----

Diamond
+++++++

.. figure:: images/chapter-08/marker-diamond.png
   :figwidth: 20%

   Figure

   Marker "diamond"

.. code:: glsl

   float marker_diamond(vec2 P, float size)
   {
      float x = M_SQRT2/2.0 * (P.x - P.y);
      float y = M_SQRT2/2.0 * (P.x + P.y);
      return max(abs(x), abs(y)) - size/(2.0*M_SQRT2);
   }

----

Disc
++++

.. figure:: images/chapter-08/marker-disc.png
   :figwidth: 20%

   Figure

   Marker "disc"


.. code:: glsl

   float marker_disc(vec2 P, float size)
   {
       return length(P) - size/2;
   }
          
----

Ellipse
+++++++

.. figure:: images/chapter-08/marker-ellipse.png
   :figwidth: 20%

   Figure

   Marker "ellipse"

.. code:: glsl

   float marker_ellipse(vec2 P, float size)
   {
       // Alternate version (approximation)
       float a = 1.0;
       float b = 2.0;
       float r = 0.5*size;
       float f = length( P*vec2(a,b) );
       f = length( P*vec2(a,b) );
       f = f*(f-r)/length( P*vec2(a*a,b*b) );
       return f;
   }

----

Heart
+++++

.. figure:: images/chapter-08/marker-heart.png
   :figwidth: 20%

   Figure

   Marker "heart"

.. code:: glsl

   float marker_heart(vec2 P, float size)
   {
      float x = M_SQRT2/2.0 * (P.x - P.y);
      float y = M_SQRT2/2.0 * (P.x + P.y);
      float r1 = max(abs(x),abs(y))-size/3.5;
      float r2 = length(P - M_SQRT2/2.0*vec2(+1.0,-1.0)*size/3.5)
                  - size/3.5;
      float r3 = length(P - M_SQRT2/2.0*vec2(-1.0,-1.0)*size/3.5)
                  - size/3.5;
      return min(min(r1,r2),r3);
   }


----


Infinity
++++++++

.. figure:: images/chapter-08/marker-infinity.png
   :figwidth: 20%

   Figure

   Marker "infinity"

.. code:: glsl

   float marker_infinity(vec2 P, float size)
   {
       const vec2 c1 = vec2(+0.2125, 0.00);
       const vec2 c2 = vec2(-0.2125, 0.00);
       float r1 = length(P-c1*size) - size/3.5;
       float r2 = length(P-c1*size) - size/7.5;
       float r3 = length(P-c2*size) - size/3.5;
       float r4 = length(P-c2*size) - size/7.5;
       return min( max(r1,-r2), max(r3,-r4));
   }
             
----
   
Ring
++++

.. figure:: images/chapter-08/marker-ring.png
   :figwidth: 20%

   Figure

   Marker "ring"

.. code:: glsl

   float marker_ring(vec2 P, float size)
   {
       float r1 = length(P) - size/2;
       float r2 = length(P) - size/4;
       return max(r1,-r2);
   }
   
----

Spade
+++++

.. figure:: images/chapter-08/marker-spade.png
   :figwidth: 20%

   Figure

   Marker "spade"

.. code:: glsl

   float marker_spade(vec2 P, float size)
   {
      // Reversed heart (diamond + 2 circles)
      float s= size * 0.85 / 3.5;
      float x = M_SQRT2/2.0 * (P.x + P.y) + 0.4*s;
      float y = M_SQRT2/2.0 * (P.x - P.y) - 0.4*s;
      float r1 = max(abs(x),abs(y)) - s;
      float r2 = length(P - M_SQRT2/2.0*vec2(+1.0,+0.2)*s) - s;
      float r3 = length(P - M_SQRT2/2.0*vec2(-1.0,+0.2)*s) - s;
      float r4 =  min(min(r1,r2),r3);

      // Root (2 circles and 2 planes)
      const vec2 c1 = vec2(+0.65, 0.125);
      const vec2 c2 = vec2(-0.65, 0.125);
      float r5 = length(P-c1*size) - size/1.6;
      float r6 = length(P-c2*size) - size/1.6;
      float r7 = P.y - 0.5*size;
      float r8 = 0.1*size - P.y;
      float r9 = max(-min(r5,r6), max(r7,r8));

       return min(r4,r9);
   }
          
----
   
Triangle
++++++++

.. figure:: images/chapter-08/marker-triangle.png
   :figwidth: 20%

   Figure

   Marker "triangle"

.. code:: glsl

   float marker_triangle(vec2 P, float size)
   {
       float x = M_SQRT2/2.0 * (P.x - (P.y-size/6));
       float y = M_SQRT2/2.0 * (P.x + (P.y-size/6));
       float r1 = max(abs(x), abs(y)) - size/(2.0*M_SQRT2);
       float r2 = P.y-size/6;
       return max(r1,r2);
   }
   
----

Arrows
-------------------------------------------------------------------------------

Texture based
-------------------------------------------------------------------------------
