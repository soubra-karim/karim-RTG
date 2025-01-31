class alu_agent extends uvm_agent;
  `uvm_component_utils(alu_agent);
  
  alu_driver drv;
  alu_monitor mon;
  alu_sequencer seqr;
  function new(string name="alu_agent", uvm_component parent);
    super.new(name,parent);
  endfunction
  
  function void build_phase(uvm_phase phase);
    super.build_phase(phase);
    drv = alu_driver::type_id::create("drv",this);
    mon = alu_monitor::type_id::create("mon",this);
    seqr = alu_sequencer::type_id::create("seqr",this);
  endfunction:build_phase
  
  
  function void connect_phase(uvm_phase phase);
    super.connect_phase(phase);
    drv.seq_item_port.connect(seqr.seq_item_export);
  endfunction: connect_phase
  
  
  task run_phase(uvm_phase phase);
    super.run_phase(phase);
    
  endtask: run_phase
  
endclass:alu_agent;