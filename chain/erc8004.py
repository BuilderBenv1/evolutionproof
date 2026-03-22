"""ERC-8004 identity registration and reads via AgentProof oracle."""

import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

AGENTPROOF_ORACLE_BASE = "https://oracle.agentproof.sh"


def register_identity(operator_wallet: str, agent_name: str = "EvolutionProof",
                       ens_name: str = None) -> dict:
    """Register a new ERC-8004 identity via AgentProof oracle.

    Returns:
        Dict with agent_id, tx_hash, and registration details.
    """
    api_key = os.getenv("AGENTPROOF_API_KEY")
    if not api_key:
        raise ValueError("AGENTPROOF_API_KEY not set")

    payload = {
        "operator": operator_wallet,
        "name": agent_name,
        "description": "Self-improving agent trust screener with verifiable on-chain improvement history",
        "capabilities": [
            "agent_screening",
            "self_improvement",
            "onchain_logging",
            "reputation_verification",
        ],
    }

    if ens_name:
        payload["ens_name"] = ens_name

    response = requests.post(
        f"{AGENTPROOF_ORACLE_BASE}/api/v1/identity/register",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


def get_identity(agent_id: str) -> dict:
    """Get ERC-8004 identity details."""
    api_key = os.getenv("AGENTPROOF_API_KEY")

    response = requests.get(
        f"{AGENTPROOF_ORACLE_BASE}/api/v1/identity/{agent_id}",
        headers={"Authorization": f"Bearer {api_key}"},
        timeout=15,
    )
    response.raise_for_status()
    return response.json()


def get_trust_score(agent_id: str = None) -> dict:
    """Get current ERC-8004 TrustScore for an agent."""
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
