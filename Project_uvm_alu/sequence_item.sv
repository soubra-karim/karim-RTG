
class alu_sequence_item extends uvm_sequence_item;
  
  `uvm_object_utils(alu_sequence_item)
  
    
  rand logic reset;
  
  rand logic [7:0] A;
  rand logic [7:0] B;
  rand logic [4:0] op;
  logic [7:0] result;
  bit carryout;
  
  
  constraint c_input {A inside {[10:20]};}
  constraint c_input2 {B inside {[1:10]};}
  
  
  constraint c_op {op inside {0,1,2,3};}
  
  function new(string name="alu_sequence_item");
    super.new(name);
    
  endfunction: new
  
  
endclass: alu_sequence_item