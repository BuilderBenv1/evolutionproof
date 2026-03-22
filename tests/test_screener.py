"""Tests for the screener module (without API calls)."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from agent.screener import DEFAULT_SCREENING_PROMPT


def test_default_prompt_exists():
    assert len(DEFAULT_SCREENING_PROMPT) > 100
    assert "verdict" in DEFAULT_SCREENING_PROMPT
    assert "trustworthy" in DEFAULT_SCREENING_PROMPT


def test_default_prompt_has_classification_rules():
    prompt = DEFAULT_SCREENING_PROMPT.lower()
    assert "failed_tx_ratio" in prompt
    assert "erc8004_score" in prompt
    assert "contract_verified" in prompt


def test_default_prompt_has_output_format():
    assert '{"verdict":' in DEFAULT_SCREENING_PROMPT or '"verdict"' in DEFAULT_SCREENING_PROMPT


if __name__ == "__main__":
    test_default_prompt_exists()
    test_default_prompt_has_classification_rules()
    test_default_prompt_has_output_format()
    print("All screener tests passed!")
