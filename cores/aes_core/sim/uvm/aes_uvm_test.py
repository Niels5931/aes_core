from pyuvm import uvm_sequence_item
import random as pyrandom

from pyuvm import uvm_sequence, uvm_sequencer, uvm_driver, uvm_component, uvm_analysis_port, uvm_component



class aesTransaction(uvm_sequence_item):
    def __init__(self, name, data_in=None, key_in=None):
        super().__init__(name)
        self.data_in = data_in if data_in else int("".join([pyrandom.choice("01") for _ in range(128)]))
        self.key_in = key_in if key_in else int("".join([pyrandom.choice("01") for _ in range(128)]))

    def __str__(self):
        return f"AESTransaction(plaintext={self.data_in.hex()}, key={self.key_in.hex()})"

class AESSequence(uvm_sequence):
    def __init__(self, name, num_items=10):
        super().__init__(name)
        self.num_items = num_items

    def body(self):
        for _ in range(self.num_items):
            txn = aesTransaction("txn")
            self.start_item(txn)
            self.finish_item(txn)    

class AESSequencer(uvm_sequencer):
    pass

class AESDriver(uvm_driver):
    def run_phase(self):
        while True:
            txn = self.seq_item_port.get_next_item()
            # Apply to DUT here
            print(f"[DRIVER] Sending plaintext={txn.data_in.hex()} key={txn.key_in.hex()}")
            # Simulate encryption (mock or real AES)
            self.seq_item_port.item_done()

class AESMonitor(uvm_component):
    def build_phase(self):
        self.ap = uvm_analysis_port("ap", self)

    def run_phase(self):
        while True:
            # In real setup, capture from DUT outputs
            observed = {"ciphertext": b"\x00"*16}  # placeholder
            print(f"[MONITOR] Observed ciphertext={observed['ciphertext'].hex()}")
            self.ap.write(observed)


class AESScoreboard(uvm_component):
    def build_phase(self):
        self.expected = []
    
    def write(self, observed):
        expected_cipher = b"\x00"*16  # placeholder AES ref model
        if observed["ciphertext"] != expected_cipher:
            print("[SCOREBOARD] Mismatch!")
        else:
            print("[SCOREBOARD] Match.")