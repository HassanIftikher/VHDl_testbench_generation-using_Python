library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity alu is
    port (
        a       : in  std_logic_vector(7 downto 0);
        b       : in  std_logic_vector(7 downto 0);
        op      : in  std_logic_vector(2 downto 0);
        result  : out std_logic_vector(7 downto 0);
        zero    : out std_logic;
        carry   : out std_logic;
        overflow: out std_logic
    );
end entity alu;

architecture behavioral of alu is
    signal result_internal : std_logic_vector(8 downto 0);
begin
    process(a, b, op)
        variable temp : signed(8 downto 0);
    begin
        case op is
            when "000" => -- ADD
                result_internal <= std_logic_vector(unsigned('0' & a) + unsigned('0' & b));
            when "001" => -- SUB
                result_internal <= std_logic_vector(unsigned('0' & a) - unsigned('0' & b));
            when "010" => -- AND
                result_internal <= '0' & (a and b);
            when "011" => -- OR
                result_internal <= '0' & (a or b);
            when "100" => -- XOR
                result_internal <= '0' & (a xor b);
            when "101" => -- SHL
                result_internal <= a & '0';
            when others =>
                result_internal <= (others => '0');
        end case;
    end process;
    
    result <= result_internal(7 downto 0);
    carry <= result_internal(8);
    zero <= '1' when result_internal(7 downto 0) = "00000000" else '0';
    overflow <= result_internal(8) xor result_internal(7);
end architecture behavioral;