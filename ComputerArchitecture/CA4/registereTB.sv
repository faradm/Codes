module registereTB();
reg[7:0] a;
reg c, clk = 1;
wire [7:0] w;
always
begin
#30 clk = 0;
#30 clk = 1;
end
registere r1(a, c, clk, w);
initial begin
a = 123;
c = 1;
#50
a = 150;
#60
c = 0;
#120
c = 1;
a = 70;
#60
c = 0;
#60
a = 3;
#60
$stop;
end
endmodule