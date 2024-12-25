

`timescale 1ns / 1ps





// implementing axi stream
module image_top(
    input ACLK,
    input ARESETn,
    //
    input TVALID_sub,
    input [7:0] TDATA_sub,
    output TREADY_sub,
    //
    output TVALID_man,
    output [7:0] TDATA_man,
    input TREADY_man,
    output INT
    );
    
    
    
    
    wire [71:0] pixel_data;
    wire pixel_data_valid;
    
    wire [7:0] data_m1;
    wire valid_m1;
    wire full;
    assign TREADY_sub = !full;
    control C1(
    .CLK(ACLK),
    .RESETH(!ARESETn),
    .PIXEL_DATA(TDATA_sub),
    .PIXEL_DATA_VALID(TVALID_sub),
    .OUT_PIXEL_DATA(pixel_data),
    .OUT_PIXEL_DATA_VALID(pixel_data_valid),
    .INT(INT)
    );
    
    
     macc m1(
    .CLK(ACLK),
    .PIXEL_DATA(pixel_data),
    .DATA_VALID(pixel_data_valid),
     .DATAOUT(data_m1),
    .DATAOUT_VALID(valid_m1)
    );
    
    outputbuffer buff(
      .wr_rst_busy(),        // output wire wr_rst_busy
      .rd_rst_busy(),        // output wire rd_rst_busy
      .s_aclk(ACLK),                  // input wire s_aclk
      .s_aresetn(ARESETn),            // input wire s_aresetn
      .s_axis_tvalid(valid_m1),    // input wire s_axis_tvalid
      .s_axis_tready(),    // output wire s_axis_tready
      .s_axis_tdata(data_m1),      // input wire [7 : 0] s_axis_tdata
      .m_axis_tvalid(TVALID_man),    // output wire m_axis_tvalid
      .m_axis_tready(TREADY_man),    // input wire m_axis_tready
      .m_axis_tdata(TDATA_man),      // output wire [7 : 0] m_axis_tdata
      .axis_prog_full(full)  // output wire axis_prog_full
    );
endmodule

/*
`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 04/01/2020 08:10:25 PM
// Design Name: 
// Module Name: imageProcessTop
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


module image_top(
input   axi_clk,
input   axi_reset_n,
//slave interface
input   i_data_valid,
input [7:0] i_data,
output  o_data_ready,
//master interface
output  o_data_valid,
output [7:0] o_data,
input   i_data_ready,
//interrupt
output  o_intr

    );

wire [71:0] pixel_data;
wire pixel_data_valid;
wire axis_prog_full;
wire [7:0] convolved_data;
wire convolved_data_valid;

assign o_data_ready = !axis_prog_full;
    
control IC(
    .i_clk(axi_clk),
    .i_rst(!axi_reset_n),
    .i_pixel_data(i_data),
    .i_pixel_data_valid(i_data_valid),
    .o_pixel_data(pixel_data),
    .o_pixel_data_valid(pixel_data_valid),
    .o_intr(o_intr)
  );    
  
 macc conv(
     .i_clk(axi_clk),
     .i_pixel_data(pixel_data),
     .i_pixel_data_valid(pixel_data_valid),
     .o_convolved_data(convolved_data),
     .o_convolved_data_valid(convolved_data_valid)
 ); 
 
 outputbuffer OB (
   .wr_rst_busy(),        // output wire wr_rst_busy
   .rd_rst_busy(),        // output wire rd_rst_busy
   .s_aclk(axi_clk),                  // input wire s_aclk
   .s_aresetn(axi_reset_n),            // input wire s_aresetn
   .s_axis_tvalid(convolved_data_valid),    // input wire s_axis_tvalid
   .s_axis_tready(),    // output wire s_axis_tready
   .s_axis_tdata(convolved_data),      // input wire [7 : 0] s_axis_tdata
   .m_axis_tvalid(o_data_valid),    // output wire m_axis_tvalid
   .m_axis_tready(i_data_ready),    // input wire m_axis_tready
   .m_axis_tdata(o_data),      // output wire [7 : 0] m_axis_tdata
   .axis_prog_full(axis_prog_full)  // output wire axis_prog_full
 );
  
    
    
endmodule
*/