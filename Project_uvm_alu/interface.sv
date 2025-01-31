interface alu_interface(input logic clock);
  
    
  
  
  
  logic reset;
  
  logic [7:0] A;
  logic [7:0] B;
  logic [3:0] op;
  logic [7:0] result;
  bit carryout;
endinterface: alu_interface;