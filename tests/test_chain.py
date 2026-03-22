"""Tests for chain modules (offline — no actual chain calls)."""

import sys
import json
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from agent.memory import AgentState, save_state, load_state, hash_prompt, append_to_agent_log


def test_agent_state_serialization():
    state = AgentState(
        iteration=5,
        current_prompt="test prompt",
        best_accuracy=0.85,
        best_prompt="best prompt",
        accuracy_history=[0.5, 0.6, 0.7, 0.8, 0.85],
    )
    d = state.to_dict()
    assert d["iteration"] == 5
    assert d["best_accuracy"] == 0.85

    restored = AgentState.from_dict(d)
    assert restored.iteration == 5
    assert restored.best_accuracy == 0.85
    assert len(restored.accuracy_history) == 5


def test_save_load_state():
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
        path = f.name

    state = AgentState(iteration=10, current_prompt="hello", best_accuracy=0.9)
    save_state(state, path)

    loaded = load_state(path)
    assert loaded.iteration == 10
    assert loaded.current_prompt == "hello"
    assert loaded.best_accuracy == 0.9

    Path(path).unlink()


def test_hash_prompt():
    h1 = hash_prompt("test prompt 1")
    h2 = hash_prompt("test prompt 2")
    h3 = hash_prompt("test prompt 1")
    assert h1 == h3  # Same input = same hash
    assert h1 != h2  # Different input = different hash
    assert len(h1) == 16  # Truncated to 16 chars


def test_append_to_agent_log():
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
        path = f.name

    # Write empty list first
    with open(path, "w") as f:
        json.dump([], f)

    entry1 = {"iteration": 0, "accuracy": 0.5}
    entry2 = {"iteration": 1, "accuracy": 0.6}

    append_to_agent_log(entry1, path)
    append_to_agent_log(entry2, path)

    with open(path) as f:
        logs = json.load(f)

    assert len(logs) == 2
    assert logs[0]["accuracy"] == 0.5
    assert logs[1]["accuracy"] == 0.6

    Path(path).unlink()


def test_filecoin_local_fallback():
    """Test that Filecoin storage falls back to local when no API key."""
    from chain.filecoin import store_iteration_log, LOCAL_STORAGE_DIR

    log_entry = {"iteration": 999, "accuracy": 0.99, "test": True}
    cid = store_iteration_log(log_entry)
    assert cid.startswith("local:")

    # Cleanup
    test_file = LOCAL_STORAGE_DIR / "iteration_0999.json"
    if test_file.exists():
        test_file.unlink()


if __name__ == "__main__":
    test_agent_state_serialization()
    test_save_load_state()
    test_hash_prompt()
    test_append_to_agent_log()
    test_filecoin_local_fallback()
    print("All chain tests passed!")
