module top_module (
    input clk,
    input [7:0] in,
    output [7:0] anyedge
);

    
    reg [7:0] prev_signals;
    
    always@(posedge clk)begin
        
        anyedge<=prev_signals^in;
       prev_signals<=in;
        
        
        
    end
endmodule
