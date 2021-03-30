---------------------------------------------------------------------
--	Filename:	gh_tvfd_coef_prom.vhd
--			
--	Description:
--		Coefficient prom for 8th order, 100 point TVFD filter 
--
--	Copyright (c) 2005, 2006 by George Huber 
--		an OpenCores.org Project
--		free to use, but see documentation for conditions 
--
--	Revision 	History:
--	Revision 	Date      	Author   	Comment
--	-------- 	----------	---------	-----------
--	1.0      	09/03/05  	S A Dodd 	Initial revision
--	2.0     	09/17/05  	h LeFevre	add tvfd_ to name
--	1.1      	02/18/06  	G Huber 	add gh_ to name
--	
------------------------------------------------------------------

library IEEE;
use IEEE.std_logic_1164.all;
use IEEE.std_logic_unsigned.all;

entity gh_tvfd_coef_prom is
	port (
		CLK : in std_logic;
		ADD : in std_logic_vector(9 downto 0);
		Q : out std_logic_vector(15 downto 0)
	);
end entity;


architecture a of gh_tvfd_coef_prom is

	signal iADD :  STD_LOGIC_VECTOR(11 DOWNTO 0);
	signal iQ :  STD_LOGIC_VECTOR(15 DOWNTO 0);

begin

PROCESS (CLK)
BEGIN
	if (rising_edge(clk)) then
		iADD <= "0" & "0" & ADD;

	end if;
END PROCESS;

PROCESS (CLK)
BEGIN
	if (rising_edge (clk)) then
		Q <= iQ;
	end if;
END PROCESS;

process(iADD)
begin
    case (iADD) is
          when x"000" => iQ <= x"0000"; 
          when x"001" => iQ <= x"0000"; 
          when x"002" => iQ <= x"0000"; 
          when x"003" => iQ <= x"0000"; 
          when x"004" => iQ <= x"7FFF"; 
          when x"005" => iQ <= x"0000"; 
          when x"006" => iQ <= x"0000"; 
          when x"007" => iQ <= x"0000"; 
          when x"008" => iQ <= x"FFFE"; 
          when x"009" => iQ <= x"0016"; 
          when x"00A" => iQ <= x"FF9D"; 
          when x"00B" => iQ <= x"014A"; 
          when x"00C" => iQ <= x"7FA9"; 
          when x"00D" => iQ <= x"FF3E"; 
          when x"00E" => iQ <= x"0021"; 
          when x"00F" => iQ <= x"FFFD"; 
          when x"010" => iQ <= x"FFFB"; 
          when x"011" => iQ <= x"002C"; 
          when x"012" => iQ <= x"FF3B"; 
          when x"013" => iQ <= x"0299"; 
          when x"014" => iQ <= x"7F49"; 
          when x"015" => iQ <= x"FE81"; 
          when x"016" => iQ <= x"0041"; 
          when x"017" => iQ <= x"FFFA"; 
          when x"018" => iQ <= x"FFF9"; 
          when x"019" => iQ <= x"0042"; 
          when x"01A" => iQ <= x"FED7"; 
          when x"01B" => iQ <= x"03ED"; 
          when x"01C" => iQ <= x"7EE1"; 
          when x"01D" => iQ <= x"FDC8"; 
          when x"01E" => iQ <= x"0060"; 
          when x"01F" => iQ <= x"FFF7"; 
          when x"020" => iQ <= x"FFF7"; 
          when x"021" => iQ <= x"0057"; 
          when x"022" => iQ <= x"FE74"; 
          when x"023" => iQ <= x"0545"; 
          when x"024" => iQ <= x"7E71"; 
          when x"025" => iQ <= x"FD15"; 
          when x"026" => iQ <= x"007F"; 
          when x"027" => iQ <= x"FFF4"; 
          when x"028" => iQ <= x"FFF4"; 
          when x"029" => iQ <= x"006D"; 
          when x"02A" => iQ <= x"FE10"; 
          when x"02B" => iQ <= x"06A1"; 
          when x"02C" => iQ <= x"7DF7"; 
          when x"02D" => iQ <= x"FC67"; 
          when x"02E" => iQ <= x"009D"; 
          when x"02F" => iQ <= x"FFF1"; 
          when x"030" => iQ <= x"FFF2"; 
          when x"031" => iQ <= x"0083"; 
          when x"032" => iQ <= x"FDAC"; 
          when x"033" => iQ <= x"0802"; 
          when x"034" => iQ <= x"7D76"; 
          when x"035" => iQ <= x"FBBD"; 
          when x"036" => iQ <= x"00BB"; 
          when x"037" => iQ <= x"FFEE"; 
          when x"038" => iQ <= x"FFF0"; 
          when x"039" => iQ <= x"0099"; 
          when x"03A" => iQ <= x"FD48"; 
          when x"03B" => iQ <= x"0967"; 
          when x"03C" => iQ <= x"7CEB"; 
          when x"03D" => iQ <= x"FB19"; 
          when x"03E" => iQ <= x"00D8"; 
          when x"03F" => iQ <= x"FFEB"; 
          when x"040" => iQ <= x"FFED"; 
          when x"041" => iQ <= x"00AE"; 
          when x"042" => iQ <= x"FCE4"; 
          when x"043" => iQ <= x"0AD0"; 
          when x"044" => iQ <= x"7C58"; 
          when x"045" => iQ <= x"FA79"; 
          when x"046" => iQ <= x"00F5"; 
          when x"047" => iQ <= x"FFE8"; 
          when x"048" => iQ <= x"FFEB"; 
          when x"049" => iQ <= x"00C4"; 
          when x"04A" => iQ <= x"FC80"; 
          when x"04B" => iQ <= x"0C3D"; 
          when x"04C" => iQ <= x"7BBD"; 
          when x"04D" => iQ <= x"F9DF"; 
          when x"04E" => iQ <= x"0111"; 
          when x"04F" => iQ <= x"FFE6"; 
          when x"050" => iQ <= x"FFE9"; 
          when x"051" => iQ <= x"00D9"; 
          when x"052" => iQ <= x"FC1D"; 
          when x"053" => iQ <= x"0DAE"; 
          when x"054" => iQ <= x"7B1A"; 
          when x"055" => iQ <= x"F949"; 
          when x"056" => iQ <= x"012C"; 
          when x"057" => iQ <= x"FFE3"; 
          when x"058" => iQ <= x"FFE7"; 
          when x"059" => iQ <= x"00EF"; 
          when x"05A" => iQ <= x"FBB9"; 
          when x"05B" => iQ <= x"0F22"; 
          when x"05C" => iQ <= x"7A6F"; 
          when x"05D" => iQ <= x"F8B8"; 
          when x"05E" => iQ <= x"0147"; 
          when x"05F" => iQ <= x"FFE0"; 
          when x"060" => iQ <= x"FFE4"; 
          when x"061" => iQ <= x"0104"; 
          when x"062" => iQ <= x"FB57"; 
          when x"063" => iQ <= x"109A"; 
          when x"064" => iQ <= x"79BC"; 
          when x"065" => iQ <= x"F82D"; 
          when x"066" => iQ <= x"0161"; 
          when x"067" => iQ <= x"FFDE"; 
          when x"068" => iQ <= x"FFE2"; 
          when x"069" => iQ <= x"0119"; 
          when x"06A" => iQ <= x"FAF4"; 
          when x"06B" => iQ <= x"1215"; 
          when x"06C" => iQ <= x"7900"; 
          when x"06D" => iQ <= x"F7A6"; 
          when x"06E" => iQ <= x"017A"; 
          when x"06F" => iQ <= x"FFDB"; 
          when x"070" => iQ <= x"FFE0"; 
          when x"071" => iQ <= x"012D"; 
          when x"072" => iQ <= x"FA92"; 
          when x"073" => iQ <= x"1393"; 
          when x"074" => iQ <= x"783D"; 
          when x"075" => iQ <= x"F724"; 
          when x"076" => iQ <= x"0193"; 
          when x"077" => iQ <= x"FFD9"; 
          when x"078" => iQ <= x"FFDE"; 
          when x"079" => iQ <= x"0142"; 
          when x"07A" => iQ <= x"FA30"; 
          when x"07B" => iQ <= x"1514"; 
          when x"07C" => iQ <= x"7773"; 
          when x"07D" => iQ <= x"F6A7"; 
          when x"07E" => iQ <= x"01AB"; 
          when x"07F" => iQ <= x"FFD6"; 
          when x"080" => iQ <= x"FFDC"; 
          when x"081" => iQ <= x"0156"; 
          when x"082" => iQ <= x"F9D0"; 
          when x"083" => iQ <= x"1698"; 
          when x"084" => iQ <= x"76A0"; 
          when x"085" => iQ <= x"F62F"; 
          when x"086" => iQ <= x"01C2"; 
          when x"087" => iQ <= x"FFD4"; 
          when x"088" => iQ <= x"FFDA"; 
          when x"089" => iQ <= x"016A"; 
          when x"08A" => iQ <= x"F96F"; 
          when x"08B" => iQ <= x"181F"; 
          when x"08C" => iQ <= x"75C6"; 
          when x"08D" => iQ <= x"F5BC"; 
          when x"08E" => iQ <= x"01D8"; 
          when x"08F" => iQ <= x"FFD2"; 
          when x"090" => iQ <= x"FFD8"; 
          when x"091" => iQ <= x"017E"; 
          when x"092" => iQ <= x"F910"; 
          when x"093" => iQ <= x"19A9"; 
          when x"094" => iQ <= x"74E5"; 
          when x"095" => iQ <= x"F54D"; 
          when x"096" => iQ <= x"01EE"; 
          when x"097" => iQ <= x"FFD0"; 
          when x"098" => iQ <= x"FFD6"; 
          when x"099" => iQ <= x"0192"; 
          when x"09A" => iQ <= x"F8B2"; 
          when x"09B" => iQ <= x"1B35"; 
          when x"09C" => iQ <= x"73FD"; 
          when x"09D" => iQ <= x"F4E3"; 
          when x"09E" => iQ <= x"0203"; 
          when x"09F" => iQ <= x"FFCD"; 
          when x"0A0" => iQ <= x"FFD4"; 
          when x"0A1" => iQ <= x"01A5"; 
          when x"0A2" => iQ <= x"F854"; 
          when x"0A3" => iQ <= x"1CC3"; 
          when x"0A4" => iQ <= x"730D"; 
          when x"0A5" => iQ <= x"F47F"; 
          when x"0A6" => iQ <= x"0218"; 
          when x"0A7" => iQ <= x"FFCB"; 
          when x"0A8" => iQ <= x"FFD2"; 
          when x"0A9" => iQ <= x"01B8"; 
          when x"0AA" => iQ <= x"F7F8"; 
          when x"0AB" => iQ <= x"1E54"; 
          when x"0AC" => iQ <= x"7217"; 
          when x"0AD" => iQ <= x"F41F"; 
          when x"0AE" => iQ <= x"022B"; 
          when x"0AF" => iQ <= x"FFC9"; 
          when x"0B0" => iQ <= x"FFD0"; 
          when x"0B1" => iQ <= x"01CA"; 
          when x"0B2" => iQ <= x"F79D"; 
          when x"0B3" => iQ <= x"1FE6"; 
          when x"0B4" => iQ <= x"7119"; 
          when x"0B5" => iQ <= x"F3C3"; 
          when x"0B6" => iQ <= x"023E"; 
          when x"0B7" => iQ <= x"FFC7"; 
          when x"0B8" => iQ <= x"FFCE"; 
          when x"0B9" => iQ <= x"01DC"; 
          when x"0BA" => iQ <= x"F743"; 
          when x"0BB" => iQ <= x"217B"; 
          when x"0BC" => iQ <= x"7015"; 
          when x"0BD" => iQ <= x"F36D"; 
          when x"0BE" => iQ <= x"0250"; 
          when x"0BF" => iQ <= x"FFC6"; 
          when x"0C0" => iQ <= x"FFCC"; 
          when x"0C1" => iQ <= x"01EE"; 
          when x"0C2" => iQ <= x"F6EA"; 
          when x"0C3" => iQ <= x"2311"; 
          when x"0C4" => iQ <= x"6F0A"; 
          when x"0C5" => iQ <= x"F31B"; 
          when x"0C6" => iQ <= x"0261"; 
          when x"0C7" => iQ <= x"FFC4"; 
          when x"0C8" => iQ <= x"FFCA"; 
          when x"0C9" => iQ <= x"0200"; 
          when x"0CA" => iQ <= x"F693"; 
          when x"0CB" => iQ <= x"24A8"; 
          when x"0CC" => iQ <= x"6DF8"; 
          when x"0CD" => iQ <= x"F2CE"; 
          when x"0CE" => iQ <= x"0272"; 
          when x"0CF" => iQ <= x"FFC2"; 
          when x"0D0" => iQ <= x"FFC9"; 
          when x"0D1" => iQ <= x"0211"; 
          when x"0D2" => iQ <= x"F63D"; 
          when x"0D3" => iQ <= x"2641"; 
          when x"0D4" => iQ <= x"6CE0"; 
          when x"0D5" => iQ <= x"F285"; 
          when x"0D6" => iQ <= x"0281"; 
          when x"0D7" => iQ <= x"FFC0"; 
          when x"0D8" => iQ <= x"FFC7"; 
          when x"0D9" => iQ <= x"0222"; 
          when x"0DA" => iQ <= x"F5E9"; 
          when x"0DB" => iQ <= x"27DB"; 
          when x"0DC" => iQ <= x"6BC2"; 
          when x"0DD" => iQ <= x"F241"; 
          when x"0DE" => iQ <= x"0290"; 
          when x"0DF" => iQ <= x"FFBF"; 
          when x"0E0" => iQ <= x"FFC5"; 
          when x"0E1" => iQ <= x"0232"; 
          when x"0E2" => iQ <= x"F596"; 
          when x"0E3" => iQ <= x"2976"; 
          when x"0E4" => iQ <= x"6A9E"; 
          when x"0E5" => iQ <= x"F202"; 
          when x"0E6" => iQ <= x"029E"; 
          when x"0E7" => iQ <= x"FFBD"; 
          when x"0E8" => iQ <= x"FFC4"; 
          when x"0E9" => iQ <= x"0242"; 
          when x"0EA" => iQ <= x"F545"; 
          when x"0EB" => iQ <= x"2B12"; 
          when x"0EC" => iQ <= x"6974"; 
          when x"0ED" => iQ <= x"F1C7"; 
          when x"0EE" => iQ <= x"02AC"; 
          when x"0EF" => iQ <= x"FFBC"; 
          when x"0F0" => iQ <= x"FFC2"; 
          when x"0F1" => iQ <= x"0251"; 
          when x"0F2" => iQ <= x"F4F6"; 
          when x"0F3" => iQ <= x"2CAF"; 
          when x"0F4" => iQ <= x"6843"; 
          when x"0F5" => iQ <= x"F190"; 
          when x"0F6" => iQ <= x"02B8"; 
          when x"0F7" => iQ <= x"FFBB"; 
          when x"0F8" => iQ <= x"FFC1"; 
          when x"0F9" => iQ <= x"0260"; 
          when x"0FA" => iQ <= x"F4A8"; 
          when x"0FB" => iQ <= x"2E4D"; 
          when x"0FC" => iQ <= x"670E"; 
          when x"0FD" => iQ <= x"F15E"; 
          when x"0FE" => iQ <= x"02C4"; 
          when x"0FF" => iQ <= x"FFB9"; 
          when x"100" => iQ <= x"FFBF"; 
          when x"101" => iQ <= x"026E"; 
          when x"102" => iQ <= x"F45D"; 
          when x"103" => iQ <= x"2FEA"; 
          when x"104" => iQ <= x"65D2"; 
          when x"105" => iQ <= x"F131"; 
          when x"106" => iQ <= x"02CF"; 
          when x"107" => iQ <= x"FFB8"; 
          when x"108" => iQ <= x"FFBE"; 
          when x"109" => iQ <= x"027C"; 
          when x"10A" => iQ <= x"F414"; 
          when x"10B" => iQ <= x"3188"; 
          when x"10C" => iQ <= x"6491"; 
          when x"10D" => iQ <= x"F107"; 
          when x"10E" => iQ <= x"02D9"; 
          when x"10F" => iQ <= x"FFB7"; 
          when x"110" => iQ <= x"FFBD"; 
          when x"111" => iQ <= x"028A"; 
          when x"112" => iQ <= x"F3CC"; 
          when x"113" => iQ <= x"3327"; 
          when x"114" => iQ <= x"634B"; 
          when x"115" => iQ <= x"F0E2"; 
          when x"116" => iQ <= x"02E3"; 
          when x"117" => iQ <= x"FFB6"; 
          when x"118" => iQ <= x"FFBB"; 
          when x"119" => iQ <= x"0297"; 
          when x"11A" => iQ <= x"F387"; 
          when x"11B" => iQ <= x"34C5"; 
          when x"11C" => iQ <= x"61FF"; 
          when x"11D" => iQ <= x"F0C2"; 
          when x"11E" => iQ <= x"02EB"; 
          when x"11F" => iQ <= x"FFB5"; 
          when x"120" => iQ <= x"FFBA"; 
          when x"121" => iQ <= x"02A3"; 
          when x"122" => iQ <= x"F344"; 
          when x"123" => iQ <= x"3662"; 
          when x"124" => iQ <= x"60AF"; 
          when x"125" => iQ <= x"F0A5"; 
          when x"126" => iQ <= x"02F3"; 
          when x"127" => iQ <= x"FFB4"; 
          when x"128" => iQ <= x"FFB9"; 
          when x"129" => iQ <= x"02AF"; 
          when x"12A" => iQ <= x"F303"; 
          when x"12B" => iQ <= x"3800"; 
          when x"12C" => iQ <= x"5F5A"; 
          when x"12D" => iQ <= x"F08D"; 
          when x"12E" => iQ <= x"02FA"; 
          when x"12F" => iQ <= x"FFB3"; 
          when x"130" => iQ <= x"FFB8"; 
          when x"131" => iQ <= x"02BA"; 
          when x"132" => iQ <= x"F2C5"; 
          when x"133" => iQ <= x"399D"; 
          when x"134" => iQ <= x"5E00"; 
          when x"135" => iQ <= x"F078"; 
          when x"136" => iQ <= x"0300"; 
          when x"137" => iQ <= x"FFB3"; 
          when x"138" => iQ <= x"FFB7"; 
          when x"139" => iQ <= x"02C5"; 
          when x"13A" => iQ <= x"F289"; 
          when x"13B" => iQ <= x"3B39"; 
          when x"13C" => iQ <= x"5CA1"; 
          when x"13D" => iQ <= x"F068"; 
          when x"13E" => iQ <= x"0306"; 
          when x"13F" => iQ <= x"FFB2"; 
          when x"140" => iQ <= x"FFB6"; 
          when x"141" => iQ <= x"02CF"; 
          when x"142" => iQ <= x"F250"; 
          when x"143" => iQ <= x"3CD4"; 
          when x"144" => iQ <= x"5B3E"; 
          when x"145" => iQ <= x"F05C"; 
          when x"146" => iQ <= x"030B"; 
          when x"147" => iQ <= x"FFB1"; 
          when x"148" => iQ <= x"FFB5"; 
          when x"149" => iQ <= x"02D8"; 
          when x"14A" => iQ <= x"F21A"; 
          when x"14B" => iQ <= x"3E6E"; 
          when x"14C" => iQ <= x"59D7"; 
          when x"14D" => iQ <= x"F053"; 
          when x"14E" => iQ <= x"030F"; 
          when x"14F" => iQ <= x"FFB1"; 
          when x"150" => iQ <= x"FFB4"; 
          when x"151" => iQ <= x"02E1"; 
          when x"152" => iQ <= x"F1E6"; 
          when x"153" => iQ <= x"4007"; 
          when x"154" => iQ <= x"586C"; 
          when x"155" => iQ <= x"F04F"; 
          when x"156" => iQ <= x"0312"; 
          when x"157" => iQ <= x"FFB1"; 
          when x"158" => iQ <= x"FFB3"; 
          when x"159" => iQ <= x"02E9"; 
          when x"15A" => iQ <= x"F1B5"; 
          when x"15B" => iQ <= x"419F"; 
          when x"15C" => iQ <= x"56FC"; 
          when x"15D" => iQ <= x"F04E"; 
          when x"15E" => iQ <= x"0314"; 
          when x"15F" => iQ <= x"FFB0"; 
          when x"160" => iQ <= x"FFB3"; 
          when x"161" => iQ <= x"02F1"; 
          when x"162" => iQ <= x"F186"; 
          when x"163" => iQ <= x"4335"; 
          when x"164" => iQ <= x"5589"; 
          when x"165" => iQ <= x"F052"; 
          when x"166" => iQ <= x"0316"; 
          when x"167" => iQ <= x"FFB0"; 
          when x"168" => iQ <= x"FFB2"; 
          when x"169" => iQ <= x"02F8"; 
          when x"16A" => iQ <= x"F15B"; 
          when x"16B" => iQ <= x"44C9"; 
          when x"16C" => iQ <= x"5412"; 
          when x"16D" => iQ <= x"F058"; 
          when x"16E" => iQ <= x"0317"; 
          when x"16F" => iQ <= x"FFB0"; 
          when x"170" => iQ <= x"FFB1"; 
          when x"171" => iQ <= x"02FE"; 
          when x"172" => iQ <= x"F133"; 
          when x"173" => iQ <= x"465C"; 
          when x"174" => iQ <= x"5298"; 
          when x"175" => iQ <= x"F063"; 
          when x"176" => iQ <= x"0317"; 
          when x"177" => iQ <= x"FFB0"; 
          when x"178" => iQ <= x"FFB1"; 
          when x"179" => iQ <= x"0303"; 
          when x"17A" => iQ <= x"F10D"; 
          when x"17B" => iQ <= x"47EC"; 
          when x"17C" => iQ <= x"511B"; 
          when x"17D" => iQ <= x"F071"; 
          when x"17E" => iQ <= x"0316"; 
          when x"17F" => iQ <= x"FFB0"; 
          when x"180" => iQ <= x"FFB1"; 
          when x"181" => iQ <= x"0308"; 
          when x"182" => iQ <= x"F0EB"; 
          when x"183" => iQ <= x"497A"; 
          when x"184" => iQ <= x"4F9A"; 
          when x"185" => iQ <= x"F083"; 
          when x"186" => iQ <= x"0315"; 
          when x"187" => iQ <= x"FFB0"; 
          when x"188" => iQ <= x"FFB0"; 
          when x"189" => iQ <= x"030C"; 
          when x"18A" => iQ <= x"F0CC"; 
          when x"18B" => iQ <= x"4B06"; 
          when x"18C" => iQ <= x"4E16"; 
          when x"18D" => iQ <= x"F098"; 
          when x"18E" => iQ <= x"0313"; 
          when x"18F" => iQ <= x"FFB0"; 
          when x"190" => iQ <= x"FFB0"; 
          when x"191" => iQ <= x"0310"; 
          when x"192" => iQ <= x"F0B0"; 
          when x"193" => iQ <= x"4C8F"; 
          when x"194" => iQ <= x"4C8F"; 
          when x"195" => iQ <= x"F0B0"; 
          when x"196" => iQ <= x"0310"; 
          when x"197" => iQ <= x"FFB0"; 
          when x"198" => iQ <= x"FFB0"; 
          when x"199" => iQ <= x"0313"; 
          when x"19A" => iQ <= x"F098"; 
          when x"19B" => iQ <= x"4E16"; 
          when x"19C" => iQ <= x"4B06"; 
          when x"19D" => iQ <= x"F0CC"; 
          when x"19E" => iQ <= x"030C"; 
          when x"19F" => iQ <= x"FFB0"; 
          when x"1A0" => iQ <= x"FFB0"; 
          when x"1A1" => iQ <= x"0315"; 
          when x"1A2" => iQ <= x"F083"; 
          when x"1A3" => iQ <= x"4F9A"; 
          when x"1A4" => iQ <= x"497A"; 
          when x"1A5" => iQ <= x"F0EB"; 
          when x"1A6" => iQ <= x"0308"; 
          when x"1A7" => iQ <= x"FFB1"; 
          when x"1A8" => iQ <= x"FFB0"; 
          when x"1A9" => iQ <= x"0316"; 
          when x"1AA" => iQ <= x"F071"; 
          when x"1AB" => iQ <= x"511B"; 
          when x"1AC" => iQ <= x"47EC"; 
          when x"1AD" => iQ <= x"F10D"; 
          when x"1AE" => iQ <= x"0303"; 
          when x"1AF" => iQ <= x"FFB1"; 
          when x"1B0" => iQ <= x"FFB0"; 
          when x"1B1" => iQ <= x"0317"; 
          when x"1B2" => iQ <= x"F063"; 
          when x"1B3" => iQ <= x"5298"; 
          when x"1B4" => iQ <= x"465C"; 
          when x"1B5" => iQ <= x"F133"; 
          when x"1B6" => iQ <= x"02FE"; 
          when x"1B7" => iQ <= x"FFB1"; 
          when x"1B8" => iQ <= x"FFB0"; 
          when x"1B9" => iQ <= x"0317"; 
          when x"1BA" => iQ <= x"F058"; 
          when x"1BB" => iQ <= x"5412"; 
          when x"1BC" => iQ <= x"44C9"; 
          when x"1BD" => iQ <= x"F15B"; 
          when x"1BE" => iQ <= x"02F8"; 
          when x"1BF" => iQ <= x"FFB2"; 
          when x"1C0" => iQ <= x"FFB0"; 
          when x"1C1" => iQ <= x"0316"; 
          when x"1C2" => iQ <= x"F052"; 
          when x"1C3" => iQ <= x"5589"; 
          when x"1C4" => iQ <= x"4335"; 
          when x"1C5" => iQ <= x"F186"; 
          when x"1C6" => iQ <= x"02F1"; 
          when x"1C7" => iQ <= x"FFB3"; 
          when x"1C8" => iQ <= x"FFB0"; 
          when x"1C9" => iQ <= x"0314"; 
          when x"1CA" => iQ <= x"F04E"; 
          when x"1CB" => iQ <= x"56FC"; 
          when x"1CC" => iQ <= x"419F"; 
          when x"1CD" => iQ <= x"F1B5"; 
          when x"1CE" => iQ <= x"02E9"; 
          when x"1CF" => iQ <= x"FFB3"; 
          when x"1D0" => iQ <= x"FFB1"; 
          when x"1D1" => iQ <= x"0312"; 
          when x"1D2" => iQ <= x"F04F"; 
          when x"1D3" => iQ <= x"586C"; 
          when x"1D4" => iQ <= x"4007"; 
          when x"1D5" => iQ <= x"F1E6"; 
          when x"1D6" => iQ <= x"02E1"; 
          when x"1D7" => iQ <= x"FFB4"; 
          when x"1D8" => iQ <= x"FFB1"; 
          when x"1D9" => iQ <= x"030F"; 
          when x"1DA" => iQ <= x"F053"; 
          when x"1DB" => iQ <= x"59D7"; 
          when x"1DC" => iQ <= x"3E6E"; 
          when x"1DD" => iQ <= x"F21A"; 
          when x"1DE" => iQ <= x"02D8"; 
          when x"1DF" => iQ <= x"FFB5"; 
          when x"1E0" => iQ <= x"FFB1"; 
          when x"1E1" => iQ <= x"030B"; 
          when x"1E2" => iQ <= x"F05C"; 
          when x"1E3" => iQ <= x"5B3E"; 
          when x"1E4" => iQ <= x"3CD4"; 
          when x"1E5" => iQ <= x"F250"; 
          when x"1E6" => iQ <= x"02CF"; 
          when x"1E7" => iQ <= x"FFB6"; 
          when x"1E8" => iQ <= x"FFB2"; 
          when x"1E9" => iQ <= x"0306"; 
          when x"1EA" => iQ <= x"F068"; 
          when x"1EB" => iQ <= x"5CA1"; 
          when x"1EC" => iQ <= x"3B39"; 
          when x"1ED" => iQ <= x"F289"; 
          when x"1EE" => iQ <= x"02C5"; 
          when x"1EF" => iQ <= x"FFB7"; 
          when x"1F0" => iQ <= x"FFB3"; 
          when x"1F1" => iQ <= x"0300"; 
          when x"1F2" => iQ <= x"F078"; 
          when x"1F3" => iQ <= x"5E00"; 
          when x"1F4" => iQ <= x"399D"; 
          when x"1F5" => iQ <= x"F2C5"; 
          when x"1F6" => iQ <= x"02BA"; 
          when x"1F7" => iQ <= x"FFB8"; 
          when x"1F8" => iQ <= x"FFB3"; 
          when x"1F9" => iQ <= x"02FA"; 
          when x"1FA" => iQ <= x"F08D"; 
          when x"1FB" => iQ <= x"5F5A"; 
          when x"1FC" => iQ <= x"3800"; 
          when x"1FD" => iQ <= x"F303"; 
          when x"1FE" => iQ <= x"02AF"; 
          when x"1FF" => iQ <= x"FFB9"; 
          when x"200" => iQ <= x"FFB4"; 
          when x"201" => iQ <= x"02F3"; 
          when x"202" => iQ <= x"F0A5"; 
          when x"203" => iQ <= x"60AF"; 
          when x"204" => iQ <= x"3662"; 
          when x"205" => iQ <= x"F344"; 
          when x"206" => iQ <= x"02A3"; 
          when x"207" => iQ <= x"FFBA"; 
          when x"208" => iQ <= x"FFB5"; 
          when x"209" => iQ <= x"02EB"; 
          when x"20A" => iQ <= x"F0C2"; 
          when x"20B" => iQ <= x"61FF"; 
          when x"20C" => iQ <= x"34C5"; 
          when x"20D" => iQ <= x"F387"; 
          when x"20E" => iQ <= x"0297"; 
          when x"20F" => iQ <= x"FFBB"; 
          when x"210" => iQ <= x"FFB6"; 
          when x"211" => iQ <= x"02E3"; 
          when x"212" => iQ <= x"F0E2"; 
          when x"213" => iQ <= x"634B"; 
          when x"214" => iQ <= x"3327"; 
          when x"215" => iQ <= x"F3CC"; 
          when x"216" => iQ <= x"028A"; 
          when x"217" => iQ <= x"FFBD"; 
          when x"218" => iQ <= x"FFB7"; 
          when x"219" => iQ <= x"02D9"; 
          when x"21A" => iQ <= x"F107"; 
          when x"21B" => iQ <= x"6491"; 
          when x"21C" => iQ <= x"3188"; 
          when x"21D" => iQ <= x"F414"; 
          when x"21E" => iQ <= x"027C"; 
          when x"21F" => iQ <= x"FFBE"; 
          when x"220" => iQ <= x"FFB8"; 
          when x"221" => iQ <= x"02CF"; 
          when x"222" => iQ <= x"F131"; 
          when x"223" => iQ <= x"65D2"; 
          when x"224" => iQ <= x"2FEA"; 
          when x"225" => iQ <= x"F45D"; 
          when x"226" => iQ <= x"026E"; 
          when x"227" => iQ <= x"FFBF"; 
          when x"228" => iQ <= x"FFB9"; 
          when x"229" => iQ <= x"02C4"; 
          when x"22A" => iQ <= x"F15E"; 
          when x"22B" => iQ <= x"670E"; 
          when x"22C" => iQ <= x"2E4D"; 
          when x"22D" => iQ <= x"F4A8"; 
          when x"22E" => iQ <= x"0260"; 
          when x"22F" => iQ <= x"FFC1"; 
          when x"230" => iQ <= x"FFBB"; 
          when x"231" => iQ <= x"02B8"; 
          when x"232" => iQ <= x"F190"; 
          when x"233" => iQ <= x"6843"; 
          when x"234" => iQ <= x"2CAF"; 
          when x"235" => iQ <= x"F4F6"; 
          when x"236" => iQ <= x"0251"; 
          when x"237" => iQ <= x"FFC2"; 
          when x"238" => iQ <= x"FFBC"; 
          when x"239" => iQ <= x"02AC"; 
          when x"23A" => iQ <= x"F1C7"; 
          when x"23B" => iQ <= x"6974"; 
          when x"23C" => iQ <= x"2B12"; 
          when x"23D" => iQ <= x"F545"; 
          when x"23E" => iQ <= x"0242"; 
          when x"23F" => iQ <= x"FFC4"; 
          when x"240" => iQ <= x"FFBD"; 
          when x"241" => iQ <= x"029E"; 
          when x"242" => iQ <= x"F202"; 
          when x"243" => iQ <= x"6A9E"; 
          when x"244" => iQ <= x"2976"; 
          when x"245" => iQ <= x"F596"; 
          when x"246" => iQ <= x"0232"; 
          when x"247" => iQ <= x"FFC5"; 
          when x"248" => iQ <= x"FFBF"; 
          when x"249" => iQ <= x"0290"; 
          when x"24A" => iQ <= x"F241"; 
          when x"24B" => iQ <= x"6BC2"; 
          when x"24C" => iQ <= x"27DB"; 
          when x"24D" => iQ <= x"F5E9"; 
          when x"24E" => iQ <= x"0222"; 
          when x"24F" => iQ <= x"FFC7"; 
          when x"250" => iQ <= x"FFC0"; 
          when x"251" => iQ <= x"0281"; 
          when x"252" => iQ <= x"F285"; 
          when x"253" => iQ <= x"6CE0"; 
          when x"254" => iQ <= x"2641"; 
          when x"255" => iQ <= x"F63D"; 
          when x"256" => iQ <= x"0211"; 
          when x"257" => iQ <= x"FFC9"; 
          when x"258" => iQ <= x"FFC2"; 
          when x"259" => iQ <= x"0272"; 
          when x"25A" => iQ <= x"F2CE"; 
          when x"25B" => iQ <= x"6DF8"; 
          when x"25C" => iQ <= x"24A8"; 
          when x"25D" => iQ <= x"F693"; 
          when x"25E" => iQ <= x"0200"; 
          when x"25F" => iQ <= x"FFCA"; 
          when x"260" => iQ <= x"FFC4"; 
          when x"261" => iQ <= x"0261"; 
          when x"262" => iQ <= x"F31B"; 
          when x"263" => iQ <= x"6F0A"; 
          when x"264" => iQ <= x"2311"; 
          when x"265" => iQ <= x"F6EA"; 
          when x"266" => iQ <= x"01EE"; 
          when x"267" => iQ <= x"FFCC"; 
          when x"268" => iQ <= x"FFC6"; 
          when x"269" => iQ <= x"0250"; 
          when x"26A" => iQ <= x"F36D"; 
          when x"26B" => iQ <= x"7015"; 
          when x"26C" => iQ <= x"217B"; 
          when x"26D" => iQ <= x"F743"; 
          when x"26E" => iQ <= x"01DC"; 
          when x"26F" => iQ <= x"FFCE"; 
          when x"270" => iQ <= x"FFC7"; 
          when x"271" => iQ <= x"023E"; 
          when x"272" => iQ <= x"F3C3"; 
          when x"273" => iQ <= x"7119"; 
          when x"274" => iQ <= x"1FE6"; 
          when x"275" => iQ <= x"F79D"; 
          when x"276" => iQ <= x"01CA"; 
          when x"277" => iQ <= x"FFD0"; 
          when x"278" => iQ <= x"FFC9"; 
          when x"279" => iQ <= x"022B"; 
          when x"27A" => iQ <= x"F41F"; 
          when x"27B" => iQ <= x"7217"; 
          when x"27C" => iQ <= x"1E54"; 
          when x"27D" => iQ <= x"F7F8"; 
          when x"27E" => iQ <= x"01B8"; 
          when x"27F" => iQ <= x"FFD2"; 
          when x"280" => iQ <= x"FFCB"; 
          when x"281" => iQ <= x"0218"; 
          when x"282" => iQ <= x"F47F"; 
          when x"283" => iQ <= x"730D"; 
          when x"284" => iQ <= x"1CC3"; 
          when x"285" => iQ <= x"F854"; 
          when x"286" => iQ <= x"01A5"; 
          when x"287" => iQ <= x"FFD4"; 
          when x"288" => iQ <= x"FFCD"; 
          when x"289" => iQ <= x"0203"; 
          when x"28A" => iQ <= x"F4E3"; 
          when x"28B" => iQ <= x"73FD"; 
          when x"28C" => iQ <= x"1B35"; 
          when x"28D" => iQ <= x"F8B2"; 
          when x"28E" => iQ <= x"0192"; 
          when x"28F" => iQ <= x"FFD6"; 
          when x"290" => iQ <= x"FFD0"; 
          when x"291" => iQ <= x"01EE"; 
          when x"292" => iQ <= x"F54D"; 
          when x"293" => iQ <= x"74E5"; 
          when x"294" => iQ <= x"19A9"; 
          when x"295" => iQ <= x"F910"; 
          when x"296" => iQ <= x"017E"; 
          when x"297" => iQ <= x"FFD8"; 
          when x"298" => iQ <= x"FFD2"; 
          when x"299" => iQ <= x"01D8"; 
          when x"29A" => iQ <= x"F5BC"; 
          when x"29B" => iQ <= x"75C6"; 
          when x"29C" => iQ <= x"181F"; 
          when x"29D" => iQ <= x"F96F"; 
          when x"29E" => iQ <= x"016A"; 
          when x"29F" => iQ <= x"FFDA"; 
          when x"2A0" => iQ <= x"FFD4"; 
          when x"2A1" => iQ <= x"01C2"; 
          when x"2A2" => iQ <= x"F62F"; 
          when x"2A3" => iQ <= x"76A0"; 
          when x"2A4" => iQ <= x"1698"; 
          when x"2A5" => iQ <= x"F9D0"; 
          when x"2A6" => iQ <= x"0156"; 
          when x"2A7" => iQ <= x"FFDC"; 
          when x"2A8" => iQ <= x"FFD6"; 
          when x"2A9" => iQ <= x"01AB"; 
          when x"2AA" => iQ <= x"F6A7"; 
          when x"2AB" => iQ <= x"7773"; 
          when x"2AC" => iQ <= x"1514"; 
          when x"2AD" => iQ <= x"FA30"; 
          when x"2AE" => iQ <= x"0142"; 
          when x"2AF" => iQ <= x"FFDE"; 
          when x"2B0" => iQ <= x"FFD9"; 
          when x"2B1" => iQ <= x"0193"; 
          when x"2B2" => iQ <= x"F724"; 
          when x"2B3" => iQ <= x"783D"; 
          when x"2B4" => iQ <= x"1393"; 
          when x"2B5" => iQ <= x"FA92"; 
          when x"2B6" => iQ <= x"012D"; 
          when x"2B7" => iQ <= x"FFE0"; 
          when x"2B8" => iQ <= x"FFDB"; 
          when x"2B9" => iQ <= x"017A"; 
          when x"2BA" => iQ <= x"F7A6"; 
          when x"2BB" => iQ <= x"7900"; 
          when x"2BC" => iQ <= x"1215"; 
          when x"2BD" => iQ <= x"FAF4"; 
          when x"2BE" => iQ <= x"0119"; 
          when x"2BF" => iQ <= x"FFE2"; 
          when x"2C0" => iQ <= x"FFDE"; 
          when x"2C1" => iQ <= x"0161"; 
          when x"2C2" => iQ <= x"F82D"; 
          when x"2C3" => iQ <= x"79BC"; 
          when x"2C4" => iQ <= x"109A"; 
          when x"2C5" => iQ <= x"FB57"; 
          when x"2C6" => iQ <= x"0104"; 
          when x"2C7" => iQ <= x"FFE4"; 
          when x"2C8" => iQ <= x"FFE0"; 
          when x"2C9" => iQ <= x"0147"; 
          when x"2CA" => iQ <= x"F8B8"; 
          when x"2CB" => iQ <= x"7A6F"; 
          when x"2CC" => iQ <= x"0F22"; 
          when x"2CD" => iQ <= x"FBB9"; 
          when x"2CE" => iQ <= x"00EF"; 
          when x"2CF" => iQ <= x"FFE7"; 
          when x"2D0" => iQ <= x"FFE3"; 
          when x"2D1" => iQ <= x"012C"; 
          when x"2D2" => iQ <= x"F949"; 
          when x"2D3" => iQ <= x"7B1A"; 
          when x"2D4" => iQ <= x"0DAE"; 
          when x"2D5" => iQ <= x"FC1D"; 
          when x"2D6" => iQ <= x"00D9"; 
          when x"2D7" => iQ <= x"FFE9"; 
          when x"2D8" => iQ <= x"FFE6"; 
          when x"2D9" => iQ <= x"0111"; 
          when x"2DA" => iQ <= x"F9DF"; 
          when x"2DB" => iQ <= x"7BBD"; 
          when x"2DC" => iQ <= x"0C3D"; 
          when x"2DD" => iQ <= x"FC80"; 
          when x"2DE" => iQ <= x"00C4"; 
          when x"2DF" => iQ <= x"FFEB"; 
          when x"2E0" => iQ <= x"FFE8"; 
          when x"2E1" => iQ <= x"00F5"; 
          when x"2E2" => iQ <= x"FA79"; 
          when x"2E3" => iQ <= x"7C58"; 
          when x"2E4" => iQ <= x"0AD0"; 
          when x"2E5" => iQ <= x"FCE4"; 
          when x"2E6" => iQ <= x"00AE"; 
          when x"2E7" => iQ <= x"FFED"; 
          when x"2E8" => iQ <= x"FFEB"; 
          when x"2E9" => iQ <= x"00D8"; 
          when x"2EA" => iQ <= x"FB19"; 
          when x"2EB" => iQ <= x"7CEB"; 
          when x"2EC" => iQ <= x"0967"; 
          when x"2ED" => iQ <= x"FD48"; 
          when x"2EE" => iQ <= x"0099"; 
          when x"2EF" => iQ <= x"FFF0"; 
          when x"2F0" => iQ <= x"FFEE"; 
          when x"2F1" => iQ <= x"00BB"; 
          when x"2F2" => iQ <= x"FBBD"; 
          when x"2F3" => iQ <= x"7D76"; 
          when x"2F4" => iQ <= x"0802"; 
          when x"2F5" => iQ <= x"FDAC"; 
          when x"2F6" => iQ <= x"0083"; 
          when x"2F7" => iQ <= x"FFF2"; 
          when x"2F8" => iQ <= x"FFF1"; 
          when x"2F9" => iQ <= x"009D"; 
          when x"2FA" => iQ <= x"FC67"; 
          when x"2FB" => iQ <= x"7DF7"; 
          when x"2FC" => iQ <= x"06A1"; 
          when x"2FD" => iQ <= x"FE10"; 
          when x"2FE" => iQ <= x"006D"; 
          when x"2FF" => iQ <= x"FFF4"; 
          when x"300" => iQ <= x"FFF4"; 
          when x"301" => iQ <= x"007F"; 
          when x"302" => iQ <= x"FD15"; 
          when x"303" => iQ <= x"7E71"; 
          when x"304" => iQ <= x"0545"; 
          when x"305" => iQ <= x"FE74"; 
          when x"306" => iQ <= x"0057"; 
          when x"307" => iQ <= x"FFF7"; 
          when x"308" => iQ <= x"FFF7"; 
          when x"309" => iQ <= x"0060"; 
          when x"30A" => iQ <= x"FDC8"; 
          when x"30B" => iQ <= x"7EE1"; 
          when x"30C" => iQ <= x"03ED"; 
          when x"30D" => iQ <= x"FED7"; 
          when x"30E" => iQ <= x"0042"; 
          when x"30F" => iQ <= x"FFF9"; 
          when x"310" => iQ <= x"FFFA"; 
          when x"311" => iQ <= x"0041"; 
          when x"312" => iQ <= x"FE81"; 
          when x"313" => iQ <= x"7F49"; 
          when x"314" => iQ <= x"0299"; 
          when x"315" => iQ <= x"FF3B"; 
          when x"316" => iQ <= x"002C"; 
          when x"317" => iQ <= x"FFFB"; 
          when x"318" => iQ <= x"FFFD"; 
          when x"319" => iQ <= x"0021"; 
          when x"31A" => iQ <= x"FF3E"; 
          when x"31B" => iQ <= x"7FA9"; 
          when x"31C" => iQ <= x"014A"; 
          when x"31D" => iQ <= x"FF9D"; 
          when x"31E" => iQ <= x"0016"; 
          when x"31F" => iQ <= x"FFFE"; 
          when others => iQ <= x"ffff";
	end case;
end process;


end architecture;
