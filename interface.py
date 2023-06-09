import hashlib
import time
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes
import tkinter as tk


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


def generate_keys():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    public_key = private_key.public_key()

    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    private_key_text.delete("1.0", tk.END)
    private_key_text.insert(tk.END, private_pem.decode())

    public_key_text.delete("1.0", tk.END)
    public_key_text.insert(tk.END, public_pem.decode())


def sign_transaction():
    private_key_pem = private_key_text.get("1.0", tk.END)
    private_key = serialization.load_pem_private_key(private_key_pem.encode(), password=None)
    transaction = Transaction(sender_entry.get(), recipient_entry.get(), amount_entry.get())
    transaction.sign_transaction(private_key)
    signature_entry.delete(0, tk.END)
    signature_entry.insert(tk.END, transaction.signature)


def verify_signature():
    public_key_pem = public_key_text.get("1.0", tk.END)
    public_key = serialization.load_pem_public_key(public_key_pem.encode())
    transaction = Transaction(sender_entry.get(), recipient_entry.get(), amount_entry.get())
    signature = signature_entry.get()
    transaction.signature = signature.encode()
    is_valid = transaction.verify_signature(public_key)
    result_label.config(text="Valid" if is_valid else "Invalid")


root = tk.Tk()
root.title("Transaction Signature")
root.geometry("400x300")

label_frame = tk.LabelFrame(root, text="Transaction Details")
label_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

sender_label = tk.Label(label_frame, text="Sender:")
sender_label.grid(row=0, column=0, sticky="e")
sender_entry = tk.Entry(label_frame)
sender_entry.grid(row=0, column=1)

recipient_label = tk.Label(label_frame, text="Recipient:")
recipient_label.grid(row=1, column=0, sticky="e")
recipient_entry = tk.Entry(label_frame)
recipient_entry.grid(row=1, column=1)

amount_label = tk.Label(label_frame, text="Amount:")
amount_label.grid(row=2, column=0, sticky="e")
amount_entry = tk.Entry(label_frame)
amount_entry.grid(row=2, column=1)

generate_keys_button = tk.Button(root, text="Generate Keys", command=generate_keys)
generate_keys_button.pack(pady=5)

private_key_label = tk.Label(root, text="Private Key:")
private_key_label.pack()
private_key_text = tk.Text(root, height=6, width=40)
private_key_text.pack()

public_key_label = tk.Label(root, text="Public Key:")
public_key_label.pack()
public_key_text = tk.Text(root, height=6, width=40)
public_key_text.pack()

sign_button = tk.Button(root, text="Sign Transaction", command=sign_transaction)
sign_button.pack(pady=5)

verify_button = tk.Button(root, text="Verify Signature", command=verify_signature)
verify_button.pack(pady=5)

signature_label = tk.Label(root, text="Signature:")
signature_label.pack()
signature_entry = tk.Entry(root)
signature_entry.pack()

result_label = tk.Label(root, text="")
result_label.pack(pady=5)

root.mainloop()
