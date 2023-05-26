import hashlib
import time

from signature import *
from sync import synchronize_chain, listen_for_requests

port = 8080
outro_host = '192.168.0.100'  # Endereço IP do outro nó
outro_port = 5000  # Porta em que o outro nó está escutando

class Transaction:
    def __init__(self, sender, recipient, amount):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.signature = None   

    def __str__(self):
        return f"Sender: {self.sender}, Recipient: {self.recipient}, Amount: {self.amount}, Signature: {self.signature}"


class Block:
    def __init__(self, index, timestamp, transactions, data, previous_hash, nonce=0):
        self.index = index
        self.timestamp = timestamp
        self.transactions = transactions
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash = self.calculate_hash()

    def __str__(self):
        transaction_details = "\n".join(str(transaction) for transaction in self.transactions)
        return f"Index: {self.index}\nTimestamp: {self.timestamp}\nTransactions:\n{transaction_details}\nHash: {self.hash}\nPrevious Hash: {self.previous_hash}"

    def calculate_hash(self):
        sha = hashlib.sha256()
        sha.update((str(self.index) + str(self.timestamp) + str(self.transactions) + str(self.previous_hash) + str(self.nonce)).encode('utf-8'))
        return sha.hexdigest()

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

# Iniciar a sincronização com outro nó na rede
blockchain.chain = synchronize_chain(outro_host, outro_port)

# Iniciar a escuta de solicitações de outros nós
listen_for_requests(port, blockchain)

transaction1 = Transaction("Bismuto", "Mafalda", 7)
transaction2 = Transaction("Saci", "Oracio", 3)
transaction3 = Transaction("Florentina", "Dolores", 0.5)

# Assinando as transações com a chave privada
sign_transaction(transaction1, private_key)
sign_transaction(transaction2, private_key)
sign_transaction(transaction3, private_key)

# Verificando a assinatura das transações com a chave pública
print("Verifying transaction signatures...")
print("Transaction 1 signature:", verify_signature(transaction1, public_key))
print("Transaction 2 signature:", verify_signature(transaction2, public_key))
print("Transaction 3 signature:", verify_signature(transaction3, public_key))

# Adicionando as transações pendentes
blockchain.add_transaction(transaction1)
blockchain.add_transaction(transaction2)
blockchain.add_transaction(transaction3)

# Mineração das transações pendentes
print("\nMinerando blocos...")
blockchain.mine_pending_transactions("Miner")

# Verificação da cadeia
print("Validade da cadeia:", blockchain.is_chain_valid())

for block in blockchain.chain:
    print(f"\nÍndice: {block.index}")
    print(f"Timestamp: {block.timestamp}")
    print("Transactions:")
    for transaction in block.transactions:
        print(transaction)
    print(f"Hash: {block.hash}")
    print(f"Previous Hash: {block.previous_hash}")