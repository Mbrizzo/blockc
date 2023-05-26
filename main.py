import hashlib
import time
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes

class Transaction:
    def __init__(self, sender, recipient, amount):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.signature = None

    def sign_transaction(self, private_key):
        message = f"{self.sender}{self.recipient}{self.amount}".encode('utf-8')
        self.signature = private_key.sign(message, padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH), hashes.SHA256())

    def verify_signature(self, public_key):
        message = f"{self.sender}{self.recipient}{self.amount}".encode('utf-8')
        try:
            public_key.verify(self.signature, message, padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH), hashes.SHA256())
            return True
        except:
            return False

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


# Generating  keys
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048
)
public_key = private_key.public_key()

# Converting keys to PEM format
private_pem = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
)
public_pem = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

# The private key is being printed only for the purpose of viewing and verifying that the code works. In a real environment, this information must be stored securely.
print("Private Key:") 
print(private_pem.decode())
print("\nPublic Key:")
print(public_pem.decode())

blockchain = Blockchain()

transaction1 = Transaction("Bismuto", "Mafalda", 7)
transaction2 = Transaction("Saci", "Oracio", 3)
transaction3 = Transaction("Florentina", "Dolores", 0.5)

# Signing transactions with the private key
transaction1.sign_transaction(private_key)
transaction2.sign_transaction(private_key)
transaction3.sign_transaction(private_key)

# Verifying the signature of transactions with the public key
print("Verifying transaction signatures...")
print("Transaction 1 signature:", transaction1.verify_signature(public_key))
print("Transaction 2 signature:", transaction2.verify_signature(public_key))
print("Transaction 3 signature:", transaction3.verify_signature(public_key))

blockchain.add_transaction(transaction1)
blockchain.add_transaction(transaction2)
blockchain.add_transaction(transaction3)

print("\nMinerando blocos...")
blockchain.mine_pending_transactions("Miner")

print("Validade da cadeia:", blockchain.is_chain_valid())

for block in blockchain.chain:
    print(f"\nÍndice: {block.index}")
    print(f"Timestamp: {block.timestamp}")
    print("Transactions:")
    for transaction in block.transactions:
        print(transaction)
    print(f"Hash: {block.hash}")
    print(f"Previous Hash: {block.previous_hash}")
