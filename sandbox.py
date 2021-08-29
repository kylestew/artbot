#%%
%load_ext nothing.helpers.ipython_cairo
import canvas

from numpy import linspace

from geom.line import Line

canvas._setup()
canvas.begin_plotting(simulate=False)
canvas.clear([1, 1, 1, 1])
canvas.set_range(-1, 1)
canvas.set_color([0, 0, 0, 1])

line = Line((-1.0, 0), (1.0, 0))

split_count = 120
splits = linspace(0, 1, split_count + 1, endpoint=False)[1:]
segs = line.shatter(splits)
line_depths = linspace(0.0, 1.0, len(segs))

for itm in zip(segs, line_depths):
    canvas.set_line_depth(itm[1])
    itm[0].draw(canvas)
canvas.end_segment()

canvas.end_plotting()
canvas._ctx

# %%
