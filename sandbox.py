#%%
%load_ext nothing.helpers.ipython_cairo
import canvas

#%%

canvas._setup()
canvas.clear([1, 1, 1, 1])
canvas.set_range(-1, 1)
canvas.set_color([0, 0, 0, 1])

from geom.line import Line

line = Line((-1.0, 0), (1.0, 0))

segs = line.shatter([0.25, 0.5, 0.75])
print(len(segs))
line_widths = [5, 2, 12, 1]

for itm in zip(segs, line_widths):
    print(itm[0].points)
    canvas.set_line_width(itm[1])
    itm[0].draw(canvas)


# cx, cy = (0, 0)
# innerRad = 0.2
# outerRad = 0.9

# from geom.circle import Circle
# inner = Circle(cx, cy, innerRad)
# outer = Circle(cx, cy, outerRad)

# inner.draw(canvas)
# outer.draw(canvas)


canvas._ctx

# %%
