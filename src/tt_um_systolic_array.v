/*
 * Copyright (c) 2024 Irene Raphael
 * SPDX-License-Identifier: Apache-2.0
 */

`default_nettype none

module tt_um_systolic_array (
    input  wire [7:0] ui_in,    // Dedicated inputs
    output wire [7:0] uo_out,   // Dedicated outputs
    input  wire [7:0] uio_in,   // IOs: Input path
    output wire [7:0] uio_out,  // IOs: Output path
    output wire [7:0] uio_oe,   // IOs: Enable path (active high: 0=input, 1=output)
    input  wire       ena,      // always 1 when the design is powered, so you can ignore it
    input  wire       clk,      // clock
    input  wire       rst_n     // reset_n - low to reset
);
wire start = ui_in[0];
wire load = ui_in[1];
wire [1:0] sel = ui_in[3:2];
wire [3:0] data = ui_in[7:4];
reg [3:0] a_row0, a_row1, weight_col0, weight_col1;
wire [7:0] data_out;
assign uo_out = data_out;
wire valid1;
assign uio_out = {7'b0,valid1};
assign uio_oe = 8'b00000001;
systolic_array systolic_array_inst(
  .clk(clk),
  .rst_n(rst_n),
  .start(start),
  .a_row0(a_row0),
  .a_row1(a_row1),
  .weight_col0(weight_col0),
  .weight_col1(weight_col1),
  .data_out(data_out),
  .valid(valid1)
);
wire _unused = &{ena, uio_in, 1'b0};
always@(posedge clk)begin
   if(!rst_n)begin
    a_row0 <= 0;
    a_row1 <= 0;
    weight_col0 <= 0;
    weight_col1 <= 0;
   end
   else if(load) begin
    case(sel)
        2'b00: a_row0 <= data;
        2'b01: a_row1 <= data;
        2'b10: weight_col0 <= data;
        2'b11: weight_col1 <= data;
    endcase
   end
end
endmodule
