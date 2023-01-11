module controller(input clk, a0, start, output logic lda, ldb, ldp, zero, shen, ready, output logic[2:0] s);
logic[1:0] ns, ps;
logic[3:0] counter;
logic selb;
always @(start, a0, ps) begin
{lda, ldb, ldp, zero, shen, ready} = 7'b 0;
s = 3'b 0;
case(ps)
0:begin
ns = (start == 1'b 1) ? 1 : 0;
ready = 1'b 1;
end
1:begin
ns = (~start == 1) ? 2: 1;
zero = 1'b 1;
counter = 0;
end
2:begin
lda = 1'b 1; ldb = 1'b 1; ns = 3; 
end
3: begin 
counter = counter + 1;
ldp = 1'b 1;
selb = a0;shen = 1'b 1;
if(counter == 8)
ns = 0;
else
ns = 3;
end
default: ns = 0;
endcase
assign s = (selb == 0) ? 3'b 001 : 3'b 000;
end
always @(posedge clk) begin
ps <= ns;
end
endmodule
