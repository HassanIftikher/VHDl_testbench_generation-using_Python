
library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;

entity shift_register_tb is
end shift_register_tb;

architecture Behavioral of shift_register_tb is
    -- Component declaration
    component shift_register
    port (
        clk : in STD_LOGIC;
        rst : in STD_LOGIC;
        d : in STD_LOGIC;
        q : out STD_LOGIC_VECTOR(3 downto 0)
    );
    end component;

    signal clk : STD_LOGIC;
    signal rst : STD_LOGIC;
    signal d : STD_LOGIC;
    signal q : STD_LOGIC_VECTOR(3 downto 0);

begin
    -- Component instantiation
    UUT: shift_register port map (
        clk => clk,
        rst => rst,
        d => d,
        q => q
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

    -- Reset process
    reset_process: process
    begin
        rst <= '1';
        wait for 20 ns;
        rst <= '0';
        wait;
    end process;

    -- Stimulus process
    stim_proc: process
    begin
        -- Initialize inputs
        -- Test case for d
        d <= '0';
        wait for 10 ns;
        d <= '1';
        wait for 10 ns;
        d <= '0';
        wait for 10 ns;

        -- End simulation
        wait;
    end process;
end Behavioral;
