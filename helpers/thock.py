from numpy import linspace, random
from scipy import interpolate


def random_thock(wiggles=6):
    x_points = linspace(0, 1, num=wiggles)
    y_points = random.rand(wiggles)
    tck = interpolate.splrep(x_points, y_points)

    def f(x):
        return interpolate.splev(x, tck)

    return f


def shaped_thock(shape):
    x_points = linspace(0, 1, num=len(shape))
    tck = interpolate.splrep(x_points, shape)

    def f(x):
        return interpolate.splev(x, tck)

    return f


def apply_thock_to_line(line, thock, complexity):
    splits = linspace(0, 1, complexity + 1, endpoint=False)[1:]
    segs = line.shatter(splits)
    thock_lines = []
    for seg_info in zip(splits, segs):
        perc, segment = seg_info
        thock_lines.append((segment, thock(perc)))
    return thock_lines
