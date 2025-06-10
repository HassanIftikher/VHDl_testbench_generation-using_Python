library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

entity shift_register is
    port (
        clk  : in  STD_LOGIC;
        rst  : in  STD_LOGIC;
        d    : in  STD_LOGIC;
        q    : out STD_LOGIC_VECTOR(3 downto 0)
    );
end entity shift_register;

architecture Behavioral of shift_register is
    signal shift_reg : STD_LOGIC_VECTOR(3 downto 0);
begin
    process (clk, rst)
    begin
        if rst = '1' then
            shift_reg <= (others => '0');
        elsif rising_edge(clk) then
            shift_reg <= shift_reg(2 downto 0) & d;  -- Shift left and add `d` to LSB
        end if;
    end process;

    q <= shift_reg;
end architecture Behavioral;