"""Eval metric computation — wraps scorer for the agent loop."""

import json
from pathlib import Path

from eval.scorer import compute_accuracy, get_failures as _get_failures, load_ground_truth


def load_test_set(path: str = None) -> list:
    """Load test set agent profiles."""
    if path is None:
        path = Path(__file__).resolve().parent.parent / "eval" / "test_set.json"
    with open(path) as f:
        return json.load(f)


def load_ground_truth_labels(path: str = None) -> dict:
    """Load ground truth labels."""
    if path is None:
        path = Path(__file__).resolve().parent.parent / "eval" / "ground_truth.json"
    return load_ground_truth(str(path))


def score(predictions: dict, ground_truth: dict = None) -> float:
    """Score predictions against ground truth.

    Returns accuracy as float 0-1.
    """
    if ground_truth is None:
        ground_truth = load_ground_truth_labels()
    return compute_accuracy(predictions, ground_truth)


def get_failures(predictions: dict, ground_truth: dict = None) -> list:
    """Get list of misclassified agents with full profile data."""
    if ground_truth is None:
        ground_truth = load_ground_truth_labels()

    failures = _get_failures(predictions, ground_truth)

    # Enrich with profile data
    test_set = load_test_set()
    profiles_by_id = {p["agent_id"]: p for p in test_set}

    for failure in failures:
        agent_id = failure["agent_id"]
        if agent_id in profiles_by_id:
            failure["profile"] = profiles_by_id[agent_id]

    return failures
