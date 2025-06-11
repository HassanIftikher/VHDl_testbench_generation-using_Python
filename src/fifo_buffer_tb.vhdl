library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;

entity fifo_buffer_tb is
end fifo_buffer_tb;

architecture Behavioral of fifo_buffer_tb is
    -- Component declaration
    component fifo_buffer
    generic (
        DATA_WIDTH : integer := 8;
        FIFO_DEPTH : integer := 16
    );
    port (
        clk : in STD_LOGIC;
        rst : in STD_LOGIC;
        wr_en : in STD_LOGIC;
        rd_en : in STD_LOGIC;
        data_in : in STD_LOGIC_VECTOR(DATA_WIDTH-1 downto 0);
        data_out : out STD_LOGIC_VECTOR(DATA_WIDTH-1 downto 0);
        empty : out STD_LOGIC;
        full : out STD_LOGIC
    );
    end component;

    -- Generic constants
    constant DATA_WIDTH : integer := 8;
    constant FIFO_DEPTH : integer := 16;

    -- Signal declarations
    signal clk : STD_LOGIC;
    signal rst : STD_LOGIC;
    signal wr_en : STD_LOGIC;
    signal rd_en : STD_LOGIC;
    signal data_in : STD_LOGIC_VECTOR(DATA_WIDTH-1 downto 0);
    signal data_out : STD_LOGIC_VECTOR(DATA_WIDTH-1 downto 0);
    signal empty : STD_LOGIC;
    signal full : STD_LOGIC;

    -- Simulation time
    constant SIM_TIME : time := 200 ns;

begin
    -- Component instantiation
    UUT: fifo_buffer
    generic map (
        DATA_WIDTH => DATA_WIDTH,
        FIFO_DEPTH => FIFO_DEPTH
    )
    port map (
        clk => clk,
        rst => rst,
        wr_en => wr_en,
        rd_en => rd_en,
        data_in => data_in,
        data_out => data_out,
        empty => empty,
        full => full
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
        wr_en <= '0';
        rd_en <= '0';
        data_in <= (others => '0');
        wait for 10 ns;  -- Allow signals to settle

        -- Test patterns for STD_LOGIC ports
        wr_en <= '0';
        rd_en <= '0';
        wait for 10 ns;

        wr_en <= '1';
        rd_en <= '0';
        wait for 10 ns;

        wr_en <= '0';
        rd_en <= '1';
        wait for 10 ns;

        wr_en <= '1';
        rd_en <= '1';
        wait for 10 ns;

        -- Write data to data_in (parametric width)
        data_in <= (others => '0');
        wait for 10 ns;
        data_in <= (0 => '1', 1 => '0', 3 => '1', 5 => '1', others => '0');  -- Example data pattern
        wait for 10 ns;
        data_in <= (0 => '0', 1 => '1', 3 => '0', 5 => '1', others => '0');  -- Example data pattern
        wait for 10 ns;
        -- End simulation
        wait;
    end process;
end Behavioral;