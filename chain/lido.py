"""wstETH yield treasury interactions on Celo."""

import os
import json
from dotenv import load_dotenv

load_dotenv()

# Minimal ABI for StETHTreasury contract
TREASURY_ABI = json.loads("""[
    {"inputs":[],"name":"getSpendableYield","outputs":[{"type":"uint256"}],"stateMutability":"view","type":"function"},
    {"inputs":[],"name":"principalDeposited","outputs":[{"type":"uint256"}],"stateMutability":"view","type":"function"},
    {"inputs":[{"name":"amount","type":"uint256"},{"name":"recipient","type":"address"}],"name":"withdrawYield","outputs":[],"stateMutability":"nonpayable","type":"function"},
    {"inputs":[],"name":"agent","outputs":[{"type":"address"}],"stateMutability":"view","type":"function"},
    {"inputs":[],"name":"owner","outputs":[{"type":"address"}],"stateMutability":"view","type":"function"},
    {"inputs":[{"name":"","type":"address"}],"name":"recipientWhitelist","outputs":[{"type":"bool"}],"stateMutability":"view","type":"function"},
    {"inputs":[],"name":"perTxCap","outputs":[{"type":"uint256"}],"stateMutability":"view","type":"function"}
]""")


def get_treasury_contract():
    """Get Web3 contract instance for StETHTreasury."""
    from chain.celo import get_web3
    w3 = get_web3()
    treasury_address = os.getenv("TREASURY_CONTRACT")
    if not treasury_address:
        raise ValueError("TREASURY_CONTRACT not set")
    return w3, w3.eth.contract(
        address=w3.to_checksum_address(treasury_address),
        abi=TREASURY_ABI,
    )


def get_spendable_yield() -> dict:
    """Query the spendable yield balance from the treasury."""
    w3, contract = get_treasury_contract()
    yield_wei = contract.functions.getSpendableYield().call()
    principal_wei = contract.functions.principalDeposited().call()

    return {
        "spendable_yield_wei": yield_wei,
        "spendable_yield_eth": w3.from_wei(yield_wei, "ether"),
        "principal_deposited_wei": principal_wei,
        "principal_deposited_eth": w3.from_wei(principal_wei, "ether"),
    }


def withdraw_yield(amount_wei: int, recipient: str) -> str:
    """Withdraw yield from the treasury to a whitelisted recipient.

    Returns transaction hash.
    """
    from chain.celo import get_operator_account
    w3, account = get_operator_account()
    _, contract = get_treasury_contract()

    tx = contract.functions.withdrawYield(
        amount_wei,
        w3.to_checksum_address(recipient),
    ).build_transaction({
        "from": account.address,
        "gas": 100000,
        "gasPrice": w3.eth.gas_price,
        "nonce": w3.eth.get_transaction_count(account.address),
        "chainId": 42220,
    })

    signed = account.sign_transaction(tx)
    tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=60)

    return receipt.transactionHash.hex()


def get_treasury_info() -> dict:
    """Get full treasury status."""
    w3, contract = get_treasury_contract()

    return {
        "agent": contract.functions.agent().call(),
        "owner": contract.functions.owner().call(),
        "per_tx_cap_wei": contract.functions.perTxCap().call(),
        **get_spendable_yield(),
    }
