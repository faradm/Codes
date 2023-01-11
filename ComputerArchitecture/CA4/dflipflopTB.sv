module dflipflopTB();
reg d, clk = 1;
wire q;
dflipflop D1(d, clk, q);
always
begin
#30 clk = 0;
#30 clk = 1;
end
initial begin
d = 1;
#50
d = 0;
#60
d = 0;
#60
d = 1;
#60
$stop;
end
endmodule
