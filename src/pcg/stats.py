import argparse
import time

import pandas as pd

from . import FLOOR, bsp, cellular
from .validator import is_playable, pick_start, reachable

GENS = {"bsp": bsp.generate, "ca": cellular.generate}


def run(gen: str, n: int) -> pd.DataFrame:
    rows = []
    for seed in range(n):
        t = time.perf_counter()
        g = GENS[gen](seed=seed)
        dt = time.perf_counter() - t
        _, m = reachable(g, pick_start(g))
        rows.append({"seed": seed, "gen_ms": dt * 1000, "floor_ratio": float((g == FLOOR).mean()), **m,
                     "playable": is_playable(g)})
    return pd.DataFrame(rows)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--gen", choices=GENS, default="bsp")
    ap.add_argument("--n", type=int, default=100)
    a = ap.parse_args()
    df = run(a.gen, a.n)
    from pathlib import Path

    out = Path(__file__).resolve().parents[2] / "results"
    out.mkdir(exist_ok=True)
    df.to_csv(out / f"stats_{a.gen}.csv", index=False)
    print(df.describe().T[["mean", "std", "min", "max"]])
    print(f"playable: {df.playable.mean():.0%}")
