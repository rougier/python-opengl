.. role:: proto
          
GLSL References
===============================================================================

.. contents:: .
   :local:
   :depth: 2
   :class: toc references


The information below has been directly extracted and reformated from the `GLES
Shading language 1.0
<https://www.khronos.org/files/opengles_shading_language.pdf>`_. Copyright (c)
2006-2009 The Khronos Group Inc. All Rights Reserved. The teaser image above
has been coded by Shadertoy Grand Master `Íñigo Quílez
<http://iquilezles.org/www/index.htm>`_ and is available from the `shadertoy
website <https://www.shadertoy.com/view/ld3Gz2>`_ which is a great resource for
learning OpenGL and WebGL (and that is more or less compatible with GLES 2.0).


Types
-----

Scalar
++++++

:proto:`void`

   for functions that do not return a value

:proto:`bool`

   a conditional type, taking on values of true or false

:proto:`int`

   a signed integer

:proto:`float`

   a single floating-point scalar

Vector
++++++

:proto:`bvec2` :proto:`bvec3` :proto:`bvec4`

   a two, three or four components Boolean vector

:proto:`ivec2` :proto:`ivec3` :proto:`ivec4`

   a two, three or four components interge vector

:proto:`vec2` :proto:`vec3` :proto:`vec4`

   a two, three or four components floating-point vector



Matrix
++++++

:proto:`mat2` :proto:`mat3` :proto:`mat4`

   a 2×2, 3×3 or 4×4 floating-point matrix

          
Texture
+++++++

:proto:`sampler2D`

   a handle for accessing a 2D texture

:proto:`samplerCube`

   a handle for accessing a cube mapped texture



Qualifiers
----------

Storage
+++++++

:proto:`<none: default>`

   local read/write memory, or an input parameter to a function
   
:proto:`const`

   a compile-time constant, or a function parameter that is read-only
   
:proto:`attribute`

   linkage between a vertex shader and OpenGL ES for  per-vertex data
   
:proto:`uniform`

   value does not change across the primitive being processed, uniforms form
   the linkage between a shader, OpenGL ES, and the application

:proto:`varying`

   linkage between a vertex shader and a fragment shader for interpolated data

   
Parameters
++++++++++

:proto:`<none: default>`

    same as `in`

:proto:`in`

   for function parameters passed into a function
       
:proto:`out`

   for function parameters passed back out of a function, but not initialized
   for use when passed in
   
:proto:`inout`

   for function parameters passed both into and out of a function



Precision
+++++++++

:proto:`highp`

   Satisfies the minimum requirements for the vertex language.
   Optional in the fragment language.
                     
:proto:`mediump`

   Satisfies the minimum requirements for the fragment language. Its range and
   precision has to be greater than or the same as provided by `lowp` and less
   than or the same as provided by `highp`.
                     
:proto:`lowp`

   Range and precision that can be less than `mediump`, but still intended to
   represent all color values for any color channel.


Built-in variables
------------------
      
Vertex shader
+++++++++++++

These built-in vertex shader variables for communicating with fixed
functionality are intrinsically declared with the following types:

.. code:: glsl
   
   highp   vec4  gl_Position;    // should be written to
   mediump float gl_PointSize;   // may be written to


:proto:`gl_Position`

   The variable `gl_Position` is intended for writing the homogeneous vertex
   position.
   
:proto:`gl_PointSize`

   The variable gl_PointSize` is intended for a vertex shader to write the size
   of the point to be rasterized. It is measured in pixels.

   
Fragment shader
+++++++++++++++

The built-in variables that are accessible from a fragment shader are
intrinsically given types as follows:

.. code:: glsl

   mediump vec4  gl_FragCoord;
           bool  gl_FrontFacing;
   mediump vec4  gl_FragColor;
   mediump vec4  gl_FragData[gl_MaxDrawBuffers];
   mediump vec2  gl_PointCoord;

   

:proto:`gl_FragColor`

   Writing to `gl_FragColor` specifies the fragment color that will be used by
   the subsequent fixed functionality pipeline.
   
:proto:`gl_FragData`

   `gl_FragData` is an array. Writing to `gl_FragData[n]` specifies the
   fragment data that will be used by the subsequent fixed functionality
   pipeline for data n.
       
:proto:`gl_FragCoord`

   The variable `gl_FragCoord` is available as a read-only variable from within
   fragment shaders and it holds the window relative coordinates x, y, z, and
   1/w values for the fragment.
   
:proto:`gl_FrontFacing`

   `gl_FrontFacing` value is true if the fragment belongs to a front-facing
   primitive.
   
:proto:`gl_PointCoord`

   The values in `gl_PointCoord` are two-dimensional coordinates indicating
   where within a point primitive the current fragment is located. They range
   from 0.0 to 1.0 across the point.


Built-in constants
------------------

The following built-in constants are provided to the vertex and fragment shaders.
The example values below are the minimum values allowed for these maximums.

.. code:: glsl
   
   const mediump int gl_MaxVertexAttribs = 8;
   const mediump int gl_MaxVertexUniformVectors = 128;
   const mediump int gl_MaxVaryingVectors = 8;
   const mediump int gl_MaxVertexTextureImageUnits = 0;
   const mediump int gl_MaxCombinedTextureImageUnits = 8;
   const mediump int gl_MaxTextureImageUnits = 8;
   const mediump int gl_MaxFragmentUniformVectors = 16;
   const mediump int gl_MaxDrawBuffers = 1;
   

Built-in functions
------------------

.. contents::
   :local:
   :class: toc
   :depth: 1


Angle and trigonometry functions
++++++++++++++++++++++++++++++++

For all the functions below, T can be a `float` or a `float` vector (`vec2`,
`vec3`, `vec4`). In case of a `float` vector, the function is computed for each
component separately.

:proto:`T radians (T degrees)`
   
   The `radians` function converts degrees to radians.

   .. code:: glsl

      float x = radians(90.0);              // x = π/2
      vec2  x = radians(vec2(45.0, 90.0));  // x = vec2(π/4, π/2)

:proto:`T degrees (T radians)`

   The `degree` function converts radians to degrees.

   .. code:: glsl

      const pi = 3.141592653589793;
      float x = degrees(pi);                    // x = 180
      vec2  x = degrees(vec2(pi/4.0, pi/2.0));  // x = vec2(45.0, 90.0)


:proto:`T sin (T angle)`

   The `sin` function returns the sine of an angle in radians.

   .. code:: glsl

      const pi = 3.141592653589793;
      float x = sin(0.0);                // x = 0
      vec2  x = sin(vec2(0.0, pi/2.0));  // x = vec2(0.0, 1.0)

:proto:`T cos (T angle)`

   The `cos` function returns the cosine of an angle in radians.

   .. code:: glsl

      const pi = 3.141592653589793;
      float x = cos(0.0);                // x = 0
      vec2  x = cos(vec2(0.0, pi/2.0));  // x = vec2(1.0, 0.0)
      
:proto:`T tan (T angle)`

   The `tan` function returns the tangent of an angle in radians.

   .. code:: glsl

      const pi = 3.141592653589793;
      float x = tan(0.0);                // x = 0
      vec2  x = tan(vec2(0.0, pi/4.0));  // x = vec2(0.0, 1.0)

:proto:`T asin (T x)`

   The `asin` returns an angle in radians whose sine is x. The range of values
   returned by this function is [−π/2,π/2] Results are undefined if ∣x∣ > 1.

   .. code:: glsl

      float x = asin(0.0);             // x = 0.0
      vec2  x = asin(vec2(0.0, 1.0));  // x = vec2(0.0, π/2)

:proto:`T acos (T x)`

   The `acos` returns an angle in radians whose cosine is x. The range of values
   returned by this function is [0,π] Results are undefined if ∣x∣ > 1.

   .. code:: glsl

      float x = acos(0.0);             // x = π/2
      vec2  x = acos(vec2(0.0, 1.0));  // x = vec2(π/2, 0.0)

:proto:`T atan (T y_over_x)`
       
   The `atan` function returns an angle whose tangent is y/x.  The signs of x and
   y are used to determine what quadrant the angle is in. The range of values
   returned by this function is [−π,π].  Results are undefined if x and y are
   both 0. 

   .. code:: glsl

      float x = atan(0.0);             // x = 0.0
      vec2  x = atan(vec2(0.0, 1.0));  // x = vec2(0.0, π/4)
 
   
Exponential functions
+++++++++++++++++++++

For all the functions below, T can be a `float` or a `float` vector (`vec2`,
`vec3`, `vec4`). In case of a `float` vector, the function is computed for each
component separately.

:proto:`T pow (T x, T y)`

   The `power` function returns x raised to the power of y, i.e., xʸ.
   Results are undefined if x < 0 or if x = 0 and y ≤ 0.

   .. code:: glsl

      float x = pow(2.0, 2.0);            // x = 4.0
      vec2  x = pow(vec2(2.0, 3.0), 2.0); // x = vec2(4.0, 9.0)

      
:proto:`T exp (T x)`
       
   The `exp` function returns the natural exponentiation of x, i.e eˣ.
       
   .. code:: glsl

      float x = exp(2.0);            // x = e²
      vec2  x = exp(vec2(2.0, 3.0)); // x = vec2(e², e³)


:proto:`T log (T x)`

   The `log` function returns the natural logarithm of x, i.e., returns the
   value y which satisfies the equation x = eʸ.
   Results are undefined if x ≤ 0.

   .. code:: glsl

      const float e = 2.718281828459045;
      float x = log(1.0);          // x = 0.0
      vec2  x = log(vec2(1.0, e)); // x = vec2(0.0, 1.0)
                        
:proto:`T exp2 (T x)`

   The `exp2` function returns 2 raised to the x power, i.e., 2ˣ

   .. code:: glsl

      float x = exp2(2.0);            // x = 4.0
      vec2  x = exp2(vec2(2.0, 3.0)); // x = vec2(4.0, 8.0)
  
:proto:`T log2 (T x)`

   The `log2` function returns the base 2 logarithm of x, i.e., returns the
   value y which satisfies the equation x = 2ʸ.
   Results are undefined if x ≤ 0.
   
   .. code:: glsl

      float x = log2(4.0);            // x = 2.0
      vec2  x = log2(vec2(4.0, 8.0)); // x = vec2(2.0, 3.0)

:proto:`T sqrt (T x)`

   The `sqrt` function returns the square root of x.
   Results are undefined if x < 0. 

   .. code:: glsl

      float x = sqrt(4.0);            // x = 2.0
      vec2  x = sqrt(vec2(4.0, 9.0)); // x = vec2(2.0, 3.0)

:proto:`T inversesqrt (T x)`

   The `inversesqrt` returns the inverse square root of x, i.e. the
   reciprocal of the square root.
   Results are undefined if x ≤ 0.

   .. code:: glsl

      float x = inversesqrt(1.0/4.0);         // x = 2.0
      vec2  x = sqrt(vec2(1.0/4.0, 1.0/9.0)); // x = vec2(2.0, 3.0)



Common functions
++++++++++++++++

For all the functions below, T can be a `float` or a `float` vector (`vec2`,
`vec3`, `vec4`). In case of a `float` vector, the function is computed for each
component separately.

:proto:`T abs (T x)`

   The `abs` function returns x if x ≥ 0, otherwise it returns –x.

   .. code:: glsl

      float x = abs(-1.0);            // x = 1.0
      vec2  x = abs(vec2(1.0, -2.0)); // x = vec2(1.0, 2.0)

:proto:`T sign (T x)`

   The `sign` function returns 1.0 if x > 0, 0.0 if x = 0, and –1.0 if x < 0.
   
   .. code:: glsl

      float x = sign(-2.0);          // x = -1.0
      vec2  x = abs(vec2(0.0, 2.0)); // x = vec2(0.0, 1.0)

:proto:`T floor (T x)`

   The `floor` function returns a value equal to the nearest integer that is
   less than or equal to x.

   .. code:: glsl

      float x = sign(1.9);             // x = 1.0
      vec2  x = sign(vec2(-0.1, 1.1)); // x = vec2(-1.0, 1.0)


:proto:`T ceil (T x)`

   The `ceil` function returns a value equal to the nearest integer that is
   greater than or equal to x.

   .. code:: glsl

      float x = sign(1.9);             // x = 2.0
      vec2  x = sign(vec2(-0.1, 1.1)); // x = vec2(0.0, 2.0)

:proto:`T fract (T x)`

   The `frac` function returns the fractional part of x, i.e. x – floor (x).

   .. code:: glsl

      float x = frac(1.9);             // x = 0.9
      vec2  x = sign(vec2(-0.1, 1.1)); // x = vec2(0.9, 0.1)

:proto:`T mod (T x, float y)`

   The `mod` function returns the modulus (modulo) of x, i.e. x – y * floor
   (x/y)

   .. code:: glsl

      float x = mod(1.1, 1.0);            // x = 0.1
      vec2  x = mod(vec2(1.1, 2.2), 1.0); // x = vec2(0.1, 0.2)

   
:proto:`T mod (T x, T y)`

   The `mod` function returns the modulus (modulo) of x, i.e. x – y * floor
   (x/y).
   
   .. code:: glsl

      float x = mod(1.1, 1.0);        // x = 0.1
      vec2  x = mod(vec2(1.1, 2.2),
                    vec2(1.0, 1.5));  // x = vec2(0.1, 0.7)
      
| :proto:`T min (T x, T y)`
| :proto:`T min (T x, float y)`

   The `min` function returns y if y < x, otherwise it returns x

   .. code:: glsl

      vec2 x = min(vec2(1.0, 2.0),
                   vec2(0.0, 3.0));      // x = vec2(0.0, 2.0)
      vec2 x = min(vec2(1.0, 2.0), 1.0); // x = vec2(1.0, 1.0)

   
| :proto:`T max (T x, T y)`
| :proto:`T max (T x, float y)`

   The `max` function returns y if x < y, otherwise it returns x

   .. code:: glsl

      vec2 x = max(vec2(1.0, 2.0),
                   vec2(0.0, 3.0));      // x = vec2(1.0, 3.0)
      vec2 x = max(vec2(1.0, 2.0), 1.0); // x = vec2(1.0, 2.0)

| :proto:`T clamp (T x, T a, T b)`
| :proto:`T clamp (T x, float a, float b)`

   The `clamp` function returns `min(max(x,a),b)`.
   Results are undefined if a > b.

   .. code:: glsl

      float x = clamp(1.1, 0.0, 1.0);            // x = 1.0;
      vec2  x = clamp(vec2(1.0, 2.0), 0.0, 1.0); // x = vec2(1.0, 1.0)
   
| :proto:`T mix (T x, T y, T a)`
| :proto:`T mix (T x, T y, float a)` 

   The `mix` function returns the linear blend of x and y, i.e. x(1-a)+ya.

   .. code:: glsl

      float x = mix(0.0, 4.0, 0.25);  // x = 1.0;
      float x = mix(0.0, 4.0, 0.75);  // x = 3.0;
   
| :proto:`T step (T edge, T x)`
| :proto:`T step (float edge, T x)`

   The `step` returns 0.0 if x < edge, otherwise it returns 1.0

   .. code:: glsl

      float x = step(0.0, -1.0); // x = -1.0;
      float x = step(0.0, 0.5);  // x = 1.0

| :proto:`T smoothstep (T edge0, T edge1, T x)`
| :proto:`T smoothstep (float edge0, float edge1, T x)`
       
  The `smoothstep` function returns 0.0 if x <= edge0 and 1.0 if x ≥ edge1 and
  performs smooth Hermite interpolation between 0 and 1 when edge0 < x <
  edge1. This is useful in cases where you would want a threshold function with
  a smooth transition. This is equivalent to:

  .. code:: glsl
     
     T t = clamp ((x – edge0) / (edge1 – edge0), 0, 1);
     return t * t * (3 – 2 * t);

  Results are undefined if edge0 >= edge1.


Geometric functions
+++++++++++++++++++

:proto:`float length (T x)`
          
   The `length` function returns the length of vector x, i.e. the square root of
   the sum of the squares components.

   .. code:: glsl

      float x = length(1.0);             // x = 1.0
      float x = length(vec2(3.0,4.0));   // x = 5.0
   
   
:proto:`float distance (T p0, T p1)`
          
   Returns the distance between p0 and p1, i.e. `length(p1-p0)`.

   .. code:: glsl

      vec3 p0 = vec3(1.0, 5.0, 7.0);
      vec3 p1 = vec3(1.0, 2.0, 3.0);
      float x = length(p0,p1); // x = 5.0

:proto:`float dot (T x, T y)`
          
   Returns the dot product of x and y

:proto:`vec3 cross (vec3 x, vec3 y)`

   The `cross` functionn returns the cross product of x and y.

:proto:`T normalize (T x)`

   The `normalize` function returns a vector in the same direction as x but
   with a length of 1.

   .. code:: glsl

      vec2 p = normalize(vec2(3.0, 4.0)); // x = vec2(3.0,4.0)/5.0

:proto:`T faceforward(T N, T I,T Nref)`

   The `faceforward` function return N if `dot(Nref, I) < 0`, otherwise it
   returns –N.

:proto:`T reflect (T I, T N)`

   For the incident vector I and surface orientation N, the `reflect` function
   returns the reflection direction: I – 2 ∗ dot(N, I) ∗ N N must already be
   normalized in order to achieve the desired result.

:proto:`T refract (T I, T N, float eta)`

   For the incident vector I and surface normal N, and the ratio of indices of
   refraction eta, the `reftact` function returns the refraction vector. The
   result is computed by:

   .. code:: glsl
      
      k = 1.0-eta*eta*(1.0-dot(N,I)*dot(N,I))
      if (k < 0.0)
          return T(0)
      return eta*I-(eta*dot(N,I)+sqrt(k))*N
                                    
   The input parameters for the incident vector I and the surface normal N must
   already be normalized to get the desired results.


   
Matrix functions
+++++++++++++++++

:proto:`mat matrixCompMult (mat x, mat y)`

   The `matrixCompMult` multiply matrix x by matrix y component-wise, i.e.,
   `result[i][j]` is the scalar product of `x[i][j]` and `y[i][j]`.

   **Note**: to get linear algebraic matrix multiplication, use the multiply
   operator (*).

   .. code:: glsl
      
      mat4 x = mat4(1.0);
      mat4 y = mat4(2.0);
      mat4 z = matrix CompMult(x,y); // z = mat4(2.0);

   

Vector Relational Functions
++++++++++++++++++++++++++++

Relational and equality operators (<, <=, >, >=, ==, !=) are defined to produce
scalar Boolean results. For vector results, use the following built-in
functions. Below, `bvecN` is a placeholder for one of `bvec2`, `bvec3`, or
`bvec4`, `ivecN` is a placeholder for one of `ivec2`, `ivec3`, or `ivec4`, and
`vecN` is a placeholder for `vec2`, `vec3`, or `vec4`. In all cases, the sizes
of the input and return vectors for any particular call must match.

| :proto:`bvecN lessThan (ivecN x, ivecN y)`
| :proto:`bvecN lessThan (vecN x, vecN y)`
       
   The `lessThan` function returns the component-wise compare of x < y.

   .. code:: glsl

      bvec2 c = lessThan(vec2(1.0,1.0),
                         vec2(1.0,2.0)); // x = vec2(false, true);

| :proto:`bvecN lessThanEqual (ivecN x, ivecN y)`
| :proto:`bvecN lessThanEqual (vecN x, vecN y)`
       
   The `lessThan` function returns the component-wise compare of x ≤ y.

   .. code:: glsl

      bvec2 c = lessThan(vec2(1.0,1.0),
                         vec2(1.0,2.0)); // x = vec2(true, true);

| :proto:`bvecN greaterThan (ivecN x, ivecN y)`
| :proto:`bvecN greaterThan (vecN x, vecN y)`
       
   The `greaterThan` function returns the component-wise compare of x > y.

   .. code:: glsl

      bvec2 c = greaterThan(vec2(1.0,1.0),
                            vec2(1.0,2.0)); // x = vec2(false, false);

| :proto:`bvecN greaterThanEqual (ivecN x, ivecN y)`
| :proto:`bvecN greaterThanEqual (vecN x, vecN y)`
       
   The `greaterThan` function returns the component-wise compare of x ≥ y.

   .. code:: glsl

      bvec2 c = greaterThan(vec2(1.0,1.0),
                            vec2(1.0,2.0)); // x = vec2(true, false);

| :proto:`bvecN equal (bvecN x, bvecN y)`
| :proto:`bvecN equal (ivecN x, ivecN y)`
| :proto:`bvecN equal (vecN x, vecN y)`

   The `equal` function returns the component-wise compare of x == y.
   
   .. code:: glsl

      ivec2 c = equald(ivec2(1,1),
                       ivec2(1,2)); // x = vec2(true, false);

| :proto:`bvecN notEqual (bvecN x, bvecN y)`
| :proto:`bvecN notEqual (ivecN x, ivecN y)`
| :proto:`bvecN notEqual (vecN x, vecN y)`

   The `notEqual` function returns the component-wise compare of x == y.
   
   .. code:: glsl

      ivec2 c = notEqual(ivec2(1,1),
                         ovec2(1,2)); // x = vec2(false, true);

:proto:`bool any (bvecN x)`

   The `any` function returns true if any component  of x is true.
   
   .. code:: glsl

      bool x = any(bvec3(true, false, false));  // x = true
      bool x = any(bvec3(false, false, false)); // x = false


:proto:`bool all (bvecN x)`
       
   The `all` function returns true only if all components of x are true.

   .. code:: glsl

      bool x = all(bvec3(true, true, true));  // x = true
      bool x = all(bvec3(true, true, false)); // x = false

:proto:`bvecN not (bvecN x)`

   Returns the component-wise logical complement of x.

   .. code:: glsl

      bvec2 x = not(bvec2(true, false)); // x = bvec2(false, true)

   

Texture lookup functions
++++++++++++++++++++++++

:proto:`vec4 texture2D (sampler2D sampler, vec2 coord)`

   Use the texture coordinate coord to do a texture lookup in the 2D texture
   currently bound to sampler.


:proto:`vec4 textureCube (samplerCube sampler, vec3 coord )`
       
   Use the texture coordinate coord to do a texture lookup in the cube map
   texture currently bound to sampler. The direction of coord is used to select
   which face to do a 2- dimensional texture lookup in, as described in section
   3.8.6 in version 2.0 of the OpenGL specification.



