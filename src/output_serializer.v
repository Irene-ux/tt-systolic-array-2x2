module output_serializer(
    input clk,
    input reset_n,
    input valid,
    input signed[7:0] acc_00,
    input signed[7:0] acc_01,
    input signed[7:0] acc_10,
    input signed[7:0] acc_11,
    output reg signed[7:0] data_out
);
reg [1:0] counter;
always@(posedge clk)begin

    if(!reset_n)begin
      counter <= 0;
      data_out <= 0;
    end 
    else if(valid)begin
    counter <= counter +1;
        case (counter)
        2'b00: data_out <= acc_00;
        2'b01: data_out <= acc_01;
        2'b10: data_out <= acc_10;
        2'b11: data_out <= acc_11;
endcase
    end 
end
endmodule