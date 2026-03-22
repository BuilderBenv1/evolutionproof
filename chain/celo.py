"""Celo chain interactions — agent operations on Celo mainnet."""

import os
from dotenv import load_dotenv

load_dotenv()

CELO_EXPLORER = "https://celoscan.io"


def get_celo_rpc_url() -> str:
    return os.getenv("CELO_RPC_URL", "https://forno.celo.org")


def get_web3():
    """Get a Web3 instance connected to Celo."""
    from web3 import Web3
    rpc_url = get_celo_rpc_url()
    w3 = Web3(Web3.HTTPProvider(rpc_url))
    if not w3.is_connected():
        raise ConnectionError(f"Cannot connect to Celo RPC at {rpc_url}")
    return w3


def get_operator_account():
    """Get the operator account from private key."""
    from web3 import Web3
    w3 = get_web3()
    private_key = os.getenv("OPERATOR_PRIVATE_KEY")
    if not private_key:
        raise ValueError("OPERATOR_PRIVATE_KEY not set")
    account = w3.eth.account.from_key(private_key)
    return w3, account


def get_balance(address: str = None) -> dict:
    """Get CELO and cUSD balance for an address."""
    w3 = get_web3()
    if address is None:
        _, account = get_operator_account()
        address = account.address

    celo_balance = w3.eth.get_balance(address)

    return {
        "address": address,
        "celo_wei": celo_balance,
        "celo": w3.from_wei(celo_balance, "ether"),
    }


def get_celo_tx_url(tx_hash: str) -> str:
    """Get Celoscan explorer URL for a transaction."""
    return f"{CELO_EXPLORER}/tx/{tx_hash}"


def send_celo(to: str, amount_wei: int) -> str:
    """Send CELO to an address. Returns tx hash."""
    w3, account = get_operator_account()

    tx = {
        "from": account.address,
        "to": w3.to_checksum_address(to),
        "value": amount_wei,
        "gas": 21000,
        "gasPrice": w3.eth.gas_price,
        "nonce": w3.eth.get_transaction_count(account.address),
        "chainId": 42220,  # Celo mainnet
    }

    signed = account.sign_transaction(tx)
    tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=60)

    return receipt.transactionHash.hex()
