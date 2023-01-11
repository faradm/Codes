module alu1(input signed [7:0] A, B, input [2:0] s, input [2:0] n, input si, output reg co, output ov, zero, neg, gt, eq, output reg [7:0] w);
  always @(A, B, s, si, n, gt) begin
    w = 8'b0;
    co = 1'b0;
    case(s)
    3'b000:
      {w, co} = A + B;
    3'b001:
      {w, co} = A + 0;
    3'b010:
      w = gt ? A : B;
    3'b011:
      w = A + (A << n);
    3'b100:
      w = A + (A >> n);
    3'b101:
      w = (A[7] == 0) ? A : (~A + 1);
    3'b110:
      {co, w} = A + B + B;
    3'b111:
      w = A & B;
    default:
      {co, w} = 9'bx;
    endcase
  end
  assign zero = w == 7'b0;
  assign gt = A > B;
  assign eq = A == B;
  assign neg = w[7] == 1'b1;
  assign ov = (w[7] & ~A[7] & ~B[7]) | (~w[7] & A[7] & B[7]);

endmodule