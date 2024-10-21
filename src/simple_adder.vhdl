library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

entity simple_adder is
    Port ( clk : in STD_LOGIC;
           rst : in STD_LOGIC;
           d : in STD_LOGIC;
           q : out STD_LOGIC);
end simple_adder;

architecture Behavioral of simple_adder is
begin
    process(clk, rst)
    begin
        if rst = '1' then
            q <= '0';
        elsif rising_edge(clk) then
            q <= d;
        end if;
    end process;
end Behavioral;



