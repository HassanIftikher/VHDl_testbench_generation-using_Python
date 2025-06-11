library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;

entity crc_shift_tb is
end crc_shift_tb;

architecture Behavioral of crc_shift_tb is
    -- Component declaration
    component crc_shift
    port (
        clk : in STD_LOGIC;
        en : in STD_LOGIC;
        reset : in STD_LOGIC;
        DataIn : in STD_LOGIC;
        Polynom : in STD_LOGIC_VECTOR(5 downto 0);
        CRC : out STD_LOGIC_VECTOR(4 downto 0)
    );
    end component;

    -- Signal declarations
    signal clk : STD_LOGIC;
    signal en : STD_LOGIC;
    signal reset : STD_LOGIC;
    signal DataIn : STD_LOGIC;
    signal Polynom : STD_LOGIC_VECTOR(5 downto 0);
    signal CRC : STD_LOGIC_VECTOR(4 downto 0);

    -- Simulation time
    constant SIM_TIME : time := 200 ns;

begin
    -- Component instantiation
    UUT: crc_shift
    port map (
        clk => clk,
        en => en,
        reset => reset,
        DataIn => DataIn,
        Polynom => Polynom,
        CRC => CRC
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
        reset <= '1';  -- Assert reset
        wait for 20 ns;
        reset <= '0';  -- Deassert reset
        wait;
    end process;

    -- Stimulus process
    stim_proc: process
    begin
        -- Initialize inputs
        -- Initialize all inputs to prevent undefined values
        en <= '0';
        DataIn <= '0';
        Polynom <= (others => '0');
        wait for 10 ns;  -- Allow signals to settle

        -- Test patterns for STD_LOGIC ports
        en <= '0';
        DataIn <= '0';
        wait for 10 ns;

        en <= '1';
        DataIn <= '0';
        wait for 10 ns;

        en <= '0';
        DataIn <= '1';
        wait for 10 ns;

        en <= '1';
        DataIn <= '1';
        wait for 10 ns;

        -- Test cases for Polynom (parametric width)
        Polynom <= (others => '0');
        wait for 10 ns;
        Polynom <= (0 => '1', others => '0');
        wait for 10 ns;
        Polynom <= (others => '1');
        wait for 10 ns;
        Polynom <= (others => '0');
        wait for 10 ns;
        -- End simulation
        wait;
    end process;
end Behavioral;