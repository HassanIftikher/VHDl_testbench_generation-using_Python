library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;

entity counter_with_enable is
    Port (
        clk : in STD_LOGIC;
        rst : in STD_LOGIC;
        enable : in STD_LOGIC;
        count : out STD_LOGIC_VECTOR(3 downto 0)
    );
end counter_with_enable;

architecture Behavioral of counter_with_enable is
    signal count_int : unsigned(3 downto 0) := (others => '0');  -- Initialize counter to zero
begin
    process(clk)
    begin
        if rising_edge(clk) then
            if rst = '1' then
                count_int <= (others => '0');  -- Synchronous reset: reset the counter to zero
            elsif enable = '1' then
                if count_int = "1111" then  -- Optional overflow check
                    count_int <= (others => '0');  -- Reset to zero on overflow
                else
                    count_int <= count_int + 1;  -- Increment counter when enabled
                end if;
            end if;
        end if;
    end process;

    count <= std_logic_vector(count_int);  -- Output the internal unsigned counter as std_logic_vector
end Behavioral;
