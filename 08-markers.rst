Rendering markers
===============================================================================

.. contents:: .
   :local:
   :depth: 2
   :class: toc chapter-08

..
   .. figure:: movies/chapter-07/triangles.mp4
      :loop:
      :autoplay:
      :controls:
      :figwidth: 30%
      :figclass: right

      Figure



   .. figure:: movies/chapter-07/ellipses.mp4
      :loop:
      :autoplay:
      :controls:
      :figwidth: 30%
      :figclass: right

      Figure


Constructive Solid Geometry
-------------------------------------------------------------------------------


.. figure:: images/chapter-07/CSG.png
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

   
.. figure:: images/chapter-07/CSG-intersection.png
   :figwidth: 30%
   :figclass: right

   Figure

   | Intersection (A and B)
   | `CSG-intersection.py <code/chapter-07/csg-intersection.py>`_ / `Shadertoy`__

__  https://www.shadertoy.com/view/XllyWn

.. figure:: images/chapter-07/CSG-union.png
   :figwidth: 30%
   :figclass: right

   Figure

   | Union (A or B)
   | `CSG-union.py <code/chapter-07/csg-union.py>`_ / `Shadertoy`__

__  https://www.shadertoy.com/view/4tlyWn

.. figure:: images/chapter-07/CSG-mix.png
   :figwidth: 30%
   :figclass: right

   Figure

   | Two SDF circles (A, B)
   | `CSG-mix.py <code/chapter-07/csg-mix.py>`_ / `Shadertoy`__

__  https://www.shadertoy.com/view/MtfcDr

----

.. figure:: images/chapter-07/CSG-exclusion.png
   :figwidth: 30%
   :figclass: right

   Figure

   | Exclusion (A xor B)
   | `CSG-exclusion.py <code/chapter-07/csg-exclusion.py>`_ / `Shadertoy`__

__  https://www.shadertoy.com/view/4tsyWn
   

.. figure:: images/chapter-07/CSG-difference-2.png
   :figwidth: 30%
   :figclass: right

   Figure

   | Difference (A not B)
   | `CSG-difference-2.py <code/chapter-07/csg-difference-2.py>`_ / `Shadertoy`__

__  https://www.shadertoy.com/view/XtsyWn

.. figure:: images/chapter-07/CSG-difference-1.png
   :figwidth: 30%
   :figclass: right

   Figure

   | Difference (B not A)
   | `CSG-difference-1.py <code/chapter-07/csg-difference-1.py>`_ / `Shadertoy`__

__  https://www.shadertoy.com/view/4llyWn


.. figure:: images/chapter-07/CSG-markers.png
   :figwidth: 50%
   :figclass: right

   Figure

   Some example of markers constructed using CSG.


Markers
-------------------------------------------------------------------------------

Arrows
-------------------------------------------------------------------------------

Texture based
-------------------------------------------------------------------------------
