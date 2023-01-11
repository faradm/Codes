module registerf(input[7:0] a, input c, clk, output[7:0] w);
wire[7:0] inflipflop;
generate
genvar i;
for(i = 0; i < 8; i++) begin:row
dflipflop Di(a[i], clk, inflipflop[i]);
end
endgenerate
assign w = (c == 1) ? inflipflop : w;
endmodule