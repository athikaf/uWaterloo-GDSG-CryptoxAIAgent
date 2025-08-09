from web3 import Web3
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize Web3 connection using Avalanche Fuji C-Chain URL
fuji_url = f'https://avalanche-fuji.infura.io/v3/bbbfbb452049447eaf52c4cc6e48efaf'  # Use Avalanche Fuji C-Chain URL
w3 = Web3(Web3.HTTPProvider(fuji_url))

# Check if the connection is successful
if not w3.is_connected():
    print("Connection failed. Check your Avalanche Fuji API key and network status.")
    exit()

# Define wallet address and private key (from environment variables)
wallet_address = os.getenv("WALLET_ADDRESS")  # Wallet address from .env
private_key = os.getenv("PRIVATE_KEY")  # Private key from .env

# Function to check wallet balance
def check_balance(wallet_address):
    return w3.eth.get_balance(wallet_address)

# Basic Autonomous Agent class
class AutonomousAgent:
    def __init__(self, wallet_address):
        self.wallet_address = wallet_address
    
    def make_decision(self):
        balance = check_balance(self.wallet_address)
        print(f"Wallet balance: {w3.from_wei(balance, 'ether')} AVAX")
        
        # Condition: If balance is greater than 0.000001 AVAX, perform a transaction
        if balance > w3.to_wei(0.000001, 'ether'):
            print("Balance is sufficient. Initiating transaction...")
            self.execute_transaction()
        else:
            print("Not enough balance to execute a transaction.")
    
    def execute_transaction(self):
        # Create a transaction to send AVAX (for demonstration, we're sending 0.000001 AVAX)
        tx = {
            'to': os.getenv("RECIPIENT_WALLET_ADDRESS"),  # Recipient wallet address from .env
            'value': w3.to_wei(0.000001, 'ether'),  # Transaction amount (0.000001 AVAX)
            'gas': 2000000,  # Gas limit
            'gasPrice': w3.to_wei('20', 'gwei'),  # Gas price (adjust as necessary)
            'nonce': w3.eth.get_transaction_count(self.wallet_address),
             'chainId': 43113  # EIP-155 Replay Protection for Avalanche Fuji C-Chain
        }

        # Sign the transaction with your private key
        signed_tx = w3.eth.account.sign_transaction(tx, private_key)

        # Send the transaction
        tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        print(f"Transaction sent. TX Hash: {tx_hash.hex()}")

# Initialize and run the AI agent
agent = AutonomousAgent(wallet_address)
agent.make_decision()
