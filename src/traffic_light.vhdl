library ieee;
use ieee.std_logic_1164.all;

entity traffic_light is
    port (
        clk         : in  std_logic;
        rst         : in  std_logic;
        sensor      : in  std_logic;  -- Car sensor input
        red_light   : out std_logic;
        yellow_light: out std_logic;
        green_light : out std_logic
    );
end entity traffic_light;

architecture behavioral of traffic_light is
    type state_type is (RED, YELLOW, GREEN);
    signal current_state, next_state : state_type;
    signal timer : integer range 0 to 50 := 0;
begin
    -- State register
    process(clk, rst)
    begin
        if rst = '1' then
            current_state <= RED;
            timer <= 0;
        elsif rising_edge(clk) then
            current_state <= next_state;
            if timer = 50 then
                timer <= 0;
            else
                timer <= timer + 1;
            end if;
        end if;
    end process;
    
    -- Next state logic
    process(current_state, timer, sensor)
    begin
        case current_state is
            when RED =>
                if timer = 50 and sensor = '1' then
                    next_state <= GREEN;
                else
                    next_state <= RED;
                end if;
            when YELLOW =>
                if timer = 20 then
                    next_state <= RED;
                else
                    next_state <= YELLOW;
                end if;
            when GREEN =>
                if timer = 40 then
                    next_state <= YELLOW;
                else
                    next_state <= GREEN;
                end if;
        end case;
    end process;
    
    -- Output logic
    red_light <= '1' when current_state = RED else '0';
    yellow_light <= '1' when current_state = YELLOW else '0';
    green_light <= '1' when current_state = GREEN else '0';
end architecture behavioral;