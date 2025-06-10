library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;

entity sine_wave_tb is
end sine_wave_tb;

architecture Behavioral of sine_wave_tb is
    -- Component declaration
    component sine_wave
    generic (
        NUM_POINTS : integer := 32;
        MAX_AMPLITUDE : integer := 255
    );
    port (
        clk : in STD_LOGIC;
        dataout : out INTEGER RANGE 0 TO MAX_AMPLITUDE
    );
    end component;

    -- Generic constants
    constant NUM_POINTS : integer := 32;
    constant MAX_AMPLITUDE : integer := 255;

    -- Signal declarations
    signal clk : STD_LOGIC;
    signal dataout : INTEGER RANGE 0 TO MAX_AMPLITUDE;

    -- Simulation time
    constant SIM_TIME : time := 100 ns;

begin
    -- Component instantiation
    UUT: sine_wave
    generic map (
        NUM_POINTS => NUM_POINTS,
        MAX_AMPLITUDE => MAX_AMPLITUDE
    )
    port map (
        clk => clk,
        dataout => dataout
    );

    -- Clock generation process
    clk_process: process
    begin
        while now < 1000 ns loop  -- Run simulation for 1000 ns
            clk <= '0';
            wait for 5.0 ns;
            clk <= '1';
            wait for 5.0 ns;
        end loop;
        wait;
    end process;

    -- Stimulus process
    stim_proc: process
    begin
        -- Initialize inputs

        -- End simulation
        wait;
    end process;
end Behavioral;