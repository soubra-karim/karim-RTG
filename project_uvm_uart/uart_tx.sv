module uart_tx(
  input tx_clk,
  input tx_start,
  input rst,
  input [7:0] tx_data,
  input [3:0] length,
  input parity_type,
  input parity_en,
  input stop2,
  output reg tx,
  output reg tx_done,
  output reg tx_err
);
    
    logic [7:0] tx_reg;
    
    logic start_b = 0;
    logic stop_b  = 1;
    logic parity_bit = 0;
    integer count = 0;
    
    typedef enum bit [2:0]  {idle = 0, start_bit = 1, send_data = 2, send_parity = 3, send_first_stop = 4, send_sec_stop = 5, done = 6} state_type;
    state_type state = idle, next_state = idle;
    
   
    always@(posedge tx_clk)begin
       if(parity_type == 1'b1) 
         begin
            case(length)
              4'd5 : parity_bit = ^(tx_data[4:0]); 
              4'd6 : parity_bit = ^(tx_data[5:0]); 
              4'd7 : parity_bit = ^(tx_data[6:0]);
              4'd8 : parity_bit = ^(tx_data[7:0]);
              default : parity_bit = 1'b0; 
            endcase
         end
        else
         begin
            case(length)
              4'd5 : parity_bit = ~^(tx_data[4:0]);
              4'd6 : parity_bit = ~^(tx_data[5:0]); 
              4'd7 : parity_bit = ~^(tx_data[6:0]);
              4'd8 : parity_bit = ~^(tx_data[7:0]);
              default : parity_bit = 1'b0; 
            endcase
         end 
    end
    
    
    always@(posedge tx_clk)begin
      if(rst)begin
       	state <= idle;
      end else begin
       	state <= next_state;
      end
    end
    
    
   
    
    
  always@(*) begin
    case(state)
      idle :begin
         tx_done= 1'b0; 
         tx= 1'b1;
         tx_reg={8{1'b0}}; 
         tx_err= 0;
         if(tx_start) begin
           next_state = start_bit;
         end else begin
           next_state=idle;
         end
                
      end
     
      start_bit : begin
      	tx_reg= tx_data;
        tx= start_b;
        next_state= send_data;
      end       
      send_data:begin
      	if(count < (length - 1)) begin
        	next_state = send_data;
            tx= tx_reg[count];
        end else if (parity_en)begin
            tx= tx_reg[count];
            next_state = send_parity;
        end else begin
            tx= tx_reg[count];
            next_state= send_first_stop;
        end
      end  
     
      
      send_parity: begin
      	tx = parity_bit;
       	next_state  = send_first_stop;
      end
     
      send_first_stop : begin
          tx  = stop_b;
        if(stop2) begin
          next_state=send_sec_stop;
        end else begin
         	next_state  = done;
        end
      end
      send_sec_stop : begin
          tx= stop_b;
          next_state  = done;
      end   
    done :begin
         tx_done = 1'b1;
         next_state  = idle;
    end
    default : next_state  = idle;
    
    endcase
 end
 
 
  always@(posedge tx_clk) begin
 		case(state)
    		send_data: begin
    	  		count <= count + 1;
    		end
    		default : count <= 0;
 		endcase
	end
endmodule