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

   Figure

   | Intersection (A and B)
   | `CSG-intersection.py <code/chapter-08/csg-intersection.py>`_ / `Shadertoy`__

__  https://www.shadertoy.com/view/XllyWn

.. figure:: images/chapter-08/CSG-union.png
   :figwidth: 30%

   Figure

   | Union (A or B)
   | `CSG-union.py <code/chapter-08/csg-union.py>`_ / `Shadertoy`__

__  https://www.shadertoy.com/view/4tlyWn

.. figure:: images/chapter-08/CSG-mix.png
   :figwidth: 30%

   Figure

   | Two SDF circles (A, B)
   | `CSG-mix.py <code/chapter-08/csg-mix.py>`_ / `Shadertoy`__

__  https://www.shadertoy.com/view/MtfcDr

----

.. figure:: images/chapter-08/CSG-exclusion.png
   :figwidth: 30%

   Figure

   | Exclusion (A xor B)
   | `CSG-exclusion.py <code/chapter-08/csg-exclusion.py>`_ / `Shadertoy`__

__  https://www.shadertoy.com/view/4tsyWn
   

.. figure:: images/chapter-08/CSG-difference-2.png
   :figwidth: 30%

   Figure

   | Difference (B not A)
   | `CSG-difference-2.py <code/chapter-08/csg-difference-2.py>`_ / `Shadertoy`__

__  https://www.shadertoy.com/view/XtsyWn

.. figure:: images/chapter-08/CSG-difference-1.png
   :figwidth: 30%

   Figure

   | Difference (A not B)
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
<http://jcgt.org/published/0003/04/01/>`_. 


All these markers are also defined in the glumpy library. Have a look at the
`marker.py <code/chapter-08/marker.py>`_ example where you can experiment with
the different markers and the different rendering options. Feel free to design
your own and to open a pull request to have them added to glumpy. Note that all
the markers have a default orientation that can be changed very easily from
within the shader.


For example, the heart marker, which is made of two discs and one sphere, reads
as follows:

.. code:: glsl

   float marker_heart(vec2 P, float size)
   {
      float x = M_SQRT2/2.0 * (P.x - P.y);
      float y = M_SQRT2/2.0 * (P.x + P.y);

      // Square
      float r1 = max(abs(x),abs(y))-size/3.5;

      // Disc 1
      float r2 = length(P - M_SQRT2/2.0*vec2(+1.0,-1.0)*size/3.5) - size/3.5;

      // Disc 2
      float r3 = length(P - M_SQRT2/2.0*vec2(-1.0,-1.0)*size/3.5) - size/3.5;
      
      return min(min(r1,r2),r3);
   }


.. figure:: images/chapter-08/marker-arrow.png
   :figwidth: 20%
   :figclass: left  

   Figure

   Marker "arrow"


.. figure:: images/chapter-08/marker-asterisk.png
   :figwidth: 20%
   :figclass: left
              
   Figure

   Marker "asterisk"


.. figure:: images/chapter-08/marker-bar.png
   :figwidth: 20%
   :figclass: left
              
   Figure

   Marker "bar"



.. figure:: images/chapter-08/marker-chevron.png
   :figwidth: 20%
   :figclass: left

   Figure

   Marker "chevron"


.. figure:: images/chapter-08/marker-clover.png
   :figwidth: 20%
   :figclass: left

   Figure

   Marker "clover"


.. figure:: images/chapter-08/marker-club.png
   :figwidth: 20%
   :figclass: left
              
   Figure

   Marker "club"


.. figure:: images/chapter-08/marker-cross.png
   :figwidth: 20%
   :figclass: left
              
   Figure

   Marker "cross"


.. figure:: images/chapter-08/marker-diamond.png
   :figwidth: 20%
   :figclass: left
              
   Figure

   Marker "diamond"


.. figure:: images/chapter-08/marker-disc.png
   :figwidth: 20%
   :figclass: left
              
   Figure

   Marker "disc"



.. figure:: images/chapter-08/marker-ellipse.png
   :figwidth: 20%
   :figclass: left
              
   Figure

   Marker "ellipse"


.. figure:: images/chapter-08/marker-heart.png
   :figwidth: 20%
   :figclass: left
              
   Figure

   Marker "heart"


.. figure:: images/chapter-08/marker-infinity.png
   :figwidth: 20%
   :figclass: left
              
   Figure

   Marker "infinity"


.. figure:: images/chapter-08/marker-pin.png
   :figwidth: 20%
   :figclass: left

   Figure

   Marker "pin"


.. figure:: images/chapter-08/marker-ring.png
   :figwidth: 20%
   :figclass: left
              
   Figure

   Marker "ring"


.. figure:: images/chapter-08/marker-spade.png
   :figwidth: 20%
   :figclass: left
              
   Figure

   Marker "spade"


.. figure:: images/chapter-08/marker-triangle.png
   :figwidth: 20%
   :figclass: left
              
   Figure

   Marker "triangle"



Arrows
-------------------------------------------------------------------------------

Arrows are a bit different from markers because they are made of a body, which
is a line basically, and a head. Most of the difficulty lies in the head
definition that may vary a lot depending on the type the arrow. For example,
the stealth arrow shader reads:

.. code:: glsl

   float line_distance(vec2 p, vec2 p1, vec2 p2) {
       vec2 center = (p1 + p2) * 0.5;
       float len = length(p2 - p1);
       vec2 dir = (p2 - p1) / len;
       vec2 rel_p = p - center;
       return dot(rel_p, vec2(dir.y, -dir.x));
   }

   float arrow_stealth(vec2 texcoord,
                       float body, float head,
                       float linewidth, float antialias)
   {
       float w = linewidth/2.0 + antialias;
       vec2 start = -vec2(body/2.0, 0.0);
       vec2 end   = +vec2(body/2.0, 0.0);
       float height = 0.5;

       // Head : 4 lines
       float d1 = line_distance(texcoord, end-head*vec2(+1.0,-height),
                                          end);
       float d2 = line_distance(texcoord, end-head*vec2(+1.0,-height),
                                          end-vec2(3.0*head/4.0,0.0));
       float d3 = line_distance(texcoord, end-head*vec2(+1.0,+height), end);
       float d4 = line_distance(texcoord, end-head*vec2(+1.0,+0.5),
                                          end-vec2(3.0*head/4.0,0.0));

       // Body : 1 segment
       float d5 = segment_distance(texcoord, start, end - vec2(linewidth,0.0));

       return min(d5, max( max(-d1, d3), - max(-d2,d4)));
   }


Glumpy provides 8 types of arrows that you can see below. You can also have a
look at the `arrow.py <code/chapter-08/arrow.py>`_ example where you can
experiment with the different shapes and rendering options. Feel free to design
your own and to open a pull request to have them added to glumpy.


.. figure:: images/chapter-08/arrow-triangle-90.png
   :figwidth: 20%
   :figclass: left
              
   Figure

   Arrow "triangle_90"

.. figure:: images/chapter-08/arrow-triangle-60.png
   :figwidth: 20%
   :figclass: left
              
   Figure

   Arrow "triangle_60"

.. figure:: images/chapter-08/arrow-triangle-30.png
   :figwidth: 20%
   :figclass: left
      
   Figure

   Arrow "triangle_30"


.. figure:: images/chapter-08/arrow-angle-90.png
   :figwidth: 20%
   :figclass: left
              
   Figure

   Arrow "angle_90"

.. figure:: images/chapter-08/arrow-angle-60.png
   :figwidth: 20%
   :figclass: left
              
   Figure

   Arrow "angle_60"

.. figure:: images/chapter-08/arrow-angle-30.png
   :figwidth: 20%
   :figclass: left
              
   Figure

   Arrow "angle_30"
   
.. figure:: images/chapter-08/arrow-stealth.png
   :figwidth: 20%
   :figclass: left
              
   Figure

   Arrow "stealth"

.. figure:: images/chapter-08/arrow-curved.png
   :figwidth: 20%
   :figclass: left
              
   Figure

   Arrow "curved"




          
Texture based
-------------------------------------------------------------------------------

.. figure:: images/chapter-08/firefox.png
   :figwidth: 30%
   :figclass: right
              
   Figure

   The black and white Firefox logo

We've seen that constructive solid geometry is a powerful tool for the design
of quite complex shapes. It is also very fast since everything is computed on
the GPU. Of course, the more complex is the shape, the slower it will be to
evaluate and thus to render. However, for really complex shapes, it might not
be possible to express the shape in mathematical terms and we have to find
another way. The idea is to actually precompute the signed distance to an
arbitrary shape on the CPU and to store the result in a texture.

This computation quite be quite intensive and this the reason why it is
preferable to code it in C. Glumpy comes with the binding for the `"Anti-Aliased
Euclidean Distance Transform"
<http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.170.1024&rep=rep1&type=pdf>`_
method proposed by Stefan Gustavson and Robin Strand.

.. figure:: images/chapter-08/firefox-sdf.png
   :figwidth: 30%
   :figclass: right
              
   Figure

   Signed distance to the Firefox logo

If you run the code below, you should obtain the image on the right.

.. code:: python

   import numpy as np
   from PIL import Image
   from glumpy.ext.sdf import compute_sdf
   
   Z = np.array(Image.open("firefox.png"))
   compute_sdf(Z)
   image = Image.fromarray((Z*255).astype(np.ubyte))
   image.save("firefox-sdf.png")
   
Even though the logo is barely recognisable on the resulting image, it carries
nonetheless the necessary information to compute the distance to the border
from within the shader. When the texture will be read inside the fragment
shader, we'll subtract 0.5 from the texture value (texture value are
normalized, hence the 0.5) to obtain the actual signed distance field. You're
then free to use this distance for accurate rendering of your shape. Needless
to say that the precision of the distance is directly correlated with the size
of your texture...


.. figure:: movies/chapter-08/texture-marker.mp4
   :loop:
   :autoplay:
   :controls:
   :figwidth: 30%

   Figure 
              
   SDF textured marker (see `texture-marker.py
   <code/chapter-08/texture-marker.py>`_)

The fragment shader reads (see also `texture-marker.py <code/chapter-08/texture-marker.py>`_):
   
.. code:: glsl

   varying float v_size;
   varying vec2 v_texcoord;
   uniform float linewidth;
   uniform float antialias;
   uniform sampler2D texture;
   void main() {
       float size = v_size + linewidth + 2.0*antialias;
       float signed_distance = size*(texture2D(texture, v_texcoord).r - 0.5);
       float border_distance = abs(signed_distance) - linewidth/2.0 + antialias;
       float alpha = border_distance/antialias;
       alpha = exp(-alpha*alpha);
       if (border_distance < 0)
           gl_FragColor = vec4(0.0, 0.0, 0.0, 1.0);
       else if (border_distance < (linewidth/2.0 + 2.0*antialias))
           gl_FragColor = vec4(0.0, 0.0, 0.0, alpha);
       else
           discard;
   }

   
Exercises
-------------------------------------------------------------------------------


Quiver plot
+++++++++++

.. figure:: images/chapter-08/quiver.png
   :figwidth: 50%
   :figclass: right
              
   Figure

   An dynamic quiver plot made of two triangles.

Now that we know how to draw arrows, we can make a quiver plot very easily. The
obvious solution would be to draw n arrows using 2×n triangles (since one arrow
is two triangle). However, if your arrows are evenly spaced as on the figure on
the right, there is a smarter solution using only two triangles.

Solution: `quiver.py <code/chapter-08/quiver.py>`_


Light and shadows
+++++++++++++++++

.. figure:: movies/chapter-08/SDF-light-shadow.mp4
   :loop:
   :autoplay:
   :controls:
   :figwidth: 50%

   Figure 
              
   2D signed distance functions by Marteen.
   Live demo at https://www.shadertoy.com/view/4dfXDn


As explained before, the `shadertoy <https://www.shadertoy.com>`_ website is a
great resource and you can learn a lot by reading the sources accompanying each
demo. As an exercise, have a look at this `wonderful demo
<https://www.shadertoy.com/view/4dfXDn>`_ by Marteen that shows two dimensional
signed distance field functions with light and shadows.

Simply gorgeous...
