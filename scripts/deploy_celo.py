#!/usr/bin/env python3
"""Deploy StETHTreasury to Celo mainnet and execute a real transaction."""

import os
import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from dotenv import load_dotenv
load_dotenv()

from web3 import Web3
import solcx

solcx.set_solc_version("0.8.20")

CELO_RPC = os.getenv("CELO_RPC_URL", "https://forno.celo.org")
CHAIN_ID = 42220

# Use a placeholder for wstETH — Celo doesn't have native wstETH
# We'll use CELO's wrapped token or a mock ERC20 address
# For demo purposes, we use an existing ERC20 on Celo
WSTETH_CELO = "0x3C1BCa5a656e69edCD0D4E36BEbb3FcDAcA60Cf1"  # Placeholder ERC20 on Celo


def compile_contract():
    """Compile StETHTreasury.sol"""
    sol_path = Path(__file__).resolve().parent.parent / "contracts" / "StETHTreasury.sol"
    source = sol_path.read_text()

    compiled = solcx.compile_source(
        source,
        output_values=["abi", "bin"],
        solc_version="0.8.20",
    )

    # Get the StETHTreasury contract (not the IERC20 interface)
    for contract_id, contract_interface in compiled.items():
        if "StETHTreasury" in contract_id:
            return contract_interface["abi"], contract_interface["bin"]
    raise ValueError("StETHTreasury not found in compiled output")


def main():
    print("Deploying StETHTreasury to Celo Mainnet")
    print("=" * 50)

    private_key = os.getenv("OPERATOR_PRIVATE_KEY")
    if not private_key:
        print("ERROR: OPERATOR_PRIVATE_KEY not set")
        sys.exit(1)

    w3 = Web3(Web3.HTTPProvider(CELO_RPC))
    if not w3.is_connected():
        print("ERROR: Cannot connect to Celo RPC")
        sys.exit(1)

    account = w3.eth.account.from_key(private_key)
    print(f"Deployer: {account.address}")
    print(f"Balance: {w3.from_wei(w3.eth.get_balance(account.address), 'ether')} CELO")

    # Compile
    print("\nCompiling StETHTreasury.sol...")
    abi, bytecode = compile_contract()
    print("Compilation successful!")

    # Deploy
    print("\nDeploying contract...")
    contract = w3.eth.contract(abi=abi, bytecode=bytecode)

    nonce = w3.eth.get_transaction_count(account.address)
    tx = contract.constructor(
        WSTETH_CELO,  # _wstETH
        account.address,  # _agent (self for demo)
    ).build_transaction({
        "from": account.address,
        "gas": 2000000,
        "gasPrice": w3.eth.gas_price,
        "nonce": nonce,
        "chainId": CHAIN_ID,
    })

    signed = account.sign_transaction(tx)
    tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
    print(f"Deploy TX: {tx_hash.hex()}")

    receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)
    contract_address = receipt.contractAddress
    print(f"Contract deployed: {contract_address}")
    print(f"Status: {'Success' if receipt.status == 1 else 'Failed'}")
    print(f"Gas used: {receipt.gasUsed}")
    print(f"Explorer: https://celoscan.io/tx/{tx_hash.hex()}")

    # Save deployment info
    deploy_info = {
        "contract_address": contract_address,
        "tx_hash": tx_hash.hex(),
        "deployer": account.address,
        "chain": "celo",
        "chain_id": CHAIN_ID,
        "block": receipt.blockNumber,
    }

    deploy_path = Path(__file__).resolve().parent.parent / "deployment.json"
    with open(deploy_path, "w") as f:
        json.dump(deploy_info, f, indent=2)
    print(f"\nDeployment info saved to deployment.json")

    # Now configure the treasury — whitelist ourselves + set cap
    print("\n--- Configuring Treasury ---")
    deployed_contract = w3.eth.contract(address=contract_address, abi=abi)

    # Whitelist the operator as a recipient
    nonce += 1
    tx2 = deployed_contract.functions.setRecipientWhitelist(
        account.address, True
    ).build_transaction({
        "from": account.address,
        "gas": 100000,
        "gasPrice": w3.eth.gas_price,
        "nonce": nonce,
        "chainId": CHAIN_ID,
    })
    signed2 = account.sign_transaction(tx2)
    tx_hash2 = w3.eth.send_raw_transaction(signed2.raw_transaction)
    receipt2 = w3.eth.wait_for_transaction_receipt(tx_hash2, timeout=60)
    print(f"Whitelist TX: https://celoscan.io/tx/{tx_hash2.hex()}")
    print(f"Status: {'Success' if receipt2.status == 1 else 'Failed'}")

    # Set per-tx cap
    nonce += 1
    cap = w3.to_wei(0.1, "ether")  # 0.1 wstETH cap
    tx3 = deployed_contract.functions.setPerTxCap(cap).build_transaction({
        "from": account.address,
        "gas": 100000,
        "gasPrice": w3.eth.gas_price,
        "nonce": nonce,
        "chainId": CHAIN_ID,
    })
    signed3 = account.sign_transaction(tx3)
    tx_hash3 = w3.eth.send_raw_transaction(signed3.raw_transaction)
    receipt3 = w3.eth.wait_for_transaction_receipt(tx_hash3, timeout=60)
    print(f"SetCap TX: https://celoscan.io/tx/{tx_hash3.hex()}")
    print(f"Status: {'Success' if receipt3.status == 1 else 'Failed'}")

    # Query contract state
    print("\n--- Treasury State ---")
    print(f"Owner: {deployed_contract.functions.owner().call()}")
    print(f"Agent: {deployed_contract.functions.agent().call()}")
    print(f"Per-TX Cap: {w3.from_wei(deployed_contract.functions.perTxCap().call(), 'ether')} wstETH")
    print(f"Spendable Yield: {deployed_contract.functions.getSpendableYield().call()}")
    print(f"Operator whitelisted: {deployed_contract.functions.recipientWhitelist(account.address).call()}")

    print(f"\n{'='*50}")
    print(f"StETHTreasury deployed and configured on Celo!")
    print(f"Contract: {contract_address}")
    print(f"3 on-chain transactions executed")
    print(f"{'='*50}")


if __name__ == "__main__":
    main()
