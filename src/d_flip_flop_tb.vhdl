library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;

entity d_flip_flop_tb is
end d_flip_flop_tb;

architecture Behavioral of d_flip_flop_tb is
    -- Component declaration
    component d_flip_flop
    port (
        clk : in STD_LOGIC;
        rst : in STD_LOGIC;
        d : in STD_LOGIC;
        q : out STD_LOGIC
    );
    end component;

    -- Signal declarations
    signal clk : STD_LOGIC;
    signal rst : STD_LOGIC;
    signal d : STD_LOGIC;
    signal q : STD_LOGIC;

    -- Simulation time
    constant SIM_TIME : time := 1200 ns;

begin
    -- Component instantiation
    UUT: d_flip_flop
    port map (
        clk => clk,
        rst => rst,
        d => d,
        q => q
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
        d <= '0';
        wait for 10 ns;  -- Allow signals to settle

        -- Test patterns for STD_LOGIC ports
        d <= '0';
        wait for 10 ns;

        d <= '1';
        wait for 10 ns;
        -- End simulation
        wait;
    end process;
end Behavioral;