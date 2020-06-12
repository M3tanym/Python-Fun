import numpy as np
import cairo

def rd(d):
    return int((0.5 - (2 * np.random.random())) * d)

def draw_leaf(ctx):
    dx = rd(50)
    dy = rd(50)

    ddx = rd(10)
    stem_curve = rd(20)

    stem_base = (250 + ddx, 490)
    stem_a = (250 + ddx + stem_curve, 485)
    stem_b = (250 + dx + (stem_curve*5), 420 + dy)


    leaf_base = (200 + dx, 400 + dy)
    leaf_a = (100 + dx + rd(10), 300 + dy + rd(10))
    leaf_b = (100 + dx + rd(10), 200 + dy + rd(10))
    leaf_c = (300 + dx + rd(10), 300 + dy + rd(10))
    leaf_d = (400 + dx + rd(10), 200 + dy + rd(10))
    leaf_top = (100, 10)

    ctx.move_to(*stem_base)
    ctx.curve_to(*stem_a, *stem_b, *leaf_base)
    ctx.line_to(*leaf_top)
    ctx.set_line_width(3)
    ctx.set_source_rgb(0.6, 0.99, 0.7)
    ctx.stroke()

    ctx.move_to(*leaf_base)
    ctx.curve_to(*leaf_a, *leaf_b, *leaf_top)
    ctx.move_to(*leaf_base)
    ctx.curve_to(*leaf_c, *leaf_d, *leaf_top)
    ctx.set_line_width(2)
    ctx.set_source_rgb(0.5, 0.9, 0.6)
    ctx.stroke()


def main():
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 500, 500)
    ctx = cairo.Context(surface)
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    ctx.set_line_join(cairo.LINE_JOIN_ROUND)
    ctx.set_source_rgb(1, 1, 1)
    ctx.paint()
    draw_leaf(ctx)
    surface.write_to_png('leaf.png')


if __name__ == '__main__':
    main()
