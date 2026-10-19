

import json
import os
from pathlib import Path

from dotenv import load_dotenv
from web3 import Web3

from app.integrity import calculate_file_hash

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
ABI_PATH = BASE_DIR / "app" / "contract_abi.json"


def connect_to_sepolia():
    rpc_url = os.getenv("SEPOLIA_RPC_URL")
    if not rpc_url:
        raise RuntimeError("SEPOLIA_RPC_URL is missing from .env")

    web3 = Web3(Web3.HTTPProvider(rpc_url))

    if not web3.is_connected():
        raise ConnectionError("Could not connect to Sepolia")

    if web3.eth.chain_id != 11155111:
        raise RuntimeError("Connected to the wrong network")

    return web3


def load_contract(web3):
    address = os.getenv("SEPOLIA_CONTRACT_ADDRESS")
    if not address:
        raise RuntimeError(
            "SEPOLIA_CONTRACT_ADDRESS is missing from .env"
        )

    if not ABI_PATH.exists():
        raise FileNotFoundError(f"ABI file not found: {ABI_PATH}")

    with ABI_PATH.open("r", encoding="utf-8") as file:
        abi = json.load(file)

    checksum_address = Web3.to_checksum_address(address)

    return web3.eth.contract(
        address=checksum_address,
        abi=abi,
    )


def check_contract():
    web3 = connect_to_sepolia()
    contract = load_contract(web3)

    print("Connected to Sepolia:", web3.eth.chain_id)
    print("Contract address:", contract.address)
    print("Latest block:", web3.eth.block_number)
    print("Contract connection: READY")

    return web3, contract


def prepare_report_anchor(report_path: str) -> dict:
    web3, contract = check_contract()
    report_hash = calculate_file_hash(report_path)

    # Read-only check; this does not send a transaction.
    result = {
        "report_path": report_path,
        "sha256": report_hash,
        "chain_id": web3.eth.chain_id,
        "contract_address": contract.address,
        "status": "READY_TO_ANCHOR",
        "message": "Contract connected. No transaction has been sent.",
    }

    return result


if __name__ == "__main__":
    result = prepare_report_anchor("reports/REGU-001.json")

    for key, value in result.items():
        print(f"{key}: {value}")
