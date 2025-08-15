


# Top-level module name of your RTL
TOPLEVEL = aes_core

# Python testbench module (without .py)
MODULE = aes_core_test

# Simulator
SIM = verilator

WAVES=1

# Verilog source files (adjust path as needed)

VERILOG_SOURCES=$(PROJECT_ROOT)/cores/*/hdl/*.sv \

PYTHONPATH=$(PROJECT_ROOT)/tests/cores/$(TARGET) \

CORENUM?=0

#COMPILE_ARGS += -P $(TOPLEVEL).CORENUM=$(CORENUM)
EXTRA_ARGS += --trace --trace-fst --trace-structs
EXTRA_ARGS += -GCORENUM=$(CORENUM)
# Include cocotb provided makefile
include $(shell cocotb-config --makefiles)/Makefile.sim

recomp:
	rm -rf sim_build/
	$(MAKE)
