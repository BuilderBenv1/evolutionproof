"""State management between iterations — persists to local JSON and Filecoin."""

import json
import hashlib
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import Optional


@dataclass
class AgentState:
    iteration: int = 0
    current_prompt: str = ""
    best_accuracy: float = 0.0
    best_prompt: str = ""
    accuracy_history: list = field(default_factory=list)
    prompt_hashes: list = field(default_factory=list)
    total_tokens_used: int = 0
    filecoin_cids: list = field(default_factory=list)
    tx_hashes: list = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "AgentState":
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})


def hash_prompt(prompt: str) -> str:
    """SHA-256 hash of a prompt string."""
    return hashlib.sha256(prompt.encode()).hexdigest()[:16]


STATE_FILE = Path(__file__).resolve().parent.parent / "agent_state.json"


def save_state(state: AgentState, path: Optional[str] = None):
    """Save agent state to local JSON file."""
    p = Path(path) if path else STATE_FILE
    with open(p, "w") as f:
        json.dump(state.to_dict(), f, indent=2)


def load_state(path: Optional[str] = None) -> AgentState:
    """Load agent state from local JSON file, or return fresh state."""
    p = Path(path) if path else STATE_FILE
    if p.exists():
        with open(p) as f:
            data = json.load(f)
        return AgentState.from_dict(data)
    return AgentState()


def append_to_agent_log(log_entry: dict, path: Optional[str] = None):
    """Append an iteration log entry to agent_log.json (Protocol Labs requirement)."""
    if path is None:
        path = Path(__file__).resolve().parent.parent / "agent_log.json"
    else:
        path = Path(path)

    if path.exists():
        with open(path) as f:
            logs = json.load(f)
    else:
        logs = []

    logs.append(log_entry)

    with open(path, "w") as f:
        json.dump(logs, f, indent=2)
