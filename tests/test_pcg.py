import numpy as np

from pcg import bsp, cellular
from pcg.validator import is_playable


def test_determinism():
    assert np.array_equal(bsp.generate(seed=7), bsp.generate(seed=7))
    assert not np.array_equal(bsp.generate(seed=7), bsp.generate(seed=8))
    assert np.array_equal(cellular.generate(seed=3), cellular.generate(seed=3))


def test_bsp_playable_mostly():
    ok = sum(is_playable(bsp.generate(seed=s)) for s in range(20))
    assert ok >= 15
