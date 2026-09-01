"""BSP-генератор: рекурсивное деление, комнаты в листьях, коридоры между соседями."""

import random
from dataclasses import dataclass

import numpy as np

from . import FLOOR, WALL


@dataclass
class Leaf:
    x: int
    y: int
    w: int
    h: int
    left: "Leaf | None" = None
    right: "Leaf | None" = None
    room: tuple | None = None

    def split(self, rng: random.Random, min_size: int) -> bool:
        if self.left or self.right:
            return False
        horizontal = rng.random() < 0.5 if abs(self.w - self.h) < 4 else self.w < self.h
        limit = (self.h if horizontal else self.w) - min_size
        if limit < min_size:
            return False
        cut = rng.randint(min_size, limit)
        if horizontal:
            self.left, self.right = Leaf(self.x, self.y, self.w, cut), Leaf(self.x, self.y + cut, self.w, self.h - cut)
        else:
            self.left, self.right = Leaf(self.x, self.y, cut, self.h), Leaf(self.x + cut, self.y, self.w - cut, self.h)
        return True


def generate(width=64, height=48, seed=0, min_leaf=10, depth=5) -> np.ndarray:
    rng = random.Random(seed)
    grid = np.full((height, width), WALL, dtype=np.int8)
    root = Leaf(0, 0, width, height)
    leaves = [root]
    for _ in range(depth):
        for leaf in list(leaves):
            if leaf.split(rng, min_leaf):
                leaves.remove(leaf)
                leaves += [leaf.left, leaf.right]

    def carve_room(leaf: Leaf):
        rw, rh = rng.randint(4, max(4, leaf.w - 2)), rng.randint(4, max(4, leaf.h - 2))
        rx, ry = leaf.x + rng.randint(1, max(1, leaf.w - rw - 1)), leaf.y + rng.randint(1, max(1, leaf.h - rh - 1))
        grid[ry:ry + rh, rx:rx + rw] = FLOOR
        leaf.room = (rx + rw // 2, ry + rh // 2)

    def connect(a: tuple, b: tuple):
        (x1, y1), (x2, y2) = a, b
        grid[y1, min(x1, x2):max(x1, x2) + 1] = FLOOR
        grid[min(y1, y2):max(y1, y2) + 1, x2] = FLOOR

    def center(leaf: Leaf) -> tuple:
        if leaf.room:
            return leaf.room
        c = center(leaf.left) if leaf.left else center(leaf.right)
        return c

    def walk(leaf: Leaf):
        if leaf.left and leaf.right:
            walk(leaf.left)
            walk(leaf.right)
            connect(center(leaf.left), center(leaf.right))
        else:
            carve_room(leaf)

    walk(root)
    return grid
