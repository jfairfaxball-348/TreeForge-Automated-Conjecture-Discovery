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
