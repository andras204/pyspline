import math
import numpy as np
import matplotlib as plt
from matplotlib.axes import Axes

class InteractiveLine:
    """Wrapper class for Line2D, that enables interactivity"""
    
    def __init__(self, ax: Axes, style: str = "ko--", select_margin: float = 0, locked: bool = False):
        line, = ax.plot([], [], style)
        if select_margin == 0:
            select_margin = min(ax.get_xlim()[1] - ax.get_xlim()[0],
                                ax.get_ylim()[1] - ax.get_ylim()[0]) / 75
        self.axes = ax
        self.line = line
        self.xs = list(line.get_xdata())
        self.ys = list(line.get_ydata())
        self.selected_index = None
        self.select_margin = select_margin
        self.locked = locked
        self.event_connections = [
            line.figure.canvas.mpl_connect("button_press_event", self._select_or_add),
            line.figure.canvas.mpl_connect("button_release_event", self._release_drag),
            line.figure.canvas.mpl_connect("figure_leave_event", self._release_drag),
            line.figure.canvas.mpl_connect("motion_notify_event", self._drag),
        ]


    def _update_line(self):
        self.line.set_data(self.xs, self.ys)
        self.line.figure.canvas.draw()


    def _select_or_add(self, event):
        """callback function to handle selecting, adding, adn removing points"""

        if event.inaxes != self.line.axes:
            return

        if event.button == plt.backend_bases.MouseButton.RIGHT:
            if len(self.xs) > 0:
                self.xs.pop()
                self.ys.pop()
                self._update_line()
            return

        if event.button != plt.backend_bases.MouseButton.LEFT:
            return

        for i in range(len(self.xs)):
            if math.sqrt(pow(self.xs[i] - event.xdata, 2) +
                         pow(self.ys[i] - event.ydata, 2)) < self.select_margin:
                self.selected_index = i
                return

        if self.locked:
            return

        self.xs.append(event.xdata)
        self.ys.append(event.ydata)
        self.selected_index = len(self.xs) - 1
        self._update_line()

        
    def _release_drag(self, event):
        """callback function to handle releasing points"""

        if event.inaxes != self.line.axes:
            return

        self.selected_index = None

        
    def _drag(self, event):
        """callback function to handle dragging points"""

        if event.inaxes != self.line.axes or self.selected_index is None:
            return

        self.xs[self.selected_index] = event.xdata
        self.ys[self.selected_index] = event.ydata
        self._update_line()
