module controller(input clk, rst, start, output logic[3:0] i, output logic seli, selx, xld, tld, ti1, rld, ri1, ready);
logic[2:0] ps, ns;
logic[3:0] ini;
logic ico, inci, init0;
parameter [2:0] wfs = 0, init = 1, getdata = 2, itp1 = 3, itp2 = 4, itp3 = 5, itp4 = 6, itp5 = 7;
always @(start, ps, ico) begin
{seli, selx, inci, xld, tld, ti1, rld, ri1, ready, init0} = 10'b 0;
case(ps)
wfs:begin
if(start == 1) ns = init;
else ns = wfs;
ready = 1; end
init:begin
if(start == 0) ns = getdata;
else ns = init;
ti1 = 1;
ri1 = 1;
init0 = 1;
end
getdata:begin
xld = 1;
ns = itp1;
end
itp1:begin
tld = 1;
selx = 1;
ns = itp2;
end
itp2:begin
tld = 1;
selx = 1;
ns = itp3;
end
itp3:begin
inci = 1;
tld = 1;
seli = 1;
ns = itp4;
end
itp4:begin
inci = 1;
tld = 1;
seli = 1;
ns = itp5;
end
itp5:begin
if(ico == 0) ns = itp1;
else ns = wfs;
rld = 1;
end
endcase
end
always@(posedge clk, posedge rst) begin
if(rst) begin ps <= 3'b 0; ico <= 0;end
else begin
ps <= ns;
if(init0 == 1'b 1) ini <= 4'b 0;
else if(ini == 4'b 1111)
ico <= 1'b 1;
else if(inci == 1'b 1) ini<= (i+1);
end
end
assign i = ini;
endmodule
