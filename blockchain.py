import functools
import json
import pickle
import requests
from collections import OrderedDict

from utility import hash_util
from utility.verification import Verification
from block import Block
from transaction import Transaction
from wallet import Wallet

MINING_REWARD = 10


class TransactionError(Exception):
    def __init__(self, message='Error adding transaction'):
        # Call the base class constructor with the parameters it needs
        super().__init__(message)


class BlockError(Exception):
    def __init__(self, message='Error adding a block'):
        # Call the base class constructor with the parameters it needs
        super().__init__(message)


class Blockchain:
    def __init__(self, public_key, node_id):
        # Initialize blockchain list
        self.public_key = public_key
        self.__peer_nodes = set()
        self.node_id = node_id
        self.resolve_conflicts = False

        self.get_genesis_block_and_transactions()
        self.load_data()

    def format_transactions(self, transactions):
        return [
            Transaction(tx['sender'], tx['recipient'],
                        tx['amount'], tx['signature'])
            for tx in transactions
        ]

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

    def add_peer_node(self, node):
        """ Add a new node to the peer_node set

        Arguments:
            :node: The node URL which should be added.
        """
        self.__peer_nodes.add(node)
        self.save_data()

    def remove_peer_node(self, node):
        """ Removes a node from the peer_node set

        Arguments:
            :node: The node URL which should be removed.
        """
        self.__peer_nodes.discard(node)
        self.save_data()

    @property
    def nodes(self):
        """ Return list of connected peer_node """
        return list(self.__peer_nodes)

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
            with open(f'blockchain-{self.node_id}.txt') as file:
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
                    json.loads(file_content[1][:-1]))

                peer_nodes = json.loads(file_content[2])
                self.__peer_nodes = set(peer_nodes)

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
            with open(f'blockchain-{self.node_id}.txt', mode='w') as file:
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
                file.write('\n')
                json.dump(list(self.__peer_nodes), file)
        except IOError:
            print('Saving failed!')

    def proof_of_work(self):
        last_block = self.__chain[-1]
        last_hash = hash_util.hash_block(last_block)
        proof = 0
        while not Verification.valid_proof(
                self.__open_tansactions,
                last_hash,
                proof):
            proof += 1

        return proof

    def get_balance(self, sender=None):
        sent = 0
        received = 0
        participant = self.public_key

        if sender:
            participant = sender

        tx_sender = [[tx.amount for tx in block.transactions
                      if tx.sender == participant] for block in self.__chain]

        open_tx_sender = [tx.amount
                          for tx in self.__open_tansactions
                          if tx.sender == participant]

        tx_sender.append(open_tx_sender)
        tx_recipient = [[tx.amount for tx in block.transactions
                         if tx.recipient == participant]
                        for block in self.__chain]

        sent = functools.reduce(lambda tx_sum, tx: tx_sum +
                                sum(tx) if len(tx) > 0 else tx_sum + 0,
                                tx_sender,
                                0)
        received = functools.reduce(
            lambda tx_sum, tx: tx_sum + sum(tx) if len(tx) > 0 else tx_sum + 0,
            tx_recipient,
            0)

        return received - sent

    def get_last_blockchain_value(self):
        """ Return the last value of the current blockchain."""
        if len(self.__chain) >= 1:
            return self.__chain[-1]
        return [1]

    def add_transaction(self,
                        recipient,
                        sender,
                        signature,
                        amount=1.0,
                        is_receiving=False):
        """ Return the last value of the current blockchain.
            Arguments:
                :sender: The sender of the coins
                :recipient: The recipient of the coins
                :amount: Amount of coins. Default to 1.0
        """

        transaction = Transaction(sender, recipient, amount, signature)

        if not Verification.verify_transaction(transaction, self.get_balance):
            raise TransactionError()

        self.__open_tansactions.append(transaction)

        self.save_data()

        if not is_receiving:
            for node in self.__peer_nodes:
                try:
                    self.__broadcast_transaction__(node, transaction)
                except (
                        requests.exceptions.ConnectionError,
                        TransactionError) as error:
                    print(error)
                    continue

        return transaction

    def mine_block(self):
        last_block = self.__chain[-1]
        hashed_block = hash_util.hash_block(last_block)
        proof = self.proof_of_work()
        reward_tx = Transaction(
            'MINING', self.public_key, MINING_REWARD, '')

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

        # if not is_receiving:
        for node in self.__peer_nodes:
            try:
                self.__broadcast_block__(node, block)
            except (requests.exceptions.ConnectionError, BlockError) as error:
                print(error)
                continue

        return block

    def add_block(self, block):
        transactions = [Transaction(
            tx['sender'], tx['recipient'], tx['amount'], tx['signature'])
            for tx in block['transactions']]

        proof_is_valid = Verification.valid_proof(
            transactions[:-1], block['previous_hash'], block['proof'])

        hashes_match = hash_util.hash_block(
            self.chain[-1]) == block['previous_hash']

        if not proof_is_valid or not hashes_match:
            raise BlockError()

        current_block = Block(block['index'], block['previous_hash'],
                              transactions, block['proof'], block['timestamp'])

        self.__chain.append(current_block)
        stored_transactions = self.__open_tansactions[:]

        for itx in block['transactions']:
            for opentx in stored_transactions:
                if (opentx.sender == itx['sender']
                    and opentx.recipient == itx['recipient']
                    and opentx.amount == itx['amount']
                        and opentx.signature == itx['signature']):
                    try:
                        self.__open_tansactions.remove(opentx)
                    except ValueError:
                        print('items was already remove')
                        continue

        self.save_data()

    def resolve(self):
        winner_chain = self.chain
        replace = False
        for node in self.__peer_nodes:
            try:
                url = f'http://{node}/chain'
                response = requests.get(url)
                node_chain = response.json()
                node_chain = [Block(
                    block['index'],
                    block['previous_hash'],
                    [Transaction(tx['sender'], tx['recipient'], tx['amount'],
                                 tx['signature'])
                     for tx in block['transactions']],
                    block['proof'],
                    block['timestamp'])
                    for block in node_chain]

                node_chain_length = len(node_chain)
                local_chain_length = len(winner_chain)

                if (node_chain_length > local_chain_length and
                        Verification.verify_chain(node_chain)):
                    winner_chain = node_chain
                    replace = True

            except requests.exceptions.ConnectionError:
                continue

        self.resolve_conflicts = False
        self.chain = winner_chain

        if replace:
            self.__open_tansactions = []

        self.save_data()

        return replace

    def __broadcast_transaction__(self, node, transaction):
        url = f'http://{node}/broadcast-transaction'
        response = requests.post(
            url,
            json={'sender': transaction.sender,
                  'recipient': transaction.recipient,
                  'amount': transaction.amount,
                  'signature': transaction.signature}
        )
        if response.status_code in [400, 500]:
            print('transaction declied, needs resolving')
            raise TransactionError()

    def __broadcast_block__(self, node, block):
        url = f'http://{node}/broadcast-block'

        dict_block = block.__dict__.copy()
        dict_block['transactions'] = [
            tx.__dict__ for tx in dict_block['transactions']]

        response = requests.post(
            url,
            json={'block': dict_block}
        )
        if response.status_code in [400, 500]:
            print('block declied, needs resolving')
            raise BlockError()

        if response.status_code == 409:
            self.resolve_conflicts = True
