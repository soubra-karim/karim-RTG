`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 12/19/2024 11:39:58 PM
// Design Name: 
// Module Name: testbench
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


`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 12/19/2024 11:18:47 PM
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
//`include "fifo.v"

module testbench;

reg CLK,RESETH,WRH_RDL;
wire FULL,EMPTY;

reg [31:0] DATAIN;
wire [31:0] DATAOUT;


fifo ff(.CLK(CLK),
        .RESETH(RESETH),
        .WRH_RDL(WRH_RDL),
        .DATAIN(DATAIN),
        .DATAOUT(DATAOUT),
        .FULL(FULL),
        .EMPTY(EMPTY));
        
        
        
        initial begin
            CLK=0;
            forever #5 CLK=~CLK;
        end
        
        
        initial begin
            
            RESETH=1;
            
            DATAIN=32'b0;
            #10
            RESETH=0;
            for (integer i=0; i<32;i=i+1)begin
                #10
                WRH_RDL=1;
                DATAIN=DATAIN+1;
                
            end
           #10;
            for (integer i=0; i<32;i=i+1)begin
                #10;
                
                WRH_RDL=0;
            end
            
           #10;
            for (integer i=32; i>=0;i=i-1)begin
                #10
                WRH_RDL=1;
                DATAIN=DATAIN+1;
                
            end
            #10;
            for (integer i=0; i<=32;i=i+1)begin
                #10;
                
                WRH_RDL=0;
            end
            
            
   
        end
  
    



endmodule

