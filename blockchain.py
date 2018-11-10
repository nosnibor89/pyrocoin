import functools
import json
import pickle
from collections import OrderedDict

import hash_util
from block import Block

# Initialize blockchain list
MINING_REWARD = 10
open_tansactions = []
owner = "Robinson"
participants = {'Robinson'}
blockchain = []


def format_transactions(transactions):
    return [
        OrderedDict([
                    ('sender', tx['sender']),
                    ('recipient', tx['recipient']),
                    ('amount', tx['amount'])
                    ]) for tx in transactions]


def get_genesis_block_and_transactions():
    global blockchain
    global open_tansactions
    genesis_block = Block(0, '', [], 100, 0)
    blockchain = []
    blockchain.append(genesis_block)

    open_tansactions = []


def load_data():
    # With picle
    # with open('blockchain.p', mode='rb') as file:
    #     file_content = pickle.loads(file.read())
    #     global blockchain
    #     global open_tansactions
    #     blockchain = file_content['chain']
    #     open_tansactions = file_content['ot']
    # ----------------------------------------------------------------------
    global blockchain
    global open_tansactions
    try:
        with open('blockchain.txt') as file:
            file_content = file.readlines()
            blockchain = json.loads(file_content[0][:-1])
            blockchain = [
                Block(
                    block['index'],
                    block['previous_hash'],
                    format_transactions(block['transactions']),
                    block['proof'],
                    block['timestamp']
                )
                for block in blockchain]

            open_tansactions = format_transactions(json.loads(file_content[1]))
    except (FileNotFoundError, IndexError):
        get_genesis_block_and_transactions()


def save_data():
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
            json.dump(blockchain, file)
            file.write('\n')
            json.dump(open_tansactions, file)
    except IOError:
        print('Saving failed!')


load_data()


def valid_proof(transactions, last_hash, proof):
    guess = (str(transactions) + str(last_hash) + str(proof)).encode()
    guess_hash = hash_util.hash_string_256(guess)
    print(guess_hash)
    return guess_hash[0:2] == '00'


def proof_of_work():
    last_block = blockchain[-1]
    last_hash = hash_util.hash_block(last_block)
    proof = 0
    while not valid_proof(open_tansactions, last_hash, proof):
        proof += 1

    return proof

def get_balance(participant):
    sent = 0
    received = 0

    tx_sender = [[tx['amount'] for tx in block.transactions
                  if tx['sender'] == participant] for block in blockchain]

    open_tx_sender = [tx['amount']
                      for tx in open_tansactions if tx['sender'] == participant]

    tx_sender.append(open_tx_sender)
    tx_recipient = [[tx['amount'] for tx in block.transactions
                     if tx['recipient'] == participant] for block in blockchain]

    sent = functools.reduce(lambda tx_sum, tx: tx_sum +
                            sum(tx) if len(tx) > 0 else tx_sum + 0, tx_sender, 0)
    received = functools.reduce(
        lambda tx_sum, tx: tx_sum + sum(tx) if len(tx) > 0 else tx_sum + 0, tx_recipient, 0)

    return received - sent


def get_last_blockchain_value():
    """ Return the last value of the current blockchain."""
    if len(blockchain) >= 1:
        return blockchain[-1]
    return [1]


def verify_transaction(transaction):
    sender_balance = get_balance(transaction['sender'])
    return sender_balance >= transaction['amount']


def add_transaction(recipient, amount=1.0, sender=owner):
    """ Return the last value of the current blockchain.
        Arguments:
            :sender: The sender of the coins
            :recipient: The recipient of the coins
            :amount: Amount of coins. Default to 1.0
    """

    transaction = OrderedDict([
        ('sender', sender),
        ('recipient', recipient),
        ('amount', amount)
    ])

    if verify_transaction(transaction):
        open_tansactions.append(transaction)
        participants.add(sender)
        participants.add(recipient)

        save_data()

        return True

    return False


def mine_block():
    last_block = blockchain[-1]
    hashed_block = hash_util.hash_block(last_block)
    proof = proof_of_work()
    reward_tx = OrderedDict([
        ('sender', 'MINING'),
        ('recipient', owner),
        ('amount', MINING_REWARD)
    ])

    copied_transactions = open_tansactions[:]
    copied_transactions.append(reward_tx)

    block = Block(len(blockchain), hashed_block, copied_transactions, proof)

    blockchain.append(block)
    return True


def get_transaction_value():
    """ Returns a tuple(tx_recipient, tx_amount) with the information for a transaction"""
    tx_recipient = input('Please, the name of the recipient: ')
    tx_amount = float(input('Your transaction amount please: '))

    # could be also like parethesis (tx_recipient, tx_amount)
    return tx_recipient, tx_amount


def get_user_choice():
    user_option = input('Your choice: ')
    return user_option


def print_blockchain_elements():
    # Output blockchain list to console
    for block in blockchain:
        print('Outputing Blocks:')
        print(block)


def verify_chain():
    """Verify is blockchain is correct"""
    for (index, block) in enumerate(blockchain):
        if index == 0:
            continue

        if block.previous_hash != hash_util.hash_block(blockchain[index-1]):
            return False

        if not valid_proof(block.transactions[:-1], block.previous_hash, block.proof):
            print('proof of work is invalid')
            return False

    return True


def verify_transactions():
    return all([verify_transaction(tx) for tx in open_tansactions])


def display_wrong_option_message():
    print('--------Input invalid, please pick a value from list--------')


waiting_for_input = True

while waiting_for_input:
    print('Please choose')
    print('1: Add new transaction value')
    print('2: Mine block')
    print('3: Output blockchain blocks')
    print('4: Output participants')
    print('5: Check transaction validity')
    print('Q: Exit the program')
    option = get_user_choice()

    try:
        if option.isnumeric() and int(option) == 1:
            recipient, amount = get_transaction_value()
            if add_transaction(recipient, amount):
                print('Added transaction')
            else:
                print('Transaction Fail')
        elif option.isnumeric() and int(option) == 2:
            if mine_block():
                open_tansactions = []
                save_data()
        elif option.isnumeric() and int(option) == 3:
            print_blockchain_elements()
        elif option.isnumeric() and int(option) == 4:
            print(participants)
        elif option.isnumeric() and int(option) == 5:
            if verify_transactions():
                print('All transactions are valid!')
            else:
                print('There are invalid transactions!')
        elif option == 'Q' or option == 'q':
            waiting_for_input = False
        else:
            display_wrong_option_message()

        if not verify_chain():
            print('Invalid blockchain!')
            break

        print(f'Balance of {owner}: {get_balance(owner):6.2f}')

    except ValueError:
        display_wrong_option_message()

else:
    print('User left')


print('Done!')

print(blockchain)
