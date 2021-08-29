#%%
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

line.draw(canvas)

canvas.end_plotting()
canvas._ctx

# %%
