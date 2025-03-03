#!/usr/bin/env python3

import numpy as np
from matplotlib import pyplot as plt
import matplotlib.animation as anim
from matplotlib.widgets import Slider, RadioButtons

from interactive_line import InteractiveLine
from interactive_spline import InteractiveSpline
from spline import Spline
from bezier_lerp import BezierLerpSpline



fig = plt.figure()

# ax = fig.subplots(1, 1)
ax, ax2, ax3 = fig.subplots(3, 1)

ax.set_title('Interactive line demo')
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)


# xs = np.array([0.2, 0.4, 0.6, 0.8])
# ys = np.array([0.5, 0.1, 0.9, 0.5])
xs = np.array([0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8])
ys = np.array([0.5, 0.1, 0.9, 0.5, 0.1, 0.9, 0.5])

# spline = Spline.b()
spline = Spline.bezier()

ispl = InteractiveSpline(ax, spline)

ispl.set_data(xs, ys)
ispl.draw_spline()

slider = Slider(ax2, "t", 0, 1, valinit=1)
slider.on_changed(ispl.draw_spline)

rad = RadioButtons(ax3, ["Bezier", "B", "Hermite", "Catmull-Rom"])

# bsp = BezierLerpSpline()

# def update(frame):
#     ispl.draw_spline((frame / 250) * ispl.segments())
#     bsp.redraw(ax, xs, ys, min(1, frame / 250))

# ani = anim.FuncAnimation(fig, update, frames=300, interval=16.6667)


plt.show()
