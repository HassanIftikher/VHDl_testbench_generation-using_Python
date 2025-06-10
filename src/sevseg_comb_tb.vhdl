library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;

entity sevseg_comb_tb is
end sevseg_comb_tb;

architecture Behavioral of sevseg_comb_tb is
    -- Component declaration
    component sevseg_comb
    port (
        sw : in STD_LOGIC_VECTOR(15 downto 0);
        sseg_ca : out STD_LOGIC_VECTOR(6 downto 0);
        sseg_an : out STD_LOGIC_VECTOR(3 downto 0)
    );
    end component;

    -- Signal declarations
    signal sw : STD_LOGIC_VECTOR(15 downto 0);
    signal sseg_ca : STD_LOGIC_VECTOR(6 downto 0);
    signal sseg_an : STD_LOGIC_VECTOR(3 downto 0);

    -- Simulation time
    constant SIM_TIME : time := 1450 ns;

begin
    -- Component instantiation
    UUT: sevseg_comb
    port map (
        sw => sw,
        sseg_ca => sseg_ca,
        sseg_an => sseg_an
    );

    -- Stimulus process
    stim_proc: process
    begin
        -- Initialize inputs
        -- Initialize all inputs to prevent undefined values
        sw <= (others => '0');
        wait for 10 ns;  -- Allow signals to settle


        -- Test cases for sw (parametric width)
        sw <= (others => '0');
        wait for 10 ns;
        sw <= (0 => '1', others => '0');
        wait for 10 ns;
        sw <= (others => '1');
        wait for 10 ns;
        sw <= (others => '0');
        wait for 10 ns;
        -- End simulation
        wait;
    end process;
end Behavioral;