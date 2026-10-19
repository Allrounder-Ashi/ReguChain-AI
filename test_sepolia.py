import os
from dotenv import load_dotenv
from web3 import Web3

load_dotenv()

rpc_url = os.getenv("SEPOLIA_RPC_URL")

if not rpc_url:
    raise RuntimeError("SEPOLIA_RPC_URL is missing from your .env file.")

w3 = Web3(Web3.HTTPProvider(rpc_url))

if not w3.is_connected():
    print("❌ Connection failed. Check your Infura endpoint and API key.")
else:
    print("✅ Connected to Ethereum!")
    print("Chain ID:", w3.eth.chain_id)
    print("Latest block:", w3.eth.block_number)

    if w3.eth.chain_id == 11155111:
        print("✅ Confirmed: connected to Sepolia testnet!")
    else:
        print("⚠️ Connected, but this is not Sepolia.")