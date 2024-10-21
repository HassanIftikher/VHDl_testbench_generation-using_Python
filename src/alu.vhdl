library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;

entity alu is
    port (
        a     : in  STD_LOGIC_VECTOR(3 downto 0);
        b     : in  STD_LOGIC_VECTOR(3 downto 0);
        sel   : in  STD_LOGIC_VECTOR(1 downto 0);
        result: out STD_LOGIC_VECTOR(3 downto 0);
        carry : out STD_LOGIC
    );
end entity alu;

architecture Behavioral of alu is
    signal a_int, b_int, res_int : unsigned(3 downto 0);
    signal carry_int : unsigned(4 downto 0);
begin
    a_int <= unsigned(a);
    b_int <= unsigned(b);

    process (a_int, b_int, sel)
    begin
        case sel is
            when "00" => res_int <= a_int + b_int;  -- Add
            when "01" => res_int <= a_int - b_int;  -- Subtract
            when "10" => res_int <= a_int and b_int;-- AND
            when others => res_int <= a_int or b_int; -- OR
        end case;
    end process;

    carry_int <= ('0' & a_int) + ('0' & b_int);  -- Calculate carry
    result <= std_logic_vector(res_int);
    carry <= carry_int(4);
end architecture Behavioral;
