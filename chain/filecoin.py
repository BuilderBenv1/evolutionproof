"""Filecoin Onchain Cloud (FOC) mainnet — iteration log storage."""

import os
import json
import hashlib
import requests
from datetime import datetime, timezone
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Local fallback storage when FOC is unavailable
LOCAL_STORAGE_DIR = Path(__file__).resolve().parent.parent / "filecoin_logs"


def _ensure_local_storage():
    LOCAL_STORAGE_DIR.mkdir(exist_ok=True)


def store_iteration_log(log_entry: dict) -> str:
    """Store an iteration log on Filecoin FOC mainnet.

    Args:
        log_entry: Dict containing iteration data

    Returns:
        CID string (content identifier)
    """
    api_key = os.getenv("FILECOIN_API_KEY")
    contract_address = os.getenv("FILECOIN_CONTRACT_ADDRESS")

    log_bytes = json.dumps(log_entry, sort_keys=True).encode()
    content_hash = hashlib.sha256(log_bytes).hexdigest()

    if api_key and contract_address:
        try:
            response = requests.post(
                f"https://api.foc.filecoin.io/v1/store",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "contract": contract_address,
                    "data": log_entry,
                    "metadata": {
                        "type": "iteration_log",
                        "agent": "EvolutionProof",
                        "content_hash": content_hash,
                    },
                },
                timeout=30,
            )
            response.raise_for_status()
            result = response.json()
            return result.get("cid", content_hash)
        except Exception as e:
            print(f"FOC storage failed, falling back to local: {e}")

    # Local fallback
    _ensure_local_storage()
    iteration = log_entry.get("iteration", 0)
    filepath = LOCAL_STORAGE_DIR / f"iteration_{iteration:04d}.json"
    with open(filepath, "w") as f:
        json.dump(log_entry, f, indent=2)

    return f"local:{content_hash}"


def retrieve_iteration_log(cid: str) -> dict:
    """Retrieve an iteration log from Filecoin by CID."""
    api_key = os.getenv("FILECOIN_API_KEY")

    if cid.startswith("local:"):
        # Search local storage
        _ensure_local_storage()
        for filepath in sorted(LOCAL_STORAGE_DIR.glob("*.json")):
            with open(filepath) as f:
                data = json.load(f)
            data_hash = hashlib.sha256(
                json.dumps(data, sort_keys=True).encode()
            ).hexdigest()
            if data_hash == cid.replace("local:", ""):
                return data
        raise FileNotFoundError(f"No local log found for {cid}")

    if api_key:
        response = requests.get(
            f"https://api.foc.filecoin.io/v1/retrieve/{cid}",
            headers={"Authorization": f"Bearer {api_key}"},
            timeout=15,
        )
        response.raise_for_status()
        return response.json()

    raise ValueError("FILECOIN_API_KEY not set and CID is not local")


def load_state_from_filecoin() -> dict:
    """Load the latest agent state from Filecoin."""
    api_key = os.getenv("FILECOIN_API_KEY")
    contract_address = os.getenv("FILECOIN_CONTRACT_ADDRESS")

    if api_key and contract_address:
        try:
            response = requests.get(
                f"https://api.foc.filecoin.io/v1/state/{contract_address}/latest",
                headers={"Authorization": f"Bearer {api_key}"},
                timeout=15,
            )
            response.raise_for_status()
            return response.json()
        except Exception:
            pass

    # Local fallback
    state_file = LOCAL_STORAGE_DIR / "agent_state.json"
    if state_file.exists():
        with open(state_file) as f:
            return json.load(f)
    return {}


def update_state_on_filecoin(state) -> str:
    """Persist agent state to Filecoin."""
    api_key = os.getenv("FILECOIN_API_KEY")
    contract_address = os.getenv("FILECOIN_CONTRACT_ADDRESS")

    state_dict = state.to_dict() if hasattr(state, "to_dict") else state

    if api_key and contract_address:
        try:
            response = requests.post(
                f"https://api.foc.filecoin.io/v1/state/{contract_address}/update",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                },
                json=state_dict,
                timeout=30,
            )
            response.raise_for_status()
            return response.json().get("cid", "")
        except Exception as e:
            print(f"Filecoin state update failed, saving locally: {e}")

    # Local fallback
    _ensure_local_storage()
    state_file = LOCAL_STORAGE_DIR / "agent_state.json"
    with open(state_file, "w") as f:
        json.dump(state_dict, f, indent=2)
    return "local:state"


def list_iteration_logs() -> list:
    """List all stored iteration logs."""
    api_key = os.getenv("FILECOIN_API_KEY")
    contract_address = os.getenv("FILECOIN_CONTRACT_ADDRESS")

    if api_key and contract_address:
        try:
            response = requests.get(
                f"https://api.foc.filecoin.io/v1/list/{contract_address}",
                headers={"Authorization": f"Bearer {api_key}"},
                timeout=15,
            )
            response.raise_for_status()
            return response.json()
        except Exception:
            pass

    # Local fallback
    _ensure_local_storage()
    logs = []
    for filepath in sorted(LOCAL_STORAGE_DIR.glob("iteration_*.json")):
        with open(filepath) as f:
            logs.append(json.load(f))
    return logs
