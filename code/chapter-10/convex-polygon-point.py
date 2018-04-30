# -----------------------------------------------------------------------------
# Python, OpenGL & Scientific Visualization
# www.labri.fr/perso/nrougier/python+opengl
# Copyright (c) 2018, Nicolas P. Rougier
# Distributed under the 2-Clause BSD License.
# -----------------------------------------------------------------------------
import numpy as np
import scipy.spatial
from glumpy import app, gl, gloo
from glumpy.graphics.collections import MarkerCollection

window = app.Window(width=512, height=512, color=(1, 1, 1, 1))

@window.event
def on_draw(dt):
    window.clear()
    points.draw()

np.random.seed(1)
P = 0.95 * np.random.uniform(-1, 1, (50,3))
O = P[scipy.spatial.ConvexHull(P[:,:2]).vertices]
points = MarkerCollection(marker="disc")
points.append(O, bg_color=(1,1,1,1), size=16)
points.append(P, bg_color=(0,0,0,1), size=4)

app.run()
