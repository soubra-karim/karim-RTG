
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
 /*
reg [7:0] line [511:0]; //line buffer
reg [8:0] wrPntr;
reg [8:0] rdPntr;

always @(posedge CLK)
begin
    if(DATA_VALID)
        line[wrPntr] <= DATA;
end

always @(posedge CLK)
begin
    if(RESETH)
        wrPntr <= 'd0;
    else if(DATA_VALID)
        wrPntr <= wrPntr + 'd1;
end

assign o_data = {line[rdPntr],line[rdPntr+1],line[rdPntr+2]};

always @(posedge CLK)
begin
    if(RESETH)
        rdPntr <= 'd0;
    else if(READ_DATA)
        rdPntr <= rdPntr + 'd1;
end
endmodule
*/
/*
`timescale 1ns / 1ps



module linebuffer(
input   i_clk,
input   i_rst,
input [7:0] i_data,
input   i_data_valid,
output [23:0] o_data,
input i_rd_data
);

reg [7:0] line [511:0]; //line buffer
reg [8:0] wrPntr;
reg [8:0] rdPntr;

always @(posedge i_clk)
begin
    if(i_data_valid)
        line[wrPntr] <= i_data;
end

always @(posedge i_clk)
begin
    if(i_rst)
        wrPntr <= 'd0;
    else if(i_data_valid)
        wrPntr <= wrPntr + 'd1;
end

assign o_data = {line[rdPntr],line[rdPntr+1],line[rdPntr+2]};

always @(posedge i_clk)
begin
    if(i_rst)
        rdPntr <= 'd0;
    else if(i_rd_data)
        rdPntr <= rdPntr + 'd1;
end


endmodule
*/