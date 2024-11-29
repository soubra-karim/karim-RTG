module top_module(
    input clk,
    input in,
    input reset,    // Synchronous reset
    output done
); 

    
    
    parameter idle_start=0,rec=1,stop=2,fin=3,disc=4;
    reg [2:0] state,nstate;
    
    
    always @(*)begin
        case(state)
            idle_start:begin
                nstate<= (in) ? idle_start : rec; 
            end
            
            rec:begin
                nstate<= (count==8) ? stop : rec; 
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
    
    reg done_rec;
    reg [3:0] count;
    initial count=0;
    always @(posedge clk) begin
        
        if(state==rec)begin
            count<=count+1;
        end else begin
           count<=0; 
        end
        
    end
    
    always@(*)begin
        if(state==fin)begin
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
