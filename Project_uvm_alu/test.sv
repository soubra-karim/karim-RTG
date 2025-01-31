class alu_test extends uvm_test;
  `uvm_component_utils(alu_test);
  alu_env env;
  alu_base_sequence reset_seq;
  alu_test_sequence test_seq;
  function new(string name="alu_test", uvm_component parent);
    super.new(name,parent);
  endfunction
  
  function void build_phase(uvm_phase phase);
    super.build_phase(phase);
    
    env = alu_env::type_id::create("env",this);
    	
  endfunction:build_phase
  
  
  function void connect_phase(uvm_phase phase);
    super.connect_phase(phase);
    
  endfunction: connect_phase
  
  
  task run_phase(uvm_phase phase);
    super.run_phase(phase);
    
    phase.raise_objection(this);
    
    //reset
    
    reset_seq = alu_base_sequence::type_id::create("reset_seq");
    
    reset_seq.start(env.agnt.seqr);
    #10;
    repeat(100) begin
      //test_seq
      test_seq = alu_test_sequence::type_id::create("test_seq");
      test_seq.start(env.agnt.seqr);
      #10;
    end
    
    
    phase.drop_objection(this);
  endtask: run_phase
  
endclass:alu_test;