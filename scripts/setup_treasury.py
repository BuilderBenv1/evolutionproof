#!/usr/bin/env python3
"""One-time: deploy and configure stETH treasury on Celo."""

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from dotenv import load_dotenv
load_dotenv()


def main():
    print("StETHTreasury Deployment Guide")
    print("=" * 50)
    print()
    print("Prerequisites:")
    print("  1. OPERATOR_PRIVATE_KEY set in .env")
    print("  2. WSTETH_ADDRESS_CELO set in .env")
    print("  3. Celo account funded with CELO for gas")
    print("  4. Hardhat installed: npm install --save-dev hardhat @nomicfoundation/hardhat-ethers")
    print()
    print("Deploy Steps:")
    print("  cd contracts")
    print("  npx hardhat run deploy.js --network celo")
    print()
    print("After deployment, add TREASURY_CONTRACT=<address> to .env")
    print()

    # Verify env vars
    missing = []
    for var in ["OPERATOR_PRIVATE_KEY", "WSTETH_ADDRESS_CELO", "CELO_RPC_URL"]:
        if not os.getenv(var):
            missing.append(var)

    if missing:
        print(f"Missing env vars: {', '.join(missing)}")
        print("Please configure .env before deploying.")
    else:
        print("All required env vars are set. Ready to deploy!")

    # Check balance
    try:
        from chain.celo import get_balance
        balance = get_balance()
        print(f"\nOperator balance: {balance['celo']} CELO")
        if float(str(balance['celo'])) < 0.01:
            print("WARNING: Low balance. Fund the operator wallet with CELO for gas.")
    except Exception as e:
        print(f"\nCould not check balance: {e}")


if __name__ == "__main__":
    main()
