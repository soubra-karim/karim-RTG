`timescale 1ns / 1ps
/*
Multiplication Algorithm 
If the LSB of Multiplier is '1', then add the multiplicand into an accumulator. 
Shift the multiplier one bit to the right and multiplicand one bit to the left. 
Stop when all bits of the multiplier are zero. 
*/



module multiplier1(
    input clk,
    input resetH,
    input [7:0] A, //multiplicand M
    input [7:0] B, //multiplier Q
    output [15:0] out, //product 
    output busy
    );
    reg [15:0] product;
    reg [4:0] count;
    reg reg_done;
    reg [7:0] A_sig,B_sig;
    
    assign busy=reg_done;
    assign out= product;
   
    always @(posedge clk)begin
        if(resetH)begin
            count<=0;
            product<=0;
            A_sig<=A;
            B_sig<=B;
            reg_done<=0;
        end else begin
            if(B_sig[0])begin
                product<=product + A_sig;
            end
            A_sig<=A_sig <<1;
            B_sig<= B_sig>>1;
            if(count<16)begin
                count<=count+1;
                reg_done<=1;
            end else begin
                reg_done<=0;
            end
            
        end
    
    end
endmodule
