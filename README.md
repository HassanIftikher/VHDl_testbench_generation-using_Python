# VHDL Testbench GeneratorAdd commentMore actions

A Python-based GUI application that automatically generates and simulates VHDL testbenches for digital design modules. This tool streamlines the VHDL testing workflow by providing an intuitive interface for parsing VHDL modules, generating comprehensive testbenches, and running simulations.

## Features

- Interactive GUI interface for VHDL module input and testbench preview
- Automatic parsing of VHDL entity declarations
- Support for various VHDL data types including std_logic, std_logic_vector, and more
- Automated testbench generation with configurable test vectors
- Built-in simulation capability using GHDL
- Waveform visualization with GTKWave
- Real-time simulation log viewing

## Prerequisites

- Python 3.10 or higher
- GHDL (VHDL simulator)
- GTKWave (Waveform viewer)
- Tkinter (Python GUI library)
- Vivado 
## Project Structure

```
vhdl_testbench_project/
├── extras/                      #Contains additional scripts, experiments, and utilities developed during the project
├── VHDL_testbench_gui.py        # Main GUI application
├── scripts/
│   ├── run_parser.py            # VHDL parsing script
│   ├── run_simulation.sh        # Simulation execution script
│   ├── testbench_generator.py   # Testbench generation logic
│   ├── vhdl_parser.py          # VHDL module parser              s
├── src/                        # Source VHDL files
│   ├── *.vhdl                  # VHDL source and testbench files
│   └── vhdl_module.json        # Generated JSON configuration
├── sim/                        # Simulation output directory
│   ├── *.fst                   # Generated waveform files
│   └── simulation.log          # Simulation logs
├── Setup_project.tcl           #Vivado integration with python
├── run_parser.py               #Vivado integartion python file
```
Features in Detail
VHDL Parser

Automated entity extraction
Generic parameter support
Port direction detection
Data type inference
Vector width parsing

Testbench Generator

Clock generation for synchronous designs
Reset signal handling
Automated test vector generation
Parametric vector width support
Customizable simulation duration

Simulation Runner

Automated GHDL compilation
FST waveform generation
GTKWave integration
Comprehensive error reporting
Simulation log capture
## Supported Components

The project includes testbenches for various VHDL components:
- Basic Components:
  - 2-to-1 Multiplexer
  - 4-Bit Adder
  - 4-to-1 Multiplexer
  - Seven Segment Display
- Sequential Components:
  - D Flip-Flop
  - 8-Bit Counter
  - Shift Register
- Complex Components:
  - Simple ALU
  - DMA Controller
  - Traffic Light Controller
  - PWM Generator
  - FIFO Buffer
  - Sine Wave Generator
  - FSM (Finite State Machine)

## Usage

1. Start the GUI application:
```bash
python VHDL_testbench_gui.py
```
2. Using the GUI:
   - Paste your VHDL module code into the input text area
   - Click "Parse Module" to analyze the VHDL code
   - Click "Generate Testbench" to create a testbench
   - Review and edit the generated testbench in the preview area
   - Click "Save Testbench" to save your changes
   - Click "Run Simulation" to execute the testbench

3. Running Simulations:
   - The simulation script (`scripts/run_simulation.sh`) will:
     - Compile the VHDL files using GHDL
     - Generate FST waveform files
     - Open the waveform automatically in GTKWave
     - Save simulation logs in `sim/simulation.log`

## Scripts Description

- `VHDL_testbench_gui.py`: Main GUI application for the testbench generator
- `run_parser.py`: Handles VHDL file parsing and analysis
- `run_simulation.sh`: Manages GHDL compilation and simulation execution
- `testbench_generator.py`: Generates VHDL testbench files
- `vhdl_parser.py`: Parses VHDL entities and architectures
