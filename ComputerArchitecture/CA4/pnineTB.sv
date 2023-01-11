module pnineTB();
wire[7:0] aluout;
reg[7:0] A, B;
reg[2:0] salu, n;
reg clk = 1, cin = 0, s;
always
begin
#50 clk = 0;
#50 clk = 1;
end
pnine P1(A, B, s, salu, n, clk, cin, aluout);
initial begin
A = 5;
B = 6;
s = 0;
n = 3'b 0;
salu = 2'b 01;
#100
s = 1;
A = 1;
#300
$stop;
end
endmodule
