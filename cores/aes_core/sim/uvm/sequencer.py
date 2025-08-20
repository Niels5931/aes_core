from pyuvm import uvm_sequencer
from transaction import AesTransaction

class AesSequencer(uvm_sequencer):
    type_name = "AesTransaction"
    def __init__(self, name="aes_sequencer", parent=None):
        super().__init__(name, parent)
