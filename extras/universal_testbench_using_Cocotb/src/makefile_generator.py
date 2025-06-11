from pathlib import Path
from typing import Dict, Union, List

class MakefileGenerator:
    def __init__(self, entity_name: str, vhdl_files: list, output_dir: str = 'sim'):
        self.entity_name = entity_name
        self.vhdl_files = vhdl_files
        self.output_dir = output_dir

    def generate(self, output_path: str) -> None:
        makefile_content = f"""# Makefile for VHDL testbench using cocotb

# Defaults
SIM ?= ghdl
TOPLEVEL_LANG ?= vhdl

# VHDL source files
VHDL_SOURCES = {' '.join(self.vhdl_files)}

# Python test file
MODULE = test_{self.entity_name}
TEST_FILE = $(PWD)/tb/test_{self.entity_name}.py

# Top level entity
TOPLEVEL = {self.entity_name}

# Output directory
SIM_BUILD = {self.output_dir}

# Include cocotb's make rules to take care of the simulator setup
include $(shell cocotb-config --makefiles)/Makefile.sim

# Clean rule
clean::
\trm -rf $(SIM_BUILD)
\trm -rf __pycache__
\trm -rf *.o
\trm -rf *.vcd
\trm -f results.xml
"""
        
        with open(output_path, 'w') as f:
            f.write(makefile_content)


def generate_makefile(entity_dict: Dict, vhdl_file: Union[str, Path], output_dir: str) -> None:
    entity_name = entity_dict['name']
    vhdl_files = [str(vhdl_file)]
    
    generator = MakefileGenerator(
        entity_name=entity_name,
        vhdl_files=vhdl_files,
        output_dir=output_dir
    )
    
    generator.generate('Makefile')

if __name__ == '__main__':
    # Example usage
    example_entity = {'name': 'counter'}
    example_file = 'examples/counter.vhd'
    generate_makefile(example_entity, example_file, 'sim')