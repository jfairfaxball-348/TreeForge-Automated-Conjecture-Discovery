from types import SimpleNamespace

from treeforge.conjecturing.txgraffiti_adapter import TxGraffitiAdapter


class Playground:
    def __init__(self, dataframe, object_symbol):
        self.dataframe = dataframe
        self.object_symbol = object_symbol
        self.conjectures = ["raw"]
        self.kwargs = None

    def discover(self, **kwargs):
        self.kwargs = kwargs

    def forall(self, conjecture):
        return f"forall {self.object_symbol}: {conjecture}"


def test_adapter_isolates_current_api_surface():
    modules = {
        "txgraffiti.playground": SimpleNamespace(ConjecturePlayground=Playground),
        "txgraffiti.generators": SimpleNamespace(convex_hull=object(), ratios=object()),
        "txgraffiti.heuristics": SimpleNamespace(morgan_accept=object(), dalmatian_accept=object()),
        "txgraffiti.processing": SimpleNamespace(remove_duplicates=object(), sort_by_touch_count=object()),
    }
    adapter = TxGraffitiAdapter(loader=modules.__getitem__)
    result = adapter.discover([{"order": 2}], target="edge_count", features=["order"])
    assert len(result) == 1
    assert result[0].engine == "TxGraffiti"
    assert result[0].engine_version == "0.4.1"
