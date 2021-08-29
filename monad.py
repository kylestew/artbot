#%%
%load_ext nothing.helpers.ipython_cairo
import canvas

from numpy import linspace

from geom.line import Line
from geom.circle import Circle

canvas._setup()
canvas.begin_plotting(debug=True)
canvas.clear([1, 1, 1, 1])
canvas.set_range(-1, 1)
canvas.set_color([0, 0, 0, 1])

line = Line((-1.0, 0), (1.0, 0))

cx, cy = (0, 0)
count = 12
innerRad = 0.1
outerRad = 0.9

inner = Circle(cx, cy, innerRad)
outer = Circle(cx, cy, outerRad)

def create_ray(a, b, t):
    return Line(a, b)

# rays are connector points between inner and outer circle
rays = []
t = linspace(0, 1, count)
for endpoints in zip(inner.vertices(n=count), outer.vertices(n=count), t):
    a, b, t = endpoints
    ray = create_ray(a, b, t)
    rays.append(ray)

canvas.set_line_depth(0.5)
for ray in rays:
    ray.draw(canvas)

canvas.end_plotting()
canvas._ctx

# %%
