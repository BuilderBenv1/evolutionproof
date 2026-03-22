#!/usr/bin/env python3
"""One-time: register ERC-8004 identity via AgentProof oracle."""

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from dotenv import load_dotenv
load_dotenv()

from chain.erc8004 import register_identity


def main():
    print("Registering ERC-8004 Identity for EvolutionProof")
    print("-" * 50)

    private_key = os.getenv("OPERATOR_PRIVATE_KEY")
    if not private_key:
        print("ERROR: OPERATOR_PRIVATE_KEY not set in .env")
        sys.exit(1)

    from web3 import Web3
    account = Web3().eth.account.from_key(private_key)
    operator_wallet = account.address
    print(f"Operator wallet: {operator_wallet}")

    try:
        result = register_identity(
            operator_wallet=operator_wallet,
            agent_name="EvolutionProof",
        )
        agent_id = result.get("agent_id")
        print(f"\nRegistration successful!")
        print(f"Agent ID: {agent_id}")
        print(f"Trust Score: {result.get('trust_score')}")
        print(f"\nAdd to .env:")
        print(f"AGENTPROOF_AGENT_ID={agent_id}")

        # Auto-update .env if AGENTPROOF_AGENT_ID is empty
        env_path = Path(__file__).resolve().parent.parent / ".env"
        if env_path.exists():
            content = env_path.read_text()
            if "AGENTPROOF_AGENT_ID=" in content:
                lines = content.split("\n")
                for i, line in enumerate(lines):
                    if line.startswith("AGENTPROOF_AGENT_ID="):
                        old_val = line.split("=", 1)[1].strip()
                        if not old_val:
                            lines[i] = f"AGENTPROOF_AGENT_ID={agent_id}"
                            env_path.write_text("\n".join(lines))
                            print(f"\n.env updated automatically!")
                            break

    except Exception as e:
        print(f"\nRegistration failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
