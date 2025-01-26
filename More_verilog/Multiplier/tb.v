`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 01/15/2025 03:16:25 PM
// Design Name: 
// Module Name: tb
// Project Name: 
// Target Devices: 
// Tool Versions: 
// Description: 
// 
// Dependencies: 
// 
// Revision:
// Revision 0.01 - File Created
// Additional Comments:
// 
//////////////////////////////////////////////////////////////////////////////////


module tb();

    reg clk;
    reg resetH;
    reg [7:0] A;
    reg [7:0] B;
    wire [15:0] out;
    wire busy;
    
    multiplier1 DUT(
        .clk(clk),
        .resetH(resetH),
        .A(A),
        .B(B),
        .out(out),
        .busy(busy)
    );
    initial begin
        clk = 0;
        forever #5 clk = ~clk;
    end
    
    initial begin
        resetH=1;
        A=8'd5;
        B=8'd5;
        
        #15;
        resetH=0;
        
        #20;
    end
endmodule
