from pyuvm import *
from cocotb.triggers import RisingEdge
import cocotb

class AesDriver(uvm_driver):
    def __init__(self, name="aes_driver", parent=None):
        super().__init__(name,parent)
        self.dut = cocotb.top

    def build_phase(self):
        self.ap = uvm_analysis_port("ap", self)

    async def run_phase(self):
        while True:
            txn = await self.seq_item_port.get_next_item()
            if txn is None:
                break
            #print(txn)
            self.dut.data_in.value = txn.data_in
            self.dut.key_in.value = txn.key_in
            await RisingEdge(self.dut.clk_i)
            self.seq_item_port.item_done()
