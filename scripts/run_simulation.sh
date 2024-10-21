
#!/bin/bash
# Navigate to the project root directory
cd "$(dirname "$0")/.."

# Step 1: Parse the VHDL file and generate the JSON output
echo "Parsing the VHDL file..."
python3 scripts/run_parser.py
if [ $? -ne 0 ]; then
    echo "VHDL parsing failed."
    exit 1
fi

# Step 2: Generate the testbench VHDL file using the testbench generator
echo "Generating the testbench..."
python3 scripts/testbench_generator.py
if [ $? -ne 0 ]; then
    echo "Testbench generation failed."
    exit 1
fi
#echo "Analyzing the testbench..."
#python3 scripts/test_analyzer.py
#if [ $? -ne 0 ]; then
    #echo "Testbench analysis failed."
    #exit 1
#fi
# Step 3: Remove unnecessary or old simulation files
rm -f *.o work-obj93.cf sim/*.fst sim/*.vcd sim/*.ghw sim/*.fst.hier

# Step 4: Compile the VHDL files
echo "Compiling VHDL files..."
ghdl -a src/d_flip_flop.vhdl src/d_flip_flop_tb.vhdl
if [ $? -ne 0 ]; then
    echo "Compilation failed."
    exit 1
fi

# Step 5: Elaborate the Testbench
echo "Elaborating the testbench..."
ghdl -e d_flip_flop_tb
if [ $? -ne 0 ]; then
    echo "Elaboration failed."
    exit 1
fi

# Step 6: Run the Simulation and Generate FST Waveform
echo "Running simulation..."
ghdl -r d_flip_flop_tb --fst=sim/d_flip_flop_tb.fst --stop-time=200ns > sim/simulation.log

if [ $? -ne 0 ]; then
    echo "Simulation failed."
    exit 1
fi

# Step 7: Open the waveform in GTKWave
echo "Opening GTKWave..."
gtkwave sim/d_flip_flop_tb.fst &

echo "Full process complete: VHDL parsing, testbench generation, compilation, simulation, and GTKWave loading."

