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
        
        # Handle other data types (from paste-2.txt)
        elif data_type in ["unsigned", "signed"]:
            if isinstance(width, dict):
                left = width.get('left')
                right = width.get('right')
                direction = width.get('direction', 'downto').lower()
                return data_type.upper(), f"({left} {direction} {right})"
            elif isinstance(width, str):
                return data_type.upper(), f"({width})"
            elif isinstance(width, (list, tuple)) and len(width) == 2:
                return data_type.upper(), f"({width[0]} downto {width[1]})"
            else:
                raise ValueError(f"Invalid width specification for {data_type.upper()}: {width}")
        
        # Handle integer types
        elif data_type in ["integer", "natural", "positive"]:
            return data_type.upper(), ""
        
        # Handle boolean type
        elif data_type == "boolean":
            return "BOOLEAN", ""
        
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

def estimate_simulation_time(ports):
    """Estimate required simulation time based on design complexity"""
    # Base simulation time
    sim_time = 1000
    
    # Add time based on number of ports
    sim_time += len(ports) * 50
    
    # Add additional time for complex modules
    vector_ports = sum(1 for p in ports if p.get('data_type', '').lower() == 'std_logic_vector')
    sim_time += vector_ports * 100
    
    return sim_time

def generate_test_vectors(ports_data, clock_signal=None, reset_signal=None):
    """Generate appropriate test vectors based on port types"""
    # Filter out clock and reset signals
    filtered_ports = [p for p in ports_data if p['name'] not in ([clock_signal] if clock_signal else []) + 
                                             ([reset_signal] if reset_signal else [])]
    
    # First, identify all STD_LOGIC ports and other port types
    std_logic_ports = []
    other_ports = []
    
    for port in filtered_ports:
        if port['direction'] not in ['in', 'inout']:
            continue
            
        port_data_type, port_range = parse_data_type(port)
        if port_data_type == "STD_LOGIC":
            std_logic_ports.append(port)
        else:
            other_ports.append(port)
    
    # ADD THE INITIALIZATION CODE HERE
    test_code = ["        -- Initialize all inputs to prevent undefined values"]
    
    for port in filtered_ports:
        if port['direction'] in ['in', 'inout']:
            port_data_type, port_range = parse_data_type(port)
            
            # Initialize based on type
            if port_data_type == "STD_LOGIC":
                test_code.append(f"        {port['name']} <= '0';")
            elif port_data_type in ["STD_LOGIC_VECTOR", "UNSIGNED", "SIGNED"]:
                test_code.append(f"        {port['name']} <= (others => '0');")
            elif port_data_type in ["INTEGER", "NATURAL", "POSITIVE"]:
                test_code.append(f"        {port['name']} <= 0;")
            elif port_data_type == "BOOLEAN":
                test_code.append(f"        {port['name']} <= false;")
    
    test_code.append("        wait for 10 ns;  -- Allow signals to settle")
    test_code.append("")
    
    # Then continue with the original test pattern generation code
    # Handle STD_LOGIC ports together in patterns
    if std_logic_ports:
        test_code.append("        -- Test patterns for STD_LOGIC ports")
        
        # ... rest of the function remains the same
        
        # Generate all possible combinations for up to 8 STD_LOGIC ports
        if len(std_logic_ports) <= 8:
            num_combinations = min(2 ** len(std_logic_ports), 16)  # Limit to 16 test cases for larger combinations
            for i in range(num_combinations):
                # Add blank line between test cases
                if i > 0:
                    test_code.append("")
                
                # Set each port based on the binary representation of i
                for j, port in enumerate(std_logic_ports):
                    bit_value = (i >> j) & 1
                    test_code.append(f"        {port['name']} <= '{bit_value}';")
                
                test_code.append("        wait for 10 ns;")
        else:
            # For many ports, just do some basic test patterns
            # All zeros
            test_code.append("")
            for port in std_logic_ports:
                test_code.append(f"        {port['name']} <= '0';")
            test_code.append("        wait for 10 ns;")
            
            # All ones
            test_code.append("")
            for port in std_logic_ports:
                test_code.append(f"        {port['name']} <= '1';")
            test_code.append("        wait for 10 ns;")
            
            # Alternating
            test_code.append("")
            for i, port in enumerate(std_logic_ports):
                test_code.append(f"        {port['name']} <= '{i % 2}';")
            test_code.append("        wait for 10 ns;")
    
    # Handle other port types individually
    for port in other_ports:
        port_data_type, port_range = parse_data_type(port)
        port_name = port['name'].lower()
        
        test_code.append("")  # Add spacing between port sections
        
        if port_data_type in ["STD_LOGIC_VECTOR", "UNSIGNED", "SIGNED"]:
            # Check for special port types
            if "addr" in port_name:
                width = get_vector_width(port_range)
                if width is not None:
                    test_code.extend([
                        f"        -- Test address {port['name']}",
                        f"        {port['name']} <= (others => '0');",
                        "        wait for 10 ns;",
                        f"        {port['name']} <= \"{format(5, '0' + str(width) + 'b')}\";",
                        "        wait for 10 ns;"
                    ])
                else:
                    test_code.extend([
                        f"        -- Test address {port['name']} (parametric width)",
                        f"        {port['name']} <= (others => '0');",
                        "        wait for 10 ns;",
                        f"        {port['name']} <= (2 => '1', 0 => '1', others => '0');  -- Example address pattern",
                        "        wait for 10 ns;"
                    ])
            # Identify data signals (commonly named with "data")
            elif "data" in port_name:
                width = get_vector_width(port_range)
                if width is not None:
                    test_code.extend([
                        f"        -- Write data to {port['name']}",
                        f"        {port['name']} <= (others => '0');",
                        "        wait for 10 ns;",
                        f"        {port['name']} <= \"{format(42, '0' + str(width) + 'b')}\";  -- Example data",
                        "        wait for 10 ns;"
                    ])
                else:
                    test_code.extend([
                        f"        -- Write data to {port['name']} (parametric width)",
                        f"        {port['name']} <= (others => '0');",
                        "        wait for 10 ns;",
                        f"        {port['name']} <= (0 => '1', 1 => '0', 3 => '1', 5 => '1', others => '0');  -- Example data pattern",
                        "        wait for 10 ns;",
                        f"        {port['name']} <= (0 => '0', 1 => '1', 3 => '0', 5 => '1', others => '0');  -- Example data pattern",
                        "        wait for 10 ns;"
                    ])
                    
                # For bidirectional ports, add specific handling
                if port['direction'] == 'inout':
                    test_code.extend([
                        f"        -- Set {port['name']} to high impedance (for reading)",
                        f"        {port['name']} <= (others => 'Z');",
                        "        wait for 10 ns;"
                    ])
            else:
                # Original code for standard vectors
                width = get_vector_width(port_range)
                if width is not None:
                    test_code.extend([
                        f"        -- Test cases for {port['name']}",
                        f"        {port['name']} <= (others => '0');",
                        "        wait for 10 ns;"
                    ])
                    
                    # Only try to create bit patterns if the width is manageable
                    if width <= 64:
                        test_code.extend([
                            f"        {port['name']} <= \"{format(1, '0' + str(width) + 'b')}\";",
                            "        wait for 10 ns;",
                            f"        {port['name']} <= \"{format(min(2**(width-1), 2**63), '0' + str(width) + 'b')}\";",
                            "        wait for 10 ns;"
                        ])
                    
                    test_code.extend([
                        f"        {port['name']} <= (others => '1');",
                        "        wait for 10 ns;"
                    ])
                    
                    # Add a few more test patterns for smaller vectors
                    if width <= 64:
                        test_code.extend([
                            f"        {port['name']} <= \"{format(min(5, 2**width-1), '0' + str(width) + 'b')}\";",
                            "        wait for 10 ns;",
                            f"        {port['name']} <= \"{format(min(10, 2**width-1), '0' + str(width) + 'b')}\";",
                            "        wait for 10 ns;"
                        ])
                else:
                    test_code.extend([
                        f"        -- Test cases for {port['name']} (parametric width)",
                        f"        {port['name']} <= (others => '0');",
                        "        wait for 10 ns;",
                        f"        {port['name']} <= (0 => '1', others => '0');",  # Set LSB
                        "        wait for 10 ns;",
                        f"        {port['name']} <= (others => '1');",  # Set all bits
                        "        wait for 10 ns;",
                        f"        {port['name']} <= (others => '0');",
                        "        wait for 10 ns;"
                    ])
        # Handle integer, natural, positive types
        elif port_data_type in ["INTEGER", "NATURAL", "POSITIVE"]:
            test_code.extend([
                f"        -- Test cases for {port['name']} ({port_data_type})",
                f"        {port['name']} <= 0;",
                "        wait for 10 ns;",
                f"        {port['name']} <= 1;",
                "        wait for 10 ns;",
                f"        {port['name']} <= 10;",
                "        wait for 10 ns;",
                f"        {port['name']} <= 100;",
                "        wait for 10 ns;"
            ])
        # Handle boolean type
        elif port_data_type == "BOOLEAN":
            test_code.extend([
                f"        -- Test cases for {port['name']} (BOOLEAN)",
                f"        {port['name']} <= false;",
                "        wait for 10 ns;",
                f"        {port['name']} <= true;",
                "        wait for 10 ns;",
                f"        {port['name']} <= false;",
                "        wait for 10 ns;"
            ])
    
    return "\n".join(test_code)

def generate_clock_process(clock_signal, clock_period):
    """Generate clock process for testbench"""
    return f"""
    -- Clock generation process
    clk_process: process
    begin
        while now < SIM_TIME loop  -- Run simulation for SIM_TIME
            {clock_signal} <= '0';
            wait for {clock_period/2} ns;
            {clock_signal} <= '1';
            wait for {clock_period/2} ns;
        end loop;
        wait;
    end process;
"""
def generate_reset_process(reset_signal, reset_active_high=True):
    """Generate reset process for testbench"""
    reset_value = "'1'" if reset_active_high else "'0'"
    inactive_value = "'0'" if reset_active_high else "'1'"
    
    return f"""
    -- Reset process
    reset_process: process
    begin
        {reset_signal} <= {reset_value};  -- Assert reset
        wait for 20 ns;
        {reset_signal} <= {inactive_value};  -- Deassert reset
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
    reset_signal = next((p['name'] for p in ports if p['name'].lower() in ['rst', 'reset', 'rstn', 'resetn']), None)
    reset_active_high = True
    if reset_signal and any(n in reset_signal.lower() for n in ['rstn', 'resetn', '_n']):
        reset_active_high = False

    # Estimate simulation time based on complexity
    sim_time = estimate_simulation_time(ports)

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
    
    # Add simulation time constant
    tb_code += f"\n    -- Simulation time\n"
    tb_code += f"    constant SIM_TIME : time := {sim_time} ns;\n"
    
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
        tb_code += generate_reset_process(reset_signal, reset_active_high)
    
    # Generate test process
    tb_code += """
    -- Stimulus process
    stim_proc: process
    begin
        -- Initialize inputs
"""

    # Generate test vectors using the enhanced function
    test_vectors = generate_test_vectors(ports, clock_signal, reset_signal)
    tb_code += test_vectors

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
