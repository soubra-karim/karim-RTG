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

    
    parameter L=0,R=1,FL=2,FR=3,DR=4,DL=5,DEAD=6;
    
    reg [2:0] state,next_state;
    reg [4:0] death_timer;
    reg dead_flag;
    initial dead_flag=0;
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
                    if(dead_flag) begin
                		next_state<=DEAD;    
                	end else begin
                        next_state<=R;
                    end
                    
                end  else begin
                    next_state<=state;
                end
            end
            FL:begin
                if(ground )begin
                     if(dead_flag) begin
                		next_state<=DEAD;    
                	end else begin
                        next_state<=L;
                    end
                end  else begin
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
            DEAD:begin
               next_state<=state; 
            end
        endcase
        
    end
    
    
    always @(posedge clk,posedge areset)begin
        if(areset)begin
            death_timer<=0;
            dead_flag<=0;
            state<=L;
        end else begin
             state <= next_state;
                if (state == FL || state == FR) begin
                    if (death_timer < 20) begin
                        death_timer <= death_timer + 1;
                        dead_flag <= 0;
                    end else begin
                        death_timer <= death_timer;
                        dead_flag <= 1;
                    end
                end 

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
            DEAD:begin
                walk_left<=0;
                walk_right<=0;
                aaah<=0;
                digging<=0;
            end
        endcase
        
    end

    
    
endmodule

