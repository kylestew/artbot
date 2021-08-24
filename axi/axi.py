import sys
import time

from pyaxidraw import axidraw


class Axi:
    def __init__(self):
        self.ad = axidraw.AxiDraw()

        self.port_pin = 4  # Logical pin RP4 drives the output labeled "B1", from

        self.pen_is_up = False
        self.pen_up_percent = 75  # Percent height that we will use for pen up
        self.pen_down_percent = 25  # Percent height that we will use for pen down
        self.setup_servo_range()

    def connect(self):
        self.ad.interactive()
        connected = self.ad.connect()
        if not connected:
            sys.exit()

    def disconnect(self):
        self.ad.disconnect()

    def setup_servo_range(self):
        # Lowest allowed position; "0%" on the scale. Default value: 10800 units, or 0.818 ms.
        servo_min = self.ad.params.servo_min
        # Highest allowed position; "100%" on the scale. Default value: 25200 units, or 2.31 ms.
        servo_max = self.ad.params.servo_max
        servo_range = servo_max - servo_min
        pen_up_pos = int(self.pen_up_percent * servo_range / 100 + servo_min)
        pen_down_pos = int(self.pen_down_percent * servo_range / 100 + servo_min)

    def set_pen_depth_range(self):
        # calibrate pen to a height where the top of range is just touching paper
        # and bottom is a fully applied stroke width
        pass

    def send_command(self):
        # docs at: http://evil-mad.github.io/EggBot/ebb.html#S2
        # command = "S2," + str(position) + "," + str(port_pin) + "\r"

        # # Optional debug statements:
        # if pen_is_up:
        #     print("Raising pen")
        # else:
        #     print("Lowering pen")
        # print("New servo position: " + str(position))
        # print("command: " + command)

        # ad.usb_command(command + "\r")

        # time.sleep(wait_time_s)
        pass

    def pen_up(self):
        pass


# TODO:
# need to set a pen depth for just touching and for lowest
# also a raised position for travel

# axi = Axi()
# axi.connect()


# except KeyboardInterrupt:
# axi.disconnect()
