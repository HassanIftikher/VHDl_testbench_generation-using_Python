library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;

entity PWM_Generator is
    Generic (
        SYSTEM_CLOCK : integer := 100_000_000;  -- System clock frequency (Hz)
        PWM_FREQUENCY : integer := 10_000;      -- PWM frequency (Hz)
        PWM_RESOLUTION : integer := 8           -- PWM resolution in bits
    );
    Port ( 
        clk       : in STD_LOGIC;
        reset     : in STD_LOGIC;
        duty_cycle: in STD_LOGIC_VECTOR(PWM_RESOLUTION-1 downto 0);
        pwm_out   : out STD_LOGIC
    );
end PWM_Generator;

architecture Behavioral of PWM_Generator is
    -- Calculate the timer period
    constant TIMER_PERIOD : integer := SYSTEM_CLOCK / PWM_FREQUENCY;
    
    -- Internal signals for counter and comparison
    signal counter : unsigned(PWM_RESOLUTION-1 downto 0) := (others => '0');
    signal pwm_reg : STD_LOGIC := '0';
    
begin
    -- PWM Generation Process
    PWM_PROC: process(clk, reset)
    begin
        if reset = '1' then
            counter <= (others => '0');
            pwm_reg <= '0';
        elsif rising_edge(clk) then
            -- Increment counter
            if counter < unsigned(duty_cycle) then
                pwm_reg <= '1';
            else
                pwm_reg <= '0';
            end if;
            
            -- Reset counter at full cycle
            if counter = (2**PWM_RESOLUTION - 1) then
                counter <= (others => '0');
            else
                counter <= counter + 1;
            end if;
        end if;
    end process PWM_PROC;
    
    -- Output assignment
    pwm_out <= pwm_reg;
end Behavioral;