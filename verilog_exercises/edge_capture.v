module top_module (
    input clk,
    input reset,
    input [31:0] in,
    output [31:0] out
);
    
    reg [31:0] out_sig;
    reg [31:0] prev_sig;

    always @(posedge clk) begin
    
   
        if(reset)begin
            out<=32'b0;
        end else begin
            
            //out<= out|out_sig;
            
            out<= out| (prev_sig & ~in);
        end
          prev_sig <= in;
        //out_sig<= prev_sig & ~in;
      
        
    end
    

endmodule

