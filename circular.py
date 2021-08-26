import time
import math
import numpy
from axi import axi

axi = axi.Axi()
axi.connect()
axi.set_pen_up()

time.sleep(0.5)

# workspace: 18 x 18 cm
center = [9, 9]
axi.goto(center[0], center[1])
spirals = 6
sweeps = 800
thetas = numpy.linspace(0, spirals * 2 * math.pi, num=sweeps)
rad = 0
for theta in thetas:
    x = math.sin(theta) * rad + center[0]
    y = math.cos(theta) * rad + center[1]
    rad += 0.01
    depth = math.sin(1.6 * theta) * 0.5 + 0.5
    axi.set_pen_depth(depth)
    axi.goto(x, y)

axi.set_pen_up()
time.sleep(1)
axi.goto(0, 0)
axi.disconnect()
