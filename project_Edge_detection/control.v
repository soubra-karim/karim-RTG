
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

