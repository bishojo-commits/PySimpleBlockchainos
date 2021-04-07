import hashlib
import json
import unittest

from Blockchain import Blockchain


class BlockchainTest(unittest.TestCase):
    def setUp(self):
        self.blockchain = Blockchain()

    def test_genesis_block_created(self):
        length = len(self.blockchain.chain)

        self.assertEqual(length, 1)

    def test_can_create_new_block(self):
        block = self.blockchain.new_block(3, 100)
        created_block = self.blockchain.chain.pop(1)

        self.assertEqual(block['proof'], created_block['proof'])

    def test_block_is_hashed(self):
        block = self.blockchain.new_block(7, 100)

        block_string = json.dumps(block, sort_keys=True).encode()
        hashed_block = hashlib.sha256(block_string).hexdigest()

        self.assertEqual(hashed_block, self.blockchain.hash(block))

    def test_last_block_retrieved(self):
        block = self.blockchain.new_block(9, 100)
        last_block = self.blockchain.last_block

        self.assertEqual(block, last_block)

    def test_new_transaction_created(self):
        self.blockchain.new_transaction("Bob", "Alice", 80000)
        transaction_created = self.blockchain.current_transactions.pop(0)

        self.assertEqual("Bob", transaction_created['sender'])

    def test_proof_of_work_returns_digit(self):
        proof = self.blockchain.proof_of_work(0)

        self.assertEquals(69732, proof)

    def test_valid_proof_varifies_correctly_to_false(self):
        is_valid = self.blockchain.valid_proof(5997989, 6868)

        self.assertFalse(is_valid)

    def test_valid_proof_varifies_correctly_to_true(self):
        proof = self.blockchain.proof_of_work(0)
        is_valid = self.blockchain.valid_proof(0, proof)

        self.assertTrue(is_valid)

