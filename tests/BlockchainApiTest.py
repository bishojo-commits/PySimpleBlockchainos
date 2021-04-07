import unittest
import requests
import json

from Blockchain import Blockchain


class BlockchainApiTest(unittest.TestCase):
    def setUp(self):
        self.API_BASE_URL = 'http://127.0.0.1:5000'
        self.API_PATH_MINE = '{}/mine'.format(self.API_BASE_URL)
        self.API_PATH_CHAIN = '{}/chain'.format(self.API_BASE_URL)
        self.API_PATH_TX_NEW = '{}/transactions/new'.format(self.API_BASE_URL)

        self.blockchain = Blockchain()

    def test_mining_endpoint_status_ok(self):
        response = requests.get(self.API_PATH_MINE)

        self.assertEqual(response.status_code, 200)

    def test_mining_endpoint_contains_message(self):
        response = requests.get(self.API_PATH_MINE)
        response_content = json.loads(response.text)

        self.assertEqual(response_content['message'], 'New block forged')

    def test_new_transaction_endpoint_status_for_missing_params(self):
        request_body = {"recipient": "test", "amount": "60"}
        response = requests.post(self.API_PATH_TX_NEW, "", request_body)

        self.assertEqual(response.status_code, 400)

    def test_new_transaction_endpoint_tx_created_ok(self):
        request_body = {"sender": "Bob", "recipient": "Alice", "amount": "60"}
        response = requests.post(self.API_PATH_TX_NEW, "", request_body)

        self.assertEqual(response.status_code, 201)

    def test_mining_endpoint_creates_new_block(self):
        response = requests.get(self.API_PATH_MINE)
        response_chain = requests.get(self.API_PATH_CHAIN)

        response_content = json.loads(response.text)
        response_chain_content = json.loads(response_chain.text)

        last_block = response_chain_content['last_block']

        self.assertEqual(response_content['index'], last_block['index'])

    def test_mining_endpoint_creates_block_with_current_transaction(self):
        request_body = {"sender": "Bob", "recipient": "Alice", "amount": "30"}

        requests.post(self.API_PATH_TX_NEW, "", request_body)
        requests.get(self.API_PATH_MINE)

        response_chain = requests.get(self.API_PATH_CHAIN)
        response_chain_content = json.loads(response_chain.text)

        last_block = response_chain_content['last_block']

        self.assertEqual(last_block['transactions'][0]['sender'], "Bob")

