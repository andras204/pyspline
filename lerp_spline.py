import matplotlib as plt
import numpy as np
from matplotlib.axes import Axes
from matplotlib.pyplot import Line2D

def lerp(a: float, b: float, t: float) -> float:
    return (1 - t) * a + t * b


class LerpSpline:
    def __init__(self):
        self.plots: [Line2D] = []
        self.annot = None


    def redraw(self, ax: Axes, xs: [float], ys: [float], t: float, depth: int = 0):
        if len(xs) != len(ys):
            raise Exception("xs and ys must be the same lenght")

        if len(self.plots) <= depth:
            self.plots.append(ax.plot(xs, ys, "o--")[0])
        else:
            self.plots[depth].set_data(xs, ys)

        if len(xs) < 2:
            if self.annot is None:
                self.annot = ax.annotate("t = {:1.2f}".format(t), (xs[0], ys[0]), fontweight = "bold", fontsize = "large")
            else:
                self.annot.set_position((xs[0], ys[0]))
                self.annot.set_text("t = {:1.2f}".format(t))

            for i in range(depth + 1, len(self.plots)):
                self.plots[i].set_data([], [])
            return

        xs_interp: [float] = []
        ys_interp: [float] = []

        for i in range(len(xs) - 1):
            xs_interp.append(lerp(xs[i], xs[i + 1], t))
            ys_interp.append(lerp(ys[i], ys[i + 1], t))

        self.redraw(ax, xs_interp, ys_interp, t, depth + 1)


    def calc_point(xs: [float], ys: [float], t: float) -> (float, float):
        if len(xs) != len(ys):
            raise Exception("xs and ys must be the same lenght")
        
        if len(xs) < 2:
            return (xs[0], ys[0])

        xs_interp: [float] = []
        ys_interp: [float] = []

        for i in range(len(xs) - 1):
            xs_interp.append(lerp(xs[i], xs[i + 1], t))
            ys_interp.append(lerp(ys[i], ys[i + 1], t))

        return LerpSpline.calc_point(xs_interp, ys_interp, t)

        
    def calc_segment(xs: [float], ys: [float], t: float, precision: int = 100) -> ([float], [float]):
        if t == 0:
            precision = 1

        ts = np.linspace(0, t, precision)
        x = []
        y = []

        for i in range(precision):
            xp, yp = LerpSpline.calc_point(xs, ys, ts[i])
            x.append(xp)
            y.append(yp)

        return (x, y)
