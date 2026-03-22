#!/usr/bin/env python3
"""Upload all iteration logs to Filecoin via Lighthouse."""

import os
import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from lighthouseweb3 import Lighthouse

LIGHTHOUSE_API_KEY = "e8891295.4d15b7a792f7420c9818998d23578a35"


def main():
    print("Uploading iteration logs to Filecoin via Lighthouse")
    print("=" * 50)

    lh = Lighthouse(token=LIGHTHOUSE_API_KEY)

    root = Path(__file__).resolve().parent.parent
    logs_dir = root / "filecoin_logs"

    # Bundle all logs into one file
    log_files = sorted(logs_dir.glob("iteration_*.json"))
    print(f"Found {len(log_files)} iteration logs")

    all_logs = []
    for f in log_files:
        all_logs.append(json.loads(f.read_text()))

    bundle = {
        "agent": "EvolutionProof",
        "description": "Self-improving agent trust screener - iteration improvement logs",
        "operator": "0xC71A15Fcb1149254F97059F6cf3f6Ed43990ebd4",
        "total_iterations": len(all_logs),
        "logs": all_logs,
    }

    bundle_path = logs_dir / "iteration_bundle.json"
    bundle_path.write_text(json.dumps(bundle, indent=2))
    print(f"Bundle created: {bundle_path}")

    # Upload bundle
    print("\nUploading to Filecoin via Lighthouse...")
    try:
        response = lh.upload(source=str(bundle_path))
        print(f"Upload response: {response}")

        # Extract CID
        if isinstance(response, dict):
            cid = response.get("Hash") or response.get("cid") or response.get("data", {}).get("Hash")
        elif hasattr(response, "data"):
            cid = response.data.get("Hash", str(response))
        else:
            cid = str(response)

        print(f"\nCID: {cid}")
        print(f"Gateway: https://gateway.lighthouse.storage/ipfs/{cid}")

        # Save CID info
        cid_info = {
            "cid": cid,
            "gateway_url": f"https://gateway.lighthouse.storage/ipfs/{cid}",
            "iterations": len(all_logs),
            "network": "filecoin-mainnet-via-lighthouse",
            "storage_provider": "lighthouse.storage",
        }
        cid_path = root / "filecoin_cid.json"
        cid_path.write_text(json.dumps(cid_info, indent=2))
        print(f"CID info saved to filecoin_cid.json")

        # Also upload agent_log.json separately
        print("\nUploading agent_log.json...")
        agent_log_path = root / "agent_log.json"
        response2 = lh.upload(source=str(agent_log_path))
        print(f"agent_log.json response: {response2}")

        # Upload agent_state.json
        print("\nUploading agent_state.json...")
        state_path = root / "agent_state.json"
        response3 = lh.upload(source=str(state_path))
        print(f"agent_state.json response: {response3}")

        print(f"\n{'='*50}")
        print("All iteration logs uploaded to Filecoin!")
        print(f"{'='*50}")

    except Exception as e:
        print(f"Upload failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
