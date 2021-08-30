#%%
# perlin noise -> vector flow field
from perlin_numpy import generate_perlin_noise_2d
import numpy as np

np.random.seed(1)
noise_density = 64
noise = generate_perlin_noise_2d((noise_density, noise_density), (8, 8))
theta = noise * 2 * np.pi
xs = np.sin(theta)
ys = np.cos(theta)
flow_field = np.column_stack((xs.flatten(), ys.flatten())).reshape(
    noise_density, noise_density, 2
)
flow_field.shape

%load_ext nothing.helpers.ipython_cairo
import canvas

from numpy import array
from geom.line import Line

CANVAS_MULT = 1 / 64.0
# CANVAS_SQUARE_SIZE = noise_density * CANVAS_MULT

canvas._setup()
# canvas.begin_plotting(debug=True)
canvas.clear([1, 1, 1, 1])
canvas.set_range(-1, 1)
canvas.set_color([0, 0, 0, 1])

canvas.set_line_depth(0.1)

for y in range(noise_density):
    for x in range(noise_density):
        a = array((x, y)) * CANVAS_MULT # space out for display
        a = a * 2 - 1
        b = a + flow_field[x][y] * CANVAS_MULT * 2
        line = Line(a, b)
        line.draw(canvas)

canvas._ctx
# %%
