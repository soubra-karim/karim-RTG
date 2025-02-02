module uart_rx(
    input rx_clk,rx_start,
    input rst, rx,
    input [3:0] length,
    input parity_type,parity_en,
    input stop2,
    output reg [7:0] rx_out,
    output logic rx_done, rx_error
    );
  
  logic parity=0;
  logic [7:0] data_rd=0;
  int count=0;
  int bit_count=0;
  typedef enum bit [2:0] {idle = 0, start_bit = 1, recv_data = 2, check_parity = 3, 
                          check_first_stop = 4, check_sec_stop= 5, done = 6} state_type;
  state_type state=idle,next_state=idle;
  
  always@(posedge rx_clk)begin
    if(rst)begin
      state<=idle;
    end else begin
      state<=next_state;
    end
  end
  
  always@(*)begin
    case(state)
      idle:begin
        rx_done=0;
        rx_error=0;
        if(rx_start && !rx)begin
          next_state=start_bit;
        end else begin
          next_state=idle;
        end
      end
      start_bit:begin
        if(count==7 && rx)begin
          next_state=idle;
        end else if(count==15)begin
          next_state=recv_data;
        end else begin
          next_state=start_bit;
        end
      end
      recv_data:begin
        if(count==7)begin
          data_rd[7:0]={rx,data_rd[7:1]};
        end else if(count==15 && bit_count==(length-1))begin
          case(length)
            5: rx_out = data_rd[7:3];
            6: rx_out = data_rd[7:2];
            7: rx_out = data_rd[7:1];
            8: rx_out = data_rd[7:0];
            default : rx_out = 8'h00;
          endcase
          
          if(parity_type)begin
            parity = ^data_rd;
          end else begin
            parity = ~^data_rd;
          end
          if(parity_en)begin
            next_state=check_parity;
          end else begin
            next_state=check_first_stop;
          end
        end else begin
          next_state=recv_data;
        end
      end
      check_parity:begin
        if(count==7)begin
          if(rx==parity)begin
            rx_error=1'b0;
          end else begin
            rx_error = 1'b1;
          end
        end else if(count==15)begin
          next_state=check_first_stop;
        end else begin
          next_state=check_parity;
        end
      end
      check_first_stop:begin
        if(count==7)begin
          if(rx!=1'b1)begin
            rx_error=1'b1;
          end else begin
            rx_error=1'b0;
          end
        end else if(count==15)begin
          if(stop2)begin
            next_state=check_sec_stop;
          end else begin
            next_state=done;
          end
        end
      end
      check_sec_stop:begin
        if(count==7)begin
          if(rx!=1'b1)begin
            rx_error=1'b1;
          end else begin
            rx_error=1'b0;
          end
        end else if(count==15)begin
          next_state=done;
        end
      end
      done:begin
        rx_done = 1'b1;
        next_state = idle;
        rx_error = 1'b0;
      end
      default:begin
      end
    endcase
  end
  
  always@(posedge rx_clk)begin
    case(state)
      idle:begin
        count     <= 0;
         bit_count <= 0;
      end
      start_bit: begin
        if(count < 15) begin
              count <= count + 1;
        end else begin
              count <= 0;
        end
       end
      recv_data: begin
        if(count < 15) begin
          count <= count + 1;
        end else begin
          count <= 0;
          bit_count <= bit_count + 1;
        end
       end
      check_parity: begin
        if(count < 15) begin
              count <= count + 1;
        end else begin
              count <= 0;
        end
       end
      check_first_stop : begin
        if(count < 15) begin
              count <= count + 1;
        end else begin
              count <= 0;
        end
       end
      check_sec_stop : begin
        if(count < 15) begin
              count <= count + 1;
        end else begin
              count <= 0;
        end
       end
      done :  begin
           count <= 0;
           bit_count <= 0;
        end 
    endcase
  end
  
endmodule


 
