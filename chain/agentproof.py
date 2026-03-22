"""AgentProof oracle calls — submit performance metrics and update TrustScore."""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

AGENTPROOF_ORACLE_BASE = "https://oracle.agentproof.sh"


def submit_performance(accuracy: float, filecoin_cid: str = None) -> str:
    """Submit performance metric to AgentProof oracle, updating TrustScore.

    Args:
        accuracy: Classification accuracy (0-1)
        filecoin_cid: CID of the iteration log on Filecoin

    Returns:
        Transaction hash string.
    """
    api_key = os.getenv("AGENTPROOF_API_KEY")
    agent_id = os.getenv("AGENTPROOF_AGENT_ID")

    if not api_key or not agent_id:
        raise ValueError("AGENTPROOF_API_KEY and AGENTPROOF_AGENT_ID must be set")

    payload = {
        "agent_id": agent_id,
        "metric_type": "screening_accuracy",
        "value": round(accuracy * 100, 2),  # Convert to percentage
        "evidence": {
            "filecoin_cid": filecoin_cid,
            "metric": "classification_accuracy",
            "raw_value": accuracy,
        },
    }

    response = requests.post(
        f"{AGENTPROOF_ORACLE_BASE}/api/v1/performance/submit",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=30,
    )
    response.raise_for_status()
    result = response.json()
    return result.get("tx_hash", result.get("transaction_hash", ""))


def get_performance_history(agent_id: str = None) -> list:
    """Get historical performance submissions for an agent."""
    if agent_id is None:
        agent_id = os.getenv("AGENTPROOF_AGENT_ID")
    api_key = os.getenv("AGENTPROOF_API_KEY")

    response = requests.get(
        f"{AGENTPROOF_ORACLE_BASE}/api/v1/performance/{agent_id}/history",
        headers={"Authorization": f"Bearer {api_key}"},
        timeout=15,
    )
    response.raise_for_status()
    return response.json()


def get_trust_score(agent_id: str = None) -> dict:
    """Get current TrustScore from AgentProof oracle."""
    if agent_id is None:
        agent_id = os.getenv("AGENTPROOF_AGENT_ID")
    api_key = os.getenv("AGENTPROOF_API_KEY")

    response = requests.get(
        f"{AGENTPROOF_ORACLE_BASE}/api/v1/trust-score/{agent_id}",
        headers={"Authorization": f"Bearer {api_key}"},
        timeout=15,
    )
    response.raise_for_status()
    return response.json()
