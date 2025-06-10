library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;

entity PWM_Generator_tb is
end PWM_Generator_tb;

architecture Behavioral of PWM_Generator_tb is
    -- Component declaration
    component PWM_Generator
    generic (
        SYSTEM_CLOCK : integer := 100_000_000;
        PWM_FREQUENCY : integer := 10_000;
        PWM_RESOLUTION : integer := 8
    );
    port (
        clk : in STD_LOGIC;
        reset : in STD_LOGIC;
        duty_cycle : in STD_LOGIC_VECTOR(PWM_RESOLUTION-1 downto 0);
        pwm_out : out STD_LOGIC
    );
    end component;

    -- Generic constants
    constant SYSTEM_CLOCK : integer := 100_000_000;
    constant PWM_FREQUENCY : integer := 10_000;
    constant PWM_RESOLUTION : integer := 8;

    -- Signal declarations
    signal clk : STD_LOGIC;
    signal reset : STD_LOGIC;
    signal duty_cycle : STD_LOGIC_VECTOR(PWM_RESOLUTION-1 downto 0);
    signal pwm_out : STD_LOGIC;

    -- Simulation time
    constant SIM_TIME : time := 1300 ns;

begin
    -- Component instantiation
    UUT: PWM_Generator
    generic map (
        SYSTEM_CLOCK => SYSTEM_CLOCK,
        PWM_FREQUENCY => PWM_FREQUENCY,
        PWM_RESOLUTION => PWM_RESOLUTION
    )
    port map (
        clk => clk,
        reset => reset,
        duty_cycle => duty_cycle,
        pwm_out => pwm_out
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
        duty_cycle <= (others => '0');
        wait for 10 ns;  -- Allow signals to settle


        -- Test cases for duty_cycle (parametric width)
        duty_cycle <= (others => '0');
        wait for 10 ns;
        duty_cycle <= (0 => '1', others => '0');
        wait for 10 ns;
        duty_cycle <= (others => '1');
        wait for 10 ns;
        duty_cycle <= (others => '0');
        wait for 10 ns;
        -- End simulation
        wait;
    end process;
end Behavioral;