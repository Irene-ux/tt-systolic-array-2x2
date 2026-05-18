module fsm(
    input clk,
    input reset_n,
    input start,
    output reg en,
    output reg clear,
    output reg valid
);

reg [1:0] state;
reg [1:0] counter;
reg [1:0] next_state;

// --------------------------------------------------------
// Pre-registered counter comparisons
// These cross the clock boundary ONE cycle early
// so the next_state logic sees already-settled values
// --------------------------------------------------------
reg counter_done_compute;  // counter == 01
reg counter_done_read;     // counter == 11

localparam [1:0] IDLE    = 2'b00,
                 COMPUTE = 2'b01,
                 DRAIN   = 2'b10,
                 READ    = 2'b11;

// --------------------------------------------------------
// Block 1 — register counter comparisons
// This is the key pipelining step
// comparison result is stored in a FF, not computed live
// --------------------------------------------------------
always @(posedge clk) begin
    if(!reset_n) begin
        counter_done_compute <= 0;
        counter_done_read    <= 0;
    end else begin
        counter_done_compute <= (counter == 2'b01);
        counter_done_read    <= (counter == 2'b11);
    end
end

// --------------------------------------------------------
// Block 2 — combinational next state
// Uses pre-registered comparisons — only 1 gate level now
// --------------------------------------------------------
always @(*) begin
    next_state = state;
    case(state)
        IDLE:    if(start)                next_state = COMPUTE;
        COMPUTE: if(counter_done_compute) next_state = DRAIN;
        DRAIN:   if(counter_done_compute) next_state = READ;
        READ:    if(counter_done_read)    next_state = IDLE;
    endcase
end

// --------------------------------------------------------
// Block 3 — register state and counter
// --------------------------------------------------------
always @(posedge clk) begin
    if(!reset_n) begin
        state   <= IDLE;
        counter <= 0;
    end else begin
        state <= next_state;
        case(state)
            COMPUTE: counter <= (counter == 2'b01) ? 0 : counter + 1;
            DRAIN:   counter <= (counter == 2'b01) ? 0 : counter + 1;
            READ:    counter <= (counter == 2'b11) ? 0 : counter + 1;
            default: counter <= 0;
        endcase
    end
end

// --------------------------------------------------------
// Block 4 — register outputs
// Uses pre-registered comparisons here too
// --------------------------------------------------------
always @(posedge clk) begin
    if(!reset_n) begin
        en    <= 0;
        valid <= 0;
        clear <= 0;
    end else begin
        en    <= 0;
        valid <= 0;
        clear <= 0;
        case(state)
            IDLE:    if(start)                en <= 1;
            COMPUTE: en <= 1;
            DRAIN:   begin
                         if(counter_done_compute) begin
                             valid <= 1;
                             en    <= 0;
                         end else
                             en <= 1;
                     end
            READ:    if(counter_done_read) clear <= 1;
        endcase
    end
end

endmodule