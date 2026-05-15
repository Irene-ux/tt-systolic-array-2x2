module pe(
    input clk,
    input reset_n,
    input en,
    input clear,
    input signed[3:0] a_in,
    input signed[3:0] weight_in,
    output reg signed[7:0] acc,
    output reg signed[3:0] weight_next,
    output reg signed[3:0] a_next
);

reg signed[7:0] acc_next;
always @(posedge clk) begin
if (!reset_n) begin
    acc         <= 0;
    weight_next <= 0;
    a_next      <= 0;
    end else if(clear)begin
      acc <= 0;
    end else begin
        acc_next = 0;
        if (weight_in[0]) acc_next = acc_next + a_in;
        if (weight_in[1]) acc_next = acc_next + (a_in << 1);
        if (weight_in[2])acc_next  = acc_next + (a_in << 2);
        if (weight_in[3])acc_next  = acc_next - (a_in << 3);

        if(en)
        acc <= acc + acc_next;
        a_next      <= a_in;
        weight_next <= weight_in;
        end
end        
endmodule