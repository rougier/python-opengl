.. meta::
   :description: An open-source book about Python and OpenGL for Scientific
                 Visualization based on experience, practice and
                 descriptive examples
.. |date| date::  %B %Y
.. default-role:: code
.. role:: subtitle
.. role:: small

===============================================================================
                   Python & OpenGL for Scientific Visualization
===============================================================================
-------------------------------------------------------------------------------
      Copyright (c) 2018 - Nicolas P. Rougier <Nicolas.Rougier@inria.fr> 
-------------------------------------------------------------------------------

.. container:: title-logos
               
   .. image:: images/cc.large.png
      :width: 32px
   .. image:: images/by.large.png
      :width: 32px
   .. image:: images/sa.large.png
      :width: 32px
   .. image:: images/nc.large.png
      :width: 32px

   | Latest version - |date|
   | |website|_

.. |website| replace:: www.labri.fr/perso/nrougier/python+opengl
.. _website: http://www.labri.fr/perso/nrougier/python+opengl


.. image:: images/teaser.png
   :class: teaser

|

.. container:: book-abstract

   **Python and OpenGL** have a long but complicated story. It used to be
   really easy to program something using the fixed-pipeline and libraries such
   as Pyglet but things have became more difficult with the introduction of the
   dynamic graphic pipeline in 2004. The goal of this book is to reconcile
   Python programmers with OpenGL, providing both an introduction to modern
   OpenGL and a set of basic and advanced techniques in order to achieve both
   fast, scalable & beautiful scientific visualizations. The book uses the GLES
   2.0 API which is the most simple API for accessing the programmable graphic
   pipeline. It does not cover up-to-date OpenGL techniques but it is
   sufficient to achieve great visualisation. In fact, modern OpenGL allows to
   control pretty much everything in the pipeline and the goal of this book is
   to explain several techniques dedicated to scientific visualisation such as
   isolines, markers, colormaps, arbitrary transformations but there are
   actually many more techniques to be discovered and explained in this
   open-access book. And of course, everything will be fast and beautiful.


.. container:: book-colophon

   | Copyright (c) 2018 by Nicolas P. Rougier
   | This work is licensed under a Creative Commons
   | Attribution-Non Commercial-Share Alike 4.0 International License
   | First published online in 2018, Bordeaux, France
   | ISBN: X-XXXXX-XXX-X

|
|
|


.. sidebar:: `Python & OpenGL <#python-opengl-for-scientific-visualization>`_
             :subtitle:`for Scientific Visualization`
             :small:`by Nicolas P. Rougier, 2017`

   .. contents::
      :local:
      :depth: 2

.. ----------------------------------------------------------------------------
.. include:: 01-preface.rst
.. include:: 02-introduction.rst
.. include:: 03-quickstart.rst
.. include:: 04-maths.rst
.. include:: 05-cube.rst
.. include:: 06-anti-grain.rst
.. include:: 07-points.rst
.. include:: 08-lines.rst
.. include:: 09-polygons.rst
.. include:: 10-meshes.rst
.. include:: 11-text.rst
.. include:: 12-framebuffer.rst
.. include:: 13-special.rst
.. include:: 14-conclusion.rst
.. include:: 15-glsl-reference.rst
.. include:: 16-bibliography.rst
