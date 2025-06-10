library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

entity fsm is
    port (
        clk  : in  STD_LOGIC;
        rst  : in  STD_LOGIC;
        input_sig : in  STD_LOGIC;
        output_sig: out STD_LOGIC
    );
end entity fsm;

architecture Behavioral of fsm is
    type state_type is (IDLE, S1, S2);  -- Define states
    signal state, next_state : state_type;

begin
    process (clk, rst)
    begin
        if rst = '1' then
            state <= IDLE;
        elsif rising_edge(clk) then
            state <= next_state;
        end if;
    end process;

    -- Next state logic
    process (state, input_sig)
    begin
        case state is
            when IDLE =>
                if input_sig = '1' then
                    next_state <= S1;
                else
                    next_state <= IDLE;
                end if;
            when S1 =>
                if input_sig = '1' then
                    next_state <= S2;
                else
                    next_state <= IDLE;
                end if;
            when S2 =>
                if input_sig = '1' then
                    next_state <= IDLE;
                else
                    next_state <= S1;
                end if;
            when others =>
                next_state <= IDLE;
        end case;
    end process;

    -- Output logic
    output_sig <= '1' when state = S2 else '0';
end architecture Behavioral;