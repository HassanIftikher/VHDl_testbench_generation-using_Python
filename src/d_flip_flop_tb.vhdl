
library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;  -- For handling unsigned/signed types

entity d_flip_flop_tb is
end d_flip_flop_tb;

architecture Behavioral of d_flip_flop_tb is
    -- Signal declarations for inputs and output of DUT
        signal clk : STD_LOGIC;
    signal rst : STD_LOGIC;
    signal d : STD_LOGIC;
    signal q : STD_LOGIC;

    -- DUT Component declaration
    component d_flip_flop
    port (
            clk : in STD_LOGIC;
        rst : in STD_LOGIC;
        d : in STD_LOGIC;
        q : out STD_LOGIC
    );
end component;

begin
    UUT: d_flip_flop 
    port map (
        clk => clk,
        rst => rst,
        d => d,
        q => q
    );

    -- Clock generation process
    clk_process : process
    begin
        while True loop
            clk <= '0';
            wait for 5.0 ns;
            clk <= '1';
            wait for 5.0 ns;
        end loop;
    end process;
        
    -- Reset signal initialization
    process
    begin
        rst <= '0';  -- Initialize reset
        wait for 10 ns;         -- Wait for some time
        rst <= '1';  -- Assert reset
        wait for 20 ns;
        rst <= '0';  -- Deassert reset
        wait;
    end process;
        
    -- Stimulus process for applying test cases
    stimulus_process : process
    begin
        -- Test case for rst
        rst <= '0';
        wait for 10 ns;
        rst <= '1';
        wait for 10 ns;
        -- Test case for d
        d <= '0';
        wait for 10 ns;
        d <= '1';
        wait for 10 ns;
        -- End simulation
        wait;
    end process;
end Behavioral;
