---------------------------------------------------------------------
--	Filename:	gh_filter_compensation_6dB.vhd
--
--	Description:
--		a 3rd order FIR compensation Filter - 
--		   with coefficients of [-.125 .75 -.125]
--		   has gain of -6 dB (at DC) to +0 dB (at .5 sample rate)
--		   uses shift and add (uses no multipliers)
--
--	Copyright (c) 2007 by George Huber 
--		an OpenCores.org Project
--		free to use, but see documentation for conditions  
--
--	Revision 	History:
--	Revision 	Date       	Author   	Comment
--	-------- 	---------- 	---------	-----------
--	1.0      	10/14/07  	H LeFevre	Initial revision
--
-----------------------------------------------------------------------------

library IEEE;
use IEEE.STD_LOGIC_1164.all;
use IEEE.STD_LOGIC_arith.all;
use IEEE.STD_LOGIC_signed.all;

entity gh_filter_compensation_6dB is
	GENERIC (size: INTEGER :=16);
	port(
		clk : in STD_LOGIC;
		rst : in STD_LOGIC;
		ce  : in STD_LOGIC:='1';
		D   : in STD_LOGIC_VECTOR(size-1 downto 0);
		Q   : out STD_LOGIC_VECTOR(size-1 downto 0)
		);
end entity;

architecture a of gh_filter_compensation_6dB is

	signal iD_d2  : STD_LOGIC_VECTOR(size downto 0);
	signal iD_d4  : STD_LOGIC_VECTOR(size downto 0);
	signal iD_d8  : STD_LOGIC_VECTOR(size downto 0);
	
	signal t0_A  : STD_LOGIC_VECTOR(size downto 0);
	signal t0_B  : STD_LOGIC_VECTOR(size downto 0);
	signal t1_A  : STD_LOGIC_VECTOR(size downto 0);
	signal t1_B  : STD_LOGIC_VECTOR(size downto 0);
	signal iQ    : STD_LOGIC_VECTOR(size downto 0);
	
begin
	
	Q <= iQ(size downto 1);

	iD_d2  <= D(size-1) & D;
	iD_d4  <= D(size-1) & D(size-1) & D(size-1 downto 1);
	iD_d8  <= D(size-1) & D(size-1) & D(size-1) & D(size-1 downto 2);

process (clk,rst)
begin
	if (rst = '1')	then
		t0_A <= (others => '0');
		t0_B <= (others => '0');
		t1_A <= (others => '0');
		t1_B <= (others => '0');
		iQ <= (others => '0');
	elsif (rising_edge(CLK)) then
		if (ce = '1') then
			t0_A <= iD_d8;
			t0_B <= iD_d2 + iD_d4;
			t1_A <= t0_A;
			t1_B <= t0_B - t1_A;
			iQ <= t1_B - t0_A;
		end if;
	end if;
end process;

end a;
