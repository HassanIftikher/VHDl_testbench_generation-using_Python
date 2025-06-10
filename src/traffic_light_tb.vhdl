library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;

entity traffic_light_tb is
end traffic_light_tb;

architecture Behavioral of traffic_light_tb is
    -- Component declaration
    component traffic_light
    port (
        clk : in STD_LOGIC;
        rst : in STD_LOGIC;
        sensor : in STD_LOGIC;
        red_light : out STD_LOGIC;
        yellow_light : out STD_LOGIC;
        green_light : out STD_LOGIC
    );
    end component;

    -- Signal declarations
    signal clk : STD_LOGIC;
    signal rst : STD_LOGIC;
    signal sensor : STD_LOGIC;
    signal red_light : STD_LOGIC;
    signal yellow_light : STD_LOGIC;
    signal green_light : STD_LOGIC;

    -- Simulation time
    constant SIM_TIME : time := 1300 ns;

begin
    -- Component instantiation
    UUT: traffic_light
    port map (
        clk => clk,
        rst => rst,
        sensor => sensor,
        red_light => red_light,
        yellow_light => yellow_light,
        green_light => green_light
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
        sensor <= '0';
        wait for 10 ns;  -- Allow signals to settle

        -- Test patterns for STD_LOGIC ports
        sensor <= '0';
        wait for 10 ns;

        sensor <= '1';
        wait for 10 ns;
        -- End simulation
        wait;
    end process;
end Behavioral;