import hashlib
import datetime


class Block:
    def __init__(self, index, data, previous_hash):
        self.index = index
        self.timestamp = str(datetime.datetime.now())
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.mine_block()

    def calculate_hash(self):
        block_string = (
            str(self.index)
            + self.timestamp
            + self.data
            + self.previous_hash
            + str(self.nonce)
        )
        return hashlib.sha256(block_string.encode()).hexdigest()

    def mine_block(self, difficulty=4):
        target = "0" * difficulty

        while True:
            hash_value = self.calculate_hash()

            if hash_value.startswith(target):
                return hash_value

            self.nonce += 1


class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block(0, "Genesis Block", "0")

    def add_block(self, data):
        previous_block = self.chain[-1]

        new_block = Block(
            len(self.chain),
            data,
            previous_block.hash
        )

        self.chain.append(new_block)

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]

            if current.hash != current.calculate_hash():
                return False

            if current.previous_hash != previous.hash:
                return False

        return True


blockchain = Blockchain()

blockchain.add_block("Alice pays Bob 10 BTC")
blockchain.add_block("Bob pays Charlie 5 BTC")
blockchain.add_block("Charlie pays David 2 BTC")

print("\nBLOCKCHAIN\n")

for block in blockchain.chain:
    print(f"Block {block.index}")
    print("Data:", block.data)
    print("Nonce:", block.nonce)
    print("Hash:", block.hash)
    print("Previous Hash:", block.previous_hash)
    print("-" * 50)

print("Blockchain Valid:", blockchain.is_chain_valid())

print("\nTampering with Block 1...\n")

blockchain.chain[1].data = "Alice pays Bob 1000 BTC"

print("Blockchain Valid:", blockchain.is_chain_valid())