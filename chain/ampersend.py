"""ampersend-sdk spend controls for agent wallet."""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

AMPERSEND_BASE = "https://api.ampersend.io/v1"


def _headers():
    api_key = os.getenv("AMPERSEND_API_KEY")
    if not api_key:
        raise ValueError("AMPERSEND_API_KEY not set")
    return {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }


def setup_spend_controls(wallet_address: str, daily_limit_usd: float = 10.0,
                          per_tx_limit_usd: float = 1.0) -> dict:
    """Configure spend controls for the agent wallet.

    Args:
        wallet_address: The agent's wallet address
        daily_limit_usd: Maximum daily spend in USD
        per_tx_limit_usd: Maximum per-transaction spend in USD

    Returns:
        Configuration response dict.
    """
    response = requests.post(
        f"{AMPERSEND_BASE}/controls/create",
        headers=_headers(),
        json={
            "wallet": wallet_address,
            "rules": [
                {
                    "type": "daily_limit",
                    "value": daily_limit_usd,
                    "currency": "USD",
                },
                {
                    "type": "per_transaction_limit",
                    "value": per_tx_limit_usd,
                    "currency": "USD",
                },
                {
                    "type": "whitelist_only",
                    "enabled": True,
                },
            ],
        },
        timeout=15,
    )
    response.raise_for_status()
    return response.json()


def get_spend_status(wallet_address: str) -> dict:
    """Get current spend status and remaining budget."""
    response = requests.get(
        f"{AMPERSEND_BASE}/controls/{wallet_address}/status",
        headers=_headers(),
        timeout=15,
    )
    response.raise_for_status()
    return response.json()


def authorize_transaction(wallet_address: str, amount_usd: float,
                           recipient: str, memo: str = "") -> dict:
    """Request transaction authorization from ampersend.

    Returns authorization result with approval status.
    """
    response = requests.post(
        f"{AMPERSEND_BASE}/transactions/authorize",
        headers=_headers(),
        json={
            "wallet": wallet_address,
            "amount": amount_usd,
            "currency": "USD",
            "recipient": recipient,
            "memo": memo,
        },
        timeout=15,
    )
    response.raise_for_status()
    return response.json()


def add_to_whitelist(wallet_address: str, recipient: str) -> dict:
    """Add a recipient to the spending whitelist."""
    response = requests.post(
        f"{AMPERSEND_BASE}/controls/{wallet_address}/whitelist",
        headers=_headers(),
        json={"recipient": recipient},
        timeout=15,
    )
    response.raise_for_status()
    return response.json()
