
library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;  -- For handling unsigned/signed types

entity multiplexer4_1_tb is
end multiplexer4_1_tb;

architecture Behavioral of multiplexer4_1_tb is
    -- Signal declarations for inputs and output of DUT
        signal i0 : STD_LOGIC;
    signal i1 : STD_LOGIC;
    signal i2 : STD_LOGIC;
    signal i3 : STD_LOGIC;
    signal sel : STD_LOGIC_VECTOR(1 downto 0);
    signal bitout : STD_LOGIC;

    -- DUT Component declaration
    component multiplexer4_1
        port (
        i0 : in STD_LOGIC;
        i1 : in STD_LOGIC;
        i2 : in STD_LOGIC;
        i3 : in STD_LOGIC;
        sel : in STD_LOGIC_VECTOR(1 downto 0);
        bitout : out STD_LOGIC
    );
end component;

begin
    UUT: multiplexer4_1
        port map (
            i0 => i0,
            i1 => i1,
            i2 => i2,
            i3 => i3,
            sel => sel,
            bitout => bitout
        );

    -- Stimulus process for applying test cases
    stimulus_process : process
    begin
        i0 <= '0';
        wait for 10 ns;
        i0 <= '1';
        wait for 10 ns;
        i1 <= '0';
        wait for 10 ns;
        i1 <= '1';
        wait for 10 ns;
        i2 <= '0';
        wait for 10 ns;
        i2 <= '1';
        wait for 10 ns;
        i3 <= '0';
        wait for 10 ns;
        i3 <= '1';
        wait for 10 ns;
        sel <= '0';
        wait for 10 ns;
        sel <= '1';
        wait for 10 ns;
        wait;
    end process;
end Behavioral;
