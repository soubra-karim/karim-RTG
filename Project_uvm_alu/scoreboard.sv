
class alu_scoreboard extends uvm_test;
  `uvm_component_utils(alu_scoreboard);
	
  
  uvm_analysis_imp #(alu_sequence_item,alu_scoreboard) scoreboard_port;
  alu_sequence_item transactions[$];
  function new(string name="alu_scoreboard", uvm_component parent);
    super.new(name,parent);
  endfunction
  
  function void build_phase(uvm_phase phase);
    super.build_phase(phase);
    scoreboard_port = new("scoreboard_port",this);
	
    	
  endfunction:build_phase
  
  
  function void connect_phase(uvm_phase phase);
    super.connect_phase(phase);
    
  endfunction: connect_phase
  
  
  function void write(alu_sequence_item item);
    transactions.push_back(item);
    
  endfunction: write
  
  
  
  
  task run_phase(uvm_phase phase);
    super.run_phase(phase);
    forever begin

      alu_sequence_item curr_trans;
      wait((transactions.size() != 0));
      curr_trans = transactions.pop_front();
      compare(curr_trans);
      
    end

  endtask: run_phase
  
  task compare(alu_sequence_item curr_trans);
    logic [7:0] expected;
    logic [7:0] actual;
    
    case(curr_trans.op)
      0: begin //A + B
        expected = curr_trans.A + curr_trans.B;
      end
      1: begin //A - B
        expected = curr_trans.A  - curr_trans.B;
      end
      2: begin //A * B
        expected = curr_trans.A  * curr_trans.B;
      end
      3: begin //A / B
        expected = curr_trans.A  / curr_trans.B;
      end
    endcase
    
    actual = curr_trans.result;
    
    if(actual != expected) begin
      `uvm_error("COMPARE", $sformatf("Transaction failed! ACT=%d, EXP=%d", actual, expected))
    end
    else begin
      // Note: Can display the input and op_code as well if you want to see what's happening
      `uvm_info("COMPARE", $sformatf("Transaction Passed! ACT=%d, EXP=%d", actual, expected), UVM_LOW)
    end
    
  endtask: compare
  
  
endclass:alu_scoreboard;