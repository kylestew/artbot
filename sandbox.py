import sys
import time

from pyaxidraw import axidraw

axi = axidraw.AxiDraw()
axi.interactive()
connected = axi.connect()
if not connected:
    sys.exit()

# NOTE: down is up!
axi.options.pen_pos_down = 40
axi.options.pen_pos_up = 90
axi.options.pen_rate_lower = 12
axi.options.pen_rate_raise = 12
axi.options.units = 1  # working units in cm
axi.update()

time.sleep(0.5)

# put pen in raised position
axi.pendown()
print("pen is fully up")

time.sleep(0.5)

# put pen in lowered position
axi.penup()
input("pen is fully lowered, check gear meshing")

# move into place
pos_x = 2
pos_y = 2
axi.lineto(pos_x, 2)
print(axi.current_pos())

# draw line varying height during draw
axi.moveto(pos_x + 10, pos_y)


# import time

# time.sleep(1.0)
# axi.pendown()
# time.sleep(1.0)
# axi.penup()

# disable motors
axi.plot_setup()
axi.options.mode = "manual"
axi.options.manual_cmd = "disable_xy"
axi.plot_run()

axi.disconnect()
