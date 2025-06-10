library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

-- Uncomment the following library declaration if using
-- arithmetic functions with Signed or Unsigned values
use IEEE.NUMERIC_STD.ALL;

-- Uncomment the following library declaration if instantiating
-- any Xilinx leaf cells in this code.
--library UNISIM;
--use UNISIM.VComponents.all;

entity crc_shift is
    Port ( 
           clk     : in  STD_LOGIC;
           en      : in  STD_LOGIC;
           reset   : in  STD_LOGIC;
           DataIn  : in  STD_LOGIC;
           Polynom : in  STD_LOGIC_VECTOR (5 downto 0);
           CRC     : out STD_LOGIC_VECTOR (4 downto 0)
           );
end crc_shift;

architecture Behavioral of crc_shift is

    signal ShiftReg   : std_logic_vector(4 downto 0);
    signal PolynomCal : std_logic_vector(5 downto 0);
    --Polynom   <= "110101"; -- x^5+x^4+x^2+1 Bluetooth

begin

    CRC <= ShiftReg;
    PolynomCal <= Polynom when ShiftReg(4)='1' else (others=> '0');
    
    process(clk)
    begin
        if rising_edge(clk) then
            if reset='1' then
                ShiftReg <= (others=>'0');
            else
                if(en='1') then
                    ShiftReg(4 downto 1) <= ShiftReg(3 downto 0) xor PolynomCal(4 downto 1);
                    ShiftReg(0) <= DataIn xor PolynomCal(0);
                end if;
                
            end if;
        end if;
        
    end process;   
    
end Behavioral;