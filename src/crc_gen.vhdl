library ieee;
use ieee.std_logic_1164.all;

entity crc_gen is
    generic (
        POLYNOMIAL_WIDTH : integer := 16
    );
    port (
        clk         : in  std_logic;
        rst         : in  std_logic;
        data_in     : in  std_logic;
        crc_init    : in  std_logic;
        crc_out     : out std_logic_vector(POLYNOMIAL_WIDTH-1 downto 0)
    );
end entity crc_gen;

architecture behavioral of crc_gen is
    signal crc_reg : std_logic_vector(POLYNOMIAL_WIDTH-1 downto 0);
    constant polynomial : std_logic_vector(POLYNOMIAL_WIDTH-1 downto 0) := x"1021"; -- CRC-16-CCITT
begin
    process(clk, rst)
        variable feedback : std_logic;
    begin
        if rst = '1' then
            crc_reg <= (others => '1');
        elsif rising_edge(clk) then
            if crc_init = '1' then
                crc_reg <= (others => '1');
            else
                feedback := crc_reg(POLYNOMIAL_WIDTH-1) xor data_in;
                crc_reg <= crc_reg(POLYNOMIAL_WIDTH-2 downto 0) & '0';
                if feedback = '1' then
                    crc_reg <= crc_reg xor polynomial;
                end if;
            end if;
        end if;
    end process;
    
    crc_out <= crc_reg;
end architecture behavioral;