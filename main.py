import hashlib
import time
class Transaction:
    def __init__(self, sender, recipient, amount):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
class Block:
    def __init__(self, index, timestamp, transactions, data, previous_hash, nonce=0):
        self.index = index
        self.timestamp = timestamp
        self.transactions = transactions
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        sha = hashlib.sha256()
        sha.update((str(self.index) + str(self.timestamp) + str(self.transactions) + str(self.previous_hash) + str(self.nonce)).encode('utf-8'))
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
        self.pending_transactions = []

    def create_genesis_block(self):
        return Block(0, time.time(), [], "Genesis Block", "0", nonce=0)

    def get_latest_block(self):
        return self.chain[-1]

    def add_transaction(self, transaction):
        self.pending_transactions.append(transaction)

    def mine_pending_transactions(self, miner_address):
        previous_hash = self.get_latest_block().hash
        block = Block(len(self.chain), time.time(), self.pending_transactions, "Block data", previous_hash, nonce=0)
        block.mine_block(self.difficulty)
        self.chain.append(block)
        self.pending_transactions = []

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

transaction1 = Transaction("Bismuto", "Mafalda", 7)
transaction2 = Transaction("Saci", "Oracio", 3)
transaction3 = Transaction("Florentina", "Dolores", 0.5)

# Adição das transações pendentes
blockchain.add_transaction(transaction1)
blockchain.add_transaction(transaction2)
blockchain.add_transaction(transaction3)

# Mineração das transações pendentes
print("Minerando blocos...")
blockchain.mine_pending_transactions("Miner")

# Verificação da cadeia
print("Validade da cadeia:", blockchain.is_chain_valid())

for block in blockchain.chain:
    print(f"Índice: {block.index}")
    print(f"Timestamp: {block.timestamp}")
    print(f"Transactions: {block.transactions}")
    print(f"Hash: {block.hash}")
    print(f"Previous Hash: {block.previous_hash}\n")