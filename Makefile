TARGET?=$(PROJECT_NAME)
BUILD_DIR?=build
CORENUM?=0

SHELL := /bin/bash

include $(shell cocotb-config --makefiles)/Makefile.sim

build:
	source source_simpl
	echo "Building $(TARGET)"
	cd cores/$(TARGET)/syn && simpl vivado

project:
	echo "Creating project for $(TARGET)"
	make_project.py $(TARGET)
	cd cores/$(TARGET)/_project/ && vivado -mode tcl -source project.tcl
	cd cores/$(TARGET)/_project/ && vivado project.xpr

open:
	cd cores/$(TARGET)/_project/ && vivado project.xpr

check_syntax:
	source source_simpl && check_syntax.py $(TARGET)

test:
	mkdir -p $(BUILD_DIR)/$(TARGET)
	@cd $(BUILD_DIR)/$(TARGET) && \
	VERILOG_SOURCES=$(PROJECT_ROOT)/cores/*/hdl/*.sv \
	SIM=icarus \
	TOPLEVEL=$(TARGET) \
	MODULE=$(TARGET)_test \
	BUILD_DIR=$(BUILD_DIR)/$(TARGET) \
	PYTHONPATH=$(PROJECT_ROOT)/tests/cores/$(TARGET) \
	WAVES=0 \
	COMPILE_ARGS+=-P$(TOPLEVEL).CORENUM=$(CORENUM) \
	make -f $(PROJECT_ROOT)/Makefile sim