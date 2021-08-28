import cairo
from numpy import pi


"""
AxiDraw V3 - A4 (297 × 210 mm)
"""


def _setup(width=297, height=210, dpmm=4):
    global _w, _h, _dpmm, _sur, _ctx
    # physical width/height in mm
    _w = width * dpmm
    _h = height * dpmm
    _dpmm = dpmm  # needed for plotting
    _sur = cairo.ImageSurface(cairo.FORMAT_ARGB32, _w, _h)
    _ctx = cairo.Context(_sur)


def set_range(r0, r1):
    global _min_x, _max_x, _min_y, _max_y, _one

    small_side = 0
    xoff = 0
    yoff = 0
    if _w > _h:
        small_side = _h
        xoff = (_w - _h) / 2
    else:
        small_side = _w
        yoff = (_h - _w) / 2

    xscale = small_side / (r1 - r0)
    yscale = small_side / (r1 - r0)

    _ctx.translate(xoff, -yoff)
    _ctx.scale(xscale, -yscale)
    _ctx.translate(-r0, -r1)

    _min_x = ((0 - xoff) / xscale) + r0
    _max_x = ((_w - xoff) / xscale) + r0
    _min_y = ((0 - yoff) / yscale) + r0
    _max_y = ((_h - yoff) / yscale) + r0

    _one = 1.0 / xscale


def clear(c):
    _ctx.set_source_rgba(*c)
    _ctx.rectangle(0, 0, _w, _h)
    _ctx.fill()


def set_color(c):
    _ctx.set_source_rgba(*c)


def set_line_width(width):
    _ctx.set_line_width(_one * width)


def line(x0, y0, x1, y1):
    _ctx.move_to(x0, y0)
    _ctx.line_to(x1, y1)
    _ctx.stroke()


def circle(x, y, r, fill=False):
    _ctx.arc(x, y, r, 0, 2 * pi)
    if fill:
        _ctx.fill()
    else:
        _ctx.stroke()
