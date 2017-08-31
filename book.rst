.. meta::
   :description: An open-source book Python and OpenGL for Scientific
                 Visualizationbased on experience, practice and
                 descriptive examples
.. |date| date::  %B %Y
.. default-role:: code
.. role:: subtitle
.. role:: small

===============================================================================
                   Python & OpenGL for Scientific Visualization
===============================================================================
-------------------------------------------------------------------------------
      Copyright (c) 2017 - Nicolas P. Rougier <Nicolas.Rougier@inria.fr> 
-------------------------------------------------------------------------------

.. container:: title-logos
               
   .. image:: data/cc.large.png
      :width: 32px
   .. image:: data/by.large.png
      :width: 32px
   .. image:: data/sa.large.png
      :width: 32px
   .. image:: data/nc.large.png
      :width: 32px

   | Latest version - |date|
   | |website|_

.. |website| replace:: www.labri.fr/perso/nrougier/python+opengl
.. _website: http://www.labri.fr/perso/nrougier/python+opengl


.. image:: data/teaser-2.png
   :class: teaser

|
|
|

.. container:: book-abstract

    Python and OpenGL have a long but complicated story. It used to be really
    easy to program something using the fixed-pipeline and libraries such as
    Pyglet but things have became more difficult with the introduction of the
    dynamic graphic pipeline in 2004. The goal of this book is to reconciliate
    Python programmers with OpenGL, providing both an introduction to modern
    OpenGL and a set of basic and advanced techniques in order to achieve both
    fast, scalable & beautiful scientific visualizations. The book uses the
    GLES 2.0 API which is the most simple API for accessing the programmable
    graphic pipeline. It does not cover up-to-date OpenGL techniques but it is
    sufficient to achieve great visualisation. In fact, modern OpenGL allows to
    control pretty much everything in the pipeline and the goal of this book is
    to explain several techniques dedicated to scientific visualisation such as
    isolines, markers, colormaps, arbitrary transformations but there are
    actually many more techniques to be discovered and explained in this
    open-access book. And of course, everything will be fast and beautiful.
    
|
|
|
           
.. sidebar:: `Python & OpenGL <#title>`_
             :subtitle:`for Scientific Visualization`
             :small:`by Nicolas P. Rougier, © 2017`

   .. contents::
      :local:
      :depth: 2

.. ----------------------------------------------------------------------------
.. include:: preface.rst
.. include:: introduction.rst
.. include:: quickstart.rst
.. include:: maths.rst
.. include:: cube.rst
.. include:: points.rst
.. include:: lines.rst
.. include:: polygons.rst
.. include:: meshes.rst
.. include:: text.rst
.. include:: framebuffer.rst
.. include:: techniques.rst
.. include:: conclusion.rst
.. include:: references.rst
.. include:: bibliography.rst

.. include:: links.rst
