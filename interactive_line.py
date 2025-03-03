import math
import numpy as np
import matplotlib as plt
from matplotlib.axes import Axes
from typing import List

class InteractiveLine:
    """Wrapper class for Line2D, that enables interactivity"""
    
    def __init__(self, ax: Axes, style: str = "ko--", select_margin: float = 0, locked: bool = False):
        line, = ax.plot([], [], style)
        if select_margin == 0:
            select_margin = min(ax.get_xlim()[1] - ax.get_xlim()[0],
                                ax.get_ylim()[1] - ax.get_ylim()[0]) / 75
        self.axes = ax
        self.line = line
        self.xs: List[float] = list(line.get_xdata())
        self.ys: List[float] = list(line.get_ydata())
        self.selected_index = None
        self.select_margin = select_margin
        self.locked = locked
        self.event_connections = [
            line.figure.canvas.mpl_connect("button_press_event", self._mouse_button_handler),
            line.figure.canvas.mpl_connect("button_release_event", self._release_handler),
            line.figure.canvas.mpl_connect("figure_leave_event", self._release_handler),
            line.figure.canvas.mpl_connect("motion_notify_event", self._drag_handler),
        ]


    def _update_plot(self):
        self.line.set_data(self.xs, self.ys)
        self.line.figure.canvas.draw()


    def _mouse_button_handler(self, event):
        """callback function to handle selecting, adding, and removing points"""

        if event.inaxes != self.line.axes:
            return

        # workaround for lists getting auto-casted into
        # numpy ndarrays DESPITE TYPEHINTS
        # 
        # in __init__():
        # print(type(self.xs)) # <class 'list'>
        # 
        # here:
        # print(type(self.xs)) # <class 'numpy.ndarray'>
        # 
        # this is why I hate python
        self.xs = list(self.xs)
        self.ys = list(self.ys)

        # remove last control point on rightclick
        if event.button == plt.backend_bases.MouseButton.RIGHT:
            if len(self.xs) > 0:
                self.xs.pop()
                self.ys.pop()
                self._update_plot()
            return

        if event.button != plt.backend_bases.MouseButton.LEFT:
            return

        # if a control point is close enough, select it
        for i in range(len(self.xs)):
            if math.sqrt(pow(self.xs[i] - event.xdata, 2) +
                         pow(self.ys[i] - event.ydata, 2)) < self.select_margin:
                self.selected_index = i
                return

        if self.locked:
            return

        # otherwise add a new control point
        self.xs.append(event.xdata)
        self.ys.append(event.ydata)
        self.selected_index = len(self.xs) - 1
        self._update_plot()

        
    def _release_handler(self, event):
        """callback function to handle releasing points"""

        if event.inaxes != self.line.axes:
            return

        self.selected_index = None

        
    def _drag_handler(self, event):
        """callback function to handle dragging points"""

        if event.inaxes != self.line.axes or self.selected_index is None:
            return

        # update the position of the selected control point
        self.xs[self.selected_index] = event.xdata
        self.ys[self.selected_index] = event.ydata
        self._update_plot()

