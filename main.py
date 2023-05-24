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
    
    #  valor de nonce será acrescido ao bloco quando a condição da mineração seja satisfeita.
    def mine_block(self, difficulty):
        target = '0' * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()


class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.difficulty = 4

    def create_genesis_block(self):
        return Block(0, time.time(), "Genesis Block", "0")

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, new_block):
        new_block.previous_hash = self.get_latest_block().hash
        new_block.mine_block(self.difficulty)
        new_block.hash = new_block.calculate_hash()
        self.chain.append(new_block)

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            if current_block.hash != current_block.calculate_hash():
                return False
            if current_block.previous_hash != previous_block.hash:
                return False
        return True

blockchain = Blockchain()

print("Mineração do bloco 1...")
block1 = Block(1, time.time(), "Red", "")
blockchain.add_block(block1)

print("Mineração do bloco 2...")
block2 = Block(2, time.time(), "Green", "")
blockchain.add_block(block2)

print("Mineração do bloco 3...")
block1 = Block(1, time.time(), "Blue", "")
blockchain.add_block(block1)

print("Mineração do bloco 4...")
block2 = Block(2, time.time(), "Black", "")
blockchain.add_block(block2)

# Verifica a validade da cadeia
print("Validade da cadeia:", blockchain.is_chain_valid())

for block in blockchain.chain:
    print(f"Block {block.index}:")
    print(f"Timestamp: {block.timestamp}")
    print(f"Data: {block.data}")
    print(f"Nonce: {block.nonce}")
    print(f"Previous Hash: {block.previous_hash}")
    print(f"Hash: {block.hash}")
    print()