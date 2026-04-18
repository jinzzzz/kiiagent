from dotenv import load_dotenv
import os
from web3 import Web3

load_dotenv(".env")

RPC_URL = os.getenv("RPC_URL")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS")

if not RPC_URL or not PRIVATE_KEY or not CONTRACT_ADDRESS:
    raise Exception("❌ Missing .env variables")

CONTRACT_ADDRESS = Web3.to_checksum_address(CONTRACT_ADDRESS)