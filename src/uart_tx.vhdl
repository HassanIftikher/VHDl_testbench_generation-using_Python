library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity uart_tx is
    generic (
        CLKS_PER_BIT : integer := 434  -- 50MHz/115200
    );
    port (
        clk         : in  std_logic;
        rst         : in  std_logic;
        tx_start    : in  std_logic;
        tx_data     : in  std_logic_vector(7 downto 0);
        tx          : out std_logic;
        tx_busy     : out std_logic
    );
end entity uart_tx;

architecture behavioral of uart_tx is
    type state_type is (IDLE, START, DATA, STOP);
    signal state : state_type;
    signal clk_count : integer range 0 to CLKS_PER_BIT-1;
    signal bit_index : integer range 0 to 7;
    signal tx_data_reg : std_logic_vector(7 downto 0);
begin
    process(clk, rst)
    begin
        if rst = '1' then
            state <= IDLE;
            tx <= '1';
            tx_busy <= '0';
            clk_count <= 0;
            bit_index <= 0;
        elsif rising_edge(clk) then
            case state is
                when IDLE =>
                    tx <= '1';
                    tx_busy <= '0';
                    clk_count <= 0;
                    bit_index <= 0;
                    
                    if tx_start = '1' then
                        tx_data_reg <= tx_data;
                        state <= START;
                        tx_busy <= '1';
                    end if;
                
                when START =>
                    tx <= '0';
                    if clk_count < CLKS_PER_BIT-1 then
                        clk_count <= clk_count + 1;
                    else
                        state <= DATA;
                        clk_count <= 0;
                    end if;
                
                when DATA =>
                    tx <= tx_data_reg(bit_index);
                    if clk_count < CLKS_PER_BIT-1 then
                        clk_count <= clk_count + 1;
                    else
                        clk_count <= 0;
                        if bit_index < 7 then
                            bit_index <= bit_index + 1;
                        else
                            state <= STOP;
                        end if;
                    end if;
                
                when STOP =>
                    tx <= '1';
                    if clk_count < CLKS_PER_BIT-1 then
                        clk_count <= clk_count + 1;
                    else
                        state <= IDLE;
                    end if;
            end case;
        end if;
    end process;
end architecture behavioral;