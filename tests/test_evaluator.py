"""Tests for the evaluator and scorer modules."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from eval.scorer import compute_accuracy, get_failures, get_confusion_matrix, load_ground_truth


def test_compute_accuracy_perfect():
    gt = {"a1": "trustworthy", "a2": "untrustworthy", "a3": "trustworthy"}
    preds = {"a1": "trustworthy", "a2": "untrustworthy", "a3": "trustworthy"}
    assert compute_accuracy(preds, gt) == 1.0


def test_compute_accuracy_zero():
    gt = {"a1": "trustworthy", "a2": "untrustworthy"}
    preds = {"a1": "untrustworthy", "a2": "trustworthy"}
    assert compute_accuracy(preds, gt) == 0.0


def test_compute_accuracy_partial():
    gt = {"a1": "trustworthy", "a2": "untrustworthy", "a3": "trustworthy", "a4": "untrustworthy"}
    preds = {"a1": "trustworthy", "a2": "trustworthy", "a3": "trustworthy", "a4": "untrustworthy"}
    assert compute_accuracy(preds, gt) == 0.75


def test_compute_accuracy_empty():
    assert compute_accuracy({}, {"a1": "trustworthy"}) == 0.0


def test_get_failures():
    gt = {"a1": "trustworthy", "a2": "untrustworthy", "a3": "trustworthy"}
    preds = {"a1": "untrustworthy", "a2": "untrustworthy", "a3": "trustworthy"}
    failures = get_failures(preds, gt)
    assert len(failures) == 1
    assert failures[0]["agent_id"] == "a1"
    assert failures[0]["predicted"] == "untrustworthy"
    assert failures[0]["actual"] == "trustworthy"


def test_confusion_matrix():
    gt = {"a1": "trustworthy", "a2": "untrustworthy", "a3": "trustworthy", "a4": "untrustworthy"}
    preds = {"a1": "trustworthy", "a2": "trustworthy", "a3": "untrustworthy", "a4": "untrustworthy"}
    cm = get_confusion_matrix(preds, gt)
    assert cm["tp"] == 1  # a1
    assert cm["fp"] == 1  # a2
    assert cm["fn"] == 1  # a3
    assert cm["tn"] == 1  # a4


def test_load_ground_truth():
    gt = load_ground_truth()
    assert len(gt) == 50
    assert gt["agent_001"] == "trustworthy"
    assert gt["agent_002"] == "untrustworthy"


if __name__ == "__main__":
    test_compute_accuracy_perfect()
    test_compute_accuracy_zero()
    test_compute_accuracy_partial()
    test_compute_accuracy_empty()
    test_get_failures()
    test_confusion_matrix()
    test_load_ground_truth()
    print("All evaluator tests passed!")
