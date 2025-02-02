`include "alu_if.sv"
module alu(
  input clock,
  input reset,
  input [7:0] A,B,                
  input [3:0] ALU_Sel,
  output reg [7:0] ALU_Out, 
  output bit CarryOut 
);

  reg [7:0] ALU_Result;
  wire [8:0] tmp;

  assign tmp = {1'b0,A} + {1'b0,B};

  
  always @(posedge clock or posedge reset) begin
    if(reset) begin
      ALU_Out  <= 8'd0;
      CarryOut <= 1'd0;
    end
    else begin
      ALU_Out <= ALU_Result;
      CarryOut <= tmp[8];
    end
  end


  always @(*) 
    begin
      case(ALU_Sel)
        4'b0000: 
          ALU_Result = A + B ; 
        4'b0001: 
          ALU_Result = A - B ;
        4'b0010: 
          ALU_Result = A * B;
        4'b0011:
          ALU_Result = A/B;
        default: ALU_Result = 8'hAC ;
      endcase
    end

endmodule