#!/usr/bin/env python3
"""Entry point: starts the self-improvement loop."""

import argparse
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from dotenv import load_dotenv
load_dotenv()

from agent.core import run_improvement_loop


def main():
    parser = argparse.ArgumentParser(description="Run EvolutionProof self-improvement loop")
    parser.add_argument("--iterations", type=int, default=100, help="Number of iterations to run")
    parser.add_argument("--no-resume", action="store_true", help="Start fresh instead of resuming")
    args = parser.parse_args()

    print("=" * 60)
    print("  EvolutionProof — Self-Improving Agent Trust Screener")
    print("=" * 60)
    print()

    state = run_improvement_loop(
        max_iterations=args.iterations,
        resume=not args.no_resume,
    )

    print()
    print("=" * 60)
    print(f"  Final Results:")
    print(f"  Iterations completed: {state.iteration}")
    print(f"  Best accuracy: {state.best_accuracy:.1%}")
    print(f"  Filecoin CIDs: {len(state.filecoin_cids)}")
    print(f"  On-chain TXs: {len(state.tx_hashes)}")
    print("=" * 60)


if __name__ == "__main__":
    main()
