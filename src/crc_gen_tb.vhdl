library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;

entity crc_gen_tb is
end crc_gen_tb;

architecture Behavioral of crc_gen_tb is
    -- Component declaration
    component crc_gen
    generic (
        POLYNOMIAL_WIDTH : integer := 16
    );
    port (
        clk : in STD_LOGIC;
        rst : in STD_LOGIC;
        data_in : in STD_LOGIC;
        crc_init : in STD_LOGIC;
        crc_out : out STD_LOGIC_VECTOR(POLYNOMIAL_WIDTH-1 downto 0)
    );
    end component;

    -- Generic constants
    constant POLYNOMIAL_WIDTH : integer := 16;

    -- Signal declarations
    signal clk : STD_LOGIC;
    signal rst : STD_LOGIC;
    signal data_in : STD_LOGIC;
    signal crc_init : STD_LOGIC;
    signal crc_out : STD_LOGIC_VECTOR(POLYNOMIAL_WIDTH-1 downto 0);

    -- Simulation time
    constant SIM_TIME : time := 1350 ns;

begin
    -- Component instantiation
    UUT: crc_gen
    generic map (
        POLYNOMIAL_WIDTH => POLYNOMIAL_WIDTH
    )
    port map (
        clk => clk,
        rst => rst,
        data_in => data_in,
        crc_init => crc_init,
        crc_out => crc_out
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
        data_in <= '0';
        crc_init <= '0';
        wait for 10 ns;  -- Allow signals to settle

        -- Test patterns for STD_LOGIC ports
        data_in <= '0';
        crc_init <= '0';
        wait for 10 ns;

        data_in <= '1';
        crc_init <= '0';
        wait for 10 ns;

        data_in <= '0';
        crc_init <= '1';
        wait for 10 ns;

        data_in <= '1';
        crc_init <= '1';
        wait for 10 ns;
        -- End simulation
        wait;
    end process;
end Behavioral;