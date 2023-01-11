module srlatchTB();
wire q, qb;
reg s, r, clk = 1;
always
begin
	#30 clk = 0;
	#30 clk = 1;
end
srlatch s1(s, r, clk, q, qb);
initial begin
s = 1;
r = 0;
#50
s = 0;
r = 1;
#60
s = 1;
r = 1;
#120
$stop;
end
endmodule