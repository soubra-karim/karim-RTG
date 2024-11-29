module top_module(
    input clk,
    input [7:0] in,
    input reset,    // Synchronous reset
    output done); //

    // State transition logic (combinational)
    parameter b1=0,b2=1,b3=2,doneb=3;
    reg [1:0] next_state, state;
    always @(*) begin
        case(state) 
            b1:begin
                if(in[3]==1)begin
                   next_state<=b2; 
                end else begin
                   next_state<=state; 
                end
            end
            b2:begin
               next_state<=b3; 
            end
            b3:begin
               next_state<=doneb; 
            end
            doneb:begin
                if(in[3]==1)begin
                   next_state<=b2; 
                end else begin
                    next_state<=b1;
                end
            end
        endcase
    end

	
    always @(posedge clk) begin
        if(reset)begin
           state<=b1; 
        end else begin
           state<=next_state; 
        end
    end
    
    assign done= (state==doneb) ? 1:0;
endmodule

