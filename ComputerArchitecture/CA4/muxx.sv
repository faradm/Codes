module muxx(input[7:0]A, B, input s, output[7:0] w);
assign w = (s == 0) ? A : B;
endmodule;