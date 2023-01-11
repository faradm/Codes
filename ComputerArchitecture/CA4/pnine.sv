module pnine(input[7:0] A, B, input s, input[2:0] salu, input[2:0] n, input clk, cin, output[7:0] aluout);
supply1 vdd;
wire[7:0] muxout, aluo;
wire co, ov, zero, neg, gt, eq, si;
muxx M1(B, aluout, s, muxout);
registerf R1(aluo, vdd, clk, aluout);
aluthree AO(A, muxout, salu, n, si, cin, ov, zero, neg, gt, eq, aluo, co);
endmodule;