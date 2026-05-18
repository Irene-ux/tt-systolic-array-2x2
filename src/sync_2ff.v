module sync_2ff(
    input core_clk,  //synchronizer only lives in the destination clock domain, so only one clock is needed
    input reset_n,
    input d,
    output reg q

);
(* ASYNC_REG = "TRUE" *)  //This tells the synthesis tool:
//Don't optimize logic across this boundary
//Place FF1 and FF2 physically close to each other on the chip — minimizes routing delay between them, 
//maximizing the time FF1 has to resolve before FF2 samples it.
reg ff1;
always@(posedge core_clk)begin
    if(!reset_n)begin
        q <= 0;
        ff1 <= 0;
    end
    else begin
        ff1 <= d;
        q <= ff1;
    end
end

endmodule