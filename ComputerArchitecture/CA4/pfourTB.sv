module pfourTB();
wire[7:0] aluout;
reg[7:0] A, B;
reg[2:0] salu, n;
reg clk = 1, cin = 0, s;
always
begin
#30 clk = 0;
#30 clk = 1;
end
pfour P1(A, B, s, salu, n, clk, cin, aluout);
initial begin
A = 5;
B = 6;
s = 0;
n = 3'b 0;
salu = 2'b 01;
#60
s = 1;
A = 1;
#180
$stop;
end
endmodule