import sys
import time
import json

from pyaxidraw import axidraw


class Axi:
    def __init__(self):
        self.ad = axidraw.AxiDraw()

        self.port_pin = 4  # Logical pin RP4 drives the output labeled "B1", from

        self.pen_is_up = False
        self.pen_up_percent = 98
        self.pen_down_percent = 10
        self.setup_servo_range()
        self.load_pen_depth()

    def connect(self):
        self.ad.interactive()
        connected = self.ad.connect()
        if not connected:
            sys.exit()
        self.set_options()

    def set_options(self):
        axi = self.ad
        axi.options.units = 2  # mm
        axi.options.speed_pendown = 10
        axi.options.speed_penup = 10
        axi.update()

    def disconnect(self):
        # unlock motors
        self.ad.plot_setup()
        self.ad.options.mode = "manual"
        self.ad.options.manual_cmd = "disable_xy"
        self.ad.plot_run()
        self.ad.disconnect()

    def setup_servo_range(self):
        # highest point the pen can be raised
        servo_min = self.ad.params.servo_min
        # lowest point the pen can be lowered to
        servo_max = self.ad.params.servo_max
        servo_range = servo_max - servo_min
        # servo operation is reversed
        # print("servo pushes pen down - min rotation is pen up position")
        # print("servo range: [", servo_min, servo_max, "]", servo_range)
        self.pen_fully_down_pos = int(
            self.pen_up_percent * servo_range / 100 + servo_min
        )
        self.pen_fully_up_pos = int(
            self.pen_down_percent * servo_range / 100 + servo_min
        )
        print("pen up (servo min):", self.pen_fully_up_pos)
        print("pen down (servo max):", self.pen_fully_down_pos)

    def load_pen_depth(self):
        try:
            with open("config.json", "r") as f:
                config = json.load(f)

            self.set_pen_depth_range(
                config["pen_depth_range_min"], config["pen_depth_range_max"]
            )

        except:
            self.set_pen_depth_range(0.1, 0.3)

    def save_pen_depth(self):
        config = {
            "pen_depth_range_min": self.pen_depth_range[0],
            "pen_depth_range_max": self.pen_depth_range[1],
        }
        with open("config.json", "w") as f:
            json.dump(config, f)

    def set_pen_depth_range(self, min_depth, max_depth):
        """
        Set depth range relative to max servo range
        (becomes subrange or trimmed servo range)
        """

        # ensure max is greater than or equal to min
        max_depth = max(max_depth, min_depth)

        self.pen_depth_range = [min_depth, max_depth]
        self.pen_min_depth = (
            min_depth * (self.pen_fully_down_pos - self.pen_fully_up_pos)
            + self.pen_fully_up_pos
        )
        self.pen_max_depth = (
            max_depth * (self.pen_fully_down_pos - self.pen_fully_up_pos)
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
        self.save_pen_depth()

    def send_pen_pos(self):
        command = "S2," + str(int(self.pen_position)) + "," + str(self.port_pin) + "\r"
        print(command)
        self.ad.usb_command(command + "\r")

    def set_pen_up(self):
        """Not touching paper - for traveling"""
        self.pen_is_up = True
        self.pen_position = self.pen_fully_up_pos
        self.send_pen_pos()

    def set_pen_down(self):
        """
        For attaching gear rack
        """
        self.pen_is_up = False
        self.pen_position = self.pen_fully_down_pos
        self.send_pen_pos()

    def set_pen_depth(self, depth):
        """
        Uses extents set in calibration
        """
        self.pen_is_up = False
        depth = min(max(depth, 0.0), 1.0)
        self.pen_position = (
            depth * (self.pen_max_depth - self.pen_min_depth) + self.pen_min_depth
        )
        self.send_pen_pos()

    def current_pos(self):
        return self.ad.current_pos()

    def goto(self, xpos, ypos):
        print("goto:", xpos, ypos)
        self.ad.goto(xpos, ypos)
