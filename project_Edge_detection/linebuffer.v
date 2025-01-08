
`timescale 1ns / 1ps



module linebuffer(
    input CLK,
    input RESETH,
    input [7:0] DATA,
    input DATA_VALID,
    output [23:0] DATA_OUT,
    input READ_DATA
    );
  

    reg [7:0] data_mem [511:0];
    reg [8:0] w_ptr;
    reg [8:0] r_ptr;
    
    always @(posedge CLK)begin
            if(DATA_VALID)begin
                data_mem[w_ptr] <= DATA;
            end
    end
    
    always @(posedge CLK)begin
    
        if(RESETH)begin
            w_ptr<='d0;
        end else if(DATA_VALID)begin
            w_ptr<=w_ptr+'d1;
        end
    
    end
    
    assign DATA_OUT =  {data_mem[r_ptr],data_mem[r_ptr+1],data_mem[r_ptr+2]};
    
    always @(posedge CLK)begin
    
        if(RESETH)begin
            r_ptr<='d0;
        end else if(READ_DATA)begin
            r_ptr<=r_ptr+'d1;
        end
    end
    
endmodule
