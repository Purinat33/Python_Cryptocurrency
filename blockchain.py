#!/usr/bin/env python
# coding: utf-8

# # Dordcoin (Making blocks)

# ## Adding flask frontend



from hashlib import sha256




# Hash the block
def hashed_blocked(*args):
    
    hashing_func = "";
    h = sha256()
    for arg in args:
        hashing_func += str(arg)
        
    h.update(hashing_func.encode('utf-8'))
    return h.hexdigest()



class Block():
    # lists of transactions
    data = None
    
    hash = None
    nonce = 0 
    # Some arbituary number that will be used in POW later
    # (Proof-Of-Work) in crypto-mining etc.
    
    # Let first-most block have prev hash of all 0
    previous_hash = "0" * 64
    
    def __init__(self, data, block_number=0):
        self.data = data
        self.block_number = block_number
        
    def hash(self):
        return hashed_blocked(self.previous_hash, 
               self.block_number, 
               self.data, 
               self.nonce)
    
    def __str__(self):
        return str('Block No: %s\nHash: %s\nPrevious_h: %s\nData: %s\nNonce: %s\n' %(
                       self.block_number, self.hash(), 
                       self.previous_hash, self.data, 
                       self.nonce
                   ))


class Blockchain():
    difficulty = 4 
    def __init__(self, chain=[]):
        self.chain = chain # If there is previous block
        
    # Append in dictionary form 
    # "List" of "Dictionary"
    
    # With each dictionary containing
    # block_number, hash, prev_hash, data, nonce
#     def add(self, block):
#         self.chain.append({
#             'number': block.block_number, 
#             'hash': block.hash(), 
#             'previous': block.previous_hash, 
#             'data': block.data, 
#             'nonce': block.nonce
#         })
    def add(self, block):
        self.chain.append(block)
    
    def remove(self, block):
        self.chain.remove(block)
        
    # Related to difficulty
    def mine(self, block):
        try:
            block.previous_hash = self.chain[-1].hash() # Latest block
        except IndexError:
            pass # If there is no previous block yet
        
        while True:
            # Loop infinitely until the nonce produce a hash with
            # difficulty number of 0 at the front (4x0)
            if block.hash()[:self.difficulty] == "0" * self.difficulty:
                self.add(block)
                break
            else:
                block.nonce = block.nonce + 1
        
    def isValid(self):
        # From 2nd block, first block have no previous to check
        for i in range(1, len(self.chain)):
            _previous = self.chain[i].previous_hash
            # Recalculate the hash of the previous block entirely
            _current = self.chain[i-1].hash()
            if _previous != _current or _current[:self.difficulty] != '0' * self.difficulty:
                return False
        
        return True

def main():
    block_chain = Blockchain()
    transactions = [
            'A sent 2 DC to B',
            'C sent 3.6 DC to D',
            'A sent 0.2 DC to C',
            'C sent 1.4 DC to A'
    ]
        
    # 1 block = 1 transaction
    num = 0
    for transaction in transactions:
        num += 1
        block_chain.mine(Block(transaction, num))
            
    #     print(block_chain.chain)
    for block in block_chain.chain:
        print(block)
        
    print(block_chain.isValid())

    # Corrupt a block chain
    block_chain.chain[2].data = 'C sent 500 DC to A'
    # Remine the block
    block_chain.mine(block_chain.chain[2])

    for block in block_chain.chain:
        print(block)
        
    print(block_chain.isValid())


if __name__ == '__main__':
    main()