module systolic_array(
    input clk,
    input reset_n,
    input start,
    input signed[3:0] a_row0,
    input signed[3:0] a_row1,
    input signed[3:0] weight_col0,
    input signed[3:0] weight_col1,
    output signed[7:0] data_out,
    output valid

);
wire en;
wire signed[7:0]  accf_00, accf_01, accf_10, accf_11;
fsm fsm_inst(
    .clk(clk),
    .reset_n(reset_n),
    .start(start),
    .en(en),
    .valid(valid)
);
array_module array_inst(
    .clk(clk),
    .reset_n(reset_n),
    .en(en),
    .a_row0(a_row0),
    .a_row1(a_row1),
    .weight_col0(weight_col0),
    .weight_col1(weight_col1),
    .acc_00(accf_00),
    .acc_01(accf_01),
    .acc_10(accf_10),
    .acc_11(accf_11)
);
output_serializer serializer_inst(
    .clk(clk),
    .reset_n(reset_n),
    .valid(valid),
    .acc_00(accf_00),
    .acc_01(accf_01),
    .acc_10(accf_10),
    .acc_11(accf_11),
    .data_out(data_out)
);
endmodule