import json
import os

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
            tb_code += f"    {generic['name']} => {generic['default_value']}"
            if i < len(generics) - 1:
                tb_code += ",\n"
        tb_code += "\n)"
        return tb_code
    return ""

def generate_testbench(vhdl_data, output_file):
    """Generates VHDL testbench code based on JSON description of the VHDL module."""
    entity_name = vhdl_data['vhdl_entity']['name']
    ports = vhdl_data['vhdl_entity']['ports']
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
        if port['data_type'] == 'STD_LOGIC':
            tb_code += f"    signal {port['name']} : {port['data_type']};\n"
        elif port['data_type'] == 'STD_LOGIC_VECTOR':
            # Check if the width is parameterized or fixed
            if isinstance(port['width'], dict):
                width = f"{port['width']['left']} downto {port['width']['right']}"
            elif isinstance(port['width'], str):  # Handle cases like DataWidth-1 downto 0
                width = port['width']
            else:
                raise NotImplementedError(f"Unsupported width type: {port['width']}")
            tb_code += f"    signal {port['name']} : {port['data_type']}({width});\n"
        elif port['data_type'].lower() in ['integer', 'boolean', 'unsigned', 'signed']:
            tb_code += f"    signal {port['name']} : {port['data_type']};\n"
        else:
            raise NotImplementedError(f"Data type {port['data_type']} is not yet supported.")

    tb_code += f"""
    -- DUT Component declaration
    component {entity_name}
    port (
    """

    # Declare port map
    for i, port in enumerate(ports):
        tb_code += f"        {port['name']} : {port['direction']} {port['data_type']}"
        if port['data_type'] == 'STD_LOGIC_VECTOR' and port['width']:
            if isinstance(port['width'], dict):
                width = f"({port['width']['left']} downto {port['width']['right']})"
            elif isinstance(port['width'], str):
                width = f"({port['width']})"
            tb_code += f"{width}"
        if i < len(ports) - 1:
            tb_code += ";\n"
    tb_code += "\n    );\nend component;\n\nbegin\n"

    # Handle generics if any
    generic_map_code = handle_generics(vhdl_data)
    tb_code += f"    UUT: {entity_name} {generic_map_code}\n"
    
    # Instantiate the DUT
    tb_code += f"    port map (\n"
    for i, port in enumerate(ports):
        tb_code += f"        {port['name']} => {port['name']}"
        if i < len(ports) - 1:
            tb_code += ",\n"
    tb_code += "\n    );\n"

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

    # Reset signal initialization
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

    # Cycle through all inputs and apply test cases
    input_ports = [p for p in ports if p['direction'] == 'in' and p['name'].lower() != 'clk']
    for port in input_ports:
        tb_code += f"        -- Test case for {port['name']}\n"
        if port['data_type'] == 'STD_LOGIC':
            tb_code += f"        {port['name']} <= '0';\n        wait for 10 ns;\n"
            tb_code += f"        {port['name']} <= '1';\n        wait for 10 ns;\n"
        elif port['data_type'] == 'STD_LOGIC_VECTOR':
            tb_code += f"        {port['name']} <= (others => '0');\n        wait for 10 ns;\n"
            tb_code += f"        {port['name']} <= (others => '1');\n        wait for 10 ns;\n"
        elif port['data_type'] in ['unsigned', 'signed']:
            tb_code += f"        {port['name']} <= to_unsigned(0, {port['width']['left']} downto {port['width']['right']});\n"
            tb_code += f"        wait for 10 ns;\n"
            tb_code += f"        {port['name']} <= to_unsigned(1, {port['width']['left']} downto {port['width']['right']});\n"
            tb_code += f"        wait for 10 ns;\n"

    # End simulation
    tb_code += "        -- End simulation\n"
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

if __name__ == "__main__":
    main()
