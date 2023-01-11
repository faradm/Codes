module srlatch(input s, r, clk, output q, qb);
wire j;
wire i;
nand #8(j, s, clk);
nand #8(i, r, clk);
nand #8(q, j, qb);
nand #8(qb, i, q);
endmodule