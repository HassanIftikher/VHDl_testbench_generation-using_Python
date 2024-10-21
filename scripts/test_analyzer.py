import re

def parse_vhdl_module(vhdl_file):
    """Parse the VHDL module and extract entity name, ports, and signal types."""
    with open(vhdl_file, 'r') as file:
        vhdl_code = file.read()

    # Extract entity name
    entity_match = re.search(r'entity\s+(\w+)\s+is', vhdl_code)
    if entity_match:
        entity_name = entity_match.group(1)
    else:
        raise ValueError("Entity name not found in the VHDL file.")
    
    # Extract ports
    port_list = re.findall(r'(\w+)\s*:\s*(in|out)\s*(std_logic|std_logic_vector\([^)]+\))', vhdl_code)
    ports = [{'name': p[0], 'direction': p[1], 'type': p[2]} for p in port_list]
    
    return entity_name, ports

def analyze_testbench(testbench_file, entity_name, ports):
    """Analyze the generated testbench and check compatibility with the VHDL module."""
    with open(testbench_file, 'r') as file:
        tb_code = file.read()
    
    # Check if the testbench instantiates the correct entity
    if entity_name not in tb_code:
        return False, f"Testbench does not instantiate the entity '{entity_name}'."
    
    # Check if all ports are correctly declared
    for port in ports:
        if port['name'] not in tb_code:
            return False, f"Port '{port['name']}' is missing in the testbench."
    
    return True, "Testbench is compatible."


if __name__ == "__main__":
    vhdl_file = 'src/simple_adder.vhdl'
    testbench_file = 'src/simple_adder_tb.vhdl'

    # Step 1: Parse the VHDL module
    entity_name, ports = parse_vhdl_module(vhdl_file)

    # Step 2: Analyze the testbench
    compatible, message = analyze_testbench(testbench_file, entity_name, ports)
    if compatible:
        print("Testbench is compatible.")
    else:
        print(f"Testbench is not compatible: {message}")
