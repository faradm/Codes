module aluthree(input signed[7:0] a, b, input[2:0] s, n, input si, input ci, output ov, z, neg, agb, eq, output logic[7:0] w, output logic co);
	always @(a, b, s, ci, n) begin
		w = 8'b00000000;
		co = 0;
		case(s)
			0: {co, w} = a + b + ci;
			1: {co, w} = a + b + 8'b 00000000;
			2: w = {~a[7], a[6:0]} > {~b[7], b[6:0]} ? a : b;
			3: w = a + $signed(a <<< n);
			4: w = a + $signed(a >>> n);
			5: w = (a[7] == 0) ? a : (~a + 1);
			6: {co, w} = a + b + b;
			7: w = a & b;
		endcase;
	end
	assign ov = (s == 6) ? ((~a[7])&(~b[6])&w[7] | a[7]&b[6]&(~w[7])) : ((~a[7])&(~b[7])&w[7] | a[7]&b[7]&(~w[7])); 
	assign z = ~|w;
	assign neg = w[7];
	assign agb = {~a[7], a[6:0]} > {~b[7], b[6:0]} ? 1 : 0;
	assign eq = a == b;	
endmodule

