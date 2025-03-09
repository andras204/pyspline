import numpy as np
import matplotlib as plt
from matplotlib.axes import Axes
from numpy import matrix


class Spline:
    def __init__(self, mat: matrix, stride: int):
        if mat.shape[0] != mat.shape[1] and mat.shape[0] != 4:
            raise Exception("mat must be a 4x4 square matrix")
        self.mat = mat
        self.stride = stride


    def b():
        return Spline(np.matrix([
            [ -1,  3, -3, 1],
            [  3, -6,  3, 0],
            [ -3,  0,  3, 0],
            [  1,  4,  1, 0],
        ]) / 6, 1)

    
    def bezier():
        return Spline(np.matrix([
            [ -1,  3, -3, 1],
            [  3, -6,  3, 0],
            [ -3,  3,  0, 0],
            [  1,  0,  0, 0],
        ]), 3)

    
    # def hermite():
    #     return Spline(np.matrix([
    #         [  1,  0,  0,  0],
    #         [  0,  1,  0,  0],
    #         [ -3, -2,  3, -1],
    #         [  2,  1, -2,  1],
    #     ]), 3)

    
    # def catmull_rom():
    #     return Spline(np.matrix([
    #         [  0,  2,  0,  0],
    #         [ -1,  0,  1,  0],
    #         [  2, -5,  4, -1],
    #         [ -1,  3, -3,  1],
    #     ]) / 2, 3)


    def draw_segment(
         self,
         xs: [float],
         ys: [float],
         ax: Axes,
         style: str = "b-",
         precision: int = 100,
         t: float = 1
     ):
        x = []
        y = []
        if t == 0:
            precision = 1

        xs = np.array(xs)
        ys = np.array(ys)
        ls = np.linspace(0, t, precision)

        for i in range(100):
            ts = np.array([pow(ls[i], 3), pow(ls[i], 2), ls[i], 1])
            mid = ts * self.mat
            x.append((mid * xs[:, np.newaxis]).flat[0])
            y.append((mid * ys[:, np.newaxis]).flat[0])

        spline, = ax.plot(x, y, style)


    def calc_segment(
         self,
         xs: [float],
         ys: [float],
         precision: int = 100,
         t: float = 1
     ) -> ([float], [float]):
        x: [float] = []
        y: [float] = []
        if t == 0:
            precision = 1

        xs = np.array(xs)
        ys = np.array(ys)
        ls = np.linspace(0, t, precision)

        for i in range(precision):
            ts = np.array([pow(ls[i], 3), pow(ls[i], 2), ls[i], 1])
            mid = ts * self.mat
            x.append((mid * xs[:, np.newaxis]).flat[0])
            y.append((mid * ys[:, np.newaxis]).flat[0])

        return (x, y)


    def calc_point(self, xs: [float], ys: [float], t: float) -> (float, float):
            ts = np.array([pow(t, 3), pow(t, 2), t, 1])
            mid = ts * self.mat
            x = (mid * xs[:, np.newaxis]).flat[0]
            y = (mid * ys[:, np.newaxis]).flat[0]
            return (x, y)
