class alu_sequencer extends uvm_sequencer#(alu_sequence_item);
  `uvm_component_utils(alu_sequencer);
  
  
  function new(string name="alu_sequencer", uvm_component parent);
    super.new(name,parent);
  endfunction
  
  function void build_phase(uvm_phase phase);
    super.build_phase(phase);
    	
  endfunction:build_phase
  
  
  function void connect_phase(uvm_phase phase);
    super.connect_phase(phase);
    
  endfunction: connect_phase
  
  
  
endclass:alu_sequencer;