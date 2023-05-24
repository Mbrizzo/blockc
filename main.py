import hashlib
import time

class Block:
    def __init__(self, index, timestamp, data, previous_hash, nonce=0):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        sha = hashlib.sha256()
        sha.update((str(self.index) + str(self.timestamp) + str(self.data) + str(self.previous_hash) + str(self.nonce)).encode('utf-8'))
        return sha.hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block(0, time.time(), "Genesis Block", "0")

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, new_block):
        new_block.previous_hash = self.get_latest_block().hash
        new_block.hash = new_block.calculate_hash()
        self.chain.append(new_block)

blockchain = Blockchain()

block1 = Block(1, time.time(), "Red", blockchain.get_latest_block().hash)
block2 = Block(2, time.time(), "Green", blockchain.get_latest_block().hash)
block3 = Block(3, time.time(), "Blue", blockchain.get_latest_block().hash)
block4 = Block(4, time.time(), "Black", blockchain.get_latest_block().hash)
block5 = Block(5, time.time(), "White", blockchain.get_latest_block().hash)

blockchain.add_block(block1)
blockchain.add_block(block2)
blockchain.add_block(block3)
blockchain.add_block(block4)
blockchain.add_block(block5)

for block in blockchain.chain:
    print(f"Block {block.index}:")
    print(f"Timestamp: {block.timestamp}")
    print(f"Data: {block.data}")
    print(f"Previous Hash: {block.previous_hash}")
    print(f"Hash: {block.hash}")
    print()