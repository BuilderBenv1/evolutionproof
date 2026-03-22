#!/usr/bin/env python3
"""One-time: register ERC-8004 identity via AgentProof oracle."""

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from dotenv import load_dotenv
load_dotenv()

from chain.erc8004 import register_identity
from chain.celo import get_web3


def main():
    print("Registering ERC-8004 Identity for EvolutionProof")
    print("-" * 50)

    # Get operator wallet address
    private_key = os.getenv("OPERATOR_PRIVATE_KEY")
    if not private_key:
        print("ERROR: OPERATOR_PRIVATE_KEY not set in .env")
        sys.exit(1)

    w3 = get_web3()
    account = w3.eth.account.from_key(private_key)
    operator_wallet = account.address
    print(f"Operator wallet: {operator_wallet}")

    ens_name = os.getenv("ENS_NAME", "evolutionproof.eth")
    print(f"ENS name: {ens_name}")

    try:
        result = register_identity(
            operator_wallet=operator_wallet,
            agent_name="EvolutionProof",
            ens_name=ens_name,
        )
        print(f"\nRegistration successful!")
        print(f"Agent ID: {result.get('agent_id')}")
        print(f"TX Hash: {result.get('tx_hash')}")
        print(f"\nAdd to .env:")
        print(f"AGENTPROOF_AGENT_ID={result.get('agent_id')}")

    except Exception as e:
        print(f"\nRegistration failed: {e}")
        print("Make sure AGENTPROOF_API_KEY is set in .env")
        sys.exit(1)


if __name__ == "__main__":
    main()
