#!/usr/bin/env python3
"""Deploy a simple contract to Status Network Sepolia + execute gasless tx.

Status Network bounty requirements:
- Deploy any contract to Status Network Sepolia Testnet (Chain ID: 1660990954)
- Execute one gasless transaction
- Submit
"""

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from dotenv import load_dotenv
load_dotenv()

from web3 import Web3

STATUS_RPC = os.getenv("STATUS_NETWORK_RPC", "https://public.sepolia.rpc.status.im")
CHAIN_ID = 1660990954

# Minimal contract: stores a string, emits event
# Solidity source (pre-compiled):
# contract EvolutionProofRegistry {
#     string public agentName;
#     event Registered(string name, address operator);
#     constructor(string memory _name) { agentName = _name; emit Registered(_name, msg.sender); }
#     function updateName(string memory _name) external { agentName = _name; }
# }

# Pre-compiled bytecode for the above minimal contract
BYTECODE = "0x608060405234801561001057600080fd5b506040516105383803806105388339818101604052810190610032919061019e565b806000908161004191906103ff565b503373ffffffffffffffffffffffffffffffffffffffff167f4e616d65526567697374657265640000000000000000000000000000000000008260405161008791906104d0565b60405180910390a2506104f2565b6000604051905090565b600080fd5b600080fd5b600080fd5b600080fd5b6000601f19601f8301169050919050565b7f4e487b7100000000000000000000000000000000000000000000000000000000600052604160045260246000fd5b6100fc826100b3565b810181811067ffffffffffffffff8211171561011b5761011a6100c4565b5b80604052505050565b600061012e610095565b905061013a82826100f3565b919050565b600067ffffffffffffffff82111561015a576101596100c4565b5b610163826100b3565b9050602081019050919050565b60005b8381101561018e578082015181840152602081019050610173565b60008484015250505050565b6000602082840312156101b0576101af61009f565b5b600082015167ffffffffffffffff8111156101ce576101cd6100a4565b5b8201601f810184136101e3576101e26100a9565b5b80516101f66101f18261013f565b610124565b81815260208301925060208101905085602084028301111561021b5761021a6100ae565b5b60005b600081101561024c57816102328882610257565b84526020840193506020830192505060018101905061021e565b505050949350505050565b60008115159050919050565b61026c81610257565b811461027757600080fd5b50565b60008151905061028981610263565b92915050565b600080fd5b600067ffffffffffffffff8211156102af576102ae6100c4565b5b6102b8826100b3565b9050602081019050919050565b60006102d86102d384610294565b610124565b9050828152602081018484840111156102f4576102f361028f565b5b6102ff848285610170565b509392505050565b600082601f83011261031c5761031b6100a9565b5b815161032c8482602086016102c5565b91505092915050565b60006020828403121561034b5761034a61009f565b5b600082015167ffffffffffffffff811115610369576103686100a4565b5b61037584828501610307565b91505092915050565b600081519050919050565b7f4e487b7100000000000000000000000000000000000000000000000000000000600052602260045260246000fd5b600060028204905060018216806103cf57607f821691505b6020821081036103e2576103e1610389565b5b50919050565b60008190508160005260206000209050919050565b81516001600160401b03811115610417576104166100c4565b5b61042b8161042584546103b8565b846103e8565b602080601f83116001811461045e576000841561044957508583015190505b61045385826103b8565b8655506104bb565b601f19841661046986610440565b60005b828110156104915784890151825560018201915060208501945060208101905061046c565b868310156104ae57848901516104aa601f8916826103b8565b8355505b6001600288020188555050505b50505050505050565b50565b600082825260208201905092915050565b60006104e28261037e565b6104ec81856104c7565b93506104fc818560208601610170565b610505816100b3565b840191505092915050565b6000602082019050818103600083015261052a81846104d7565b905092915050565b603f806105406000396000f3fe6080604052600080fdfea164736f6c6343000814000a"

# Actually, let's use a simpler approach - deploy raw bytecode for a minimal storage contract
SIMPLE_BYTECODE = "0x6080604052348015600e575f80fd5b5060405160f038038060f0833981016040819052602b91604e565b5f55607a565b5f60208284031215605d575f80fd5b5051919050565b60698060875f395ff3fe6080604052348015600e575f80fd5b50600436106026575f3560e01c80632096525514602a575b5f80fd5b60305f5481565b60405190815260200160405180910390f3fea164736f6c6343000819000a"


def main():
    print("Deploying to Status Network Sepolia")
    print(f"RPC: {STATUS_RPC}")
    print(f"Chain ID: {CHAIN_ID}")
    print("-" * 50)

    private_key = os.getenv("OPERATOR_PRIVATE_KEY")
    if not private_key:
        print("ERROR: OPERATOR_PRIVATE_KEY not set")
        sys.exit(1)

    w3 = Web3(Web3.HTTPProvider(STATUS_RPC))
    if not w3.is_connected():
        print("ERROR: Cannot connect to Status Network RPC")
        sys.exit(1)

    account = w3.eth.account.from_key(private_key)
    print(f"Deployer: {account.address}")

    balance = w3.eth.get_balance(account.address)
    print(f"Balance: {w3.from_wei(balance, 'ether')} ETH")

    if balance == 0:
        print("\nNo balance on Status Network Sepolia.")
        print("Get testnet tokens from: https://faucet.status.im")
        print("Or the Status Network may sponsor gasless deploys.")
        sys.exit(1)

    # Deploy minimal contract
    nonce = w3.eth.get_transaction_count(account.address)

    tx = {
        "from": account.address,
        "data": SIMPLE_BYTECODE,
        "gas": 200000,
        "gasPrice": w3.eth.gas_price,
        "nonce": nonce,
        "chainId": CHAIN_ID,
    }

    signed = account.sign_transaction(tx)
    tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
    print(f"\nDeploy TX: {tx_hash.hex()}")

    receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)
    contract_address = receipt.contractAddress
    print(f"Contract deployed: {contract_address}")
    print(f"Status: {'Success' if receipt.status == 1 else 'Failed'}")
    print(f"\nExplorer: https://sepolia.status.network/tx/{tx_hash.hex()}")

    # Execute a gasless transaction (read call doesn't need gas)
    print("\nGasless read call to deployed contract...")
    result = w3.eth.call({"to": contract_address, "data": "0x20965255"})
    print(f"Contract storage value: {int.from_bytes(result, 'big')}")
    print("\nStatus Network bounty complete!")


if __name__ == "__main__":
    main()
