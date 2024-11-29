
module top_module(
    input clk,
    input [7:0] in,
    input reset,    // Synchronous reset
    output [23:0] out_bytes,
    output done); //


    parameter b1=0,b2=1,b3=2,doneb=3;
    
    reg [1:0] state,nstate;
    reg [23:0] out_b;
    reg restart_flag;
    always @(*) begin
        case(state) 
            b1:begin
                restart_flag<=0;
                if(in[3]==1)begin
                   nstate<=b2; 
                end else begin
                   nstate<=b1; 
                end
            end
            b2:begin
                nstate<=b3; 
                
            end
            b3:begin
               nstate<=doneb; 
            end
            doneb:begin
                if(in[3]==1)begin
                   restart_flag<=1;
                   nstate<=b2; 
                end else begin
                   nstate<=b1; 
                end
            end
        endcase
        
    end
    
    always @(posedge clk)begin
        if(reset)begin
           state<=b1; 
        end else begin
           state<=nstate; 
        end
    end
    
    reg [7:0] done_b1;
    always @(*) begin 
        case(state)
            b1:begin
                if(in[3]==1)begin
                    out_b[23:16]<=in;
                end
                
            end
            
            b2:begin
                if(restart_flag)begin
                    out_b[23:16] <=done_b1; 
                end
                out_b[15:8]<=in;
            end
            b3: begin
                out_b[7:0]<=in; 
            end
            doneb:begin
                if(in[3]==1)begin
                   done_b1<=in; 
                end
            end
                
            endcase
            
        
    end
    
    assign done= (state==doneb);
    
    assign out_bytes=(state==doneb) ? out_b : 23'bx; 
endmodule 



