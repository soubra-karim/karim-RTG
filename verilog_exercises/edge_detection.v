module top_module (
    input clk,
    input [7:0] in,
    output [7:0] pedge
);
    
    reg [7:0] prev_signal;
     
    always @(posedge clk) begin
       
        pedge<= in & prev_signal;
        prev_signal <= ~in; 
    end
    
   
endmodule

