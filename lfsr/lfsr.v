`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 12/19/2024 07:32:24 PM
// Design Name: 
// Module Name: lfsr
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
//1   2  3  4  5  6  7  8  9  10  11 12 13 14  15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30   31   32
//31 30 29 28 27 26 25 24 23 22 21 20 19 18  17 16 15 14 13 12 11 10 9 8 7 6 5 4 3 2            1    0
module lfsr(
    input wire CLK,
    input wire RESETH,
    output wire [31:0] OUTDATA
    );
    reg [31:0] rand_data;
    always @(posedge CLK)begin
        if(RESETH)begin
            rand_data<=32'hFFFFFFFF; 
        end else begin
            rand_data<={rand_data[0]^rand_data[9]^rand_data[29]^rand_data[30],rand_data[31:1]};
        end
    end
    
endmodule
