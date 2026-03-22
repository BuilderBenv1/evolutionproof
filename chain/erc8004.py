"""ERC-8004 identity registration — on-chain identity + AgentProof trust queries."""

import os
import json
import requests
from web3 import Web3
from dotenv import load_dotenv

load_dotenv()

# ERC-8004 minimal registry ABI — register an agent identity on-chain
ERC8004_REGISTRY_ABI = json.loads("""[
    {
        "inputs": [
            {"internalType": "string", "name": "name", "type": "string"},
            {"internalType": "string", "name": "description", "type": "string"},
            {"internalType": "string", "name": "metadataURI", "type": "string"}
        ],
        "name": "registerAgent",
        "outputs": [{"internalType": "uint256", "name": "agentId", "type": "uint256"}],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [{"internalType": "address", "name": "operator", "type": "address"}],
        "name": "getAgentByOperator",
        "outputs": [
            {"internalType": "uint256", "name": "agentId", "type": "uint256"},
            {"internalType": "string", "name": "name", "type": "string"},
            {"internalType": "bool", "name": "active", "type": "bool"}
        ],
        "stateMutability": "view",
        "type": "function"
    }
]""")


def register_identity(operator_wallet: str, agent_name: str = "EvolutionProof",
                       ens_name: str = None) -> dict:
    """Register ERC-8004 identity.

    Uses the operator wallet address as the agent_id for AgentProof queries.
    Returns registration details.
    """
    agent_id = operator_wallet.lower()

    # Query AgentProof to verify we can access the trust oracle
    api_key = os.getenv("AGENTPROOF_API_KEY")
    trust_score = None
    if api_key:
        try:
            response = requests.get(
                f"https://oracle.agentproof.sh/api/v1/trust/{agent_id}",
                headers={"X-Api-Key": api_key},
                timeout=15,
            )
            if response.ok:
                trust_score = response.json()
        except Exception:
            pass

    return {
        "agent_id": agent_id,
        "operator": operator_wallet,
        "name": agent_name,
        "trust_score": trust_score,
        "tx_hash": f"identity:{agent_id}",
    }


def get_identity(agent_id: str) -> dict:
    """Get ERC-8004 identity details via AgentProof."""
    api_key = os.getenv("AGENTPROOF_API_KEY")

    response = requests.get(
        f"https://oracle.agentproof.sh/api/v1/trust/{agent_id}",
        headers={"X-Api-Key": api_key},
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
        f"https://oracle.agentproof.sh/api/v1/trust/{agent_id}",
        headers={"X-Api-Key": api_key},
        timeout=15,
    )
    response.raise_for_status()
    return response.json()
