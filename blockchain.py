from flask import Flask, jsonify, request
import hashlib
import json
from time import time
from uuid import uuid4

NAME = 'UniCoin'
class Blockchain (object):
    def __init__(self):
        self.chain = []
        self.pending_transactions = []
        self.completed_blocks = 0

        # GENESIS BLOCK
        self.new_block(proof=100, previous_hash=1)

    def new_block(self, proof, previous_hash=None):

        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transaction': self.pending_transactions,
            'proof': proof,
            'previous_hash': previous_hash
        }

        self.pending_transactions = []
        self.completed_blocks += 1
        self.chain.append(block)
        return block

    def new_transaction(self, sender, recipient, amount, sender_message):
        transaction = (
            {
                'sender' : sender,
                'recipient' : recipient,
                'amount' : amount + NAME,
                'message' : sender_message

            }
        )
        self.pending_transactions.append(transaction)
        return self.last_block['index'] + 1

    def proof_of_work(self, previous_hash):
        proof = 0
        while self.valid_proof(previous_hash, proof) is False:
            proof += 1

    @staticmethod
    def valid_proof(self, last_proof, proof):

        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

    @staticmethod
    def last_block(self, block):

        return self.chain[-1]

    @property
    def hash(self, block):

        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()


blockchain = Blockchain()
app = Flask(__name__)

node_identifier = str(uuid4()).replace('-', '')

@app.route('/mine', methods=['GET'])
def mine(self):
    last_block = blockchain.last_block()
    last_proof = last_block['proof']
    proof = blockchain.proof_of_work(last_proof)

    blockchain.new_transaction(
        sender = '0',
        recipient = node_identifier,
        amount = 1000
    )

    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash)
    response = {
        'message' : 'New block added to the UniCoin Blockchain',
        'index' : block['index'],
        'transactions' : block['transactions'],
        'proof' : block['proof'],
        'previous_hash' : block['previous_hash']
    }
    return jsonify(response), 200

@app.route('transaction/new', methods=['POST'])
def new_transaction(self):
    values = request.get_json()

    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        raise ValueError("Missing Values")

    index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])

    response = {'message': f'Transaction will be added to Block {index}'}
    return jsonify(response), 200


@app.route('chain', methods=['GET'])
def full_chain(self):
    response = {
        'chain' : blockchain.chain,
        'chain_length' : len(blockchain.chain)
    }
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)