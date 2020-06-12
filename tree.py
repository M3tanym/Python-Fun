# adapted from https://github.com/neozhaoliang/pywonderland :)
# Thanks for being smort @Max
# python 3

import numpy as np
import cairo
from PIL import Image

ITERATIONS = 16  # total number of iterations
ROOT_COLOR = np.array([0.0, 0.0, 0.0])  # root branch color

#LEAF_COLOR = np.array([1.0, 1.0, 0.2])  # leaf color
#LEAF_COLOR = np.array([1.0, 0.3, 0.7])  # leaf color
#LEAF_COLOR = np.array([0.3, 0.6, 1.0])  # leaf color
def r():
    return 0.1 + np.random.random()
LEAF_COLOR = np.array([r(), r(), r()])
print(LEAF_COLOR)

TRUNK_LEN = 550  # initial length of the trunk
TRUNK_RAD = 6.5  # initial radius of the trunk
THETA = np.pi / 2  # initial angle of the branch
ANGLE = np.pi / 4.5  # angle between branches in the same level
PERTURB = 6.0  # perturb the angle a little to make the tree look random
RATIO = 0.8  # contraction factor between successive trunks
WIDTH = 3000  # image width
HEIGHT = 2000  # image height
ROOT = (WIDTH / 2.0, HEIGHT + 50)  # pixel position of the root

branches = []

def cairo_to_pil( surface ):
    pilMode = 'RGB'
    argbArray = np.frombuffer(bytes(surface.get_data()), 'c').reshape( -1, 4 )
    rgbArray = argbArray[:, 2::-1]
    pilData = rgbArray.reshape(-1).tostring()
    pilImage = Image.frombuffer(pilMode,
         (surface.get_width(), surface.get_height()), pilData, 'raw',
         pilMode, 0, 1)
    pilImage = pilImage.convert(pilMode)

    return pilImage

def get_color(level):
    """
    Return an interpolation of the two colors `ROOT_COLOR` and `LEAF_COLOR`.
    """
    a = float(level) / ITERATIONS
    return a * ROOT_COLOR + (1 - a) * LEAF_COLOR


def get_line_width(level):
    """Return the line width of a given level."""
    return max(1, TRUNK_RAD * level / ITERATIONS)


def fractal_tree(level,       # current level in the iterations
                 start,       # (x, y) coordinates of the start of this trunk
                 t,           # current trunk length
                 r,           # factor to contract the trunk in each iteration
                 theta,       # orientation of current trunk
                 angle,       # angle between branches in the same level
                 perturb,     # perturb the angle
                 ):

    if level == 0:
        return

    x0, y0 = start
    # randomize the length
    randt = np.random.random() * t
    x, y = x0 + randt * np.cos(theta), y0 - randt * np.sin(theta)

    branches.append((level, start, (x, y)))

    theta1 = theta + np.random.random() * (perturb / level) * angle
    theta2 = theta - np.random.random() * (perturb / level) * angle
    # recursively draw the next branches
    fractal_tree(level - 1, (x, y), t * r, r, theta1, angle, perturb)
    fractal_tree(level - 1, (x, y), t * r, r, theta2, angle, perturb)


def main():

    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
    ctx = cairo.Context(surface)
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    ctx.set_line_join(cairo.LINE_JOIN_ROUND)
    ctx.set_source_rgb(1, 1, 1)
    ctx.paint()
    fractal_tree(ITERATIONS, ROOT, TRUNK_LEN, RATIO, THETA, ANGLE, PERTURB)

    branches.sort(key=lambda x: -x[0])

    cur = ITERATIONS
    images = []

    for b in branches:
        ctx.move_to(*b[1])
        ctx.line_to(*b[2])
        ctx.set_line_width(get_line_width(b[0]))
        ctx.set_source_rgb(*get_color(b[0]))
        ctx.stroke()

        if b[0] != cur:
            images.append(cairo_to_pil(surface))
            cur = b[0]

    s = cairo_to_pil(surface)
    for i in range(3):
        images.append(s)

    surface.write_to_png('tree.png')
    images[0].save('tree.gif', save_all=True, append_images=images[1:],
                   duration=100, loop=1)


if __name__ == '__main__':
    main()
