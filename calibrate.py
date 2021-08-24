#!/usr/bin/env python

#%%

usage = """
Mouse Controls
==============
- 1st button on mouse (left click) to toggle events 'grabed'.
- 3rd button on mouse (right click) to toggle mouse visible.
- The window can be resized.
- Mouse the mouse around to see mouse events.
- If events grabbed and mouse invisible show virtual mouse coords.
Keyboard Joystick Controls
==========================
- press keys up an down to see events.
- you can see joystick events if any are plugged in.
- press "c" to toggle events generated by controllers.
"""

import pygame as pg


def main():
    pg.init()
    print(usage)

    running = True
    while running:
        for e in pg.event.get():
            print(e.type)

        pg.time.wait(10)


if __name__ == "__main__":
    main()
