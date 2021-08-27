#!/usr/bin/env python

import pygame as pg
from axi import axi


class Calibration:
    """
    4 step process

    1) Attach
    2) Set travel (top)
    3) Set upper limit (thin stroke)
    4) Set lower limit (fat stroke)
    """

    def __init__(self):
        self.axi = axi.Axi()
        self.axi.connect()
        self.calibration_bump = 0.004
        self.restart()
        self.preview_y_offset = 0
        self.preview_y_dir = 1

    def restart(self):
        self.step = 0
        self.axi.set_pen_down()

    def end(self):
        self.axi.disconnect()

    def step_instructions(self):
        if self.step == 0:
            return [
                "STEP 0:",
                "At bottom position",
                "Attach gear rack (if not attached)",
                "As close to metal mounting block as possible",
                "[DELETE to reset range]",
                "| next ->",
            ]
        if self.step == 1:
            return [
                "STEP 1:",
                "At top position",
                "Attach marker at travel height",
                "It should clear paper (not leave a mark)",
                "<- prev | next ->",
            ]
        if self.step == 2:
            return [
                "STEP 2:",
                "Set min pen depth (highest drawing point)",
                "Lower tip until it draws a THIN line",
                "[up/down arrows, space to test line]",
                "<- prev | next ->",
            ]
        else:
            return [
                "STEP 3:",
                "Set max pen depth (lowest drawing point)",
                "Lower tip until it draws a THICK line",
                "(careful not to hit the end of range)",
                "[up/down arrows, space to test line]",
                "<- prev |",
            ]

    def input_enter(self):
        if self.step == 0:
            self.step = 1
            self.axi.set_pen_up()
        elif self.step == 1:
            self.step = 2
            self.axi.set_pen_depth(0.0)
        elif self.step == 2:
            self.step = 3
            self.axi.set_pen_depth(1.0)

    def input_left_arrow(self):
        if self.step == 2:
            self.step = 1
            self.axi.set_pen_up()
        elif self.step == 3:
            self.step = 2
            self.axi.set_pen_depth(0.0)
        elif self.step == 4:
            self.step = 3
            self.axi.set_pen_depth(1.0)
        else:
            self.step = 0
            self.axi.set_pen_down()

    def input_right_arrow(self):
        self.input_enter()

    def input_down(self):
        range = self.axi.pen_depth_range
        if self.step == 2:
            range[0] = range[0] + self.calibration_bump
        elif self.step == 3:
            range[1] = range[1] + self.calibration_bump
        else:
            return
        self.axi.set_pen_depth_range(range[0], range[1])
        self.axi.set_pen_depth(0.0 if self.step == 2 else 1.0)

    def input_up(self):
        range = self.axi.pen_depth_range
        if self.step == 2:
            range[0] = range[0] - self.calibration_bump
        elif self.step == 3:
            range[1] = range[1] - self.calibration_bump
        else:
            return
        self.axi.set_pen_depth_range(range[0], range[1])
        self.axi.set_pen_depth(0.0 if self.step == 2 else 1.0)

    def input_delete(self):
        self.axi.set_pen_depth_range(0.5, 0.75)
        self.restart()

    def input_space(self):
        """
        Does calibration lines like Prusa printers
        """
        move = self.preview_y_dir * 10
        self.axi.goto(move, self.preview_y_offset)
        self.preview_y_offset += 2
        self.axi.goto(move, self.preview_y_offset)
        self.preview_y_dir = -self.preview_y_dir

    def draw_status(self, win):
        bgcolor = 50, 50, 50
        xpad = 20

        win.fill(bgcolor, (0, 0, win.get_width(), win.get_height()))

        # instructional text
        ypos = xpad
        for line in self.step_instructions():
            newpos = show_text(win, (xpad, ypos), line, (255, 255, 255), bgcolor)
            ypos = newpos[1]

        # range visual
        box_height = 40
        box_width = win.get_width() - xpad * 2
        box_x = xpad
        box_y = win.get_height() - xpad - box_height
        pg.draw.rect(win, (250, 250, 250), (box_x, box_y, box_width, box_height))

        # depth range
        range_box_y = box_y + 2
        range_box_height = box_height - 4
        range = self.axi.pen_depth_range
        range_box_x = box_x + range[0] * box_width
        range_box_width = (range[1] - range[0]) * box_width
        pg.draw.rect(
            win,
            (128, 100, 128),
            (range_box_x, range_box_y, range_box_width, range_box_height),
        )

        # current position
        perc = (self.axi.pen_position - self.axi.pen_fully_up_pos) / (
            self.axi.pen_fully_down_pos - self.axi.pen_fully_up_pos
        )
        box_x = xpad + box_width * perc - 3
        marker_box_width = 6
        pg.draw.rect(win, (190, 32, 64), (box_x, box_y, marker_box_width, box_height))


font = None


def show_text(win, pos, text, color, bgcolor):
    textimg = font.render(text, 1, color, bgcolor)
    win.blit(textimg, pos)
    return pos[0] + textimg.get_width() + 6, pos[1] + textimg.get_height() + 6


def main():
    pg.init()

    cali = Calibration()

    win = pg.display.set_mode((420, 300))
    pg.display.set_caption("3AxiDraw Calibration")

    global font
    font = pg.font.Font(None, 26)

    running = True
    while running:
        for e in pg.event.get():
            if e.type == pg.KEYDOWN:
                if e.key == pg.K_ESCAPE:
                    running = False
                elif e.key == pg.K_RETURN:
                    cali.input_enter()
                elif e.key == pg.K_RIGHT:
                    cali.input_right_arrow()
                elif e.key == pg.K_LEFT:
                    cali.input_left_arrow()
                elif e.key == pg.K_DELETE:
                    cali.input_delete()
                elif e.key == pg.K_BACKSPACE:
                    cali.input_delete()
                elif e.key == pg.K_DOWN:
                    cali.input_down()
                elif e.key == pg.K_UP:
                    cali.input_up()
                elif e.key == pg.K_SPACE:
                    cali.input_space()

            if e.type == pg.QUIT:
                running = False

        cali.draw_status(win)

        pg.display.flip()
        pg.time.wait(10)

    cali.end()

    pg.quit()
    raise SystemExit


if __name__ == "__main__":
    main()
