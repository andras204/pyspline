#!/usr/bin/env python3

import numpy as np
from matplotlib import pyplot as plt
import matplotlib.animation as anim

from interactive_line import InteractiveLine
from interactive_spline import InteractiveSpline
from spline import Spline

fig, ax = plt.subplots()

ax.set_title('Interactive line demo')
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)


xs = np.array([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7])
ys = np.array([0.3, 0.6, 0.7, 0.3, 0.1, 0.8, 0.2])

# spline = Spline.b()
spline = Spline.bezier()

ispl = InteractiveSpline(ax, spline)

ispl.set_data(xs, ys)
ispl.draw_spline(0)

def update(frame):
    ispl.draw_spline(frame / 100)

ani = anim.FuncAnimation(fig, update, frames=300, interval=16.6667)

plt.show()
