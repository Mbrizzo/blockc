import hashlib
import time

class Block:
    def __init__(self, index, timestamp, data, previous_hash, nonce):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = nonce

    def calculate_hash(self):
        sha = hashlib.sha256()
        sha.update((str(self.index) + str(self.timestamp) + str(self.data) + str(self.previous_hash) + str(self.nonce)).encode('utf-8'))
        return sha.hexdigest()

# teste
block = Block(1, '2023-05-24 00:00:00', 'Dados do bloco', 'hash_anterior', 12345)

# Calcular o hash do bloco
hash_result = block.calculate_hash()

print(hash_result)