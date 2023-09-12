import time
import hashlib

class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_genesisblock()

    def create_genesisblock(self):
        # Creates the genesis block. Will not be used otherwise
        genesis = Block([])
        genesis.height = 0
        # The previous hash is set to 0 since there is no previous block
        genesis.prev_hash = "0"
        genesis.height = 0
        genesis.nonce = 0

        # Hashing of genesis block
        hashed_data = ""
        nonce = 0
        while hashed_data[:4] != "0000":
            data = str(genesis.timestamp) + str(nonce)
            hashed_data = hashlib.sha256(data.encode()).hexdigest()
            nonce+=1

        genesis.nonce = nonce
        genesis.hash = hashed_data
        
        self.chain.append(genesis)
    
    def addblock(self, transactions):
        # Adds a block to the blockchain and generates it's hash value
        new_block = Block(transactions)
        new_block.hash = self.add_hash(new_block)
        new_block.height = self.get_blockchain_height()+1
        self.chain.append(new_block)
        
        print()
        print(f" --- Added block with height {self.get_blockchain_height()} --- ")
        print()

    def add_hash(self, block):
        # Hashing
        hashed_data = ""
        prev_hash = self.get_prev_hash()

        nonce = 0
        # Loops though nonce values starting from zero until it finds the correct one
        while hashed_data[:4] != "0000":
            data = str(block.timestamp) + str(block.transactions) + str(prev_hash) + str(nonce)
            hashed_data = hashlib.sha256(data.encode()).hexdigest()
            #print(nonce, " - ", hashed_data[:4])
            nonce+=1

        block.nonce = nonce
        block.prev_hash = prev_hash

        return hashed_data
    
    def get_blockchain_height(self):
        return len(self.chain)-1

    def get_prev_hash(self):
        return self.chain[-1].hash
    
    def print_latest_block(self):
        return self.chain[-1].printself()
    
    def display_all(self):
        for i in self.chain:
            i.printself()
            print()


class Block:
    def __init__(self, transactions, hash = "", prev_hash = ""):
        # Many of these variables have null values becuase they are unknown at the moment
        self.timestamp = time.ctime()
        self.transactions = transactions
        self.hash = None
        self.prev_hash = None
        self.nonce = None
        self.height = None

    def printself(self):
        print("Timestamp:", self.timestamp)
        print("Transactions:", self.transactions)
        print("Height:", self.height)
        print("Hash:", self.hash)
        print("Previous hash:", self.prev_hash)
        print("Nonce", self.nonce)
        print()

def add_transaction():
    global transactions
    sender = input("Sender: ")
    recipient = input("Recipient: ")

    # Error handling for the amount. Makes sure amount is a number
    while True:
        amount = input("Amount: ")
        try:
            float(amount)
            transactions.append((sender, recipient, amount))
            print("Transaction added!")
            print()
            break
        except ValueError:
            print("Invalid input. Amount mist be a number")

# Main function containing the control panel
def main():
    ThorsteinCoin = Blockchain()

    # The loop makes sure the program always runs
    while True:
        print(""" --- Blockchain control panel ---
1 - Add a transaction
2 - View transactions
3 - Create a block containing unconfirmed transactions
4 - View the lastest block
5 - Display the blockchain
6 - Exit
        """)

        choice = input(">")
        if choice not in ("1", "2", "3", "4", "5", "6"):
            print("Invalid input")
            continue
        elif choice == "1":
            global transactions
            add_transaction()
            #print(transactions)
        elif choice == "2":
            if not transactions:
                print("There are no transactions!")
                print()
                continue
            print("Pool ofnconfirmed transactions:")
            for i in transactions:
                print(i)
            print()
        elif choice == "3":
            ThorsteinCoin.addblock(transactions)
            ThorsteinCoin.print_latest_block()
            transactions = []
        elif choice == "4":
            ThorsteinCoin.print_latest_block()
        elif choice == "5":
            ThorsteinCoin.display_all()
        elif choice == "6":
            return



transactions = []

if __name__ == "__main__":
    main()