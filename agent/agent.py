#!/usr/bin/env python3
"""
AI agent that re-balances AgentVault on Somnia every 5 min
- fetches on-chain state (current ratio)
- computes optimal ratio (simple mean-variance)
- computes novelty score (on-chain risk check)
- calls rebalance() via web3
"""
import os, time
from web3 import Web3

# --- ENV ---
RPC        = os.getenv("RPC", "https://devnet.somnia.network")
PRIV_KEY   = os.getenv("PK")
VAULT_ADDR = os.getenv("VAULT_ADDR")
# --- ABI ---
# (only need rebalance + ratioA funcs)
ABI = """
[
  {
    "inputs": [
      { "name": "_newRatioA", "type": "uint256" },
      { "name": "_noveltyScore", "type": "uint256" }
    ],
    "name": "rebalance",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "ratioA",
    "outputs": [{ "name": "", "type": "uint256" }],
    "stateMutability": "view",
    "type": "function"
  }
]
"""

# --- SETUP ---
w3 = Web3(Web3.HTTPProvider(RPC))
acct = w3.eth.account.from_key(PRIV_KEY)
vault = w3.eth.contract(address=VAULT_ADDR, abi=ABI)

def get_optimal_ratio():
    """
    Dummy ML model: 50% ± 10% based on block hash randomness.
    (Replace with actual mean-variance, risk, etc. model)
    """
    latest_block = w3.eth.get_block('latest')
    block_hash_int = int(latest_block.hash.hex(), 16)
    # Simple deterministic randomness from block hash
    return 5000 + (block_hash_int % 2000) - 1000  # Range: 4000-6000 bp

def main():
    """
    Main agent loop: fetch state, compute action, execute on-chain.
    """
    print(f"🤖 AI Agent started for vault: {VAULT_ADDR}")
    print(f"   -> Rebalancing as address: {acct.address}")

    while True:
        try:
            # 1. Fetch current on-chain state
            current_ratio = vault.functions.ratioA().call()
            print(f"\nFetched on-chain state. Current ratioA: {current_ratio} bp")

            # 2. Compute optimal new state (off-chain)
            new_ratio = get_optimal_ratio()
            print(f"Computed off-chain optimal ratio: {new_ratio} bp")

            # 3. Compute novelty score for on-chain check
            novelty_score = abs(new_ratio - current_ratio)
            print(f"Novelty score (on-chain risk check): {novelty_score} bp")

            # 4. Build and send transaction
            nonce = w3.eth.get_transaction_count(acct.address)
            tx_data = {
                'chainId': 52351,  # Somnia DevNet
                'from': acct.address,
                'nonce': nonce,
                'gas': 200_000,
                'gasPrice': w3.toWei('1', 'gwei'),
            }
            tx = vault.functions.rebalance(new_ratio, novelty_score).build_transaction(tx_data)

            signed_tx = w3.eth.account.sign_transaction(tx, private_key=PRIV_KEY)
            tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)

            print(f"✅ Rebalance submitted! Tx: {tx_hash.hex()}")
            print(f"   -> Waiting for receipt...")

            tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)
            if tx_receipt.status == 1:
                print("   -> ✅ Transaction successful!")
            else:
                print("   -> ❌ Transaction failed! Check explorer.")


        except Exception as e:
            print(f"❌ An error occurred: {e}")

        print("\n--- Sleeping for 5 minutes ---")
        time.sleep(300)

if __name__ == "__main__":
    main()
