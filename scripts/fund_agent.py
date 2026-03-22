#!/usr/bin/env python3
"""Fund agent with initial yield budget and configure ampersend spend controls."""

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from dotenv import load_dotenv
load_dotenv()

from chain.celo import get_balance, get_web3
from chain.ampersend import setup_spend_controls


def main():
    print("Agent Funding & Spend Control Setup")
    print("=" * 50)

    private_key = os.getenv("OPERATOR_PRIVATE_KEY")
    if not private_key:
        print("ERROR: OPERATOR_PRIVATE_KEY not set")
        sys.exit(1)

    w3 = get_web3()
    account = w3.eth.account.from_key(private_key)
    wallet = account.address

    # Check balance
    balance = get_balance(wallet)
    print(f"Wallet: {wallet}")
    print(f"Balance: {balance['celo']} CELO")

    # Setup ampersend spend controls
    ampersend_key = os.getenv("AMPERSEND_API_KEY")
    if ampersend_key:
        print("\nConfiguring ampersend spend controls...")
        try:
            result = setup_spend_controls(
                wallet_address=wallet,
                daily_limit_usd=10.0,
                per_tx_limit_usd=1.0,
            )
            print(f"Spend controls configured: {result}")
        except Exception as e:
            print(f"ampersend setup failed: {e}")
    else:
        print("\nAMPERSEND_API_KEY not set — skipping spend controls")

    print("\nSetup complete!")


if __name__ == "__main__":
    main()
