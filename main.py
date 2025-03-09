#!/usr/bin/env python3

import numpy as np
from matplotlib import pyplot as plt
import matplotlib.animation as anim
from matplotlib.widgets import Slider, RadioButtons

from interactive_line import InteractiveLine
from interactive_spline import InteractiveSpline
from spline import Spline
from lerp_spline import LerpSpline, lerp


def interactive_demo():
    fig = plt.figure()

    axes = fig.subplot_mosaic("""
        s
        s
        s
        s
        s
        s
        s
        v
        t
        t
    """)

    ax = axes["s"]
    ax2 = axes["v"]
    ax3 = axes["t"]

    ax.set_title("Interactive spline demo")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    xs = np.array([0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8])
    ys = np.array([0.5, 0.1, 0.9, 0.5, 0.1, 0.9, 0.5])

    spline = Spline.bezier()

    ispl = InteractiveSpline(ax, spline, control_style="")

    ispl.set_data(xs, ys)
    ispl.draw_spline()

    slider = Slider(ax2, "t", 0, 1, valinit=1)
    slider.on_changed(ispl.draw_spline)

    rad = RadioButtons(ax3, ["Bezier", "B"])
    rad.on_clicked(ispl.change_spline_str)

    plt.show()


def bezier_spline(show = True):
    fig = plt.figure()
    ax = fig.subplots(1, 1)
    ax.set_title("spline")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    xs = np.linspace(0.1, 0.9, 7)
    ys = np.array([0.5, 0.2, 0.8, 0.5, 0.2, 0.8, 0.5])

    ispl = InteractiveSpline(ax, Spline.bezier(), draw_control=False)
    ispl.set_data(xs, ys)
    ispl.draw_spline()

    if show:
        plt.show()
    else:
        plt.savefig("./outputs/bezier_spline.png")
        print("saved: ", "./outputs/bezier_spline.png")


def b_spline(show = True):
    fig = plt.figure()
    ax = fig.subplots(1, 1)
    ax.set_title("spline")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    xs = np.array([0.25, 0.1, 0.05, 0.25, 0.45, 0.75, 0.95, 0.7, 0.65, 0.35])
    ys = np.array([0.1, 0.25, 0.5, 0.75, 0.5, 0.2, 0.5, 0.9, 0.6, 0.8])

    ispl = InteractiveSpline(ax, Spline.b(), draw_control=False)
    ispl.set_data(xs, ys)
    ispl.draw_spline()

    if show:
        plt.show()
    else:
        plt.savefig("./outputs/b_spline.png")
        print("saved: ", "./outputs/b_spline.png")


def lerp_anim(show = True):
    fig = plt.figure()
    ax = fig.subplots(1, 1)
    ax.set_title("lerp")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    xs = np.array([0.2, 0.8])
    ys = np.array([0.9, 0.2])
    labels = ["P₀", "P₁", "P₂", "P₃"]
    ax.plot(xs, ys, "bo-")
    for i in range(len(xs)):
        ax.annotate(labels[i], (xs[i], ys[i]), fontweight = "bold", fontsize = "large")

    bsp = LerpSpline()

    def update(frame):
        t = max(0, min(1, (frame - 25) / 225))
        bsp.redraw(ax, xs, ys, t)

    ani = anim.FuncAnimation(fig, update, frames=300, interval=16.6667)

    if show:
        plt.show()
    else:
        ani.save("./outputs/lerp.gif", fps = 60)
        print("saved: ", "./outputs/lerp.gif")


def curve_anim(show = True):
    fig = plt.figure()
    ax = fig.subplots(1, 1)
    ax.set_title("parameterized curve")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    xs = np.array([0.2, 0.4, 0.6, 0.8])
    ys = np.array([0.5, 0.1, 0.9, 0.5])

    bez = Spline.bezier()

    spx, spy = bez.calc_segment(xs, ys)

    ax.plot(spx, spy, "b-", linewidth = 3)
    ax.plot([spx[0], spx[len(spx) - 1]], [spy[0], spy[len(spy) - 1]], "bo")

    x, y = bez.calc_point(xs, ys, 0)
    p, = ax.plot(x, y, "ro")
    a = ax.annotate("t = 0.00", (x, y), fontweight = "bold", fontsize = "large")


    def update(frame):
        t = max(0, min(1, (frame - 25) / 225))
        x, y = bez.calc_point(xs, ys, t)
        a.set_position((x, y))
        a.set_text("t = {:1.2f}".format(t))
        p.set_data([x], [y])

    ani = anim.FuncAnimation(fig, update, frames=300, interval=16.6667)

    if show:
        plt.show()
    else:
        ani.save("./outputs/parametric_curve.gif", fps = 60)
        print("saved: ", "./outputs/parametric_curve.gif")


def control_points(show = True):
    fig = plt.figure()
    ax = fig.subplots(1, 1)
    ax.set_title("control points")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    xs = np.array([0.2, 0.4, 0.6, 0.8])
    ys = np.array([0.5, 0.1, 0.9, 0.5])

    ax.plot(xs, ys, "ko--")

    if show:
        plt.show()
    else:
        plt.savefig("./outputs/control_points.png")
        print("saved: ", "./outputs/control_points.png")


def curve_control_anim(show = True):
    fig = plt.figure()
    ax = fig.subplots(1, 1)
    ax.set_title("parameterized curve")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    xs = np.array([0.2, 0.4, 0.6, 0.8])
    ys = np.array([0.5, 0.1, 0.9, 0.5])

    bez = Spline.bezier()

    spx, spy = bez.calc_segment(xs, ys, t = 0)

    ax.plot(xs, ys, "ko--")
    sp_plot, = ax.plot(spx, spy, "b-", linewidth = 3)
    sp_join, = ax.plot([spx[0], spx[len(spx) - 1]], [spy[0], spy[len(spy) - 1]], "bo")

    x, y = bez.calc_point(xs, ys, 0)
    p, = ax.plot(x, y, "ro")
    a = ax.annotate("t = 0.00", (x, y), fontweight = "bold", fontsize = "large")


    def update(frame):
        t = max(0, min(1, (frame - 25) / 225))
        x, y = bez.calc_point(xs, ys, t)
        spx, spy = bez.calc_segment(xs, ys, t = t)
        sp_plot.set_data(spx, spy)
        sp_join.set_data([spx[0], spx[len(spx) - 1]], [spy[0], spy[len(spy) - 1]])
        a.set_position((x, y))
        a.set_text("t = {:1.2f}".format(t))
        p.set_data([x], [y])

    ani = anim.FuncAnimation(fig, update, frames=300, interval=16.6667)

    if show:
        plt.show()
    else:
        ani.save("./outputs/parametric_curve_control.gif", fps = 60)
        print("saved: ", "./outputs/parametric_curve_control.gif")

def bezier3_anim(show = True):
    fig = plt.figure()
    ax = fig.subplots(1, 1)
    ax.set_title("3rd order Bézier curve")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    xs = np.array([0.2, 0.4, 0.6, 0.8])
    ys = np.array([0.5, 0.1, 0.9, 0.5])
    labels = ["P₀", "P₁", "P₂", "P₃"]
    for i in range(len(xs)):
        ax.annotate(labels[i], (xs[i], ys[i]), fontweight = "bold", fontsize = "large")

    bsp = LerpSpline()
    ispl = InteractiveSpline(ax, Spline.bezier())
    ispl.set_data(xs, ys)

    def update(frame):
        t = max(0, min(1, (frame - 25) / 225))
        ispl.draw_spline(t)
        bsp.redraw(ax, xs, ys, t)

    ani = anim.FuncAnimation(fig, update, frames=300, interval=16.6667)

    if show:
        plt.show()
    else:
        ani.save("./outputs/bezier_lerp3.gif", fps = 60)
        print("saved: ", "./outputs/bezier_lerp3.gif")
        

def lin_spline(show = True):
    fig = plt.figure()
    ax = fig.subplots(1, 1)
    ax.set_title("linear spline")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    xs = np.array([0.25, 0.1, 0.05, 0.25, 0.45, 0.75, 0.95, 0.7, 0.65, 0.35])
    ys = np.array([0.1, 0.25, 0.5, 0.75, 0.5, 0.2, 0.5, 0.9, 0.6, 0.8])

    ax.plot(xs, ys, "bo-", linewidth = 3)

    p, = ax.plot(xs[0], ys[0], "ro")
    a = ax.annotate("t = 0.00", (xs[0], ys[0]), fontweight = "bold", fontsize = "large")

    def update(frame):
        t_norm = max(0, min(1, (frame - 25) / 225))
        t = t_norm * (len(xs) - 1)
        if t >= len(xs) - 1:
            t -= 0.0001
        i = int(t // 1)
        f = t % 1
        x = lerp(xs[i], xs[i + 1], f)
        y = lerp(ys[i], ys[i + 1], f)
        p.set_data([x], [y])
        a.set_position((x, y))
        a.set_text("t = {:1.2f}".format(t))

    ani = anim.FuncAnimation(fig, update, frames=300, interval=16.6667)
    
    if show:
        plt.show()
    else:
        ani.save("./outputs/lin_spline.gif", fps = 60)
        print("saved: ", "./outputs/lin_spline.gif")


def bezier2_anim(show = True):
    fig = plt.figure()
    ax = fig.subplots(1, 1)
    ax.set_title("2nd order Bézier curve")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    xs = np.array([0.2, 0.5, 0.8])
    ys = np.array([0.2, 0.9, 0.2])
    labels = ["P₀", "P₁", "P₂", "P₃"]
    for i in range(len(xs)):
        ax.annotate(labels[i], (xs[i], ys[i]), fontweight = "bold", fontsize = "large")

    bsp = LerpSpline()

    curve, = ax.plot([], [], "b-", linewidth = 3)

    def update(frame):
        t = max(0, min(1, (frame - 25) / 225))
        ls = np.linspace(0, t, 100)
        x, y = LerpSpline.calc_segment(xs, ys, t)
        curve.set_data(x, y)
        bsp.redraw(ax, xs, ys, t)

    ani = anim.FuncAnimation(fig, update, frames=300, interval=16.6667)

    if show:
        plt.show()
    else:
        ani.save("./outputs/bezier_lerp2.gif", fps = 60)
        print("saved: ", "./outputs/bezier_lerp2.gif")
        


def gen_all():
    bezier_spline(False)
    b_spline(False)
    curve_anim(False)
    control_points(False)
    lerp_anim(False)
    bezier3_anim(False)
    curve_control_anim(False)
    lin_spline(False)
    bezier2_anim(False)


#---------------------------------------------------------------------

# bezier_spline()

# b_spline()

# curve_anim()

# control_points()

# lerp_anim()

# bezier3_anim()

# curve_control_anim()

# lin_spline()

# bezier2_anim()

gen_all()


# interactive_demo()
