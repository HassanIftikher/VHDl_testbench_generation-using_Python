#cd VHDl_testbench_generation-using_Python

#exec /opt/Xilinx/Vivado/2020.2/tps/lnx64/python-3.8.3/bin/python3 ./scripts/testbench_generator.py
# simple commands for running Python scripts

# For parser with file path as an argument
proc run_parser {vhdl_file} {
    set output_json_file "src/vhdl_module.json"  ;# Fixed output file path
    if {[catch {exec /opt/Xilinx/Vivado/2020.2/tps/lnx64/python-3.8.3/bin/python3 ./scripts/run_parser.py $vhdl_file $output_json_file} result]} {
        puts "Error: $result"
    } else {
        puts "Parsed VHDL file and saved to src/vhdl_module.json"
    }
}
# For testbench
proc run_testbench {} {
    if {[catch {exec /opt/Xilinx/Vivado/2020.2/tps/lnx64/python-3.8.3/bin/python3 ./scripts/testbench_generator.py} result]} {
        puts "Error: $result"
    } else {
        puts $result
    }
}

# For GUI interface
proc run_interface {} {
    if {[catch {exec /opt/Xilinx/Vivado/2020.2/tps/lnx64/python-3.8.3/bin/python3 ./VHDl_testbench_gui.py} result]} {
        puts "Error: $result"
    } else {
        puts $result
    }
}

puts "Commands loaded successfully:"
puts "  run_parser <vhdl_file> - Execute the parser with the specified VHDL file"
puts "  run_testbench          - Execute the testbench generator"
puts "  run_interface          - Execute the GUI interface"

