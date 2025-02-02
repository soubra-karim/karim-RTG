`include "uvm_macros.svh"
import uvm_pkg::*;

class alu_config extends uvm_object;
  `uvm_object_utils(alu_config)
  
  function new(string name="alu_config");
    super.new(name);
  endfunction
  uvm_active_passive_enum  is_active = UVM_ACTIVE;
  
endclass

class alu_seq_item extends uvm_sequence_item;
  `uvm_object_utils(alu_seq_item)
  rand logic [7:0] A;
  rand logic [7:0] B;
  rand logic [3:0] alu_sel;
  rand logic reset;
  logic [7:0] alu_out;
  bit carryout;
  
  constraint alu_sel_c {alu_sel inside {0,1,2,3};}
  constraint A_c{A inside {[0:20]};}
  constraint B_c{B inside {[0:20]};}
  function new(string name="alu_seq_item");
    super.new(name);
  endfunction
    
endclass

class alu_seq extends uvm_sequence#(alu_seq_item);
  `uvm_object_utils(alu_seq)
  function new(string name="alu_seq");
    super.new(name);
  endfunction
  alu_seq_item tr;
  virtual task body();
    
      
        tr=alu_seq_item::type_id::create("tr");
        start_item(tr);
        assert(tr.randomize());
    	tr.reset=1'b0;
        finish_item(tr);
      
  endtask
  
endclass

class reset_alu_seq extends uvm_sequence#(alu_seq_item);
  `uvm_object_utils(reset_alu_seq)
  function new(string name="reset_alu_seq");
    super.new(name);
  endfunction
  alu_seq_item tr;
  virtual task body();
    
      
        tr=alu_seq_item::type_id::create("tr");
        start_item(tr);
        assert(tr.randomize());
    	tr.reset=1'b1;
        finish_item(tr);
      
  endtask
  
endclass
class drv extends uvm_driver#(alu_seq_item);
  `uvm_component_utils(drv)
  virtual alu_if vif;
  alu_seq_item tr;
  
  function new(string name="drv", uvm_component parent=null);
    super.new(name,parent);
  endfunction
  
  virtual function void build_phase(uvm_phase phase);
    super.build_phase(phase);
    
    if(!uvm_config_db#(virtual alu_if)::get(this,"","vif",vif))
      `uvm_error("drv","unable to access interface");
  endfunction
  
  virtual task run_phase(uvm_phase phase);
    super.run_phase(phase);
  
     forever begin
       tr=alu_seq_item::type_id::create("tr");
       seq_item_port.get_next_item(tr);
       @(posedge vif.clk);
       vif.A<=tr.A;
       vif.B<=tr.B;
       vif.alu_sel<=tr.alu_sel;
       vif.reset<=tr.reset;
      // `uvm_info("DRV", $sformatf("driving OP:%0d A:%0d B:%0d reset:%0d",tr.alu_sel,tr.A,tr.B,tr.reset), UVM_NONE);

       seq_item_port.item_done();
     end
     
   
  endtask
endclass

class mon extends uvm_monitor;
  `uvm_component_utils(mon)
  uvm_analysis_port#(alu_seq_item) send;
  alu_seq_item tr;
  virtual alu_if vif;
  
  function new(string name="mon",uvm_component parent=null);
    super.new(name,parent);
  endfunction
  
  virtual function void build_phase(uvm_phase phase);
    super.build_phase(phase);
    tr=alu_seq_item::type_id::create("tr");
    send = new("send",this);
    if(!uvm_config_db#(virtual alu_if)::get(this,"","vif",vif))
      `uvm_error("mon","unable to access interface");
  endfunction
  
  virtual task run_phase(uvm_phase phase);
    super.run_phase(phase);
    
    forever begin
      tr=alu_seq_item::type_id::create("tr");
      @(posedge vif.clk);
      	
        tr.A=vif.A;
        tr.B=vif.B;
      	tr.alu_sel = vif.alu_sel;
      	tr.reset=vif.reset;
        
      @(posedge vif.clk);
        tr.alu_out=vif.alu_out;
        tr.carryout=vif.carryout;
      if(tr.reset)begin
          `uvm_info("MON", "SYSTEM RESET DETECTED", UVM_NONE);
        end else begin
          `uvm_info("MON", $sformatf("driving OP:%0d A:%0d B:%0d reset:%0d result:%0d cout:%0d",tr.alu_sel,tr.A,tr.B,tr.reset,tr.alu_out,tr.carryout), UVM_NONE);
         end
      	send.write(tr);
      
        
      
    end
  endtask
  
endclass

class sco extends uvm_scoreboard;
  `uvm_component_utils(sco)
  uvm_analysis_imp#(alu_seq_item,sco) recv;
  
  function new(string inst="sco",uvm_component parent=null);
    super.new(inst,parent);
  endfunction
  
  virtual function void build_phase(uvm_phase phase);
    super.build_phase(phase);
    recv=new("recv",this);
  endfunction
  virtual function void write(alu_seq_item tr);
    logic [7:0] expected;
    logic [7:0] actual;
    if(tr.reset==1'b1)begin
      `uvm_info("SCO", "System Reset", UVM_NONE)
      
    end else begin
        logic [7:0] expected;
    	logic [7:0] actual;
      case(tr.alu_sel)
        0: begin //A + B
          expected = tr.A + tr.B;
        end
        1: begin //A - B
          expected = tr.A  - tr.B;
        end
        2: begin //A * B
          expected = tr.A  * tr.B;
        end
        3: begin //A / B
          expected = tr.A  / tr.B;
        end
      endcase
      actual = tr.alu_out;
      if(actual != expected) begin
        `uvm_error("COMPARE", $sformatf("Transaction failed! ACT=%d, EXP=%d", actual, expected))
      end
      else begin
        
        `uvm_info("COMPARE", $sformatf("Transaction Passed! ACT=%d, EXP=%d", actual, expected), UVM_LOW)
      end
    end
    
  endfunction
  
  
endclass

class agent extends uvm_agent;
  `uvm_component_utils(agent)
  alu_config cfg;
  function new(string inst="agent",uvm_component parent=null);
    super.new(inst,parent);
  endfunction
  drv d;
  mon m;
  uvm_sequencer#(alu_seq_item) seqr;
  virtual function void build_phase(uvm_phase phase);
    super.build_phase(phase);
    m=mon::type_id::create("m",this);
    cfg=alu_config::type_id::create("cfg");
    if(cfg.is_active == UVM_ACTIVE)begin
      d=drv::type_id::create("d",this);
      seqr=uvm_sequencer#(alu_seq_item)::type_id::create("seqr",this);
    end
  endfunction
  
  virtual function void connect_phase(uvm_phase phase);
    super.connect_phase(phase);
    if(cfg.is_active==UVM_ACTIVE)begin
      d.seq_item_port.connect(seqr.seq_item_export);
    end
  endfunction
endclass

class env extends uvm_env;
  `uvm_component_utils(env);
  agent a;
  sco s;
  function new(string inst="env",uvm_component parent);
    super.new(inst,parent);
  endfunction
  virtual function void build_phase(uvm_phase phase);
    super.build_phase(phase);
    a=agent::type_id::create("a",this);
    s=sco::type_id::create("s",this);
  endfunction
  
  virtual function void connect_phase(uvm_phase phase);
    super.connect_phase(phase);
    a.m.send.connect(s.recv);
  endfunction
endclass

class test extends uvm_test;
  `uvm_component_utils(test)
  function new(string inst="test",uvm_component c);
    super.new(inst,c);
  endfunction
  
  env e;
  alu_seq rand_input;
	reset_alu_seq reset_rand_input;
  virtual function void build_phase(uvm_phase phase);
    super.build_phase(phase);
    e=env::type_id::create("e",this);
    rand_input=alu_seq::type_id::create("rand_input");
    reset_rand_input=reset_alu_seq::type_id::create("reset_rand_input");
  endfunction
  
  virtual task run_phase(uvm_phase phase);
    phase.raise_objection(this);
    reset_rand_input.start(e.a.seqr);
    #20;
    repeat(5)
      begin
        rand_input.start(e.a.seqr);
    	#20;
      end
    
    phase.drop_objection(this);
  endtask
endclass

module tb;
  alu_if vif();
  alu dut(.clock(vif.clk),.reset(vif.reset),.A(vif.A),.B(vif.B),.ALU_Sel(vif.alu_sel),.ALU_Out(vif.alu_out),.CarryOut(vif.carryout));
  
  initial begin
    uvm_config_db#(virtual alu_if)::set(null,"*","vif",vif);
    run_test("test");
  end
 	
  initial begin
    vif.clk=0;
  end
  
  always #10 vif.clk=~vif.clk;
  initial begin
    $dumpfile("dump.vcd");
    $dumpvars;
  end
endmodule
  