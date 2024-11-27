module top_module(
    input clk,
    input areset,    // Freshly brainwashed Lemmings walk left.
    input bump_left,
    input bump_right,
    input ground,
    input dig,
    output walk_left,
    output walk_right,
    output aaah,
    output digging ); 
    
        
    parameter L=0,R=1,FL=2,FR=3,DR=4,DL=5;
    
    reg [2:0] state,next_state;
    always@(*)begin
        case(state)
            L:begin
                 if(!ground) begin
                   next_state<=FL; 
                end else if(dig) begin
                    next_state<=DL;
                end else if(bump_left)begin
                    next_state<=R;
                end else begin
                   next_state<=state; 
                    
                end
            end
            
            R:begin
                if(!ground)begin
                    next_state<=FR;
                end else if(dig) begin
                    next_state<=DR;
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
            DR:begin
                if(!ground)begin
                    next_state<=FR;
                end else begin
                    next_state<=state;
                end
            end
            DL:begin
                if(!ground)begin
                    next_state<=FL;
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
                digging<=0;
            end
            L:begin
                walk_left<=1;
                walk_right<=0;
                aaah<=0;
                digging<=0;
            end
            FL:begin
                walk_left<=0;
                walk_right<=0;
                aaah<=1;
                digging<=0;
            end
            FR:begin
                walk_left<=0;
                walk_right<=0;
                aaah<=1;
                digging<=0;
            end
            DR:begin
                walk_left<=0;
                walk_right<=0;
                aaah<=0;
                digging<=1;
            end
            DL:begin
                walk_left<=0;
                walk_right<=0;
                aaah<=0;
                digging<=1;
            end
        endcase
        
    end

endmodule



