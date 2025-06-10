#!/bin/bash

# Check if entity name is provided
if [ -z "$ENTITY_NAME" ]; then
    echo "Error: ENTITY_NAME environment variable not set"
    exit 1
fi

# Construct module and testbench paths
VHDL_MODULE="src/${ENTITY_NAME}.vhdl"
TESTBENCH="src/${ENTITY_NAME}_tb.vhdl"

# Verify files exist
if [ ! -f "$VHDL_MODULE" ]; then
    echo "Error: Module file $VHDL_MODULE not found"
    exit 1
fi

if [ ! -f "$TESTBENCH" ]; then
    echo "Error: Testbench file $TESTBENCH not found"
    exit 1
fi

# Create simulation directories if they don't exist
mkdir -p sim

# Step 1: Remove unnecessary or old simulation files
rm -f *.o work-obj93.cf sim/*.fst sim/*.vcd sim/*.ghw sim/*.fst.hier

# Step 2: Compile the VHDL files
echo "Compiling VHDL files..."
ghdl -a "$VHDL_MODULE" "$TESTBENCH"
if [ $? -ne 0 ]; then
    echo "Compilation failed."
    exit 1
fi

# Step 3: Elaborate the Testbench
TESTBENCH_NAME="${ENTITY_NAME}_tb"
echo "Elaborating the testbench..."
ghdl -e "$TESTBENCH_NAME"
if [ $? -ne 0 ]; then
    echo "Elaboration failed."
    exit 1
fi

# Step 4: Run the Simulation and Generate FST Waveform
echo "Running simulation..."
ghdl -r "$TESTBENCH_NAME" --fst="sim/${TESTBENCH_NAME}.fst" --stop-time=1000ns > sim/simulation.log
if [ $? -ne 0 ]; then
    echo "Simulation failed."
    exit 1
fi

# Step 5: Open the waveform in GTKWave
echo "Opening GTKWave..."
gtkwave "sim/${TESTBENCH_NAME}.fst" &

echo "Full process complete: VHDL parsing, testbench generation, compilation, simulation, and GTKWave loading."