interface alu_if;  
  logic reset;
  logic clk;
  logic [7:0] A;
  logic [7:0] B;
  logic [3:0] alu_sel;
  logic [7:0] alu_out;
  logic carryout;
endinterface