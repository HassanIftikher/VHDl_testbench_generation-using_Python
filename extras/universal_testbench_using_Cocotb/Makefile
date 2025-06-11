# Makefile for VHDL testbench using cocotb

# Defaults
SIM ?= ghdl
TOPLEVEL_LANG ?= vhdl

# VHDL source files
VHDL_SOURCES = examples/my_module.vhd

# Python test file
MODULE = test_my_module
TEST_FILE = $(PWD)/tb/test_my_module.py

# Top level entity
TOPLEVEL = my_module

# Output directory
SIM_BUILD = generated

# Include cocotb's make rules to take care of the simulator setup
include $(shell cocotb-config --makefiles)/Makefile.sim

# Clean rule
clean::
	rm -rf $(SIM_BUILD)
	rm -rf __pycache__
	rm -rf *.o
	rm -rf *.vcd
	rm -f results.xml
