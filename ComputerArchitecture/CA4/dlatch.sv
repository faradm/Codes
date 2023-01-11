module dlatch(input d, clk, output q, qb);
wire db;
inverter inv1(d, db);
srlatch s1(d, db, clk, q, qb);
endmodule