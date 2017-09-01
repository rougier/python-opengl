Special techniques
===============================================================================

.. contents:: .
   :local:
   :depth: 2
   :class: toc chapter-12


Colormaps
---------

Contours
--------

Transparency
------------

Generic transformation
----------------------

Grids
-----

Cartesian grid
++++++++++++++

.. figure:: data/quad-grid.mp4
   :loop:
   :autoplay:
   :controls:
   :figwidth: 35%
   :figclass: left
            
   Figure

   An animated antialiased shader grid with constant rendering time,
   i.e. independent of the number of lines displayed.


If you're familiar with the old fixed pipeline (or any other graphic library
for that matter), you should know that the most obvious way to display a grid
is to draw lines one by one. Of course, the more lines you have and the slower
your program will be. Using modern GL, we can have a constant rendering time,
that is, indepent of the number of displayed line. How? you might wonder. The
trick is to draw lines within the shader. If we reconsider the `quad simple.py
<code/chapter-03/quad-simple.py>`_ example, you might discover that the
fragment shader may have access to its exact coordinate, provided we pass this
information from the vertex shader. Let's imagine the window size is 512x512
and we multiply the normalized vertex coordinate by 256, we then have the exact
position for any fragment within the fragment shader. We can then compute a
distance to the nearest major or minor line by using the `mod` (modulo)
operator. Using this distance, we can decide what will be the color of the
fragment. It it is close enough from a major or minor line, it'll be black,
else it'll be white. For a flawless rendering, you'll actually need to modulate
the color depending on the distance using the GLSL `mix` function. (`solution 4
<code/chapter-03/quad-grid.py>`_)

Hexagonal grid
++++++++++++++


Polar grid
++++++++++
