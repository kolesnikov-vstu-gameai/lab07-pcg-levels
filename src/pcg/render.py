import argparse
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

from .stats import GENS  # noqa: E402

OUT = Path(__file__).resolve().parents[2] / "results" / "levels"

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--gen", choices=GENS, default="bsp")
    ap.add_argument("--seeds", type=int, default=10)
    a = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    for s in range(a.seeds):
        plt.figure(figsize=(6, 4.5))
        plt.imshow(GENS[a.gen](seed=s), cmap="gray_r")
        plt.title(f"{a.gen} seed={s}")
        plt.axis("off")
        plt.savefig(OUT / f"{a.gen}_{s}.png", dpi=120, bbox_inches="tight")
        plt.close()
    print("→", OUT)
