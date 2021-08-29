#%%
# %load_ext nothing.helpers.ipython_cairo
import canvas

from numpy import linspace, random
from scipy import interpolate


canvas._setup()
canvas.begin_plotting(debug=False)
canvas.clear([1, 1, 1, 1])
canvas.set_range(-1, 1)
canvas.set_color([0, 0, 0, 1])

from geom.line import Line
from geom.circle import Circle


def draw_stroke_test(y_off, split_count):
    count = 7
    x_points = linspace(0, 1, num=count)
    y_points = random.rand(count)
    tck = interpolate.splrep(x_points, y_points)

    def f(x):
        return interpolate.splev(x, tck)

    line = Line((-1.0, y_off), (1.0, y_off))

    splits = linspace(0, 1, split_count + 1, endpoint=False)[1:]
    segs = line.shatter(splits)
    for seg_info in zip(splits, segs):
        perc, segment = seg_info
        canvas.set_line_depth(f(perc))
        segment.draw(canvas)
    canvas.end_segment()


divisions = 100
ys = linspace(0.8, -0.8, 20)
for y in ys:
    draw_stroke_test(y, divisions)

canvas.end_plotting()
canvas._ctx
# %%
