// Copyright (C) 2017  Intel Corporation. All rights reserved.
// Your use of Intel Corporation's design tools, logic functions 
// and other software and tools, and its AMPP partner logic 
// functions, and any output files from any of the foregoing 
// (including device programming or simulation files), and any 
// associated documentation or information are expressly subject 
// to the terms and conditions of the Intel Program License 
// Subscription Agreement, the Intel Quartus Prime License Agreement,
// the Intel MegaCore Function License Agreement, or other 
// applicable license agreement, including, without limitation, 
// that your use is for the sole purpose of programming logic 
// devices manufactured by Intel and sold by Intel or its 
// authorized distributors.  Please refer to the applicable 
// agreement for further details.

// PROGRAM		"Quartus Prime"
// VERSION		"Version 17.0.0 Build 595 04/25/2017 SJ Standard Edition"
// CREATED		"Tue May 30 08:02:15 2017"


module lpm_add_sub_5(dataa,datab,result);
input [15:0] dataa;
input [15:0] datab;
output [15:0] result;

lpm_add_sub	lpm_instance(.dataa(dataa),.datab(datab),.result(result));
	defparam	lpm_instance.LPM_DIRECTION = "ADD";
	defparam	lpm_instance.LPM_WIDTH = 16;

endmodule
