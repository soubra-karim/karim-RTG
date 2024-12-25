`timescale 1ns / 1ps



module macc(
    input CLK,
    input [71:0] PIXEL_DATA,
    input DATA_VALID,
    output reg [7:0] DATAOUT,
    output reg DATAOUT_VALID
    );


//Sobel edge detection

integer i;
reg [7:0] kernel [8:0];
reg [7:0] kernel2 [8:0];
reg [15:0] mulresult[8:0];
reg [15:0] mulresult2[8:0];
reg [15:0] addresult;
reg [15:0] addresult2;
reg [15:0] finaladdresult;
reg [15:0] finaladdresult2;
reg [31:0] sq;
reg [31:0] sq2;
wire [31:0] final_sq;
reg data_valid_mul_add;
reg data_valid_add_sq;
reg data_sq_div;
reg final_valid;
initial begin
    kernel[0] =  1;
    kernel[1] =  0;
    kernel[2] = -1;
    kernel[3] =  2;
    kernel[4] =  0;
    kernel[5] = -2;
    kernel[6] =  1;
    kernel[7] =  0;
    kernel[8] = -1;
    
    kernel2[0] =  1;
    kernel2[1] =  2;
    kernel2[2] =  1;
    kernel2[3] =  0;
    kernel2[4] =  0;
    kernel2[5] =  0;
    kernel2[6] = -1;
    kernel2[7] = -2;
    kernel2[8] = -1;

end

always @(posedge CLK)begin
    for(i=0;i<9;i=i+1)begin
                            //LSB = i+8  MSB=i*8+7
        mulresult[i]<=$signed(kernel[i])*$signed({1'b0,PIXEL_DATA[i*8+:8]});    
        mulresult2[i]<=$signed(kernel2[i])*$signed({1'b0,PIXEL_DATA[i*8+:8]});   
    end
    data_valid_mul_add<= DATA_VALID;
end
always @(*)begin
    addresult=0;
    addresult2=0;
    for(i=0; i<9;i=i+1)begin
        addresult = $signed(addresult) + $signed(mulresult[i]);
        addresult2 = $signed(addresult2) + $signed(mulresult2[i]);
    end
    
end
always @(posedge CLK)begin
    finaladdresult<=addresult;
    finaladdresult2<=addresult2;
    data_valid_add_sq<=data_valid_mul_add;
end
always @(posedge CLK)begin
    sq<= $signed(finaladdresult)*$signed(finaladdresult);
    sq2<= $signed(finaladdresult2)*$signed(finaladdresult2);
    data_sq_div<=data_valid_add_sq;
end
assign final_sq = sq + sq2;

always @(posedge CLK)begin
    if(final_sq > 4000)begin
        DATAOUT <= 8'hff;
    end else begin
        DATAOUT <= 8'h00;
    end
    //DATAOUT <= finaladdresult/9;
    DATAOUT_VALID<= data_sq_div;
end
// Downsampling
/*
integer i;
reg [7:0] kernel [8:0];
reg [15:0] mulresult[8:0];
reg [15:0] addresult;
reg [15:0] finaladdresult;
reg [7:0] finaldata;

reg data_valid_mul_add;
reg data_valid_add_div;
reg final_valid;
initial begin
    for(i=0; i<9;i=i+1)begin
        kernel[i] = 1;
    end
end



// multiply pixel with kernel
always @(posedge CLK)begin
    for(i=0;i<9;i=i+1)begin
                            //LSB = i+8  MSB=i*8+7
        mulresult[i]<=kernel[i]*PIXEL_DATA[i*8+:8];    
    end
    
    data_valid_mul_add<= DATA_VALID;
end

// add result of mul

always @(*)begin
    addresult=0;
    for(i=0; i<9;i=i+1)begin
        addresult = addresult + mulresult[i];
    end
    
end

always @(posedge CLK)begin
    finaladdresult<=addresult;
    data_valid_add_div<=data_valid_mul_add;
end


always @(posedge CLK)begin
    DATAOUT <= finaladdresult/9;
    DATAOUT_VALID<= data_valid_add_div;
end
//assign DATAOUT_VALID = final_valid;
//assign DATAOUT = finaldata;
*/
endmodule

