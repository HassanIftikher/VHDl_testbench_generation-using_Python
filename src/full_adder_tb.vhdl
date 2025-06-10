library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;

entity full_adder_tb is
end full_adder_tb;

architecture Behavioral of full_adder_tb is
    -- Component declaration
    component full_adder
    port (
        A : in STD_LOGIC;
        B : in STD_LOGIC;
        Cin : in STD_LOGIC;
        S : out STD_LOGIC;
        Cout : out STD_LOGIC
    );
    end component;

    -- Signal declarations
    signal A : STD_LOGIC;
    signal B : STD_LOGIC;
    signal Cin : STD_LOGIC;
    signal S : STD_LOGIC;
    signal Cout : STD_LOGIC;

    -- Simulation time
    constant SIM_TIME : time := 1250 ns;

begin
    -- Component instantiation
    UUT: full_adder
    port map (
        A => A,
        B => B,
        Cin => Cin,
        S => S,
        Cout => Cout
    );

    -- Stimulus process
    stim_proc: process
    begin
        -- Initialize inputs
        -- Initialize all inputs to prevent undefined values
        A <= '0';
        B <= '0';
        Cin <= '0';
        wait for 10 ns;  -- Allow signals to settle

        -- Test patterns for STD_LOGIC ports
        A <= '0';
        B <= '0';
        Cin <= '0';
        wait for 10 ns;

        A <= '1';
        B <= '0';
        Cin <= '0';
        wait for 10 ns;

        A <= '0';
        B <= '1';
        Cin <= '0';
        wait for 10 ns;

        A <= '1';
        B <= '1';
        Cin <= '0';
        wait for 10 ns;

        A <= '0';
        B <= '0';
        Cin <= '1';
        wait for 10 ns;

        A <= '1';
        B <= '0';
        Cin <= '1';
        wait for 10 ns;

        A <= '0';
        B <= '1';
        Cin <= '1';
        wait for 10 ns;

        A <= '1';
        B <= '1';
        Cin <= '1';
        wait for 10 ns;
        -- End simulation
        wait;
    end process;
end Behavioral;