module myrom(input[3:0] address, output[15:0] one_i);
logic[15:0] w;
always @(address) begin
w = 16'b 0;
case(address)
0: w = 16'b 1;
1: w = 16'b 1000000000000000;
2: w = 16'b 0101010101010101;
3: w = 16'b 0100000000000000;
4: w = 16'b 0011001100110011;
5: w = 16'b 0010101010101010;
6: w = 16'b 0010010010010010;
7: w = 16'b 0010000000000000;
8: w = 16'b 0001110001110001;
9: w = 16'b 0001100110011001;
10:w = 16'b 0001011101000101;
11:w = 16'b 0001010101010101;
12:w = 16'b 0001001110110001;
13:w = 16'b 0001001001001001;
14:w = 16'b 0001000100010001;
15:w = 16'b 0001000000000000;
default: w = 16'b 0;
endcase
end
assign one_i = w;
endmodule