
Bibliography
===============================================================================

.. contents:: .
   :local:
   :depth: 2
   :class: toc chapter-17


This is a curated list of some computer graphics resources (peoole, articles,
books & tutorials) addressing different aspects. Some are very specific to
OpenGL while some others offer a broader view on computer graphics and
geometry.


People
------

* `Íñigo Quílez <http://iquilezles.org/www/index.htm>`_ wrote short articles on
  the techniques he developed for computer graphics experiments, demos,
  shadertoys and movies. All content is beginner and medium level, and mostly
  pragmatic rather than theoretical. He is also a master in raymarched distance
  fields and wrote some of the most amazing scripts on `shadertoys
  <https://www.shadertoy.com>`_ (see for example his beautiful `snail script
  <http://iquilezles.org/www/articles/raymarchingdf/raymarchingdf.htm>`_.

* `Paul Bourke <http://paulbourke.net>`_ offers on his website a very large set
  of resources concerning Geometry, Surfaces, Curves & Polyhedra (among other
  things). He generally get straight to the point with demonstration and
  code. I cannot count the number of times I landed on his page when asking a
  simple geometry questions (distance between two lines in 3D, circles passing
  through three points, intersecion of two circles, etc).

* `Philip Rideout <http://github.prideout.net>`_ maintains the Little
  Grasshoper website where he explains some specific techniques such as
  volumetric smoke, tesselation, clipping). Everything comes with code, demos
  and explanations and I translated some of his `techniques
  <http://prideout.net/blog/>`_ in this book.
  

Tutorials
---------

.. |tutorial-1| replace:: Open GL tutorial (C)
.. _tutorial-1: http://www.opengl-tutorial.org

.. |tutorial-2| replace:: Learn OpenGL (C)
.. _tutorial-2: https://learnopengl.com/

.. |tutorial-3| replace:: An intro to modern OpenGL (C)
.. _tutorial-3: http://duriansoftware.com/joe/An-intro-to-modern-OpenGL.-Table-of-Contents.html

.. |tutorial-4| replace:: OpenGL Wiki
.. _tutorial-4: https://www.khronos.org/opengl/wiki/Main_Page

.. |tutorial-5| replace:: Fundamental OpenGL tutorial
.. _tutorial-5: http://www.songho.ca/opengl/index.html

.. |tutorial-6| replace:: Tiny renderer
.. _tutorial-6: https://github.com/ssloy/tinyrenderer/wiki

* |tutorial-1|_, Sam Hocevar, 2017.
* |tutorial-2|_, Joey de Vries, 2017.
* |tutorial-3|_, Joe Groff, 2010.
* |tutorial-4|_, Community Edited, 2017.
* |tutorial-5|_, Song Ho Ahn (안성호), 2017.
* |tutorial-6|_, Dmitry V. Sokolov, 2016.

  
Articles
--------

.. |article-1|
   replace:: Higher Quality 2D Text Rendering
.. _article-1: http://jcgt.org/published/0002/01/04/

.. |article-2|
   replace:: Shader-based Antialiased Dashed Stroke Poylines
.. _article-2: http://jcgt.org/published/0002/02/08/

.. |article-3|
   replace:: Antialiased 2D Grid, Marker, and Arrow Shaders
.. _article-3: http://jcgt.org/published/0003/04/01/

* | |article-1|_
  | N. P. Rougier,
    Journal of Computer Graphics Techniques (JCGT), vol. 2, no. 1, pp. 50–64, 2013.

  .. container:: abstract

     Even though text is pervasive in most 3D applications, there is
     surprisingly no native support for text rendering in OpenGL. To cope with
     this absence, Mark Kilgard introduced the use of texture fonts [Kilgard
     1997]. This technique is well known and widely used and ensures both good
     performances and a decent quality in most situations. However, the quality
     may degrade strongly in orthographic mode (screen space) due to pixelation
     effects at large sizes and to legibility problems at small sizes due to
     incorrect hinting and positioning of glyphs. In this paper, we consider
     font-texture rendering to develop methods to ensure the highest quality in
     orthographic mode. The method used allows for both the accurate render-
     ing and positioning of any glyph on the screen. While the method is
     compatible with complex shaping and/or layout (e.g., the Arabic alphabet),
     these specific cases are not studied in this article.


* | |article-2|_
  | N. P. Rougier
    Journal of Computer Graphics Techniques (JCGT), vol. 2, no. 2, pp. 105–121, 2013. 

  .. container:: abstract

     Dashed stroked paths are a widely-used feature found in the vast majority
     of vector-drawing software and libraries. They enable, for example, the
     highlighting of a given path, such as the current selection, in drawing
     software or distinguishing curves, in the case of a scientific plotting
     package. This paper introduces a shader-based method for rendering
     arbitrary dash patterns along any continuous polyline (smooth or
     broken). The proposed method does not tessellate individual dash patterns
     and allows for fast and nearly accurate rendering of any user-defined dash
     pattern and caps. Benchmarks indicate a slowdown ratio between 1.1 and 2.1
     with an increased memory consumption between 3 and 6. Furthermore, the
     method can be used for solid thick polylines with correct caps and joins
     with only a slowdown factor of 1.1.



* | |article-3|_
  | N. P. Rougier
    Journal of Computer Graphics Techniques (JCGT), vol. 3, no. 4, pp. 1–52, 2014. 

  .. container:: abstract

     Grids, markers, and arrows are important components in scientific
     visualisation. Grids are widely used in scientific plots and help visually
     locate data. Markers visualize individual points and aggregated
     data. Quiver plots show vector fields, such as a velocity buffer, through
     regularly-placed arrows. Being able to draw these components quickly is
     critical if one wants to offer interactive visualisation. This article
     provides algorithms with GLSL implementations for drawing grids, markers,
     and arrows using implicit surfaces that make it possible quickly render
     pixel-perfect antialiased shapes.

  

Books
-----

.. |book-1| replace:: The Graphics Codex
.. _book-1: http://graphicscodex.com

.. |book-2| replace:: Real-time Rendering, 3ʳᵈ edition
.. _book-2: http://www.realtimerendering.com/

.. |book-3| replace:: Computer Graphics: Principles and Practice, 3ʳᵈ edition
.. _book-3: http://dept.cs.williams.edu/~morgan/cgpp/about.xml

.. |book-4| replace:: Fundamentals of Computer Graphics, 4ᵗʰ edition
.. _book-4: https://www.crcpress.com/Fundamentals-of-Computer-Graphics/Shirley-Ashikhmin-Marschner/p/book/9781568814698

.. |book-5| replace:: From Python to Numpy
.. _book-5: http://www.labri.fr/perso/nrougier/from-python-to-numpy/

* | |book-1|_
  | Morgan McGuire, 2017.

  .. container:: abstract

     The Graphics Codex is designed to support a course either as the sole,
     standalone text or as lecture notes and an encyclopedic reference
     alongside a traditional textbook. It contains 400 cross-referenced
     equation and diagram entries, 14 chapters on physically-based shading and
     rendering Multi-platform programming projects, Links to external DirectX,
     OpenGL, Unity, Mitsuba, G3D, and other API documentation, PDF links and
     full citations for primary sources and textbooks, Free updates with new
     content every month
                  
* | |book-2|_
  | Tomas Akenine-Moller, Eric Haines, Naty Hoffman

  .. container:: abstract
                   
     Thoroughly revised, this third edition focuses on modern techniques used
     to generate synthetic three-dimensional images in a fraction of a
     second. With the advent of programmable shaders, a wide variety of new
     algorithms have arisen and evolved over the past few years. This edition
     discusses current, practical rendering methods used in games and other
     applications. It also presents a solid theoretical framework and relevant
     mathematics for the field of interactive computer graphics, all in an
     approachable style.

* | |book-3|_
  | John F. Hughes, Andries van Dam, Morgan McGuire, David F. Sklar,
    James D. Foley, Steven K. Feiner, Kurt Akeley

  .. container:: abstract
                   
     In this book, we explain the principles, as well as the mathematics,
     underlying computer graphics--knowledge that is essential for successful
     work both now and in the future. Early chapters show how to create 2D and
     3D pictures right away, supporting experimentation. Later chapters,
     covering a broad range of topics, demonstrate more sophisticated
     approaches. Sections on current computer graphics practice show how to
     apply given principles in common situations, such as how to approximate an
     ideal solution on available hardware, or how to represent a data structure
     more efficiently. Topics are reinforced by exercises, programming
     problems, and hands-on projects.


* | |book-4|_
  | Peter Shirley, Michael Ashikhmin, Steve Marschner

  .. container:: abstract

     The third edition of this widely adopted text gives students a
     comprehensive, fundamental introduction to computer graphics. The authors
     present the mathematical foundations of computer graphics with a focus on
     geometric intuition, allowing the programmer to understand and apply those
     foundations to the development of efficient code.

* | |book-5|_
  | Nicolas P. Rougier

  .. container:: abstract

     There are already a fair number of books about Numpy and a legitimate
     question is to wonder if another book is really necessary. As you may have
     guessed by reading these lines, my personal answer is yes, mostly because
     I think there is room for a different approach concentrating on the
     migration from Python to Numpy through vectorization. There are a lot of
     techniques that you don't find in books and such techniques are mostly
     learned through experience. The goal of this book is to explain some of
     these techniques and to provide an opportunity for making this experience
     in the process.
