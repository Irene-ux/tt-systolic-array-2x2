module async_fifo (
    input wr_clk,
    input rd_clk,
    input reset_n_wr,
    input reset_n_rd,
    input wr_en,
    input rd_en,
    input [7:0]wr_data,
    output reg [7:0]rd_data,
    output reg empty,
    output reg full
);
reg [7:0] fifo [7:0];
reg [3:0] wr_ptr,rd_ptr,rd_ptr_gray,wr_ptr_gray;
wire [3:0] wr_ptr_gray_sync,rd_ptr_gray_sync;

genvar i;
generate
    for(i=0;i<4;i = i+1)begin: sync_wr
    sync_2ff sync_wr_ptr_gray(
    .core_clk(rd_clk),
    .reset_n(reset_n_rd),
    .d(wr_ptr_gray[i]),
    .q(wr_ptr_gray_sync[i])
);
    end
endgenerate
generate
    for(i=0; i<4; i = i+1)begin: sync_rd
    sync_2ff sync_rd_ptr_gray(
    .core_clk(wr_clk),
    .reset_n(reset_n_wr),
    .d(rd_ptr_gray[i]),
    .q(rd_ptr_gray_sync[i])
);
    end
endgenerate

always@(posedge wr_clk) begin
    if(!reset_n_wr)begin
        wr_ptr <= 4'b0;
        wr_ptr_gray <= 4'b0;
    end
    else if(wr_en && !full)begin
        fifo[wr_ptr[2:0]] <= wr_data;
        wr_ptr <= wr_ptr +1;
        wr_ptr_gray <= ((wr_ptr+1) >> 1) ^ (wr_ptr +1);

    end

end

always@(posedge rd_clk)begin
    if(!reset_n_rd)begin
        rd_ptr <= 4'b0;
        rd_ptr_gray <= 4'b0;

    end
    else if(rd_en && !empty)begin
        rd_data <= fifo[rd_ptr[2:0]];
        rd_ptr <= rd_ptr +1;
        rd_ptr_gray <= ((rd_ptr+1) >> 1) ^ (rd_ptr +1);
    end
end
always@(posedge wr_clk)begin
        if(!reset_n_wr)begin
            full <= 0;
        end
        else begin
            full <= (wr_ptr_gray == {~rd_ptr_gray_sync[3],rd_ptr_gray_sync[2:0]});
        end
    end
always@(posedge rd_clk)begin
    if(!reset_n_rd)begin
        empty <=1;
    end
    else begin
        empty <= (wr_ptr_gray_sync == rd_ptr_gray);
    end
end

endmodule