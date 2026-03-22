"""AgentProof oracle calls — query trust scores and submit performance metrics."""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

AGENTPROOF_ORACLE_BASE = "https://oracle.agentproof.sh"


def _headers():
    api_key = os.getenv("AGENTPROOF_API_KEY")
    if not api_key:
        raise ValueError("AGENTPROOF_API_KEY not set")
    return {"X-Api-Key": api_key, "Content-Type": "application/json"}


def get_trust_score(agent_id: str = None) -> dict:
    """Get current TrustScore from AgentProof oracle."""
    if agent_id is None:
        agent_id = os.getenv("AGENTPROOF_AGENT_ID")
    if not agent_id:
        raise ValueError("agent_id required")

    response = requests.get(
        f"{AGENTPROOF_ORACLE_BASE}/api/v1/trust/{agent_id}",
        headers=_headers(),
        timeout=15,
    )
    response.raise_for_status()
    return response.json()


def get_risk_assessment(agent_id: str = None) -> dict:
    """Get risk assessment details for an agent."""
    if agent_id is None:
        agent_id = os.getenv("AGENTPROOF_AGENT_ID")

    response = requests.get(
        f"{AGENTPROOF_ORACLE_BASE}/api/v1/trust/{agent_id}/risk",
        headers=_headers(),
        timeout=15,
    )
    response.raise_for_status()
    return response.json()


def get_trusted_agents() -> list:
    """Get list of verified/trusted agents from the network."""
    response = requests.get(
        f"{AGENTPROOF_ORACLE_BASE}/api/v1/agents/trusted",
        headers=_headers(),
        timeout=15,
    )
    response.raise_for_status()
    return response.json()


def get_network_stats() -> dict:
    """Get network-wide trust statistics."""
    response = requests.get(
        f"{AGENTPROOF_ORACLE_BASE}/api/v1/network/stats",
        headers=_headers(),
        timeout=15,
    )
    response.raise_for_status()
    return response.json()


def get_usage() -> dict:
    """Get API usage metrics for our integration."""
    response = requests.get(
        f"{AGENTPROOF_ORACLE_BASE}/api/v1/integrations/usage",
        headers=_headers(),
        timeout=15,
    )
    response.raise_for_status()
    return response.json()


def submit_performance(accuracy: float, filecoin_cid: str = None) -> str:
    """Submit performance metric — logs locally and queries trust score.

    AgentProof is a query service, not a write service.
    We log performance to Filecoin and query our trust score after.

    Returns:
        Trust score response or empty string on failure.
    """
    agent_id = os.getenv("AGENTPROOF_AGENT_ID")
    if not agent_id:
        return ""

    try:
        result = get_trust_score(agent_id)
        return str(result.get("composite_score", ""))
    except Exception:
        return ""
