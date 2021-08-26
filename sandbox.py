import time
import math
import numpy
from axi import axi

axi = axi.Axi()
axi.connect()
axi.set_pen_up()

time.sleep(0.5)

num = 100
space = 20 / num
thetas = numpy.linspace(0, 5 * math.pi, num=num)
x_off = 0
for theta in thetas:
    depth = math.sin(theta) * 0.5 + 0.5
    axi.set_pen_depth(depth)
    axi.goto(x_off, 0)
    x_off += space
    # time.sleep(0.01)

axi.set_pen_up()
time.sleep(1)
axi.goto(0, 0)
axi.disconnect()
