library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity fifo_buffer is
    generic (
        DATA_WIDTH : integer := 8;
        FIFO_DEPTH : integer := 16
    );
    port (
        clk     : in  std_logic;
        rst     : in  std_logic;
        wr_en   : in  std_logic;
        rd_en   : in  std_logic;
        data_in : in  std_logic_vector(DATA_WIDTH-1 downto 0);
        data_out: out std_logic_vector(DATA_WIDTH-1 downto 0);
        empty   : out std_logic;
        full    : out std_logic
    );
end entity fifo_buffer;

architecture behavioral of fifo_buffer is
    type fifo_array is array (0 to FIFO_DEPTH-1) of std_logic_vector(DATA_WIDTH-1 downto 0);
    signal memory : fifo_array;
    signal wr_ptr, rd_ptr : unsigned(3 downto 0);
    signal count : unsigned(4 downto 0);
    signal internal_empty : std_logic;
    signal internal_full : std_logic;
begin
    -- Flag generation
    internal_empty <= '1' when count = 0 else '0';
    internal_full <= '1' when count = FIFO_DEPTH else '0';
    empty <= internal_empty;
    full <= internal_full;

    -- Write and read pointer management
    process(clk, rst)
    begin
        if rst = '1' then
            wr_ptr <= (others => '0');
            rd_ptr <= (others => '0');
            count <= (others => '0');
        elsif rising_edge(clk) then
            -- Write operation
            if wr_en = '1' and internal_full = '0' then
                memory(to_integer(wr_ptr)) <= data_in;
                if wr_ptr = FIFO_DEPTH-1 then
                    wr_ptr <= (others => '0');
                else
                    wr_ptr <= wr_ptr + 1;
                end if;
                count <= count + 1;
            end if;
            
            -- Read operation
            if rd_en = '1' and internal_empty = '0' then
                if rd_ptr = FIFO_DEPTH-1 then
                    rd_ptr <= (others => '0');
                else
                    rd_ptr <= rd_ptr + 1;
                end if;
                count <= count - 1;
            end if;
        end if;
    end process;

    -- Output data management
    process(memory, rd_ptr, internal_empty)
    begin
        if internal_empty = '1' then
            data_out <= (others => '0');
        else
            data_out <= memory(to_integer(rd_ptr));
        end if;
    end process;

end architecture behavioral;