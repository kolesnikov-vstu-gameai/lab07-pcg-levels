"""Валидатор проходимости: BFS от старта; финиш — самая дальняя достижимая клетка."""

from collections import deque

import numpy as np

from . import FLOOR


def reachable(grid: np.ndarray, start: tuple) -> tuple[np.ndarray, dict]:
    h, w = grid.shape
    dist = np.full((h, w), -1, dtype=np.int32)
    q = deque([start])
    dist[start] = 0
    while q:
        y, x = q.popleft()
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            ny, nx = y + dy, x + dx
            if 0 <= ny < h and 0 <= nx < w and grid[ny, nx] == FLOOR and dist[ny, nx] < 0:
                dist[ny, nx] = dist[y, x] + 1
                q.append((ny, nx))
    floor = int((grid == FLOOR).sum())
    reached = int((dist >= 0).sum())
    far = np.unravel_index(dist.argmax(), dist.shape)
    return dist, {"floor_cells": floor, "reached": reached, "reach_ratio": reached / max(1, floor),
                  "finish": tuple(int(v) for v in far), "path_len": int(dist.max())}


def pick_start(grid: np.ndarray) -> tuple:
    ys, xs = np.where(grid == FLOOR)
    return (int(ys[0]), int(xs[0]))


def is_playable(grid: np.ndarray, min_reach=0.6, min_path=20) -> bool:
    if (grid == FLOOR).sum() == 0:
        return False
    _, m = reachable(grid, pick_start(grid))
    return m["reach_ratio"] >= min_reach and m["path_len"] >= min_path
