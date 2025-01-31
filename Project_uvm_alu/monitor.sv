class alu_monitor extends uvm_monitor;
  `uvm_component_utils(alu_monitor);
  virtual alu_interface vif;
  alu_sequence_item item;
  
  
  
  uvm_analysis_port #(alu_sequence_item) monitor_port;
  function new(string name="alu_monitor", uvm_component parent);
    super.new(name,parent);
  endfunction
  
  function void build_phase(uvm_phase phase);
    super.build_phase(phase);
    
    monitor_port = new("monitor_port",this);
    if(!(uvm_config_db #(virtual alu_interface)::get(this, "*", "vif", vif))) begin
      `uvm_error("monitor", "Failed to get VIF from config DB!")
    end
  endfunction:build_phase
  
  
  function void connect_phase(uvm_phase phase);
    super.connect_phase(phase);
    
  endfunction: connect_phase
  
  
  task run_phase(uvm_phase phase);
    super.run_phase(phase);
    forever begin
      item = alu_sequence_item::type_id::create("item");
      wait(!vif.reset);
      
      @(posedge vif.clock);
      	item.A = vif.A;
      	item.B = vif.B;
      	item.op = vif.op;
      @(posedge vif.clock);
      	item.result = vif.result;
      
      
      
      
      
      monitor_port.write(item);
      
      
      
    end
  endtask: run_phase
  
endclass:alu_monitor;