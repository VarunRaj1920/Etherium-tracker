"""
This script tracks deposits to the Ethereum 2.0
deposit contract and sends a Telegram notification for each new deposit.

It uses the Web3.py library to interact with the Ethereum blockchain,
and the requests library to send Telegram notifications.

The script also saves deposit details to a SQLite database.

Before running the script, make sure to install the required Python packages from requirements.txt:

pip install -r requirements.txt
"""

import os
import time
import logging
import json
import sqlite3
import requests

from web3 import Web3
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Initalize sqlite3 db
con = sqlite3.connect("eth_deposit.db")
cur = con.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS deposit (
  blockNumber BIGINT NOT NULL,
  blockTimestamp BIGINT NOT NULL,
  fee DECIMAL(38, 0) NOT NULL,
  hash VARCHAR(256) NOT NULL,
  pubkey VARCHAR(256) NOT NULL
)""")

# Initialize Web3
w3 = Web3(Web3.HTTPProvider(os.getenv('ETHEREUM_RPC_URL')))

# Beacon Deposit Contract address
DEPOSIT_CONTRACT_ADDRESS = os.getenv('BEACON_DEPOSIT_CONTRACT')

# # Telegram bot details
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')


class DepositTracker:
    """
    A class to track deposits to the Ethereum 2.0 deposit contract
    """

    def __init__(self):
        """
        Initializes the DepositTracker class
        """
        self.last_processed_block = self.get_last_processed_block()

    def __del__(self):
        """
        Destructor to close the database connection
        """
        con.close()

    def get_last_processed_block(self):
        """
        Get the last processed block number from the database.
        If no block number is found, it returns a block number 1000 blocks ago.
        """
        # In a production environment, you'd retrieve this from a database
        return w3.eth.get_block('latest')['number'] - 1000  # Start from 1000 blocks ago

    def track_deposits(self):
        """
        Track new deposits to the deposit contract.
        This function runs indefinitely and checks for new blocks every 15 seconds.
        """
        while True:
            try:
                current_block = w3.eth.get_block('latest')['number']
                if current_block > self.last_processed_block:
                    self.process_new_blocks(self.last_processed_block + 1, current_block)
                    self.last_processed_block = current_block
                time.sleep(15)  # Wait for 15 seconds before checking for new blocks
            except Exception as e:
                logger.error(f"Error in tracking deposits: {str(e)}")
                time.sleep(10)  # Wait for a minute before retrying

    def process_new_blocks(self, start_block, end_block):
        """
        Process new blocks to check for deposits
        :param start_block: The block number to start processing
        :param end_block: The block number to end processing
        """
        for block_number in range(start_block, end_block + 1):
            block = w3.eth.get_block(block_number, full_transactions=True)
            for tx in block['transactions']:
                if tx['to'] and tx['to'].lower() == DEPOSIT_CONTRACT_ADDRESS.lower():
                    self.process_deposit(tx, block)

    def process_deposit(self, tx, block):
        """
        Process a new deposit transaction
        :param tx: The transaction object
        :param block: The block object
        """

        deposit = {
            'blockNumber': block['number'],
            'blockTimestamp': block['timestamp'],
            'fee': tx['gas'] * tx['gasPrice'],
            'hash': tx['hash'].hex(),
            'pubkey': tx['input'][2:98]  # Extract pubkey from input data
        }
        self.save_deposit(deposit)
        self.send_alert(deposit)

    def save_deposit(self, deposit):
        """
        Save the deposit details to a database and log the details
        :param deposit: The deposit details
        """

        # In a production environment, you'd save this to a database
        logger.info(f"Saved deposit: {json.dumps(deposit, indent=2)}")

        cur.execute(f"""
            INSERT INTO deposit (blockNumber, blockTimestamp, fee, hash, pubkey) VALUES
            (?, ?, ?, ?, ?)
        """, (
            deposit['blockNumber'],
            deposit['blockTimestamp'],
            deposit['fee'],
            deposit['hash'],
            deposit['pubkey']
        ))

        con.commit()

    def send_alert(self, deposit):
        """
        Send an alert for the new deposit
        :param deposit: The deposit details
        """

        self.send_telegram_notification(deposit)
        # self.update_grafana_dashboard(deposit)

    def send_telegram_notification(self, deposit):
        """
        Send a Telegram notification for the new deposit
        :param deposit: The deposit details
        """

        message = f"New ETH deposit detected!\n\nBlock: {deposit['blockNumber']}\nAmount: {w3.fromWei(deposit['fee'], 'ether')} ETH\nTransaction: {deposit['hash']}"
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message
        }
        try:
            response = requests.post(url, json=payload, timeout=1000)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to send Telegram notification: {str(e)}")

    # def update_grafana_dashboard(self, deposit):
    #     # This is a simplified example. In a real-world scenario, you'd use a more robust method to update Grafana
    #     url = f"{GRAFANA_URL}/api/dashboards/db"
    #     headers = {
    #         "Authorization": f"Bearer {GRAFANA_API_KEY}",
    #         "Content-Type": "application/json"
    #     }
    #     payload = {
    #         "dashboard": {
    #             "id": None,
    #             "title": "ETH Deposits Dashboard",
    #             "panels": [
    #                 {
    #                     "id": 1,
    #                     "title": "Latest Deposit",
    #                     "type": "text",
    #                     "content": f"Block: {deposit['blockNumber']}\nAmount: {w3.from_wei(deposit['fee'], 'ether')} ETH\nTransaction: {deposit['hash']}"
    #                 }
    #             ]
    #         },
    #         "overwrite": True
    #     }
    #     try:
    #         response = requests.post(url, headers=headers, json=payload)
    #         response.raise_for_status()
    #     except requests.exceptions.RequestException as e:
    #         logger.error(f"Failed to update Grafana dashboard: {str(e)}")


if __name__ == "__main__":
    tracker = DepositTracker()
    tracker.track_deposits()
