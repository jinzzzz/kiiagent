import time
import requests
from web3 import Web3
from config import RPC_URL, PRIVATE_KEY, CONTRACT_ADDRESS

# connect blockchain
w3 = Web3(Web3.HTTPProvider(RPC_URL))
account = w3.eth.account.from_key(PRIVATE_KEY)

# contract ABI (rút gọn)
abi = [
    {
        "inputs": [],
        "name": "swap",
        "outputs": [],
        "stateMutability": "payable",
        "type": "function"
    }
]

contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=abi)

# ===== PRICE =====
def get_price():
    try:
        r = requests.get(
            "https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd",
            timeout=10
        )

        data = r.json()

        if "ethereum" in data:
            return data["ethereum"]["usd"]
        else:
            print("⚠️ API response lỗi:", data)
            return None

    except Exception as e:
        print("⚠️ Fetch lỗi:", e)
        return None

# ===== STRATEGY =====
BUY_ZONE = 2377
SELL_ZONE = 2379

last_action = None

def decide(price):
    global last_action

    if price < BUY_ZONE and last_action != "buy":
        return "buy"

    if price > SELL_ZONE and last_action != "sell":
        return "sell"

    return None

# ===== EXECUTE =====
def execute(amount):
    nonce = w3.eth.get_transaction_count(account.address)

    tx = contract.functions.swap().build_transaction({
        "from": account.address,
        "value": w3.to_wei(amount, "ether"),
        "nonce": nonce,
        "gas": 300000,
        "gasPrice": w3.to_wei("80", "gwei"),
        "chainId": 1336
    })

    signed_tx = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)

    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)

    print("TX:", tx_hash.hex())
# ===== MAIN LOOP =====
def run():
    global last_action

    while True:
        try:
            price = get_price()
            print("Price:", price)

            action = decide(price)

            if action == "buy":
                print("BUY 🚀")
                execute(0.1)
                last_action = "buy"

            elif action == "sell":
                print("SELL 💰")
                execute(0.005)
                last_action = "sell"

            time.sleep(30)

        except Exception as e:
            print("Error:", e)
            time.sleep(10)

if __name__ == "__main__":
    run()