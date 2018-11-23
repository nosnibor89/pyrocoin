from flask import Flask, jsonify, request
from flask_cors import CORS

from wallet import Wallet, WalletError
from blockchain import Blockchain, TransactionError


app = Flask(__name__)
wallet = Wallet()
blockchain = Blockchain(wallet.public_key)
CORS(app)


@app.route('/', methods=['GET'])
def get_ui():
    return 'This works'


@app.route('/transaction', methods=['POST'])
def add_transaction():
    print(request)
    recipient = request.get_json()['recipient']
    amount = request.get_json()['amount']
    status = 400
    response = {
        'message': 'Incorrect or bad formed input provided'
    }
    global wallet

    if not recipient or not amount:
        return jsonify(response), status

    try:
        signature = wallet.sign_transaction(
            wallet.public_key, recipient, amount)
        transaction = blockchain.add_transaction(
            recipient, wallet.public_key, signature, amount)

        transaction_dict = transaction.to_ordered_dict()
        transaction_dict['signature'] = signature
        response = {
            'message': 'Transaction added succesfully',
            'transaction': transaction_dict,
            'funds': blockchain.get_balance()
        }
        status = 201
    except TransactionError as error:
        print(error)
        response = {
            'message': str(error)
        }
        status = 500
    finally:
        return jsonify(response), status


@app.route('/transactions', methods=['GET'])
def get_open_transactions():
    trans = [tx.to_ordered_dict() for tx in blockchain.open_tansactions]

    return jsonify(trans), 200


@app.route('/mine', methods=['POST'])
def mine():
    block = blockchain.mine_block()

    if block != None:
        dict_block = block.__dict__.copy()
        dict_block['transactions'] = [tx.__dict__.copy()
                                      for tx in dict_block['transactions']]
        response = {
            'message': 'Block added succesfully',
            'block': dict_block,
            'funds': blockchain.get_balance()
        }
        return jsonify(response), 201

    response = {
        'message': 'Adding a block failed',
        'wallet_set_up': wallet.private_key != None
    }
    return jsonify(response), 500


@app.route('/chain', methods=['GET'])
def get_chain():
    chain = blockchain.chain
    dict_chain = [block.__dict__.copy() for block in chain]

    for dict_block in dict_chain:
        dict_block['transactions'] = [tx.__dict__.copy()
                                      for tx in dict_block['transactions']]

    return jsonify(dict_chain), 200


@app.route('/wallet', methods=['POST'])
def create_keys():
    status = 500
    wallet.create_keys()

    try:
        wallet.save_keys()
        status = 201
        global blockchain
        blockchain = Blockchain(wallet.public_key)

        response = {
            'public_key': wallet.public_key,
            'private_key': wallet.private_key,
            'funds': blockchain.get_balance()
        }
    except WalletError as error:
        response = {
            'message': str(error)
        }
    finally:
        return jsonify(response), status


@app.route('/wallet', methods=['GET'])
def load_keys():
    status = 500
    try:
        wallet.load_keys()
        status = 200
        global blockchain
        blockchain = Blockchain(wallet.public_key)

        response = {
            'public_key': wallet.public_key,
            'private_key': wallet.private_key,
            'funds': blockchain.get_balance()
        }

    except WalletError as error:
        response = {
            'message': str(error)
        }
    finally:
        return jsonify(response), status


@app.route('/balance')
def get_balance():
    response = {
        'message': 'Balance fetched',
        'funds': blockchain.get_balance()
    }

    return jsonify(response), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
