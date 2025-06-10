library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;

entity fsm_tb is
end fsm_tb;

architecture Behavioral of fsm_tb is
    -- Component declaration
    component fsm
    port (
        clk : in STD_LOGIC;
        rst : in STD_LOGIC;
        input_sig : in STD_LOGIC;
        output_sig : out STD_LOGIC
    );
    end component;

    -- Signal declarations
    signal clk : STD_LOGIC;
    signal rst : STD_LOGIC;
    signal input_sig : STD_LOGIC;
    signal output_sig : STD_LOGIC;

    -- Simulation time
    constant SIM_TIME : time := 1200 ns;

begin
    -- Component instantiation
    UUT: fsm
    port map (
        clk => clk,
        rst => rst,
        input_sig => input_sig,
        output_sig => output_sig
    );

    -- Clock generation process
    clk_process: process
    begin
        while now < SIM_TIME loop  -- Run simulation for SIM_TIME
            clk <= '0';
            wait for 5.0 ns;
            clk <= '1';
            wait for 5.0 ns;
        end loop;
        wait;
    end process;

    -- Reset process
    reset_process: process
    begin
        rst <= '1';  -- Assert reset
        wait for 20 ns;
        rst <= '0';  -- Deassert reset
        wait;
    end process;

    -- Stimulus process
    stim_proc: process
    begin
        -- Initialize inputs
        -- Initialize all inputs to prevent undefined values
        input_sig <= '0';
        wait for 10 ns;  -- Allow signals to settle

        -- Test patterns for STD_LOGIC ports
        input_sig <= '0';
        wait for 10 ns;

        input_sig <= '1';
        wait for 10 ns;
        -- End simulation
        wait;
    end process;
end Behavioral;