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

def parse_data_type(port):
    """Enhanced parse_data_type function to handle various VHDL data types and vector widths"""
    if isinstance(port, dict):
        data_type = port.get('data_type', '').strip().lower()
        width = port.get('width')

        # Handle STD_LOGIC_VECTOR with explicit width specification
        if data_type == "std_logic_vector":
            if isinstance(width, dict):
                left = width.get('left')
                right = width.get('right')
                direction = width.get('direction', 'downto').lower()
                
                # Handle parametric expressions (e.g., DATA_WIDTH-1)
                if isinstance(left, str) and any(c.isalpha() for c in left):
                    return "STD_LOGIC_VECTOR", f"({left} {direction} {right})"
                if isinstance(right, str) and any(c.isalpha() for c in right):
                    return "STD_LOGIC_VECTOR", f"({left} {direction} {right})"
                    
                return "STD_LOGIC_VECTOR", f"({left} {direction} {right})"
            elif isinstance(width, str):
                # Handle width specified as string, including parametric expressions
                return "STD_LOGIC_VECTOR", f"({width})"
            elif isinstance(width, (list, tuple)) and len(width) == 2:
                # Handle width specified as [high, low]
                return "STD_LOGIC_VECTOR", f"({width[0]} downto {width[1]})"
            else:
                raise ValueError(f"Invalid width specification for STD_LOGIC_VECTOR: {width}")

        # Handle STD_LOGIC
        elif data_type == "std_logic":
            return "STD_LOGIC", ""
        
        else:
            raise ValueError(f"Unsupported data type: {data_type}")

    raise ValueError("Invalid port definition format")

def get_vector_width(range_str):
    """Extract vector width from range string, handling parametric expressions"""
    # Check if the range contains parametric expressions
    if any(c.isalpha() for c in range_str):
        return None  # Return None for parametric widths
        
    match = re.search(r'\((\d+)\s+downto\s+(\d+)\)', range_str)
    if match:
        high, low = map(int, match.groups())
        return high - low + 1
    return None

def generate_test_vectors(port, data_type, range_str):
    """Generate appropriate test vectors based on port type"""
    test_code = []
    port_name = port['name']
    
    if port['direction'] != 'in':
        return ""

    if data_type == "STD_LOGIC":
        test_code.extend([
            f"        -- Test case for {port_name}",
            f"        {port_name} <= '0';",
            "        wait for 10 ns;",
            f"        {port_name} <= '1';",
            "        wait for 10 ns;",
            f"        {port_name} <= '0';",
            "        wait for 10 ns;"
        ])
    elif data_type == "STD_LOGIC_VECTOR":
        width = get_vector_width(range_str)
        if width:
            # Generate test vectors for fixed width
            test_code.extend([
                f"        -- Test cases for {port_name}",
                f"        {port_name} <= (others => '0');",
                "        wait for 10 ns;",
                f"        {port_name} <= \"{format(1, '0' + str(width) + 'b')}\";",
                "        wait for 10 ns;",
                f"        {port_name} <= \"{format(2**(width-1), '0' + str(width) + 'b')}\";",
                "        wait for 10 ns;",
                f"        {port_name} <= (others => '1');",
                "        wait for 10 ns;",
                f"        {port_name} <= \"{format(5, '0' + str(width) + 'b')}\";",
                "        wait for 10 ns;",
                f"        {port_name} <= \"{format(10, '0' + str(width) + 'b')}\";",
                "        wait for 10 ns;"
            ])
        else:
            # Generate generic test vectors for parametric width
            test_code.extend([
                f"        -- Test cases for {port_name} (parametric width)",
                f"        {port_name} <= (others => '0');",
                "        wait for 10 ns;",
                f"        {port_name} <= (0 => '1', others => '0');",  # Set LSB
                "        wait for 10 ns;",
                f"        {port_name} <= (others => '1');",  # Set all bits
                "        wait for 10 ns;",
                f"        {port_name} <= (others => '0');",
                "        wait for 10 ns;"
            ])
    
    return "\n".join(test_code)

def generate_clock_process(clock_signal, clock_period):
    """Generate clock process for testbench"""
    return f"""
    -- Clock generation process
    clk_process: process
    begin
        while now < 1000 ns loop  -- Run simulation for 1000 ns
            {clock_signal} <= '0';
            wait for {clock_period/2} ns;
            {clock_signal} <= '1';
            wait for {clock_period/2} ns;
        end loop;
        wait;
    end process;
"""

def generate_reset_process(reset_signal):
    """Generate reset process for testbench"""
    return f"""
    -- Reset process
    reset_process: process
    begin
        {reset_signal} <= '1';
        wait for 20 ns;
        {reset_signal} <= '0';
        wait;
    end process;
"""

def generate_testbench(vhdl_data, output_file):
    """Enhanced testbench generator with proper signal initialization and test vectors"""
    entity_name = vhdl_data['vhdl_entity']['name']
    ports = vhdl_data['vhdl_entity']['ports']
    clock_period = 10

    # Find clock and reset signals if they exist
    clock_signal = next((p['name'] for p in ports if p['name'].lower() in ['clk', 'clock']), None)
    reset_signal = next((p['name'] for p in ports if p['name'].lower() in ['rst', 'reset']), None)

    # Generate the testbench header
    tb_code = f"""library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;

entity {entity_name}_tb is
end {entity_name}_tb;

architecture Behavioral of {entity_name}_tb is
    -- Component declaration
    component {entity_name}"""

    # Add generics only if present and not empty
    if 'generics' in vhdl_data['vhdl_entity'] and vhdl_data['vhdl_entity']['generics']:
        tb_code += "\n    generic (\n"
        for i, generic in enumerate(vhdl_data['vhdl_entity']['generics']):
            name = generic['name']
            data_type = generic['data_type']
            value = generic['default_value']
            tb_code += f"        {name} : {data_type} := {value}"
            if i < len(vhdl_data['vhdl_entity']['generics']) - 1:
                tb_code += ";\n"
            else:
                tb_code += "\n"
        tb_code += "    );"
    
    # Port declarations in component
    tb_code += "\n    port (\n"
    for i, port in enumerate(ports):
        data_type, range_str = parse_data_type(port)
        tb_code += f"        {port['name']} : {port['direction']} {data_type}{range_str}"
        if i < len(ports) - 1:
            tb_code += ";\n"
    tb_code += "\n    );\n"
    tb_code += "    end component;\n\n"

    # Add generic constants only if present and not empty
    if 'generics' in vhdl_data['vhdl_entity'] and vhdl_data['vhdl_entity']['generics']:
        tb_code += "    -- Generic constants\n"
        for generic in vhdl_data['vhdl_entity']['generics']:
            name = generic['name']
            value = generic['default_value']
            data_type = generic['data_type']
            tb_code += f"    constant {name} : {data_type} := {value};\n"
        tb_code += "\n"
    
    # Signal declarations
    tb_code += "    -- Signal declarations\n"
    for port in ports:
        data_type, range_str = parse_data_type(port)
        tb_code += f"    signal {port['name']} : {data_type}{range_str};\n"
    
    # Begin architecture
    tb_code += "\nbegin\n"
    
    # Component instantiation
    tb_code += "    -- Component instantiation\n"
    tb_code += f"    UUT: {entity_name}"
    
    # Add generic map only if generics are present and not empty
    if 'generics' in vhdl_data['vhdl_entity'] and vhdl_data['vhdl_entity']['generics']:
        tb_code += "\n    generic map (\n"
        for i, generic in enumerate(vhdl_data['vhdl_entity']['generics']):
            name = generic['name']
            tb_code += f"        {name} => {name}"
            if i < len(vhdl_data['vhdl_entity']['generics']) - 1:
                tb_code += ",\n"
            else:
                tb_code += "\n"
        tb_code += "    )"
    
    # Port map
    tb_code += "\n    port map (\n"
    for i, port in enumerate(ports):
        tb_code += f"        {port['name']} => {port['name']}"
        if i < len(ports) - 1:
            tb_code += ",\n"
        else:
            tb_code += "\n"
    tb_code += "    );\n"

    # Add clock process if needed
    if clock_signal:
        tb_code += generate_clock_process(clock_signal, clock_period)

    # Add reset process if needed
    if reset_signal:
        tb_code += generate_reset_process(reset_signal)
    
    # Generate test process
    tb_code += """
    -- Stimulus process
    stim_proc: process
    begin
        -- Initialize inputs
"""
    
    # Generate test vectors for each input port
    for port in ports:
        if port['direction'] == 'in' and port['name'] not in [clock_signal, reset_signal]:
            data_type, range_str = parse_data_type(port)
            tb_code += generate_test_vectors(port, data_type, range_str) + "\n"
    
    tb_code += """
        -- End simulation
        wait;
    end process;
end Behavioral;
"""

    # Write the generated testbench
    with open(output_file, 'w') as f:
        f.write(tb_code)

def main():
    # Create src directory if it doesn't exist
    if not os.path.exists("src"):
        os.makedirs("src")

    json_file = 'src/vhdl_module.json'
    if not os.path.exists(json_file):
        print(f"Error: JSON file '{json_file}' not found.")
        return

    try:
        vhdl_data = load_vhdl_data(json_file)
        entity_name = vhdl_data['vhdl_entity']['name']
        tb_file = os.path.join("src", f"{entity_name}_tb.vhdl")
        
        generate_testbench(vhdl_data, tb_file)
        print(f"Successfully generated testbench: {tb_file}")
        
    except Exception as e:
        print(f"Error generating testbench: {str(e)}")

if __name__ == "__main__":
    main()
