library ieee;
use ieee.std_logic_1164.all;

entity mux_4to1 is
    port (
        input0  : in  std_logic_vector(7 downto 0);
        input1  : in  std_logic_vector(7 downto 0);
        input2  : in  std_logic_vector(7 downto 0);
        input3  : in  std_logic_vector(7 downto 0);
        sel     : in  std_logic_vector(1 downto 0);
        output  : out std_logic_vector(7 downto 0)
    );
end entity mux_4to1;

architecture behavioral of mux_4to1 is
begin
    process(sel, input0, input1, input2, input3)
    begin
        case sel is
            when "00" => output <= input0;
            when "01" => output <= input1;
            when "10" => output <= input2;
            when "11" => output <= input3;
            when others => output <= (others => '0');
        end case;
    end process;
end architecture behavioral;