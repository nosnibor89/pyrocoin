"""Provide verification helper methods."""
from utility import hash_util

from wallet import Wallet

class Verification:

    @staticmethod
    def verify_transaction(transaction, get_balance, check_funds = True):
        if check_funds:
            sender_balance = get_balance()
            return sender_balance >= transaction.amount and Wallet.verify_transaction(transaction)

        return Wallet.verify_transaction(transaction)

    @staticmethod
    def valid_proof(transactions, last_hash, proof):
        guess = (str([tx.to_ordered_dict() for tx in transactions]) +
                 str(last_hash) + str(proof)).encode()
        guess_hash = hash_util.hash_string_256(guess)
        print(guess_hash)
        return guess_hash[0:2] == '00'

    @classmethod
    def verify_chain(cls, blockchain):
        """Verify is blockchain is correct"""
        for (index, block) in enumerate(blockchain):
            if index == 0:
                continue

            if block.previous_hash != hash_util.hash_block(blockchain[index-1]):
                return False

            if not cls.valid_proof(block.transactions[:-1], block.previous_hash, block.proof):
                print('proof of work is invalid')
                return False

        return True

    @classmethod
    def verify_transactions(cls, open_tansactions, get_balance):
        return all([cls.verify_transaction(tx, get_balance, False) for tx in open_tansactions])
