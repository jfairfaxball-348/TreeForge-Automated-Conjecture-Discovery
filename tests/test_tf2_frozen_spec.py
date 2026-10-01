from pathlib import Path

from treeforge.experiments import load_frozen_spec


def test_tf2_frozen_spec_keeps_burned_order_out_of_split():
    spec = load_frozen_spec(Path("experiments/TF2-0001/spec.json"))
    assert spec["experiment_id"] == "TF2-0001"
    assert spec["discovery_orders"] == [2, 10]
    assert spec["burned_orders_excluded"] == [11]
    assert spec["holdout_orders"] == [12, 12]
    assert spec["expected_discovery_tree_count"] == 200
    assert spec["expected_holdout_tree_count"] == 551
    assert spec["target"] == "domination_number"
    assert spec["txgraffiti"]["methods"] == ["convex_hull", "ratios"]
    assert spec["txgraffiti"]["hypothesis_payload"] == []
