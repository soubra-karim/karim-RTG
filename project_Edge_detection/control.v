
`timescale 1ns / 1ps



module control(
    input CLK,
    input RESETH,
    input [7:0] PIXEL_DATA,
    input PIXEL_DATA_VALID,
    output reg [71:0] OUT_PIXEL_DATA,
    output OUT_PIXEL_DATA_VALID,
    output reg INT
    );
    reg [8:0] counter;
    reg [1:0] current_buffer;
    reg [3:0] current_valid;
    
    reg interrupt;
    
    reg [1:0] read_current_buffer;
    reg [3:0] read_current_valid;
    reg [8:0] read_counter;
    reg read_en;
    
    
    
    wire [23:0] buffer_data1;
    wire [23:0] buffer_data2;
    wire [23:0] buffer_data3;
    wire [23:0] buffer_data4;
    
    reg [71:0] final_output_pixel_data;
    
    reg [11:0] total_pixels_received;
    reg current_state;
    
    assign OUT_PIXEL_DATA_VALID=read_en;
    //assign INT = interrupt;
    always @(posedge CLK)begin
        if(RESETH)begin
            total_pixels_received<=0;
        end else begin
            if(PIXEL_DATA_VALID & !read_en)begin
            
                total_pixels_received<=total_pixels_received+1;
            end else if(!PIXEL_DATA_VALID & read_en)begin
            
                total_pixels_received<=total_pixels_received-1;
            end
        end
    
    end
    
    parameter idle_state=0,read_state=1;
    always @(posedge CLK)begin
        if(RESETH) begin
            read_en<=0;
            INT<=0;
            current_state<=idle_state;
        end else begin
            case(current_state)
                idle_state:begin
                    INT<=0;
                    if(total_pixels_received >= 1536)begin
                        read_en<=1;
                        current_state<=read_state;
                    end
                
                end
                read_state:begin
                    if(read_counter==511)begin
                        read_en<=0;
                        current_state<=idle_state;
                        INT<=1;
                    end
                end
                                
            endcase
        
        end
    
    end
    
    always @(posedge CLK)begin
        if(RESETH)begin
            counter<=0;
        end else begin
            if(PIXEL_DATA_VALID)begin
            
                counter<=counter+1;
            end
        end
      
    
    end
    
    always @(posedge CLK)begin
    
        if(RESETH)begin
            current_buffer<=0;
        
        end else begin
            if(counter==511 & PIXEL_DATA_VALID)begin
                current_buffer<=current_buffer+1;
            
            end 
        
        end
    
    end

    
    always @(*)begin
        current_valid = 4'h0;
        current_valid[current_buffer] = PIXEL_DATA_VALID;
      
    end
        //reg [1:0] read_current_buffer;
    //reg [3:0] read_current_valid;
    
    always @(posedge CLK)begin
        if(RESETH)begin
            read_current_buffer<=0;
        end else begin
              if(read_counter==511 & read_en)begin
              
                read_current_buffer <= read_current_buffer+1;
              end
        end
    
    end
    
    always @(posedge CLK)begin
        if(RESETH)begin
            read_counter<=0;
        
        end else begin
            if(read_en)begin
                read_counter <= read_counter+1;
            end
        end 
    end
    
    
    always @(*)begin
        case(read_current_buffer)
            0:begin
                OUT_PIXEL_DATA = {buffer_data3,buffer_data2,buffer_data1};
            end
            1:begin
                OUT_PIXEL_DATA = {buffer_data4,buffer_data3,buffer_data2};
            end
            2:begin
                OUT_PIXEL_DATA = {buffer_data1,buffer_data4,buffer_data3};
            end
            3:begin
                OUT_PIXEL_DATA = {buffer_data2,buffer_data1,buffer_data4};
            end
            
        endcase
    end
    //assign OUT_PIXEL_DATA = final_output_pixel_data;

    always @(*)begin
        case(read_current_buffer)
            0:begin
                read_current_valid = {1'b0,read_en,read_en,read_en};
            end
            1:begin
                read_current_valid = {read_en,read_en,read_en,1'b0};
            end
            2:begin
               read_current_valid = {read_en,read_en,1'b0,read_en};
            end
            3:begin
                read_current_valid = {read_en,1'b0,read_en,read_en};
            end
            
        endcase
    end
    
    
    linebuffer buffer1(
    .CLK(CLK),
    .RESETH(RESETH),
    .READ_DATA(read_current_valid[0]),
    .DATA(PIXEL_DATA),
    .DATA_VALID(current_valid[0]),
    .DATA_OUT(buffer_data1)
    );
    linebuffer buffer2(
    .CLK(CLK),
    .RESETH(RESETH),
    .READ_DATA(read_current_valid[1]),
    .DATA(PIXEL_DATA),
    .DATA_VALID(current_valid[1]),
    .DATA_OUT(buffer_data2)
    );
    linebuffer buffer3(
    .CLK(CLK),
    .RESETH(RESETH),
    .READ_DATA(read_current_valid[2]),
    .DATA(PIXEL_DATA),
    .DATA_VALID(current_valid[2]),
    .DATA_OUT(buffer_data3)
    );
    linebuffer buffer4(
    .CLK(CLK),
    .RESETH(RESETH),
    .READ_DATA(read_current_valid[3]),
    .DATA(PIXEL_DATA),
    .DATA_VALID(current_valid[3]),
    .DATA_OUT(buffer_data4)
    );
endmodule

/*
`timescale 1ns / 1ps
module control(
input                    i_clk,
input                    i_rst,
input [7:0]              i_pixel_data,
input                    i_pixel_data_valid,
output reg [71:0]        o_pixel_data,
output                   o_pixel_data_valid,
output reg               o_intr
);

reg [8:0] pixelCounter;
reg [1:0] currentWrLineBuffer;
reg [3:0] lineBuffDataValid;
reg [3:0] lineBuffRdData;
reg [1:0] currentRdLineBuffer;
wire [23:0] lb0data;
wire [23:0] lb1data;
wire [23:0] lb2data;
wire [23:0] lb3data;
reg [8:0] rdCounter;
reg rd_line_buffer;
reg [11:0] totalPixelCounter;
reg rdState;

localparam IDLE = 'b0,
           RD_BUFFER = 'b1;

assign o_pixel_data_valid = rd_line_buffer;

always @(posedge i_clk)
begin
    if(i_rst)
        totalPixelCounter <= 0;
    else
    begin
        if(i_pixel_data_valid & !rd_line_buffer)
            totalPixelCounter <= totalPixelCounter + 1;
        else if(!i_pixel_data_valid & rd_line_buffer)
            totalPixelCounter <= totalPixelCounter - 1;
    end
end

always @(posedge i_clk)
begin
    if(i_rst)
    begin
        rdState <= IDLE;
        rd_line_buffer <= 1'b0;
        o_intr <= 1'b0;
    end
    else
    begin
        case(rdState)
            IDLE:begin
                o_intr <= 1'b0;
                if(totalPixelCounter >= 1536)
                begin
                    rd_line_buffer <= 1'b1;
                    rdState <= RD_BUFFER;
                end
            end
            RD_BUFFER:begin
                if(rdCounter == 511)
                begin
                    rdState <= IDLE;
                    rd_line_buffer <= 1'b0;
                    o_intr <= 1'b1;
                end
            end
        endcase
    end
end
    
always @(posedge i_clk)
begin
    if(i_rst)
        pixelCounter <= 0;
    else 
    begin
        if(i_pixel_data_valid)
            pixelCounter <= pixelCounter + 1;
    end
end


always @(posedge i_clk)
begin
    if(i_rst)
        currentWrLineBuffer <= 0;
    else
    begin
        if(pixelCounter == 511 & i_pixel_data_valid)
            currentWrLineBuffer <= currentWrLineBuffer+1;
    end
end


always @(*)
begin
    lineBuffDataValid = 4'h0;
    lineBuffDataValid[currentWrLineBuffer] = i_pixel_data_valid;
end

always @(posedge i_clk)
begin
    if(i_rst)
        rdCounter <= 0;
    else 
    begin
        if(rd_line_buffer)
            rdCounter <= rdCounter + 1;
    end
end

always @(posedge i_clk)
begin
    if(i_rst)
    begin
        currentRdLineBuffer <= 0;
    end
    else
    begin
        if(rdCounter == 511 & rd_line_buffer)
            currentRdLineBuffer <= currentRdLineBuffer + 1;
    end
end


always @(*)
begin
    case(currentRdLineBuffer)
        0:begin
            o_pixel_data = {lb2data,lb1data,lb0data};
        end
        1:begin
            o_pixel_data = {lb3data,lb2data,lb1data};
        end
        2:begin
            o_pixel_data = {lb0data,lb3data,lb2data};
        end
        3:begin
            o_pixel_data = {lb1data,lb0data,lb3data};
        end
    endcase
end

always @(*)
begin
    case(currentRdLineBuffer)
        0:begin
            lineBuffRdData[0] = rd_line_buffer;
            lineBuffRdData[1] = rd_line_buffer;
            lineBuffRdData[2] = rd_line_buffer;
            lineBuffRdData[3] = 1'b0;
        end
       1:begin
            lineBuffRdData[0] = 1'b0;
            lineBuffRdData[1] = rd_line_buffer;
            lineBuffRdData[2] = rd_line_buffer;
            lineBuffRdData[3] = rd_line_buffer;
        end
       2:begin
             lineBuffRdData[0] = rd_line_buffer;
             lineBuffRdData[1] = 1'b0;
             lineBuffRdData[2] = rd_line_buffer;
             lineBuffRdData[3] = rd_line_buffer;
       end  
      3:begin
             lineBuffRdData[0] = rd_line_buffer;
             lineBuffRdData[1] = rd_line_buffer;
             lineBuffRdData[2] = 1'b0;
             lineBuffRdData[3] = rd_line_buffer;
       end        
    endcase
end
    
linebuffer lB0(
    .i_clk(i_clk),
    .i_rst(i_rst),
    .i_data(i_pixel_data),
    .i_data_valid(lineBuffDataValid[0]),
    .o_data(lb0data),
    .i_rd_data(lineBuffRdData[0])
 ); 
 
 linebuffer lB1(
     .i_clk(i_clk),
     .i_rst(i_rst),
     .i_data(i_pixel_data),
     .i_data_valid(lineBuffDataValid[1]),
     .o_data(lb1data),
     .i_rd_data(lineBuffRdData[1])
  ); 
  
  linebuffer lB2(
      .i_clk(i_clk),
      .i_rst(i_rst),
      .i_data(i_pixel_data),
      .i_data_valid(lineBuffDataValid[2]),
      .o_data(lb2data),
      .i_rd_data(lineBuffRdData[2])
   ); 
   
   linebuffer lB3(
       .i_clk(i_clk),
       .i_rst(i_rst),
       .i_data(i_pixel_data),
       .i_data_valid(lineBuffDataValid[3]),
       .o_data(lb3data),
       .i_rd_data(lineBuffRdData[3])
    );    
    
endmodule
*/