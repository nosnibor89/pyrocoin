import functools
import json
import pickle
from collections import OrderedDict

from utility import hash_util
from utility.verification import Verification
from block import Block
from transaction import Transaction
from wallet import Wallet

MINING_REWARD = 10


class Blockchain:
    def __init__(self, hosting_node_id):
        # Initialize blockchain list
        # self.__chain = []
        # self.__open_tansactions = []
        self.get_genesis_block_and_transactions()
        self.load_data()
        self.hosting_node_id = hosting_node_id

    def format_transactions(self, transactions):
        return [Transaction(tx['sender'], tx['recipient'], tx['amount'], tx['signature']) for tx in transactions]

    def get_genesis_block_and_transactions(self):
        genesis_block = Block(0, '', [], 100, 0)
        self.__chain = []
        self.__chain.append(genesis_block)

        self.__open_tansactions = []

    @property
    def chain(self):
        return self.__chain[:]

    @chain.setter
    def chain(self, val):
        self.__chain = val

    @property
    def open_tansactions(self):
        return self.__open_tansactions[:]

    @open_tansactions.setter
    def open_tansactions(self, val):
        self.__open_tansactions = val

    def load_data(self):
        # With picle
        # with open('blockchain.p', mode='rb') as file:
        #     file_content = pickle.loads(file.read())
        #     global blockchain
        #     global open_tansactions
        #     blockchain = file_content['chain']
        #     open_tansactions = file_content['ot']
        # ----------------------------------------------------------------------
        try:
            with open('blockchain.txt') as file:
                file_content = file.readlines()
                blockchain = json.loads(file_content[0][:-1])
                self.chain = [
                    Block(
                        block['index'],
                        block['previous_hash'],
                        self.format_transactions(block['transactions']),
                        block['proof'],
                        block['timestamp']
                    )
                    for block in blockchain]

                self.open_tansactions = self.format_transactions(
                    json.loads(file_content[1]))
        except (FileNotFoundError, IndexError, json.decoder.JSONDecodeError):
            print('Error lading file')

    def save_data(self):
        # With pickle
        # with open('blockchain.p', mode='wb') as file:
        #     save_data = {
        #         'chain': blockchain,
        #         'ot': open_tansactions
        #     }
        #     file.write(pickle.dumps(save_data))
        # ----------------------------------------
        try:
            with open('blockchain.txt', mode='w') as file:
                formatted_chain = [
                    block.__dict__ for block in [
                        Block(
                            b.index,
                            b.previous_hash,
                            [tx.__dict__ for tx in b.transactions],
                            b.proof,
                            b.timestamp
                        )
                        for b in self.__chain]
                ]
                formatted_transactions = [
                    tx.__dict__ for tx in self.__open_tansactions]
                json.dump(formatted_chain, file)
                file.write('\n')
                json.dump(formatted_transactions, file)
        except IOError:
            print('Saving failed!')

    def proof_of_work(self):
        last_block = self.__chain[-1]
        last_hash = hash_util.hash_block(last_block)
        proof = 0
        while not Verification.valid_proof(self.__open_tansactions, last_hash, proof):
            proof += 1

        return proof

    def get_balance(self):
        sent = 0
        received = 0
        participant = self.hosting_node_id

        tx_sender = [[tx.amount for tx in block.transactions
                      if tx.sender == participant] for block in self.__chain]

        open_tx_sender = [tx.amount
                          for tx in self.__open_tansactions if tx.sender == participant]

        tx_sender.append(open_tx_sender)
        tx_recipient = [[tx.amount for tx in block.transactions
                         if tx.recipient == participant] for block in self.__chain]

        sent = functools.reduce(lambda tx_sum, tx: tx_sum +
                                sum(tx) if len(tx) > 0 else tx_sum + 0, tx_sender, 0)
        received = functools.reduce(
            lambda tx_sum, tx: tx_sum + sum(tx) if len(tx) > 0 else tx_sum + 0, tx_recipient, 0)

        return received - sent

    def get_last_blockchain_value(self):
        """ Return the last value of the current blockchain."""
        if len(self.__chain) >= 1:
            return self.__chain[-1]
        return [1]

    def add_transaction(self, recipient, sender, signature, amount=1.0):
        """ Return the last value of the current blockchain.
            Arguments:
                :sender: The sender of the coins
                :recipient: The recipient of the coins
                :amount: Amount of coins. Default to 1.0
        """

        transaction = Transaction(sender, recipient, amount, signature)

        if not Verification.verify_transaction(transaction, self.get_balance):
            return False

        self.__open_tansactions.append(transaction)

        self.save_data()

        return True

    def mine_block(self):
        last_block = self.__chain[-1]
        hashed_block = hash_util.hash_block(last_block)
        proof = self.proof_of_work()
        reward_tx = Transaction(
            'MINING', self.hosting_node_id, MINING_REWARD, '')

        copied_transactions = self.open_tansactions
        for tx in copied_transactions:
            if not Wallet.verify_transaction(tx):
                return None

        copied_transactions.append(reward_tx)

        block = Block(len(self.__chain), hashed_block,
                      copied_transactions, proof)

        self.__chain.append(block)
        self.__open_tansactions = []
        self.save_data()
        return block


# print(blockchain)
