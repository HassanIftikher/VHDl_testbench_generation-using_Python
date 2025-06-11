import cocotb
from cocotb.triggers import Timer, RisingEdge
from cocotb.clock import Clock
import random
from cocotb.handle import SimHandleBase

class my_moduleTB:
    def __init__(self, dut: SimHandleBase):
        self.dut = dut
        self.log = dut._log

    async def initialize(self):
        """Initialize the testbench"""
        # Initialize inputs
        self.dut.d.value = 0  # Scalar signal


    async def reset(self):
        """Reset the DUT"""
        # Reset initialization
        self.dut.rst.value = 1  # Active reset
        await Timer(20, units='ns')  # Wait for 20ns
        self.dut.rst.value = 0  # Release reset
        await Timer(10, units='ns')  # Wait for 10ns after reset


    async def check_outputs(self):
        """Check output validity"""
        # Add output checking logic here
        pass

@cocotb.test()
async def my_module_basic_test(dut):
    """Basic test for my_module"""
    
    # Initialize testbench
    tb = my_moduleTB(dut)

    # Create clocks
        # Create clk clock
        clock_clk = Clock(self.dut.clk, 10, units="ns")
        cocotb.start_soon(clock_clk.start())  # Start clock without 'await'

    
    # Initialize signals
    await tb.initialize()
    
    # Apply reset
    await tb.reset()
    
    # Test scenarios
        # Test scenarios
        for i in range(5):
            await RisingEdge(self.dut.clk)  # Wait for rising edge of the clock
            self.dut.d.value = i % 2  # Toggle value for d

            # Check outputs
            value = self.dut.q.value
            assert value is not None, 'Output q is None'

    
    # Final checks
    await tb.check_outputs()
    
    await Timer(100, units='ns')

@cocotb.test()
async def my_module_random_test(dut):
    """Random test for my_module"""
    
    tb = my_moduleTB(dut)
    
    # Create clocks
        # Create clk clock
        clock_clk = Clock(self.dut.clk, 10, units="ns")
        cocotb.start_soon(clock_clk.start())  # Start clock without 'await'

    
    # Initialize signals
    await tb.initialize()
    
    # Apply reset
    await tb.reset()
    
    # Random test scenarios
    for i in range(100):
        await RisingEdge(tb.dut.clk)
        
        # Generate random stimuli for each input
        tb.dut.d.value = random.randint(0, 1)

        # Check outputs
        await tb.check_outputs()
    
    await Timer(100, units='ns')
