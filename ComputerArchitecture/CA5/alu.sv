module alu(input signed [7:0] A, B, input [2:0] s, input [2:0] n, input si, output reg co, output ov, zero, neg, gt, eq, output reg [7:0] w);
	wire signed[7:0] temp;
	wire my_ci;
  
  
	always @(A, B, s, si, n, gt) begin
		
		w = 8'b0;
		co = 1'b0;
		
		case(s)
		(3'b000 | 3'b001 | 3'b011 | 3'b100 |3'b110):
			{w, co} = A + temp;
  
		3'b010:
			w = gt ? A : B;
      
		3'b101:
			w = (A[7] == 0) ? A : (~A + 1);
  
		3'b111:
			w = A & B;
		
		default:
			{co, w} = 9'bx;
		
		endcase
	end
	
	assign temp=(s==3'b000)?(B):(s==3'b001)?(0):(s==3'b011)?(A << n):(s==3'b100)? (A >> n): (s==3'b110)?B<<1:8'bz;
	assign zero = w == 7'b0;
	assign gt = A > B;
	assign eq = A == B;
	assign neg = w[7] == 1'b1;
	assign ov = (w[7] & ~A[7] & ~temp[7]) | (~w[7] & A[7] & temp[7]);

endmodule