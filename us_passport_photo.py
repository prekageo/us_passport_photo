#!/usr/bin/env python3

import os.path
import sys
from PIL import Image, ImageDraw

class Box():
    def __init__(self, cx, cy, width, height):
        self.left = cx - width / 2
        self.right = cx + width / 2
        self.top = cy - height / 2
        self.bottom = cy + height / 2

def hline(draw, y, x1, x2, width, fill):
    draw.rectangle([(x1, y), (x2, y + width)], fill=fill)

def vline(draw, x, y1, y2, width, fill):
    draw.rectangle([(x, y1), (x + width, y2)], fill=fill)

def main():
    DPI = 300
    WIDTH = 6 * DPI
    HEIGHT = 4 * DPI
    PHOTO_WIDTH = 2 * DPI
    PHOTO_HEIGHT = 2 * DPI
    LINE_WIDTH = 2
    GAP = 20

    if len(sys.argv) < 4:
        print('Usage: %s left_pic right_pic outfile' % (sys.argv[0],), file=sys.stderr)
        sys.exit(1)

    left_pic = sys.argv[1]
    right_pic = sys.argv[2]
    outfile = sys.argv[3]
    if os.path.exists(outfile):
        print('File \'%s\' already exists. Not overwriting.' % outfile, file=sys.stderr)
        sys.exit(1)

    faces = [
        [sys.argv[1], WIDTH / 3 - PHOTO_WIDTH / 6, HEIGHT / 2],
        [sys.argv[2], 2 * WIDTH / 3 + PHOTO_WIDTH / 6, HEIGHT / 2],
    ]

    im = Image.new('RGB', (WIDTH, HEIGHT), (255, 255, 255))
    draw = ImageDraw.Draw(im)

    hline(draw, 0, 0, WIDTH - 1, LINE_WIDTH, 0)
    hline(draw, HEIGHT - 1, 0, WIDTH, -LINE_WIDTH, 0)
    vline(draw, 0, 0, HEIGHT - 1, LINE_WIDTH, 0)
    vline(draw, WIDTH - 1, 0, HEIGHT, -LINE_WIDTH, 0)

    for _, x, y in faces:
        box = Box(x, y, PHOTO_WIDTH, PHOTO_HEIGHT)
        hline(draw, box.top, 0, WIDTH, -LINE_WIDTH, 0)
        hline(draw, box.bottom, 0, WIDTH, LINE_WIDTH, 0)
        vline(draw, box.left, 0, HEIGHT, -LINE_WIDTH, 0)
        vline(draw, box.right, 0, HEIGHT, LINE_WIDTH, 0)

    for filename, x, y in faces:
        box = Box(x, y, PHOTO_WIDTH, PHOTO_HEIGHT)
        hline(draw, box.top, box.left - GAP, box.right + GAP, -LINE_WIDTH, fill=(255, 255, 255))
        hline(draw, box.bottom, box.left - GAP, box.right + GAP, LINE_WIDTH, fill=(255, 255, 255))
        vline(draw, box.left, box.top - GAP, box.bottom + GAP, -LINE_WIDTH, fill=(255, 255, 255))
        vline(draw, box.right, box.top - GAP, box.bottom + GAP, LINE_WIDTH, fill=(255, 255, 255))
        im.paste(Image.open(filename), (int(box.left), int(box.top)))

    im.save(outfile, dpi=(DPI, DPI))

if __name__ == '__main__':
    main()
