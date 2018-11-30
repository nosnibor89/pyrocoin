from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

from wallet import Wallet, WalletError
from blockchain import Blockchain, TransactionError


app = Flask(__name__)
wallet = Wallet()
blockchain = Blockchain(wallet.public_key)
CORS(app)


def __handle_node__(node, method):
    """ Handle nodes stored in blockchain

    Arguments:
        :node:  The node to handle
        :method: HTTP method we use to handle the action
    """
    action = 'added'
    if not node:
        response = {
            'message': 'Incorrect or bad formed input provided',
        }

        return jsonify(response), 400

    if method == 'POST':
        blockchain.add_peer_node(node)
    else:
        blockchain.remove_peer_node(node)
        action = 'removed'

    response = {
        'message': f'Node {action} successfuly',
        'nodes': blockchain.nodes,
    }

    return jsonify(response), 200


@app.route('/', methods=['GET'])
def get_ui():
    return send_from_directory('ui', 'node.html')

@app.route('/network', methods=['GET'])
def get_network_ui():
    return send_from_directory('ui', 'network.html')


@app.route('/transaction', methods=['POST'])
def add_transaction():
    print(request)
    recipient = request.get_json()['recipient']
    amount = request.get_json()['amount']
    status = 400
    response = {
        'message': 'Incorrect or bad formed input provided',
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
            'funds': blockchain.get_balance(),
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
            'funds': blockchain.get_balance(),
        }
        return jsonify(response), 201

    response = {
        'message': 'Adding a block failed',
        'wallet_set_up': wallet.private_key != None,
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
            'funds': blockchain.get_balance(),
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
            'funds': blockchain.get_balance(),
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
        'funds': blockchain.get_balance(),
    }

    return jsonify(response), 200


@app.route('/node', methods=['POST'])
def add_node():
    node = request.get_json()['node']
    return __handle_node__(node, request.method)


@app.route('/node/<node>', methods=['DELETE'])
def delete_node(node):
    return __handle_node__(node, request.method)


@app.route('/nodes', methods=['GET'])
def get_nodes():
    response = {
        'message': 'Nodes fetched',
        'nodes': blockchain.nodes,
    }

    return jsonify(response), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
