import json
import os
import re

def load_vhdl_data(json_file):
    """Loads the VHDL entity data from a JSON file."""
    try:
        with open(json_file, 'r') as f:
            data = json.load(f)
            if 'vhdl_entity' not in data or 'name' not in data['vhdl_entity'] or 'ports' not in data['vhdl_entity']:
                raise ValueError("Invalid JSON format: Missing 'vhdl_entity', 'name', or 'ports' fields.")
            return data
    except json.JSONDecodeError:
        raise ValueError(f"Error decoding JSON from file {json_file}. Please check the file format.")
    except FileNotFoundError:
        raise FileNotFoundError(f"JSON file '{json_file}' not found.")

def handle_generics(vhdl_data):
    """Handle generics in the VHDL module."""
    generics = vhdl_data.get('vhdl_entity', {}).get('generics', [])
    if generics:
        tb_code = "generic map (\n"
        for i, generic in enumerate(generics):
            # Use the default value or a placeholder if no default is available
            default_value = generic.get('default_value', '0')
            tb_code += f"    {generic['name']} => {default_value}"
            if i < len(generics) - 1:
                tb_code += ",\n"
        tb_code += "\n)"
        return tb_code
    return ""




def parse_data_type(port):
    """
    Extracts the data type and range for a given port.
    Handles various input formats including string and dictionary representations.
    """
    # If port is a dictionary, use existing logic
    if isinstance(port, dict):
        # Normalize the data_type string
        data_type = port.get('data_type', '').strip()
        width = port.get('width')
        
        # Special handling for STD_LOGIC_VECTOR with unclosed parenthesis
        if data_type.lower().startswith("std_logic_vector"):
            # Try to extract range from the data_type string
            range_match = re.search(r'\((\w+)\s*(downto|to)\s*(\w+)', data_type, re.IGNORECASE)
            if range_match:
                high = range_match.group(1)
                low = range_match.group(3)
                return 'STD_LOGIC_VECTOR', f'({high} downto {low})'
            else:
                return 'STD_LOGIC_VECTOR', ''
        
        if data_type.lower() == "std_logic":
            return "STD_LOGIC", ""
        
        elif data_type.lower() == "std_logic_vector":
            if isinstance(width, dict):
                width_str = f"{width['left']} {width['direction']} {width['right']}"
                return "STD_LOGIC_VECTOR", f"({width_str})"
            elif isinstance(width, str):
                range_match = re.search(r'\((\w+)\s+downto\s+(\w+)\)', width)
                if range_match:
                    high = range_match.group(1)
                    low = range_match.group(2)
                    return 'STD_LOGIC_VECTOR', f'({high} downto {low})'
            else:
                raise ValueError(f"Missing or invalid width for {data_type}.")
        
        elif data_type.lower().startswith("integer"):
            range_match = re.search(r'range\s+(.+)', data_type, re.IGNORECASE)
            if range_match:
                range_str = range_match.group(1)
                return "INTEGER", f"range {range_str}"
            else:
                return "INTEGER", ""
        
        elif data_type.lower() in ['boolean', 'unsigned', 'signed']:
            return data_type.upper(), ""
        
        else:
            raise NotImplementedError(f"Data type {data_type} is not yet supported.")
    
    # Existing code for string and other input types remains the same
    # ... (rest of the previous implementation)                                                                                                                                                                           


def generate_testbench(vhdl_data, output_file):
    """Generates VHDL testbench code based on JSON description of the VHDL module."""
    entity_name = vhdl_data['vhdl_entity']['name']
    ports = vhdl_data['vhdl_entity']['ports']
    generics = vhdl_data['vhdl_entity']['generics']
    clock_period = 10  # Default clock period for clock signal

    tb_code = f"""
library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;  -- For handling unsigned/signed types

entity {entity_name}_tb is
end {entity_name}_tb;

architecture Behavioral of {entity_name}_tb is
    -- Signal declarations for inputs and output of DUT
    """

    # Declare signals for all ports
    for port in ports:
        data_type, range_str = parse_data_type(port)
        tb_code += f"    signal {port['name']} : {data_type}{range_str};\n"

    tb_code += f"""
    -- DUT Component declaration
    component {entity_name}
    """

    # Add generic map declaration
    if generics:
        tb_code += "    generic (\n"
        for i, generic in enumerate(generics):
            tb_code += f"        {generic['name']} : {generic['data_type']}"
            if generic['default_value']:
                tb_code += f" := {generic['default_value']}"
            if i < len(generics) - 1:
                tb_code += ";\n"
        tb_code += "\n    );\n"

    # Add port declaration
    tb_code += "    port (\n"
    for i, port in enumerate(ports):
        data_type, range_str = parse_data_type(port)
        tb_code += f"        {port['name']} : {port['direction']} {data_type}{range_str}"
        if i < len(ports) - 1:
            tb_code += ";\n"
    tb_code += "\n    );\nend component;\n\nbegin\n"

    # Handle generic mapping in the instantiation
    if generics:
        tb_code += f"    UUT: {entity_name}\n"
        tb_code += "        generic map (\n"
        for i, generic in enumerate(generics):
            tb_code += f"            {generic['name']} => {generic['default_value']}"
            if i < len(generics) - 1:
                tb_code += ",\n"
        tb_code += "\n        )\n"
    else:
        tb_code += f"    UUT: {entity_name}\n"

    # Instantiate the DUT
    tb_code += "        port map (\n"
    for i, port in enumerate(ports):
        tb_code += f"            {port['name']} => {port['name']}"
        if i < len(ports) - 1:
            tb_code += ",\n"
    tb_code += "\n        );\n"

    # Clock generation process if a clock port is detected
    clock_signal = next((p['name'] for p in ports if p['name'].lower() == 'clk'), None)
    if clock_signal:
        tb_code += f"""
    -- Clock generation process
    clk_process : process
    begin
        while True loop
            {clock_signal} <= '0';
            wait for {clock_period / 2} ns;
            {clock_signal} <= '1';
            wait for {clock_period / 2} ns;
        end loop;
    end process;
        """

    # Reset signal initialization (if any)
    reset_signal = next((p['name'] for p in ports if p['name'].lower() == 'rst'), None)
    if reset_signal:
        tb_code += f"""
    -- Reset signal initialization
    process
    begin
        {reset_signal} <= '0';  -- Initialize reset
        wait for 10 ns;         -- Wait for some time
        {reset_signal} <= '1';  -- Assert reset
        wait for 20 ns;
        {reset_signal} <= '0';  -- Deassert reset
        wait;
    end process;
        """

    # Stimulus process for inputs (excluding clock)
    tb_code += "\n    -- Stimulus process for applying test cases\n"
    tb_code += "    stimulus_process : process\n    begin\n"

    # Test cases for input signals (e.g., setting clk or data values)
    for port in ports:
        if port['direction'] == 'in' and port['name'].lower() != 'clk':
            tb_code += f"        {port['name']} <= '0';\n        wait for 10 ns;\n"
            tb_code += f"        {port['name']} <= '1';\n        wait for 10 ns;\n"

    tb_code += "        wait;\n    end process;\nend Behavioral;\n"

    # Write the generated testbench to the output file
    output_file_path = os.path.join("src", output_file)
    with open(output_file_path, "w") as tb_file:
        tb_file.write(tb_code)
    print(f"Testbench generated: {output_file_path}")


def main():
    json_file = 'src/vhdl_module.json'  # Ensure this file exists and has valid data
    if not os.path.exists(json_file):
        print(f"Error: JSON file '{json_file}' not found.")
        return

    vhdl_data = load_vhdl_data(json_file)
    entity_name = vhdl_data['vhdl_entity']['name']
    tb_file = f"{entity_name}_tb.vhdl"

    # Generate the testbench in the src folder
    generate_testbench(vhdl_data, tb_file)


def main():
    json_file = 'src/vhdl_module.json'  # Ensure this file exists and has valid data
    if not os.path.exists(json_file):
        print(f"Error: JSON file '{json_file}' not found.")
        return

    vhdl_data = load_vhdl_data(json_file)
    entity_name = vhdl_data['vhdl_entity']['name']
    tb_file = f"{entity_name}_tb.vhdl"

    # Generate the testbench in the src folder
    generate_testbench(vhdl_data, tb_file)

if __name__ == "__main__":
    main()
