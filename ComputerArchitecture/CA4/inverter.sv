module inverter(input a, output b);
supply1 vdd;
supply0 gnd;
pmos #8(b, vdd, a);
nmos #6(b, gnd, a);
endmodule;