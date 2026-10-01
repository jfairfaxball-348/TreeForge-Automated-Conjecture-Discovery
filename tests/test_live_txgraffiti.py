import importlib.util

import pytest

from treeforge.conjecturing.txgraffiti_adapter import TxGraffitiAdapter


def test_live_txgraffiti_optional_api_surface():
    if importlib.util.find_spec("txgraffiti") is None:
        pytest.skip("optional txgraffiti dependency not installed")

    import pandas as pd
    from txgraffiti.generators import convex_hull, ratios
    from txgraffiti.heuristics import dalmatian_accept, morgan_accept
    from txgraffiti.playground import ConjecturePlayground
    from txgraffiti.processing import remove_duplicates, sort_by_touch_count

    assert ConjecturePlayground is not None
    assert all(callable(item) for item in [convex_hull, ratios, dalmatian_accept, morgan_accept])
    assert all(callable(item) for item in [remove_duplicates, sort_by_touch_count])

    # Exercise the same public API through TreeForge's adapter.  The content is
    # calibration-only: we assert compatibility, not that TxGraffiti must emit
    # a particular conjecture or ordering.
    frame = pd.DataFrame(
        {
            "order": [2, 3, 4, 5, 6],
            "edge_count": [1, 2, 3, 4, 5],
        }
    )
    result = TxGraffitiAdapter().discover(frame, target="edge_count", features=["order"])
    assert isinstance(result, list)
