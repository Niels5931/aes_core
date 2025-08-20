from pyuvm import *
from cocotb import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge

from transaction import AesTransaction
from driver import AesDriver
from sequencer import AesSequencer
from sequence import AesSequence

import pyuvm

class AesEnv(uvm_env):
    def build_phase(self):
        self.sequencer = AesSequencer("seqr",self)
        self.driver = AesDriver.create("driver", self)
    
    def connect_phase(self):
        self.driver.seq_item_port.connect(self.sequencer.seq_item_export)

class AesTestBase(uvm_test):
    def build_phase(self):
        self.env = AesEnv("env", self)

    def end_of_elaboration_phase(self):
        self.test_all = AesSequence.create("test")

    async def run_phase(self):
        self.raise_objection()
        dut = cocotb.top
        cocotb.start_soon(Clock(dut.clk_i, 10, units="ns").start())
        await self.test_all.start(self.env.sequencer)
        self.drop_objection()

@pyuvm.test()
class AesTest(AesTestBase):
    """AesTest"""