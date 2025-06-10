library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

entity sevseg_comb is
  port ( 
    sw      : in  STD_LOGIC_VECTOR(15 downto 0);
    sseg_ca : out STD_LOGIC_VECTOR(6 downto 0);
    sseg_an : out STD_LOGIC_VECTOR(3 downto 0)
    );
end sevseg_comb;

architecture arch_sevseg_comb of sevseg_comb is
begin
    sseg_ca <= "1000000" when sw(3 downto 0) = "0000" else
               "1111001" when sw(3 downto 0) = "0001" else
               "0100100" when sw(3 downto 0) = "0010" else
               "0110000" when sw(3 downto 0) = "0011" else
               "0011001" when sw(3 downto 0) = "0100" else
               "0010010" when sw(3 downto 0) = "0101" else
               "0000010" when sw(3 downto 0) = "0110" else
               "1111000" when sw(3 downto 0) = "0111" else
               "0000000" when sw(3 downto 0) = "1000" else
               "0010000" when sw(3 downto 0) = "1001" else
               "0001000" when sw(3 downto 0) = "1010" else
               "0000011" when sw(3 downto 0) = "1011" else
               "1000110" when sw(3 downto 0) = "1100" else
               "0100001" when sw(3 downto 0) = "1101" else
               "0000110" when sw(3 downto 0) = "1110" else
               "0001110";

    sseg_an(3) <= sw(15);
    sseg_an(2) <= sw(14);
    sseg_an(1) <= sw(13);
    sseg_an(0) <= sw(12);
end arch_sevseg_comb;