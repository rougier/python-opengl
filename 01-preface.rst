Preface
===============================================================================

.. contents:: .
   :local:
   :depth: 2
   :class: toc chapter-01


This book is open-access (i.e. it's free to read at `this address
<http://www.labri.fr/perso/nrougier/python-opengl>`_) because I believe
knowledge should be free. However, if you think the book is worth a few
dollars, you can give me a few euros (`5€
<https://www.paypal.me/NicolasPRougier/5>`_ or `10€
<https://www.paypal.me/NicolasPRougier/10>`_). This money will help me to
travel to Python conferences and to write other books as well.  If you don't
have money, it's fine. Just enjoy the book and spread the word about it. The
teaser image above comes from the `artwork section
<http://www.labri.fr/perso/nrougier/artwork/index.html>`_ of my website. It has
been made some years ago using the `Povray <http://www.povray.org>`_
(Persistence of Vision) raytracer. I like it very much because it is a kind of
résumé of my `research
<http://www.labri.fr/perso/nrougier/research/index.html>`_.
           

About the author
-------------------------------------------------------------------------------

I am a full-time research scientist at Inria_ which is the French national
institute for research in computer science and control. This is a public
scientific and technological establishment (EPST) under the double supervision
of the Research & Education Ministry, and the Ministry of Economy Finance and
Industry. I'm working within the Mnemosyne_ project which lies at the frontier
between integrative and computational neuroscience in association with the
`Institute of Neurodegenerative Diseases`_, the Bordeaux laboratory for
research in computer science (LaBRI_), the `University of Bordeaux`_ and the
national center for scientific research (CNRS_).

I've been using Python for more than 15 years and numpy for more than 10 years
for modeling in neuroscience, machine learning and for advanced visualization
(OpenGL). I'm the author of several online resources and tutorials (Matplotlib,
numpy, OpenGL) and I've been teaching Python, numpy and scientific
visualization at the University of Bordeaux and in various conferences and
schools worldwide (SciPy, EuroScipy, etc). I'm also the author of the popular
article `Ten Simple Rules for Better Figures`_ , a popular `matplotlib
tutorial`_ and an open access book `From Python To Numpy`_.



About this book
-------------------------------------------------------------------------------

This book has been written in |ReST|_ format and generated using a `customized
version <rst2html.py>`_ of the docutils rst2html.py command line (available from
the docutils_ python package) and a custom `template <book-template.txt>`_.

If you want to rebuild the html output, from the top directory, type:

.. code-block::

   $ ./rst2html.py --link-stylesheet            \
                   --cloak-email-addresses      \
                   --toc-top-backlinks          \
                   --stylesheet book.css        \
                   --stylesheet-dirs .          \
                   book.rst book.html

Or you use the provided `make.sh <make.sh>`_ shell script.
                   
The sources are available from https://github.com/rougier/python-opengl.

Last point, I wrote the book in a kind of modern `Kerouac
<https://en.wikipedia.org/wiki/Jack_Kerouac>`_'s style such that you can
download it once and continue reading it offline. Initial loading may be
slow though.


.. |ReST| replace:: restructured text
.. _ReST: http://docutils.sourceforge.net/rst.html
.. _docutils: http://docutils.sourceforge.net/

Prerequisites
+++++++++++++

This is not a Python nor a NumpPy beginner guide and you should have an
intermediate level in both Python and NumPy. No prior knowledge of OpenGL is
necessary because I'll explain everything.

Conventions
+++++++++++

I will use usual naming conventions. If not stated explicitly, each script
should import numpy, scipy and glumpy as:

.. code-block:: python
   
   import numpy as np
   import scipy as sp
   import glumpy as gp


We'll use up-to-date versions (at the date of writing, i.e. August, 2017) of the
different packages:

=========== =========
Packages    Version
=========== =========
Python      3.6.0
----------- ---------
Numpy       1.12.0
----------- ---------
Scipy       0.18.1
----------- ---------
Cython      0.25.2
----------- ---------
Triangle    20170106
----------- ---------
Glumpy      1.0.6
=========== =========

How to contribute
+++++++++++++++++

If you want to contribute to this book, you can:

* Report issues (https://github.com/rougier/python-opengl/issues)
* Suggest improvements (https://github.com/rougier/python-opengl/pulls)
* Correct English (https://github.com/rougier/python-opengl/issues)
* Star the project (https://github.com/rougier/python-opengl)
* Suggest a more responsive design for the HTML Book
* Spread the word about this book (Reddit, Hacker News, etc.)

Publishing
++++++++++

If you're an editor interested in publishing this book, you can `contact me
<mailto:Nicolas.Rougier@inria.fr>`_ if you agree to have this version and all
subsequent versions open access (i.e. online at `this address
<http://www.labri.fr/perso/nrougier/python-opengl>`_), you know how to deal
with `restructured text <http://docutils.sourceforge.net/rst.html>`_ (Word is
not an option), you provide a real added-value as well as supporting services,
and more importantly, you have a truly amazing latex book template (and be
warned that I'm a bit picky about typography & design: `Edward Tufte
<https://www.edwardtufte.com/tufte/>`_ is my hero). Still here?


License
-------------------------------------------------------------------------------

Book
++++

This work is licensed under a `Creative Commons Attribution-Non Commercial-Share
Alike 4.0 International License <https://creativecommons.org/licenses/by-nc-sa/4.0/>`_. You are free to:

* **Share** — copy and redistribute the material in any medium or format
* **Adapt** — remix, transform, and build upon the material

The licensor cannot revoke these freedoms as long as you follow the license terms.

Under the following terms:

* **Attribution** — You must give appropriate credit, provide a link to the
  license, and indicate if changes were made. You may do so in any reasonable
  manner, but not in any way that suggests the licensor endorses you or your
  use.
* **NonCommercial** — You may not use the material for commercial purposes.
* **ShareAlike** — If you remix, transform, or build upon the material, you
  must distribute your contributions under the same license as the original.


Code
++++

The code is licensed under the `OSI-approved BSD 2-Clause License
<LICENSE-code.txt>`_.



.. --- Links ------------------------------------------------------------------
.. _Nicolas P. Rougier:
         http://www.labri.fr/perso/nrougier/
.. _Inria:
         http://www.inria.fr/en
.. _Mnemosyne:
         http://www.inria.fr/en/teams/mnemosyne
.. _LaBRI:
         https://www.labri.fr/
.. _CNRS:
         http://www.cnrs.fr/index.php
.. _University of Bordeaux:
         http://www.u-bordeaux.com/
.. _Institute of Neurodegenerative Diseases:
         http://www.imn-bordeaux.org/en/
.. _Ten Simple Rules for Better Figures:
         http://dx.doi.org/10.1371/journal.pcbi.1003833
.. _matplotlib tutorial:
         http://www.labri.fr/perso/nrougier/teaching/matplotlib/matplotlib.html
.. _From Python To Numpy:
         http://www.labri.fr/perso/nrougier/from-python-to-numpy/
.. ----------------------------------------------------------------------------
