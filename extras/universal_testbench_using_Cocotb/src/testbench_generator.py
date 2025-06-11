import json
from pathlib import Path
from typing import Dict, Union

class TestBenchGenerator:
    def __init__(self, entity_data: Union[Dict, str, Path]):
        """
        Initialize with either a dictionary of entity data or path to JSON file.
        If a path to a JSON file is provided, it loads the entity data from the file.
        """
        try:
            if isinstance(entity_data, (str, Path)):
                # Load from JSON file
                with open(entity_data, 'r') as f:
                    data = json.load(f)
                    self.entity_data = data['vhdl_entity']
            else:
                self.entity_data = entity_data
            
            # Extract entity name, generics, and ports
            self.entity_name = self.entity_data['name']
            self.generics = self.entity_data.get('generics', [])
            self.ports = self.entity_data['ports']
        except KeyError as e:
            raise ValueError(f"Missing required key in entity data: {e}")
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON file")
        except Exception as e:
            raise ValueError(f"Error initializing TestBenchGenerator: {e}")

    def _generate_clock_code(self) -> str:
        """Generate clock creation code for all clock signals"""
        clock_code = ""
        clock_ports = [p for p in self.ports if p['name'].lower().startswith(('clk', 'clock'))]
        
        for port in clock_ports:
            clock_name = port['name']
            clock_code += f"""        # Create {clock_name} clock
        clock_{clock_name} = Clock(self.dut.{clock_name}, 10, units="ns")
        cocotb.start_soon(clock_{clock_name}.start())  # Start clock without 'await'\n"""
        
        return clock_code

    def _generate_reset_code(self) -> str:
        """Generate reset initialization code"""
        reset_code = ""
        reset_ports = [p for p in self.ports if any(r in p['name'].lower() for r in ['rst', 'reset'])]
        
        if reset_ports:
            reset_port = reset_ports[0]
            reset_name = reset_port['name']
            reset_active = 0 if reset_name.endswith('_n') else 1
            reset_inactive = 1 if reset_name.endswith('_n') else 0
            
            reset_code += f"""        # Reset initialization
        self.dut.{reset_name}.value = {reset_active}  # Active reset
        await Timer(20, units='ns')  # Wait for 20ns
        self.dut.{reset_name}.value = {reset_inactive}  # Release reset
        await Timer(10, units='ns')  # Wait for 10ns after reset\n"""
            
        return reset_code

    def _generate_input_initialization(self) -> str:
        """Generate initialization code for input ports"""
        init_code = "        # Initialize inputs\n"
        
        for port in self.ports:
            if port['direction'].lower() == 'in':
                # Skip clock and reset signals
                if port['name'].lower().startswith(('clk', 'clock', 'rst', 'reset')):
                    continue
                
                # Check if the port is a vector signal or scalar
                if 'width' in port and port['width'] is not None:
                    # Vector type
                    width = port['width']
                    init_code += f"        self.dut.{port['name']}.value = 0  # {width['left']} down to {width['right']} vector\n"
                else:
                    # Scalar type
                    if port['data_type'].lower() == 'boolean':
                        init_code += f"        self.dut.{port['name']}.value = False  # Boolean signal\n"
                    else:
                        init_code += f"        self.dut.{port['name']}.value = 0  # Scalar signal\n"
                    
        return init_code

    def _generate_test_scenarios(self) -> str:
        """Generate basic test scenarios based on port types"""
        scenario_code = """        # Test scenarios
        for i in range(5):
            await RisingEdge(self.dut.clk)  # Wait for rising edge of the clock\n"""
        
        # Add value changes for each input port
        for port in self.ports:
            if port['direction'].lower() == 'in' and \
               not port['name'].lower().startswith(('clk', 'clock', 'rst', 'reset')):
                if 'width' in port and port['width'] is not None:
                    scenario_code += f"            self.dut.{port['name']}.value = i  # Test different values for {port['name']}\n"
                else:
                    if port['data_type'].lower() == 'boolean':
                        scenario_code += f"            self.dut.{port['name']}.value = (i % 2 == 0)  # Toggle boolean {port['name']}\n"
                    else:
                        scenario_code += f"            self.dut.{port['name']}.value = i % 2  # Toggle value for {port['name']}\n"
                        
        # Add output checks for each output port
        scenario_code += "\n            # Check outputs\n"
        for port in self.ports:
            if port['direction'].lower() == 'out':
                scenario_code += f"            value = self.dut.{port['name']}.value\n"
                scenario_code += f"            assert value is not None, 'Output {port['name']} is None'\n"
                
        return scenario_code

    def generate_testbench(self) -> str:
        """Generate complete testbench code"""
        tb = f"""import cocotb
from cocotb.triggers import Timer, RisingEdge
from cocotb.clock import Clock
import random
from cocotb.handle import SimHandleBase

class {self.entity_name}TB:
    def __init__(self, dut: SimHandleBase):
        self.dut = dut
        self.log = dut._log

    async def initialize(self):
        \"\"\"Initialize the testbench\"\"\"
{self._generate_input_initialization()}

    async def reset(self):
        \"\"\"Reset the DUT\"\"\"
{self._generate_reset_code()}

    async def check_outputs(self):
        \"\"\"Check output validity\"\"\"
        # Add output checking logic here
        pass

@cocotb.test()
async def {self.entity_name}_basic_test(dut):
    \"\"\"Basic test for {self.entity_name}\"\"\"
    
    # Initialize testbench
    tb = {self.entity_name}TB(dut)

    # Create clocks
{self._generate_clock_code()}
    
    # Initialize signals
    await tb.initialize()
    
    # Apply reset
    await tb.reset()
    
    # Test scenarios
{self._generate_test_scenarios()}
    
    # Final checks
    await tb.check_outputs()
    
    await Timer(100, units='ns')

@cocotb.test()
async def {self.entity_name}_random_test(dut):
    \"\"\"Random test for {self.entity_name}\"\"\"
    
    tb = {self.entity_name}TB(dut)
    
    # Create clocks
{self._generate_clock_code()}
    
    # Initialize signals
    await tb.initialize()
    
    # Apply reset
    await tb.reset()
    
    # Random test scenarios
    for i in range(100):
        await RisingEdge(tb.dut.clk)
        
        # Generate random stimuli for each input
"""
        
        # Add random test generation for each input
        for port in self.ports:
            if port['direction'].lower() == 'in' and \
               not port['name'].lower().startswith(('clk', 'clock', 'rst', 'reset')):
                if 'width' in port and port['width'] is not None:
                    width = port['width']
                    tb += f"        tb.dut.{port['name']}.value = random.randint(0, 2**{width['left']}-1)\n"
                else:
                    if port['data_type'].lower() == 'boolean':
                        tb += f"        tb.dut.{port['name']}.value = random.choice([True, False])\n"
                    else:
                        tb += f"        tb.dut.{port['name']}.value = random.randint(0, 1)\n"

        tb += """
        # Check outputs
        await tb.check_outputs()
    
    await Timer(100, units='ns')
"""
        
        return tb

    def save_testbench(self, output_path: str) -> None:
        """Save the generated testbench to a file"""
        try:
            testbench_code = self.generate_testbench()
            output_path = Path(output_path)
            
            # Create directory if it doesn't exist
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_path, 'w') as f:
                f.write(testbench_code)
        except Exception as e:
            raise ValueError(f"Error saving testbench: {e}")