import math
import numpy as np
import matplotlib as plt
from matplotlib.axes import Axes
from numpy import matrix

from interactive_line import InteractiveLine
from spline import Spline


class InteractiveSpline(InteractiveLine):
    """Base class for interactive splines"""
    
    def __init__(
         self,
         ax: Axes,
         spline: Spline,
         spline_style: str = "b-",
         join_style: str = "bo",
         control_style: str = "ko--",
         precision: int = 100,
         select_margin: float = 0,
         locked: bool = False,
         draw_control: bool = True
     ):
        super().__init__(ax)
        if not draw_control:
            self.line.set_alpha(0)
        self.spline = spline
        self.spline_plot = ax.plot([], [], spline_style, linewidth=3)[0]
        self.join_plot = ax.plot([], [], join_style, linewidth=3)[0]
        self.precision = precision


    def set_data(self, x: [float], y: [float]):
        self.xs = x
        self.ys = y
        self._update_plot()


    def change_spline_str(self, spline_name: str):
        splines = {
            "bezier": Spline.bezier(),
            "b": Spline.b(),
            # "hermite": Spline.hermite(),
            # "catmull-rom": Spline.catmull_rom(),
        }

        self.spline = splines[spline_name.lower()]
        self._update_plot()


    def draw_spline(self, t: float = -1, normalized = True):
        if len(self.xs) < 4:
            self.spline_plot.set_data([], [])
            return

        if normalized:
            t *= self.segments() 

        if t < 0:
            t = self.segments()

        x = []
        y = []
        jx = []
        jy = []

        asd: float = 0

        for seg in range(3, len(self.xs), self.spline.stride):
            a = min(1, t - asd)
            if a < 0:
                break
            cpxs = self.xs[(seg - 3):(seg + 1)]
            cpys = self.ys[(seg - 3):(seg + 1)]
            xs, ys = self.spline.calc_segment(cpxs, cpys, self.precision, a)
            jx.append(xs[0])
            jy.append(ys[0])
            jx.append(xs[len(xs) - 1])
            jy.append(ys[len(ys) - 1])
            x.extend(xs)
            y.extend(ys)
            asd += 1

        self.spline_plot.set_data(x, y)
        self.join_plot.set_data(jx, jy)


    def segments(self) -> int:
        if len(self.xs) < 4:
            return 0
        return 1 + ((len(self.xs) - 4) // self.spline.stride)

    def _update_plot(self):
        self.draw_spline()
        super()._update_plot()

