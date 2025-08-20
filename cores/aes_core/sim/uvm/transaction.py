import random
from pyuvm import uvm_sequence_item

class AesTransaction(uvm_sequence_item):
    def __init__(self, data_in=None, key_in=None, name="aes_txn"):
        super().__init__(name)
        self.data_in = data_in
        self.key_in = key_in

    def randomize_operands(self):
        self.data_in = random.getrandbits(128)
        self.key_in = random.getrandbits(128)

    def randomize(self):
        self.randomize_operands()

    def __str__(self):
        return (f"AES Transaction: data_in={hex(self.data_in)}, "
                f"key_in={hex(self.key_in)}, "
                f"expected_out={hex(self.expected_out) if self.expected_out else None}")
