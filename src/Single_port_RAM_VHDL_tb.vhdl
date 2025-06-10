library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;

entity Single_port_RAM_VHDL_tb is
end Single_port_RAM_VHDL_tb;

architecture Behavioral of Single_port_RAM_VHDL_tb is
    -- Component declaration
    component Single_port_RAM_VHDL
    port (
        RAM_ADDR : in STD_LOGIC_VECTOR(6 downto 0);
        RAM_DATA_IN : in STD_LOGIC_VECTOR(7 downto 0);
        RAM_WR : in STD_LOGIC;
        RAM_CLOCK : in STD_LOGIC;
        RAM_DATA_OUT : out STD_LOGIC_VECTOR(7 downto 0)
    );
    end component;

    -- Signal declarations
    signal RAM_ADDR : STD_LOGIC_VECTOR(6 downto 0);
    signal RAM_DATA_IN : STD_LOGIC_VECTOR(7 downto 0);
    signal RAM_WR : STD_LOGIC;
    signal RAM_CLOCK : STD_LOGIC;
    signal RAM_DATA_OUT : STD_LOGIC_VECTOR(7 downto 0);

    -- Simulation time
    constant SIM_TIME : time := 1550 ns;

begin
    -- Component instantiation
    UUT: Single_port_RAM_VHDL
    port map (
        RAM_ADDR => RAM_ADDR,
        RAM_DATA_IN => RAM_DATA_IN,
        RAM_WR => RAM_WR,
        RAM_CLOCK => RAM_CLOCK,
        RAM_DATA_OUT => RAM_DATA_OUT
    );

    -- Stimulus process
    stim_proc: process
    begin
        -- Initialize inputs
        -- Initialize all inputs to prevent undefined values
        RAM_ADDR <= (others => '0');
        RAM_DATA_IN <= (others => '0');
        RAM_WR <= '0';
        RAM_CLOCK <= '0';
        wait for 10 ns;  -- Allow signals to settle

        -- Test patterns for STD_LOGIC ports
        RAM_WR <= '0';
        RAM_CLOCK <= '0';
        wait for 10 ns;

        RAM_WR <= '1';
        RAM_CLOCK <= '0';
        wait for 10 ns;

        RAM_WR <= '0';
        RAM_CLOCK <= '1';
        wait for 10 ns;

        RAM_WR <= '1';
        RAM_CLOCK <= '1';
        wait for 10 ns;

        -- Test address RAM_ADDR (parametric width)
        RAM_ADDR <= (others => '0');
        wait for 10 ns;
        RAM_ADDR <= (2 => '1', 0 => '1', others => '0');  -- Example address pattern
        wait for 10 ns;

        -- Write data to RAM_DATA_IN (parametric width)
        RAM_DATA_IN <= (others => '0');
        wait for 10 ns;
        RAM_DATA_IN <= (0 => '1', 1 => '0', 3 => '1', 5 => '1', others => '0');  -- Example data pattern
        wait for 10 ns;
        RAM_DATA_IN <= (0 => '0', 1 => '1', 3 => '0', 5 => '1', others => '0');  -- Example data pattern
        wait for 10 ns;
        -- End simulation
        wait;
    end process;
end Behavioral;