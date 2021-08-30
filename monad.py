#%%
%load_ext nothing.helpers.ipython_cairo
import canvas

from numpy import linspace, pi
from helpers.thock import random_thock, shaped_thock

from geom.circle import Circle
from geom.line import Line

canvas._setup()
canvas.begin_plotting(debug=False)
canvas.clear([1, 1, 1, 1])
canvas.set_range(-1, 1)
canvas.set_color([0, 0, 0, 1])

cx, cy = (0, 0)
count = 32
complexity = 128
innerRad = 0.08
outerRad = 0.9

# flipped = 1
flipped = -1
inner = Circle(cx, cy, innerRad)
# inner = inner.rotate(pi / (9.0 * flipped))
outer = Circle(cx, cy, outerRad)
# outer = outer.rotate(pi / (9.0 * -flipped))


def create_ray(a, b, complexity):
    """Plots a ray with varying thickness through its body"""
    thock = random_thock(wiggles=12)
    shaper = shaped_thock([0, 0.2, 0.4, 0.6, 1, 1, 1, 1, 1, 0.1])
    line = Line(a, b)

    splits = linspace(0, 1, complexity + 1, endpoint=False)[1:]
    segs = line.shatter(splits)
    for seg_info in zip(splits, segs):
        perc, segment = seg_info
        canvas.set_line_depth(thock(perc) * shaper(perc))
        segment.draw(canvas)
    canvas.end_segment()


# rays are connector points between inner and outer circle
t = linspace(0, 1, count)
for endpoints in zip(inner.vertices(n=count), outer.vertices(n=count), t):
    a, b, t = endpoints
    create_ray(a, b, complexity)

canvas.end_plotting()
canvas._ctx

# %%
