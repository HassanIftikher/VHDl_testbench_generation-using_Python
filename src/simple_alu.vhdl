library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;

entity simple_alu is
    Port ( 
        a       : in  STD_LOGIC_VECTOR(7 downto 0);
        b       : in  STD_LOGIC_VECTOR(7 downto 0);
        op_sel  : in  STD_LOGIC_VECTOR(2 downto 0);  -- Operation select
        result  : out STD_LOGIC_VECTOR(7 downto 0);
        zero    : out STD_LOGIC;                      -- Zero flag
        carry   : out STD_LOGIC                       -- Carry flag
    );
end simple_alu;

architecture Behavioral of simple_alu is
    signal temp_result : STD_LOGIC_VECTOR(8 downto 0);  -- 9 bits for carry
begin
    process(a, b, op_sel)
        variable a_unsigned : unsigned(8 downto 0);
        variable b_unsigned : unsigned(8 downto 0);
    begin
        -- Zero-extend inputs to 9 bits for carry detection
        a_unsigned := '0' & unsigned(a);
        b_unsigned := '0' & unsigned(b);
        
        case op_sel is
            when "000" =>  -- Addition
                temp_result <= std_logic_vector(a_unsigned + b_unsigned);
                
            when "001" =>  -- Subtraction
                temp_result <= std_logic_vector(a_unsigned - b_unsigned);
                
            when "010" =>  -- AND
                temp_result <= '0' & (a and b);
                
            when "011" =>  -- OR
                temp_result <= '0' & (a or b);
                
            when "100" =>  -- XOR
                temp_result <= '0' & (a xor b);
                
            when others => -- Default case
                temp_result <= (others => '0');
        end case;
    end process;

    -- Output assignments
    result <= temp_result(7 downto 0);
    carry  <= temp_result(8);
    zero   <= '1' when temp_result(7 downto 0) = "00000000" else '0';

end Behavioral;