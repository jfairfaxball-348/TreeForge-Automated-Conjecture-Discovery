from types import SimpleNamespace

from treeforge.conjecturing.txgraffiti_adapter import TxGraffitiAdapter


class Playground:
    last_instance = None

    def __init__(self, dataframe, object_symbol):
        self.df = dataframe
        self.object_symbol = object_symbol
        self.conjectures = ["raw"]
        self.kwargs = None
        Playground.last_instance = self

    def discover(self, **kwargs):
        self.kwargs = kwargs

    def forall(self, conjecture):
        return f"forall {self.object_symbol}: {conjecture}"


def _modules():
    return {
        "txgraffiti.playground": SimpleNamespace(ConjecturePlayground=Playground),
        "txgraffiti.generators": SimpleNamespace(convex_hull=object(), ratios=object()),
        "txgraffiti.heuristics": SimpleNamespace(
            morgan_accept=object(), dalmatian_accept=object()
        ),
        "txgraffiti.processing": SimpleNamespace(
            remove_duplicates=object(), sort_by_touch_count=object()
        ),
    }


def test_adapter_isolates_current_api_surface():
    adapter = TxGraffitiAdapter(loader=_modules().__getitem__)
    result = adapter.discover(
        [{"order": 2}],
        target="edge_count",
        features=["order"],
        hypothesis=[],
    )
    assert len(result) == 1
    assert result[0].engine == "TxGraffiti"
    assert result[0].engine_version == "0.4.1"
    assert Playground.last_instance.kwargs["hypothesis"] is None


def test_cached_always_true_pipeline_matches_live_upstream():
    pd = __import__("pandas")
    pytest = __import__("pytest")
    pytest.importorskip("txgraffiti")

    from txgraffiti.generators import convex_hull, ratios
    from txgraffiti.heuristics import dalmatian_accept, morgan_accept
    from txgraffiti.playground import ConjecturePlayground
    from txgraffiti.processing import remove_duplicates, sort_by_touch_count

    frame = pd.DataFrame(
        {
            "x": [1, 2, 1, 2, 3, 1, 3, 2],
            "z": [1, 1, 2, 2, 1, 3, 2, 3],
            "y": [1, 3, 2, 5, 4, 6, 7, 5],
        }
    )

    upstream = ConjecturePlayground(frame, object_symbol="T")
    upstream.discover(
        methods=[convex_hull, ratios],
        features=["x", "z"],
        target="y",
        hypothesis=None,
        heuristics=[morgan_accept, dalmatian_accept],
        post_processors=[remove_duplicates, sort_by_touch_count],
    )
    expected = [str(upstream.forall(conjecture)) for conjecture in upstream.conjectures]

    adapter = TxGraffitiAdapter()
    actual = [
        item.statement
        for item in adapter.discover(
            frame,
            target="y",
            features=["x", "z"],
            object_symbol="T",
            hypothesis=[],
        )
    ]

    assert actual == expected
    assert adapter.last_stage_counts is not None
    assert adapter.last_stage_counts["final_discover_output"] == len(expected)


def test_adapter_can_restrict_generator_method_set():
    modules = _modules()
    adapter = TxGraffitiAdapter(loader=modules.__getitem__)
    adapter.discover(
        [{"order": 2}],
        target="edge_count",
        features=["order"],
        hypothesis=[],
        methods=["ratios"],
    )
    assert Playground.last_instance.kwargs["methods"] == [modules["txgraffiti.generators"].ratios]


def test_ratios_only_adapter_matches_live_upstream():
    pd = __import__("pandas")
    pytest = __import__("pytest")
    pytest.importorskip("txgraffiti")

    from txgraffiti.generators import ratios
    from txgraffiti.heuristics import dalmatian_accept, morgan_accept
    from txgraffiti.playground import ConjecturePlayground
    from txgraffiti.processing import remove_duplicates, sort_by_touch_count

    frame = pd.DataFrame(
        {
            "x": [1, 2, 1, 2, 3, 1, 3, 2],
            "z": [1, 1, 2, 2, 1, 3, 2, 3],
            "y": [1, 3, 2, 5, 4, 6, 7, 5],
        }
    )

    upstream = ConjecturePlayground(frame, object_symbol="T")
    upstream.discover(
        methods=[ratios],
        features=["x", "z"],
        target="y",
        hypothesis=None,
        heuristics=[morgan_accept, dalmatian_accept],
        post_processors=[remove_duplicates, sort_by_touch_count],
    )
    expected = [str(upstream.forall(conjecture)) for conjecture in upstream.conjectures]

    adapter = TxGraffitiAdapter()
    actual = [
        item.statement
        for item in adapter.discover(
            frame,
            target="y",
            features=["x", "z"],
            object_symbol="T",
            hypothesis=[],
            methods=["ratios"],
        )
    ]

    assert actual == expected
