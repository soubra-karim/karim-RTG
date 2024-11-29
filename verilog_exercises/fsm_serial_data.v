module top_module(
    input clk,
    input in,
    input reset,    // Synchronous reset
    output [7:0] out_byte,
    output done
); //


    
    
    parameter idle_start=0,rec=1,stop=2,fin=3,disc=4;
    reg [2:0] state,nstate;
    
    
    always @(*)begin
        case(state)
            idle_start:begin
                nstate<= (in) ? idle_start : rec; 
            end
            
            rec:begin
                nstate<= (count==7) ? stop : rec; 
            end
            
            stop:begin
                nstate<= (in) ? fin : disc; 
            end
            
            fin:begin
                nstate<= (in) ? idle_start : rec; 
            end
            
            disc:begin
                nstate<= (in) ? idle_start : disc; 
            end
        endcase
        
    end
    
    
    reg [3:0] count;
    reg [7:0] rec_data;
    always @(posedge clk) begin
        
        if(state==rec)begin
            rec_data[count] <= in;
            count<=count+1;
        end else begin
           count<=0; 
        end
        
    end
    
    always@(*)begin
        if(state==fin)begin
            out_byte<=rec_data;
           done<=1; 
        end else begin
           done<=0; 
        end
        
    end
    
    always @(posedge clk) begin
        if(reset)begin
           state<=idle_start; 
        end else begin
           state<=nstate; 
        end
    end
    
    


endmodule

