Rendering a mesh
===============================================================================

Work in Progress.

..
   .. contents:: .
      :local:
      :depth: 2
      :class: toc chapter-11


   Ok, it is now time to go 3D! I'm pretty sure you're reading this book only for
   this. I won't explain everything since you'll find a lot of online resources
   dedicated to 3D rendering using OpenGL. Instead, I'll concentrate on common
   techniques found in scientific visualization. The teaser image is a Klein
   bottle rendered using glumpy. Sources are available from the
   `geometric-parametric.py
   <https://github.com/glumpy/glumpy/blob/master/examples/geometry-parametric.py>`_
   example.


   Parametric surfaces
   -------------------

   From Wikipedia:

       *A parametric surface is a surface in the Euclidean space ℝ³ which is
       defined by a parametric equation with two parameters f(u,v) : ℝ² →
       ℝ³. Parametric representation is a very general way to specify a surface,
       as well as implicit representation.*

   Surfaces such as `Boy's surface
   <https://en.wikipedia.org/wiki/Boy%27s_surface>`_, `Klein bottle
   <https://en.wikipedia.org/wiki/Klein_bottle>`_, `Möbius strip
   <https://en.wikipedia.org/wiki/Klein_bottle>`_ are all parametric surfaces that
   can be described using more or less simple equations. Let's consider the Boy's
   surface. Considering two parameters (u,v) in [0,π], the (x,y,z) surface writes (thanks `Mayavi <http://docs.enthought.com/mayavi/mayavi/auto/example_boy.html>`_):

   .. code:: python

      x = 2 / 3. * (cos(u) * cos(2 * v)
          + sqrt(2) * sin(u) * cos(v)) * cos(u) / (sqrt(2) - sin(2 * u) * sin(3 * v))
      y = 2 / 3. * (cos(u) * sin(2 * v) -
           sqrt(2) * sin(u) * sin(v)) * cos(u) / (sqrt(2) - sin(2 * u) * sin(3 * v))
      z = -sqrt(2) * cos(u) * cos(u) / (sqrt(2) - sin(2 * u) * sin(3 * v))


   What is nice with such (u,v) parameterization is that we can easily triangulate
   the surface. We only have to iterate over u and v and compute the corresponding
   vertices:

   .. code:: python

       vtype = [('position', np.float32, 3)]
       vcount += 1
       ucount += 1
       n = vcount*ucount
       Un = np.repeat(np.linspace(0, 1, ucount, endpoint=True), vcount)
       U = umin+Un*(umax-umin) # normalization
       Vn = np.tile  (np.linspace(0, 1, vcount, endpoint=True), ucount)
       V = vmin+Vn*(vmax-vmin) # normalization
       vertices = np.zeros(n, dtype=vtype)
       for i,(u,v) in enumerate(zip(U,V)):
           x,y,z = func(u,v)
           vertices["position"][i] = x,y,z


   Then (and because this a regular surface), we can easily build the
   corresponding indices:

   .. code:: python

      for i in range(ucount-1):
          for j in range(vcount-1):
              indices.append(i*(vcount) + j        )
              indices.append(i*(vcount) + j+1      )
              indices.append(i*(vcount) + j+vcount+1)
              indices.append(i*(vcount) + j+vcount  )
              indices.append(i*(vcount) + j+vcount+1)
              indices.append(i*(vcount) + j        )
      indices = np.array(indices, dtype=itype)


   .. figure:: images/chapter-11/boy-tesselation.png
      :figwidth: 100%

      Figure

      Tesselated Boy's surface using 16, 32, 64 and 128 steps.
      See `boy-tesselation.py <code/chapter-11/boy-tesselation.py>`_


   .. figure:: movies/chapter-11/boy.mp4
      :figclass: right
      :loop:
      :controls:
      :figwidth: 35%

      Figure

      Colored Boy's surface using an approximated Viridis colormap by `Jérôme
      Liard <https://www.shadertoy.com/user/blackjero>`_.
      See `boy.py <code/chapter-11/boy.py>`_


   We can make the rendering a bit nicer using colors according to (u,v)
   coordinates. For this, we just need to provide the fragment shader with the
   (uv) coordinate and decide how to paint the surface acccording to u, v or both.
   Furthermore, instead of drawing the surface twices to display the grid lines,
   we can directly render them in the same shader.

   .. code:: glsl

      varying vec2 v_uv;
      void main()
      {
          float x = 1 - sin(v_uv.x);
          vec4 color = vec4(vec3(x), 1.0);
          vec4 black = vec4(vec3(0.0), 1.0);
          vec2 d = fract((v_uv/M_PI)*64.0);
          vec2 f = fwidth(d);
          vec2 a = smoothstep(0.99-f, 0.99+f, d);
          gl_FragColor =  mix(color, black, max(a.x,a.y));
      }



   Height fields
   -------------

   Height fields are also a very common object in scientific visualization. It
   allows to visualize a function of the type z = f(x,y) over a specific domain.


   Mesh models
   -----------
