module top_module (
    input clk,
    input d,
    output q
);
	reg falling_sig;
    reg rising_sig;
    
    always @(clk) begin
		
        
        if(clk)begin
            rising_sig<=d;
        end else begin
            falling_sig<=d;
        end
		q<=clk ? falling_sig : rising_sig;
    end
    

endmodule
