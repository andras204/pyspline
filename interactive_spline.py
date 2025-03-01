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
         control_style: str = "ko--",
         precision: int = 100,
         select_margin: float = 0,
         locked: bool = False
     ):
        super().__init__(ax)
        self.spline = spline
        self.spline_plot = ax.plot([], [], spline_style, linewidth=3)[0]
        self.precision = precision


    def set_data(self, x: [float], y: [float]):
        self.xs = x
        self.ys = y
        self._update_line()
    

    def draw_spline(self, t: float = -1):
        if len(self.xs) < 4:
            self.spline_plot.set_data([], [])
            return

        if t == -1:
            t = self.segments()

        inc = 3
        if self.spline.striped:
            inc = 1

        x = []
        y = []

        asd: float = 0

        for seg in range(3, len(self.xs), inc):
            a = min(1, t - asd)
            if a < 0:
                break
            cpxs = self.xs[(seg - 3):(seg + 1)]
            cpys = self.ys[(seg - 3):(seg + 1)]
            xs, ys = self.spline.calc_segment(cpxs, cpys, self.precision, a)
            asd += 1
            x.extend(xs)
            y.extend(ys)

        self.spline_plot.set_data(x, y)


    def segments(self) -> int:
        if len(self.xs) < 4:
            return 0
        if self.spline.striped:
            return len(self.xs) - 3
        return 1 + ((len(self.xs) - 4) // 3)


    def _update_line(self):
        self.draw_spline()
        super()._update_line()
