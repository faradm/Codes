module controllerTB();
reg clk = 0, a0 = 0, start;
wire lda, ldb, ldp, zero, shen, ready;wire[3:0] counter = 0;
wire [2:0] s;
controller C1(clk, a0, start, lda, ldb, ldp, zero, shen, ready, s, counter);
always
begin
#15 clk = 1;
#15 clk = 0;
end
initial begin
start = 0;
#15
start = 0;
#15
start = 1;
#15
start = 1;
#15
start = 0;
#15
a0 = 0;
#15
a0 = 0;
#15
a0 = 1;
#15
a0 = 1;
#300
$stop;
end
endmodule