#%%
%load_ext nothing.helpers.ipython_cairo
import canvas

from numpy import linspace


canvas._setup()
canvas.begin_plotting()
canvas.clear([1, 1, 1, 1])
canvas.set_range(-1, 1)
canvas.set_color([0, 0, 0, 1])

from geom.line import Line

# test coordinate conversion
result = canvas.pixel_point_to_mm((0, 0))
assert result == (148.5, 105)
result = canvas.pixel_point_to_mm((0, -1))
assert result == (148.5, 0)
result = canvas.pixel_point_to_mm((-1, 0))
assert result == (43.5, 105)

canvas.set_line_depth(0.5)
line = Line((-1.0, 0), (1.0, 0))

# split_count = 12
# splits = linspace(0, 1, split_count + 1, endpoint=False)[1:]
# segs = line.shatter(splits)
# line_depths = linspace(0.0, 1.0, len(segs))

# for itm in zip(segs, line_depths):
#     canvas.set_line_depth(itm[1])
#     itm[0].draw(canvas)

line.draw(canvas)

canvas.end_plotting()
canvas._ctx

# %%
