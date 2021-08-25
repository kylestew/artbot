import sys
import time

from pyaxidraw import axidraw


class Axi:
    def __init__(self):
        self.ad = axidraw.AxiDraw()

        self.port_pin = 4  # Logical pin RP4 drives the output labeled "B1", from

        self.pen_is_up = False
        self.pen_up_percent = 90
        self.pen_down_percent = 20
        self.setup_servo_range()
        self.set_pen_depth_range(0.1, 0.9)

    def connect(self):
        self.ad.interactive()
        connected = self.ad.connect()
        if not connected:
            sys.exit()

    def disconnect(self):
        self.ad.disconnect()

    def setup_servo_range(self):
        # highest point the pen can be raised
        servo_min = self.ad.params.servo_min
        # lowest point the pen can be lowered to
        servo_max = self.ad.params.servo_max
        servo_range = servo_max - servo_min
        # servo operation is reversed
        print("servo pushes pen down - min rotation is pen up position")
        print("servo range: [", servo_min, servo_max, "]", servo_range)
        self.pen_fully_down_pos = int(
            self.pen_up_percent * servo_range / 100 + servo_min
        )
        self.pen_fully_up_pos = int(
            self.pen_down_percent * servo_range / 100 + servo_min
        )
        print("pen up (servo min):", self.pen_fully_up_pos)
        print("pen down (servo max):", self.pen_fully_down_pos)

    def set_pen_depth_range(self, min, max):
        """
        Set depth range relative to max servo range
        (becomes subrange or trimmed servo range)
        """
        self.pen_min_depth = (
            min * (self.pen_fully_down_pos - self.pen_fully_up_pos)
            + self.pen_fully_up_pos
        )
        self.pen_max_depth = (
            max * (self.pen_fully_down_pos - self.pen_fully_up_pos)
            + self.pen_fully_up_pos
        )
        print(
            "depth range: [",
            self.pen_min_depth,
            self.pen_max_depth,
            "]",
            "(",
            self.pen_fully_up_pos,
            self.pen_fully_down_pos,
            ")",
        )

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

    def set_pen_up(self):
        """Not touching paper - for traveling"""
        self.pen_is_up = True
        self.pen_position = self.pen_fully_up_pos
        print("pen pos", self.pen_position)
        # TODO: send command

    def set_pen_depth(self, depth):
        """
        Uses extents set in calibration
        """
        self.pen_is_up = False
        depth = min(max(depth, 0.0), 1.0)

        self.pen_position = (
            depth * (self.pen_max_depth - self.pen_min_depth) + self.pen_min_depth
        )

        print("pen pos", self.pen_position)
        # TODO: send command


# TODO:
# need to set a pen depth for just touching and for lowest
# also a raised position for travel

# axi = Axi()
# axi.connect()


# except KeyboardInterrupt:
# axi.disconnect()
