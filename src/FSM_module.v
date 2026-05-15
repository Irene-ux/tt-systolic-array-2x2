module fsm(
    input clk,
    input reset_n,
    input start,
    output reg en,
    output reg clear,
    output reg valid
);
reg [1:0] counter;
reg [1:0] state;
localparam [1:0] IDLE = 2'b00,
                 COMPUTE = 2'b01,
                 DRAIN = 2'b10,
                 READ = 2'b11;

always@(posedge clk)begin
  if(!reset_n)begin
    state <= IDLE;
    counter <= 0;
    valid <= 0;
    en <= 0;
    clear <= 0;
    end else begin
    case (state)
        IDLE: begin
          if(start == 1)begin
            en <= 1;
            state <= COMPUTE;
          end
            else
            en <= 0;
        end

        COMPUTE: begin
            if(counter == 2'b01)begin
                counter <= 0;
              state <= DRAIN;
            end
            else
            counter <= counter +1;
        end
        DRAIN: begin
          if(counter == 2'b01)begin
            counter <= 0;
            state <= READ;
            en <= 0;
            valid <= 1;
          end
          else
          counter <= counter +1;
        end
        READ: begin
          if(counter == 2'b11)begin
            counter <= 0;
            state <= IDLE;
            valid <= 0;
            en <= 0;
            clear <= 1;
          end
            else begin
                  counter <= counter +1; 
                  clear <= 0; 
            end

        end
    endcase
  end
end
endmodule