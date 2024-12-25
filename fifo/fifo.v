`timescale 1ns / 1ps



module fifo(
        input wire CLK,
        input wire RESETH,
        input wire WRH_RDL,
        input wire [31:0] DATAIN,
        output reg [31:0] DATAOUT,
        output wire FULL,
        output wire EMPTY
    );
    reg [31:0] fifo [31:0];
    
    reg [4:0] write_p,read_p;
    
    reg [5:0] count;
    reg full,empty;
    reg [31:0]data;
    assign EMPTY = (count == 0);
    assign FULL  = (count == 32);
    always @(posedge CLK ) begin
        if (RESETH) begin
            write_p <= 0;
        end else begin
            if (WRH_RDL && !FULL) begin
                fifo[write_p] <= DATAIN;
                write_p <= write_p + 1'b1;
            end
        end
    end
    
    always @(posedge CLK ) begin
        if (RESETH) begin
            read_p  <= 0;
            DATAOUT <= 32'h0;
        end else begin
            if (!WRH_RDL && !EMPTY) begin
                DATAOUT <= fifo[read_p];
                read_p <= read_p + 1'b1;
            end
        end
    end  
    
    
        always @(posedge CLK ) begin
        if (RESETH) begin
            count <= 0;
        end else begin
        
            if(WRH_RDL && !FULL)begin
                count <= count + 1;
            
            end else if(!WRH_RDL && !EMPTY)begin
                count <= count - 1;
            
            end else begin
            
                count <= count;
            end
            
        end
    end
    /*
    assign DATAOUT=data;
    assign FULL=full;
    assign EMPTY=empty;
   
    always @(*)begin
        if(RESETH)begin
            full<=0;
            empty<=0;
        
        end else begin
            full<=((write_p+1'b1)==read_p) ? 1 : 0;
            empty<=(write_p==read_p) ? 1 : 0;
        end
    
    end
    always @(posedge CLK,full,empty)begin
        if(RESETH)begin
            write_p<=0;
            read_p<=0;
            data<=32'b0;
          
        end else if(WRH_RDL && !full)begin
            
            fifo[write_p] <=DATAIN;
            write_p<=write_p+1;
        end else if (!WRH_RDL && !empty) begin
            
            data<=fifo[read_p];
            read_p<=read_p+1;
        end 
    end
    
    
    */
    
    
endmodule