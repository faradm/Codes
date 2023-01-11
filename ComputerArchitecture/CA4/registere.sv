module registere(input[7:0] a, input c, clk, output[7:0] w);
wire[7:0] j, inlatch;
generate
genvar i;
for(i = 0; i < 8; i++) begin:row
dlatch Di(a[i], clk, inlatch[i], j[i]);
end
endgenerate
assign w = (c == 1) ? inlatch : 8'b z;
endmodule