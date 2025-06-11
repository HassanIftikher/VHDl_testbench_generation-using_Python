library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;

entity counter_8bit_tb is
end counter_8bit_tb;

architecture Behavioral of counter_8bit_tb is
    -- Component declaration
    component counter_8bit
    port (
        clk : in STD_LOGIC;
        rst : in STD_LOGIC;
        enable : in STD_LOGIC;
        count : out STD_LOGIC_VECTOR(7 downto 0)
    );
    end component;

    -- Signal declarations
    signal clk : STD_LOGIC;
    signal rst : STD_LOGIC;
    signal enable : STD_LOGIC;
    signal count : STD_LOGIC_VECTOR(7 downto 0);

    -- Simulation time
    constant SIM_TIME : time := 200 ns;

begin
    -- Component instantiation
    UUT: counter_8bit
    port map (
        clk => clk,
        rst => rst,
        enable => enable,
        count => count
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
        enable <= '0';
        wait for 10 ns;  -- Allow signals to settle

        -- Test patterns for STD_LOGIC ports
        enable <= '0';
        wait for 10 ns;

        enable <= '1';
        wait for 10 ns;
        -- End simulation
        wait;
    end process;
end Behavioral;