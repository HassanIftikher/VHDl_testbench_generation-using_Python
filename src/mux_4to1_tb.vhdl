library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;

entity mux_4to1_tb is
end mux_4to1_tb;

architecture Behavioral of mux_4to1_tb is
    -- Component declaration
    component mux_4to1
    port (
        input0 : in STD_LOGIC_VECTOR(7 downto 0);
        input1 : in STD_LOGIC_VECTOR(7 downto 0);
        input2 : in STD_LOGIC_VECTOR(7 downto 0);
        input3 : in STD_LOGIC_VECTOR(7 downto 0);
        sel : in STD_LOGIC_VECTOR(1 downto 0);
        output : out STD_LOGIC_VECTOR(7 downto 0)
    );
    end component;

    -- Signal declarations
    signal input0 : STD_LOGIC_VECTOR(7 downto 0);
    signal input1 : STD_LOGIC_VECTOR(7 downto 0);
    signal input2 : STD_LOGIC_VECTOR(7 downto 0);
    signal input3 : STD_LOGIC_VECTOR(7 downto 0);
    signal sel : STD_LOGIC_VECTOR(1 downto 0);
    signal output : STD_LOGIC_VECTOR(7 downto 0);

    -- Simulation time
    constant SIM_TIME : time := 1900 ns;

begin
    -- Component instantiation
    UUT: mux_4to1
    port map (
        input0 => input0,
        input1 => input1,
        input2 => input2,
        input3 => input3,
        sel => sel,
        output => output
    );

    -- Stimulus process
    stim_proc: process
    begin
        -- Initialize inputs
        -- Initialize all inputs to prevent undefined values
        input0 <= (others => '0');
        input1 <= (others => '0');
        input2 <= (others => '0');
        input3 <= (others => '0');
        sel <= (others => '0');
        wait for 10 ns;  -- Allow signals to settle


        -- Test cases for input0 (parametric width)
        input0 <= (others => '0');
        wait for 10 ns;
        input0 <= (0 => '1', others => '0');
        wait for 10 ns;
        input0 <= (others => '1');
        wait for 10 ns;
        input0 <= (others => '0');
        wait for 10 ns;

        -- Test cases for input1 (parametric width)
        input1 <= (others => '0');
        wait for 10 ns;
        input1 <= (0 => '1', others => '0');
        wait for 10 ns;
        input1 <= (others => '1');
        wait for 10 ns;
        input1 <= (others => '0');
        wait for 10 ns;

        -- Test cases for input2 (parametric width)
        input2 <= (others => '0');
        wait for 10 ns;
        input2 <= (0 => '1', others => '0');
        wait for 10 ns;
        input2 <= (others => '1');
        wait for 10 ns;
        input2 <= (others => '0');
        wait for 10 ns;

        -- Test cases for input3 (parametric width)
        input3 <= (others => '0');
        wait for 10 ns;
        input3 <= (0 => '1', others => '0');
        wait for 10 ns;
        input3 <= (others => '1');
        wait for 10 ns;
        input3 <= (others => '0');
        wait for 10 ns;

        -- Test cases for sel (parametric width)
        sel <= (others => '0');
        wait for 10 ns;
        sel <= (0 => '1', others => '0');
        wait for 10 ns;
        sel <= (others => '1');
        wait for 10 ns;
        sel <= (others => '0');
        wait for 10 ns;
        -- End simulation
        wait;
    end process;
end Behavioral;