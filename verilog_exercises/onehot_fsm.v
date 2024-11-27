module top_module(
    input in,
    input [9:0] state,
    output [9:0] next_state,
    output out1,
    output out2);
    /*
    parameter [9:0] s0=10'd1,s1=10'd2,s2=10'd4,s3=10'd8,s4=10'd16,s5=10'd32,s6=10'd64,s7=10'd128,s8=10'd256,s9=10'd512;
    
    
    always @(*)begin
        case(state)
            s0:begin
                if(in)begin
                    next_state<=s1; 
                end else begin
                   next_state<=s0; 
                end
            end
            s1:begin
                if(in)begin
                   next_state<=s2; 
                    
                end else begin
                   next_state<=s0; 
                end
            end
            s2:begin
                if(in)begin
                    next_state<=s3; 
                end else begin
                   next_state<=s0; 
                end
            end
            s3:begin
                if(in)begin
                    next_state<=s4; 
                end else begin
                   next_state<=s0; 
                end
            end
            s4:begin
                if(in)begin
                    next_state<=s5; 
                end else begin
                   next_state<=s0; 
                end
            end
            s5:begin
                if(in)begin
                    next_state<=s6; 
                end else begin
                   next_state<=s8; 
                end
            end
            s6:begin
                if(in)begin
                    next_state<=s7; 
                end else begin
                   next_state<=s9; 
                end
            end
            s7:begin
                if(in)begin
                    next_state<=s7; 
                end else begin
                   next_state<=s0; 
                end
            end
            s8:begin
                if(in)begin
                    next_state<=s1; 
                end else begin
                   next_state<=s0; 
                end
            end
            s9:begin
                if(in)begin
                    next_state<=s1; 
                end else begin
                   next_state<=s0; 
                end
            end
        endcase


            
        
        
    end
    
    always@(*)begin

        if(state==s7)begin
           out2<=1;
            out1<=0;
        end else if(state==s8)begin
           out2<=0;
            out1<=1;
        end else if(state==s9)begin
           out2<=1;
            out1<=1;
        end else begin
           out2<=0;
            out1<=0;
        end
    end
    
*/

    assign next_state[0] = (state[0] & ~in) | (state[1] & ~in) | (state[2] & ~in) | (state[3] & ~in) | (state[4] & ~in) | (state[7] & ~in) | (state[8] & ~in) | (state[9] & ~in);
    assign next_state[1] = (state[0] & in) | (state[8] &in) | (state[9] & in);
    assign next_state[2] = state[1] & in;
    assign next_state[3] = state[2] & in;
    assign next_state[4] = state[3] & in;
    assign next_state[5] = state[4] & in;
    assign next_state[6] = state[5] & in;
    assign next_state[7] = (state[6] & in) | (state[7] & in);
    assign next_state[8] = state[5] & ~in;
    assign next_state[9] = state[6] & ~in;



    assign out1 = (state[8] == 1) | (state[9] == 1);
    assign out2 = (state[9] ==1) | (state[7] == 1);
endmodule

