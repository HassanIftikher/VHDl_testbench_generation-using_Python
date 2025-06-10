library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;

entity uart_tx_tb is
end uart_tx_tb;

architecture Behavioral of uart_tx_tb is
    -- Component declaration
    component uart_tx
    generic (
        CLKS_PER_BIT : integer := 434
    );
    port (
        clk : in STD_LOGIC;
        rst : in STD_LOGIC;
        tx_start : in STD_LOGIC;
        tx_data : in STD_LOGIC_VECTOR(7 downto 0);
        tx : out STD_LOGIC;
        tx_busy : out STD_LOGIC
    );
    end component;

    -- Generic constants
    constant CLKS_PER_BIT : integer := 434;

    -- Signal declarations
    signal clk : STD_LOGIC;
    signal rst : STD_LOGIC;
    signal tx_start : STD_LOGIC;
    signal tx_data : STD_LOGIC_VECTOR(7 downto 0);
    signal tx : STD_LOGIC;
    signal tx_busy : STD_LOGIC;

    -- Simulation time
    constant SIM_TIME : time := 1400 ns;

begin
    -- Component instantiation
    UUT: uart_tx
    generic map (
        CLKS_PER_BIT => CLKS_PER_BIT
    )
    port map (
        clk => clk,
        rst => rst,
        tx_start => tx_start,
        tx_data => tx_data,
        tx => tx,
        tx_busy => tx_busy
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
        tx_start <= '0';
        tx_data <= (others => '0');
        wait for 10 ns;  -- Allow signals to settle

        -- Test patterns for STD_LOGIC ports
        tx_start <= '1';
        wait for 50 ns;

        tx_start <= '0';
        wait for 10 ns;

        -- Write data to tx_data (parametric width)
        tx_data <= (others => '0');
        wait for 10 ns;
        tx_data <= (0 => '1', 1 => '0', 3 => '1', 5 => '1', others => '0');  -- Example data pattern
        wait for 10 ns;
        tx_data <= (0 => '0', 1 => '1', 3 => '0', 5 => '1', others => '0');  -- Example data pattern
        wait for 10 ns;
        -- End simulation
        wait;
    end process;
end Behavioral;