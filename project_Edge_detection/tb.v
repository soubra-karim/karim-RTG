`timescale 1ns / 1ps
`define headerSize 1080
`define imageSize 512*512

module tb();


reg clk,reset,data_valid;
wire INT;
reg [7:0] data;
wire [7:0] output_data;
wire output_data_valid;
integer file,file2,i,data_sent;
integer rec_data=0;
initial begin
    clk=0;
    forever
    begin
        #5 clk = ~clk;
    end

end
initial begin
    
    reset=0;
    data_valid=0;
    data_sent=0;
    #100;
    reset=1;
    #100;
    file = $fopen("lena_gray.bmp","rb");
    file2 = $fopen("blurred_lena_gray.bmp","wb");
    for(i=0;i<1080;i=i+1)begin
         $fscanf(file,"%c",data);
         $fwrite(file2,"%c",data);
    end
    for(i=0;i<4*512;i=i+1)begin
        @(posedge clk);
        $fscanf(file,"%c",data);
        data_valid<=1;
    end
    data_sent=4*512;
    @(posedge clk);
    data_valid<=0;
    while(data_sent<512*512)begin
        @(posedge INT);
            for(i=0;i<512;i=i+1)begin
                @(posedge clk);
                $fscanf(file,"%c",data);
                data_valid<=1;
            end
            @(posedge clk);
            data_valid<=0;
            data_sent=data_sent+512;
    end
    @(posedge clk);
    data_valid<=0;
    @(posedge INT);
    for(i=0;i<512;i=i+1)begin
        @(posedge clk);
        data<=0;
        data_valid<=1;
    end
    @(posedge clk);
    data_valid<=0;
    @(posedge INT);
    for(i=0;i<512;i=i+1)begin
        @(posedge clk);
        data<=0;
        data_valid<=1;
    end
    @(posedge clk);
    data_valid<=0;
    $fclose(file);
end



always @(posedge clk)begin
    if(output_data_valid)begin
        $fwrite(file2,"%c",output_data);
        rec_data=rec_data+1;
    end
    if(rec_data== 512*512)begin
        $fclose(file2);
        $stop;  
    end

end
image_top DUT(
    .ACLK(clk),
    .ARESETn(reset),
    //
    .TVALID_sub(data_valid),
    .TDATA_sub(data),
    .TREADY_sub(),
    //
    .TVALID_man(output_data_valid),
    .TDATA_man(output_data),
    .TREADY_man(1'b1),
    .INT(INT)
    );
endmodule


/*
 reg clk;
 reg reset;
 reg [7:0] imgData;
 integer file,file1,i;
 reg imgDataValid;
 integer sentSize;
 wire intr;
 wire [7:0] outData;
 wire outDataValid;
 integer receivedData=0;

 initial
 begin
    clk = 1'b0;
    forever
    begin
        #5 clk = ~clk;
    end
 end
 
 initial
 begin
    reset = 0;
    sentSize = 0;
    imgDataValid = 0;
    #100;
    reset = 1;
    #100;
    file = $fopen("lena_gray.bmp","rb");
    file1 = $fopen("blurred_lena.bmp","wb");
    for(i=0;i<`headerSize;i=i+1)
    begin
        $fscanf(file,"%c",imgData);
        $fwrite(file1,"%c",imgData);
    end
    
    for(i=0;i<4*512;i=i+1)
    begin
        @(posedge clk);
        $fscanf(file,"%c",imgData);
        imgDataValid <= 1'b1;
    end
    sentSize = 4*512;
    @(posedge clk);
    imgDataValid <= 1'b0;
    while(sentSize < `imageSize)
    begin
        @(posedge intr);
        for(i=0;i<512;i=i+1)
        begin
            @(posedge clk);
            $fscanf(file,"%c",imgData);
            imgDataValid <= 1'b1;    
        end
        @(posedge clk);
        imgDataValid <= 1'b0;
        sentSize = sentSize+512;
    end
    @(posedge clk);
    imgDataValid <= 1'b0;
    @(posedge intr);
    for(i=0;i<512;i=i+1)
    begin
        @(posedge clk);
        imgData <= 0;
        imgDataValid <= 1'b1;    
    end
    @(posedge clk);
    imgDataValid <= 1'b0;
    @(posedge intr);
    for(i=0;i<512;i=i+1)
    begin
        @(posedge clk);
        imgData <= 0;
        imgDataValid <= 1'b1;    
    end
    @(posedge clk);
    imgDataValid <= 1'b0;
    $fclose(file);
 end
 
 always @(posedge clk)
 begin
     if(outDataValid)
     begin
         $fwrite(file1,"%c",outData);
         receivedData = receivedData+1;
     end 
     if(receivedData == `imageSize)
     begin
        $fclose(file1);
        $stop;
     end
 end

 image_top dut(
    .axi_clk(clk),
    .axi_reset_n(reset),
    //slave interface
    .i_data_valid(imgDataValid),
    .i_data(imgData),
    .o_data_ready(),
    //master interface
    .o_data_valid(outDataValid),
    .o_data(outData),
    .i_data_ready(1'b1),
    //interrupt
    .o_intr(intr)
);   
    
    image_top DUT(
    .ACLK(clk),
    .ARESETn(reset),
    //
    .TVALID_sub(imgDataValid),
    .TDATA_sub(imgData),
    .TREADY_sub(),
    //
    .TVALID_man(outDataValid),
    .TDATA_man(outData),
    .TREADY_man(1'b1),
    .INT(intr)
    );
endmodule
*/