module dflipflop(input d, clk, output q);
wire i, ib, qb;
dlatch D1(d, clk, i, ib); 
dlatch D2(i, ~clk, q, qb);
endmodule;