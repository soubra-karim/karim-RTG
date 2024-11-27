module top_module(
    input clk,
    input areset,    // Freshly brainwashed Lemmings walk left.
    input bump_left,
    input bump_right,
    input ground,
    output walk_left,
    output walk_right,
    output aaah ); 
    
    parameter L=0,R=1,FL=2,FR=3;
    
    reg [1:0] state,next_state;
    always@(*)begin
        case(state)
            L:begin
                 if(!ground) begin
                   next_state<=FL; 
                end else if(bump_left)begin
                    next_state<=R;
                end else begin
                   next_state<=state; 
                    
                end
            end
            
            R:begin
               if(!ground)begin
                    next_state<=FR;
                end else if(bump_right)begin
                   next_state<=L; 
                end else begin
                    next_state<=state;
                end
            end
            FR:begin
                if(ground)begin
                    next_state<=R;
                end else begin
                    next_state<=state;
                end
            end
            FL:begin
                if(ground)begin
                    next_state<=L;
                end else begin
                   next_state<=state;
                end
            end
        endcase
        
    end
    
    
    always @(posedge clk,posedge areset)begin
        if(areset)begin
            state<=L;
        end else begin
            state<=next_state;
        end 
    end
    
    always@(*)begin
        case(state)
            R:begin
                walk_left<=0;
                walk_right<=1;
                aaah<=0;
            end
            L:begin
                walk_left<=1;
                walk_right<=0;
                aaah<=0;
            end
            default:begin
                walk_left<=0;
                walk_right<=0;
                aaah<=1;
            end
        endcase
        
    end

endmodule

