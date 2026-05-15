module array_module(
    input clk,
    input reset_n,
    input en,
    input signed[3:0] a_row0,
    input signed[3:0] a_row1,    
    input signed[3:0] weight_col0,
    input signed[3:0] weight_col1,
    output wire signed[7:0] acc_00,
    output wire signed[7:0] acc_01,
    output wire signed[7:0] acc_10,
    output wire signed[7:0] acc_11
);

wire signed[3:0]a_row0_next,a_row1_next;
wire signed[3:0]weight_col0_next,weight_col1_next;
reg signed[3:0]a_row1_skewed,weight_col1_skewed;

pe pe00(
    .clk(clk),
    .reset_n(reset_n),
    .en(en),
    .a_in(a_row0),
    .weight_in(weight_col0),
    .acc(acc_00),
    .weight_next(weight_col0_next),
    .a_next(a_row0_next)
);
pe pe01(
    .clk(clk),
    .reset_n(reset_n),
    .en(en),
    .a_in(a_row0_next),
    .weight_in(weight_col1_skewed),
    .acc(acc_01),
    .weight_next(weight_col1_next),
    .a_next() //intentionally unconnected
);
pe pe10(
    .clk(clk),
    .reset_n(reset_n),
    .en(en),
    .a_in(a_row1_skewed),
    .weight_in(weight_col0_next),
    .acc(acc_10),
    .weight_next(), //intentionally unconnected
    .a_next(a_row1_next)
);
pe pe11(
    .clk(clk),
    .reset_n(reset_n),
    .en(en),
    .a_in(a_row1_next),
    .weight_in(weight_col1_next),
    .acc(acc_11),
    .weight_next(), //intentionally unconnected
    .a_next() //intentionally unconnected
);


always@(posedge clk)begin
  
    if(!reset_n)begin
      a_row1_skewed <= 4'b0;
      weight_col1_skewed <= 4'b0;
    end else begin
      weight_col1_skewed <= weight_col1;
      a_row1_skewed <= a_row1;
    end

end
endmodule

