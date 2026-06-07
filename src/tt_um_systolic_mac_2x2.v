`default_nettype none
module tt_um_systolic_mac_2x2 (
    input  wire [7:0] ui_in,
    output wire [7:0] uo_out,
    input  wire [7:0] uio_in,
    output wire [7:0] uio_out,
    output wire [7:0] uio_oe,
    input  wire       ena,
    input  wire       clk,
    input  wire       rst_n
);
wire        start    = ui_in[0];
wire        load     = ui_in[1];
wire [1:0]  sel      = ui_in[3:2];
wire signed [3:0] data_c1 = ui_in[7:4];
wire signed [3:0] data_c2 = uio_in[7:4];
reg signed [3:0] a_row0_c1, a_row1_c1, w_col0_c1, w_col1_c1;
reg signed [3:0] a_row0_c2, a_row1_c2, w_col0_c2, w_col1_c2;
reg [1:0] stream_cnt;
reg streaming;
always@(posedge clk) begin
    if(!rst_n) begin
        stream_cnt <= 0;
        streaming  <= 0;
    end else if(start) begin
        stream_cnt <= 1;
        streaming  <= 1;
    end else if(streaming) begin
        if(stream_cnt == 2'b11) begin
            stream_cnt <= 0;
            streaming  <= 0;
        end else
            stream_cnt <= stream_cnt + 1;
    end
end
reg signed [3:0] a_row0, a_row1, w_col0, w_col1;
always@(*) begin
    case(stream_cnt)
        2'b01: begin
            a_row0 = a_row0_c1; a_row1 = a_row1_c1;
            w_col0 = w_col0_c1; w_col1 = w_col1_c1;
        end
        2'b10: begin
            a_row0 = a_row0_c2; a_row1 = a_row1_c2;
            w_col0 = w_col0_c2; w_col1 = w_col1_c2;
        end
        default: begin
            a_row0 = 0; a_row1 = 0;
            w_col0 = 0; w_col1 = 0;
        end
    endcase
end
always@(posedge clk) begin
    if(!rst_n) begin
        a_row0_c1 <= 0; a_row1_c1 <= 0;
        w_col0_c1 <= 0; w_col1_c1 <= 0;
        a_row0_c2 <= 0; a_row1_c2 <= 0;
        w_col0_c2 <= 0; w_col1_c2 <= 0;
    end else if(load) begin
        case(sel)
            2'b00: begin a_row0_c1 <= data_c1; a_row0_c2 <= data_c2; end
            2'b01: begin a_row1_c1 <= data_c1; a_row1_c2 <= data_c2; end
            2'b10: begin w_col0_c1 <= data_c1; w_col0_c2 <= data_c2; end
            2'b11: begin w_col1_c1 <= data_c1; w_col1_c2 <= data_c2; end
        endcase
    end
end
wire [7:0] data_out;
wire valid1;
systolic_array systolic_array_inst(
    .clk        (clk),
    .reset_n    (rst_n),
    .start      (start),
    .a_row0     (a_row0),
    .a_row1     (a_row1),
    .weight_col0(w_col0),
    .weight_col1(w_col1),
    .data_out   (data_out),
    .valid      (valid1)
);
assign uo_out  = data_out;
assign uio_out = {7'b0, valid1};
assign uio_oe  = 8'b00000001;
wire _unused   = &{ena, uio_in[6:0], 1'b0};
endmodule
