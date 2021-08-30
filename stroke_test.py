#%%
%load_ext nothing.helpers.ipython_cairo
import canvas

from numpy import linspace
from helpers import thock

canvas._setup()
canvas.begin_plotting(debug=True)
canvas.clear([1, 1, 1, 1])
canvas.set_range(-1, 1)
canvas.set_color([0, 0, 0, 1])

from geom.line import Line
from geom.circle import Circle



def draw_stroke_test(y_off, complexity):
    line = Line((-1.0, y_off), (1.0, y_off))
    thk = thock.random_thock(wiggles=60)

    for thock_line in thock.apply_thock_to_line(line, thk, complexity):
        segment, depth = thock_line
        canvas.set_line_depth(depth)
        segment.draw(canvas)
    canvas.end_segment()


divisions = 128
ys = linspace(0.8, -0.8, 40)
for y in ys:
    draw_stroke_test(y, divisions)

canvas.end_plotting()
canvas._ctx
# %%
