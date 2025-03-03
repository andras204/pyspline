import matplotlib as plt
from matplotlib.axes import Axes
from matplotlib.pyplot import Line2D

def lerp(a: float, b: float, t: float) -> float:
    return (1 - t) * a + t * b


class BezierLerpSpline:
    def __init__(self):
        self.plots: [Line2D] = []


    def redraw(self, ax: Axes, xs: [float], ys: [float], t: float, depth: int = 0):
        if len(xs) != len(ys):
            raise Exception("xs and ys must be the same lenght")

        if len(self.plots) <= depth:
            self.plots.append(ax.plot(xs, ys, "o--")[0])
        else:
            self.plots[depth].set_data(xs, ys)

        if len(xs) < 2:
            for i in range(depth + 1, len(self.plots)):
                self.plots[i].set_data([], [])
            return

        xs_interp: [float] = []
        ys_interp: [float] = []

        for i in range(len(xs) - 1):
            xs_interp.append(lerp(xs[i], xs[i + 1], t))
            ys_interp.append(lerp(ys[i], ys[i + 1], t))

        self.redraw(ax, xs_interp, ys_interp, t, depth + 1)

