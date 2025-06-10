library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;

entity alu_tb is
end alu_tb;

architecture Behavioral of alu_tb is
    -- Component declaration
    component alu
    port (
        a : in STD_LOGIC_VECTOR(7 downto 0);
        b : in STD_LOGIC_VECTOR(7 downto 0);
        op : in STD_LOGIC_VECTOR(2 downto 0);
        result : out STD_LOGIC_VECTOR(7 downto 0);
        zero : out STD_LOGIC;
        carry : out STD_LOGIC;
        overflow : out STD_LOGIC
    );
    end component;

    -- Signal declarations
    signal a : STD_LOGIC_VECTOR(7 downto 0);
    signal b : STD_LOGIC_VECTOR(7 downto 0);
    signal op : STD_LOGIC_VECTOR(2 downto 0);
    signal result : STD_LOGIC_VECTOR(7 downto 0);
    signal zero : STD_LOGIC;
    signal carry : STD_LOGIC;
    signal overflow : STD_LOGIC;

    -- Simulation time
    constant SIM_TIME : time := 1750 ns;

begin
    -- Component instantiation
    UUT: alu
    port map (
        a => a,
        b => b,
        op => op,
        result => result,
        zero => zero,
        carry => carry,
        overflow => overflow
    );

    -- Stimulus process
    stim_proc: process
    begin
        -- Initialize inputs
        -- Initialize all inputs to prevent undefined values
        a <= (others => '0');
        b <= (others => '0');
        op <= (others => '0');
        wait for 10 ns;  -- Allow signals to settle


        -- Test cases for a (parametric width)
        a <= (others => '0');
        wait for 10 ns;
        a <= (0 => '1', others => '0');
        wait for 10 ns;
        a <= (others => '1');
        wait for 10 ns;
        a <= (others => '0');
        wait for 10 ns;

        -- Test cases for b (parametric width)
        b <= (others => '0');
        wait for 10 ns;
        b <= (0 => '1', others => '0');
        wait for 10 ns;
        b <= (others => '1');
        wait for 10 ns;
        b <= (others => '0');
        wait for 10 ns;

        -- Test cases for op (parametric width)
        op <= (others => '0');
        wait for 10 ns;
        op <= (0 => '1', others => '0');
        wait for 10 ns;
        op <= (others => '1');
        wait for 10 ns;
        op <= (others => '0');
        wait for 10 ns;
        -- End simulation
        wait;
    end process;
end Behavioral;