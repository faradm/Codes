module dlatchTB();
wire q, qb;
reg d, clk = 1;
always
begin
	#30 clk = 0;
	#30 clk = 1;
end
dlatch d1(d, clk, q, qb);
initial begin
d = 1;
#50
d = 0;
#60
d = 1;
#60
d = 0;
#60
$stop;
end
endmodule