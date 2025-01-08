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


