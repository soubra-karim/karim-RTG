`timescale 1ns / 1ps

module processor(
    input wire clk,
    input wire  reset
    );
 
    reg [31:0] mem_inst[0:255];
    reg [31:0] mem_data[0:255];
    reg [31:0] RegisterBank [0:31];
    //control signals
      
      
    reg [31:0] PC; 
   
    
    //FETCHH|DECODE
    reg [31:0] F_D_PC;
    reg [31:0] F_D_inst;
        //DECODE|EXECUTE
    reg [31:0] D_E_inst;
    reg [4:0] d_ex_rs1_addr;
    reg [4:0] d_ex_rs2_addr;
    reg [4:0] d_ex_shamt;
    reg [6:0] d_ex_opcode;
    reg [2:0] d_ex_funct3; 
    reg [6:0] d_ex_funct7; 
    reg [4:0] d_ex_rd_addr; 
    reg [31:0] d_ex_rs1; 
    reg [31:0] d_ex_rs2; 
    
    reg [31:0] d_ex_PC;
    reg isImm;
    
    reg [31:0] data_write;
    
    reg d_ex_isLB,d_ex_isLH,d_ex_isLW,d_ex_isLBU,d_ex_isLHU;
    reg d_ex_isSB,d_ex_isSH,d_ex_isSW;
    //      1        0      1       0          1                0             
   //     Rtype or Itype | rs2 or imm   | write mem data or alu result  | write to rf WB| MEM read    | MEM write     |  is br?   | is j ? 
    reg d_ex_reg_ret_addr, d_ex_mem_wb_result_or_data,     d_ex_wb_rf_wen, d_ex_mem_read, d_ex_mem_write, d_ex_isbr, d_ex_isj;
    

    
    
    
    
    
    /*
        d_ex_reg_ret_addr: datermines if instruction is I type or R type
        
        d_ex_alu_imm: Determines alu uses rs2 or imm
        
        d_ex_mem_wb_result_or_data: determines if to write alu result or data from data mem
        
        d_ex_wb_rf_wen: RF write 
        
        d_ex_mem_read: data mem read 
        
        
        d_ex_mem_write: data mem write
        d_ex_isbr: is branch? 
        d_ex_isj: is jump?
        
    */
    
    reg [31:0] E_M_inst;
    reg [31:0] ex_mem_alu_result;
    reg [4:0] ex_m_addr;
    reg [31:0] ex_mem_PC;
    reg ex_mem_reg_ret_addr, ex_mem_alu_imm, ex_mem_mem_wb_result_or_data,     ex_mem_wb_rf_wen, ex_mem_mem_read, ex_mem_mem_write, ex_mem_isbr, ex_mem_isj;
    reg [6:0] ex_mem_opcode;
    reg ex_mem_isLB,ex_mem_isLH,ex_mem_isLW,ex_mem_isLBU,ex_mem_isLHU;
    reg ex_mem_isSB,ex_mem_isSH,ex_mem_isSW;
    reg [31:0] ex_mem_data_write;
    reg [31:0] M_W_inst;
    reg [31:0] mem_wb_alu_result;
    reg [4:0] mem_wb_addr;
    reg [31:0] mem_wb_PC;
    reg mem_wb_reg_ret_addr, mem_wb_alu_imm, mem_wb_mem_wb_result_or_data,     mem_wb_wb_rf_wen, mem_wb_mem_read, mem_wb_mem_write, mem_wb_isbr, mem_wb_isj;
    reg [6:0] mem_wb_opcode;
    reg mem_wb_isLB,mem_wb_isLH,mem_wb_isLW,mem_wb_isLBU,mem_wb_isLHU;
    reg mem_wb_isSB,mem_wb_isSH,mem_wb_isSW;
    reg [31:0] mem_wb_data_write;
    initial begin
        {F_D_PC,D_E_inst,d_ex_rs1_addr,d_ex_rs2_addr,d_ex_opcode,d_ex_funct3,d_ex_funct7,
        d_ex_rd_addr,d_ex_rs1,d_ex_rs2,d_ex_PC,d_ex_isLB,d_ex_isLH,d_ex_isLW,d_ex_isLBU,d_ex_isLHU,isImm}=0;
        jump_taken=0;
        branch_taken=0;
        {E_M_inst,ex_mem_alu_result,ex_m_addr,ex_mem_PC,ex_mem_opcode,ex_mem_isLB,ex_mem_isLH,ex_mem_isLW,ex_mem_isLBU,ex_mem_isLHU}=0;
        {M_W_inst,mem_wb_alu_result,mem_wb_addr,mem_wb_PC,mem_wb_opcode,mem_wb_isLB,mem_wb_isLH,mem_wb_isLW,mem_wb_isLBU,mem_wb_isLHU}=0;
         PC=0;
         F_D_inst=32'b0000000_00000_11111_010_00001_0000011; //load //LW $0,x31,x1 //done
         mem_inst[0] = 32'b0000000_00000_11111_010_00001_0000011;
         mem_inst[1] = 32'b0000000_00001_00010_000_00011_0110011; // ADD x1,x2,x3
         mem_inst[2] = 32'b0000000_00011_00011_000_00111_0110011; // ADD x1,x2,x3
         mem_inst[3] = 32'b0000000_00111_00111_000_11111_0110011; // ADD x1,x2,x3
        // mem_inst[2] = 32'b0000000_00011_00000_010_00000_0100011; // store
         //mem_inst[1] = 32'b0000000_00001_01000_000_00011_0110011;
            /*
            F_D_inst=32'b0000000_00000_11111_010_01000_0000011; //load
            mem_inst[0] = 32'b0000000_00000_11111_010_01000_0000011;
            
            mem_inst[1] = 32'b0000000_00001_01000_000_00011_0110011;
            mem_inst[2] = 32'b0000000_01000_01000_000_00111_0110011; 
           
           
            mem_inst[3] = 32'b0000000_00001_00000_100_00110_1100011; //BLT
          
            
            mem_inst[4] = 32'b0000000_00001_01000_000_00011_0110011;
            mem_inst[5] = 32'b0000000_01001_01000_000_00011_0110011; 
            mem_inst[6] = 32'b0000000_01010_01000_000_00011_0110011;
            mem_inst[7] = 32'b0000000_01011_01000_000_00011_0110011; 
            //
            mem_inst[8] = 32'b0000000_11111_11111_000_00011_0110011;
            mem_inst[9] = 32'b0000000_11110_11110_000_00011_0110011;
            mem_inst[10] = 32'b0000000_11101_11101_000_00011_0110011;
            
            mem_inst[11] = 32'b0000000_11111_00000_010_00001_0000011; //load
            mem_inst[12] = 32'b0000000_00010_00001_000_11111_0110011; //add
            
            mem_inst[13] = 32'b0000000_11111_00000_010_00000_0100011; // store
            */
            
          for (integer i=0; i<32;i=i+1)begin
            RegisterBank[i]=i;
          end
          for (integer i=0; i<256;i=i+1)begin
            mem_data[i]=i;
          end
    end

    

  
    always @(posedge clk)begin
            if(reset)begin
                PC<=0;
                F_D_PC <= 0;
                F_D_inst <=32'b0000000_00000_00000_000_00000_0010011; // switch with noop
            end else if(!stall) begin 
                /// add flush and branch and stall
                PC<=PC+1;
                F_D_PC <= PC;
                F_D_inst <= mem_inst[PC];
            
            end  else begin
                F_D_PC<=F_D_PC;
                PC<=PC;
                F_D_inst<=F_D_inst;
            end
            
            if(jump_taken||branch_taken)begin
                PC<=ex_mem_alu_result;
                F_D_inst<=32'b0000000_00000_00000_000_00000_0010011;
            end
    end
    
    /*
    wire hazard_r1_em=ex_mem_wb_rf_wen && (E_M_inst[11:7]==F_D_inst[19:15]&& E_M_inst[11:7]!=0);;
    wire hazard_r1_mw=mem_wb_wb_rf_wen &&(M_W_inst[11:7]==F_D_inst[19:15]&& M_W_inst[11:7]!=0);
    wire hazard_r2_em=ex_mem_wb_rf_wen && (E_M_inst[11:7]==F_D_inst[24:20] && E_M_inst[11:7]!=0);
    wire hazard_r2_mw= mem_wb_wb_rf_wen &&(M_W_inst[11:7]==F_D_inst[24:20]&& M_W_inst[11:7]!=0);
    */
    wire hazard_r1_em= (D_E_inst[11:7]==F_D_inst[19:15]&& D_E_inst[11:7]!=0);
    wire hazard_r1_mw=(E_M_inst[11:7]==F_D_inst[19:15]&& E_M_inst[11:7]!=0);
    wire hazard_r2_em=(D_E_inst[11:7]==F_D_inst[24:20] && D_E_inst[11:7]!=0);
    wire hazard_r2_mw= (E_M_inst[11:7]==F_D_inst[24:20]&& E_M_inst[11:7]!=0);
    wire stall = (D_E_inst[6:0]==7'b0000011 ||E_M_inst[6:0]==7'b0000011 ) && (hazard_r1_em||hazard_r1_mw||hazard_r2_em||hazard_r2_mw); // stall 1 cc if load instruction
    reg isload;
    reg[31:0] branch_imm;
    reg[31:0] branch_addr;
    always @(posedge clk)begin
        // ADD STALL AND RESET LOGIC
        if(!stall && !jump_taken && !branch_taken)begin
             {d_ex_funct7,d_ex_rs2_addr,d_ex_rs1_addr,d_ex_rd_addr,d_ex_opcode}<={F_D_inst[31:25],F_D_inst[24:20],F_D_inst[19:15],F_D_inst[11:7],F_D_inst[6:0]};
             D_E_inst<=F_D_inst;
             d_ex_PC<=F_D_PC;
             d_ex_isLB<=(F_D_inst[14:12]==3'b000);
             d_ex_isLH<=(F_D_inst[14:12]==3'b001);
             d_ex_isLW<=(F_D_inst[14:12]==3'b010);
             d_ex_isLBU<=(F_D_inst[14:12]==3'b100);
             d_ex_isLHU<=(F_D_inst[14:12]==3'b101);
             d_ex_isSB<=(F_D_inst[14:12]==3'b000);
             d_ex_isSH<=(F_D_inst[14:12]==3'b001);
             d_ex_isSW<=(F_D_inst[14:12]==3'b010);
             // Forwarding logic
             d_ex_rs1<=(hazard_r1_em)? ex_mem_alu_result : (hazard_r1_mw) ? mem_wb_alu_result : RegisterBank[F_D_inst[19:15]];
             case(F_D_inst[6:0])
                7'b0010011:begin
                    // r type Imm
                    isload<=0;
                    d_ex_reg_ret_addr<=1;
                    data_write<=32'b0;
                    d_ex_mem_wb_result_or_data<=0;
                    d_ex_wb_rf_wen<=1;
                    d_ex_mem_read<=0;
                    d_ex_mem_write<=0;
                    d_ex_isbr<=0;
                    d_ex_isj<=0;
                    isImm<=1;
                    d_ex_funct3<=F_D_inst[14:12];
                    if(F_D_inst[14:12]==3'b001 ||F_D_inst[14:12]==3'b101 )begin
                        d_ex_rs2<=F_D_inst[24:20];
                    end else begin
                        d_ex_rs2<={{20{F_D_inst[31]}}, F_D_inst[31:20]};
                    end
                    
                end
                7'b0110011:begin
                                
                    // Forwarding logic
                    // r type
                    isload<=0;
                    d_ex_rs2<=(hazard_r2_em)? ex_mem_alu_result : (hazard_r2_mw) ? mem_wb_alu_result : RegisterBank[F_D_inst[24:20]];
                    isImm<=0;
                    d_ex_reg_ret_addr<=1;
                    data_write<=32'b0;
                    d_ex_mem_wb_result_or_data<=0;
                    d_ex_wb_rf_wen<=1;
                    d_ex_mem_read<=0;
                    d_ex_mem_write<=0;
                    d_ex_isbr<=0;
                    d_ex_isj<=0;
                    d_ex_funct3<=F_D_inst[14:12];
                end
                7'b0000011:begin
                    //load
                    isload<=1;
                    d_ex_reg_ret_addr<=1;
                    data_write<=32'b0;
                    isImm<=1;
                    d_ex_mem_wb_result_or_data<=1;
                    d_ex_wb_rf_wen<=1;
                    d_ex_mem_read<=1;
                    d_ex_mem_write<=0;
                    d_ex_isbr<=0;
                    d_ex_isj<=0; 
                    d_ex_rs2<={{20{F_D_inst[31]}}, F_D_inst[31:20]};
                    d_ex_funct3<=3'b000;
                end
                7'b0100011:begin
                    //store
                    isload<=0;
                    d_ex_reg_ret_addr<=1;
                    //data_write<= RegisterBank[F_D_inst[24:20]];
                    data_write<= (hazard_r2_em)? ex_mem_alu_result : (hazard_r2_mw) ? mem_wb_alu_result : RegisterBank[F_D_inst[24:20]];
                    isImm<=1;
                    d_ex_mem_wb_result_or_data<=1;
                    d_ex_wb_rf_wen<=1;
                    d_ex_mem_read<=0;
                    d_ex_mem_write<=1;
                    d_ex_isbr<=0;
                    d_ex_isj<=0; 
                    d_ex_rs2<={20'b0,F_D_inst[31:25],F_D_inst[11:7]};
                    d_ex_funct3<=3'b000;
                end
                7'b1101111:begin
                    //JAL
                    isload<=0;
                    d_ex_isj<=1;
                    d_ex_reg_ret_addr<=1;
                    data_write<=32'b0;
                    d_ex_mem_wb_result_or_data<=0;
                    d_ex_wb_rf_wen<=1;
                    d_ex_mem_read<=0;
                    d_ex_mem_write<=0;
                    d_ex_isbr<=0;
                    isImm<=0;
                    d_ex_funct3<=3'b000;
                    d_ex_rs1<=F_D_PC;
                    d_ex_rs2<={{11{F_D_inst[31]}},F_D_inst[31],F_D_inst[19:12],F_D_inst[20],F_D_inst[30:21],1'b0};
         
                end
                7'b1100111:begin
                    //JALR
                    isload<=0;
                    d_ex_isj<=1;
                    d_ex_reg_ret_addr<=1;
                    data_write<=32'b0;
                    d_ex_mem_wb_result_or_data<=0;
                    d_ex_wb_rf_wen<=1;
                    d_ex_mem_read<=0;
                    d_ex_mem_write<=0;
                    d_ex_isbr<=0;
                    isImm<=1;
                    d_ex_funct3<=3'b000;
                   // d_ex_rs1<=F_D_PC;
                    d_ex_rs2<={{20{F_D_inst[31]}}, F_D_inst[31:20]};
         
                end
                7'b1100011:begin
                    //branch
                    isload<=0;
                    d_ex_isj<=0;
                    d_ex_reg_ret_addr<=1;
                    data_write<=32'b0;
                    d_ex_mem_wb_result_or_data<=0;
                    d_ex_wb_rf_wen<=1;
                    d_ex_mem_read<=0;
                    d_ex_mem_write<=0;
                    d_ex_isbr<=1;
                    isImm<=0;
                    d_ex_funct3<=F_D_inst[14:12];
                    branch_imm<={{19{F_D_inst[31]}},F_D_inst[31],F_D_inst[7],F_D_inst[30:25],F_D_inst[11:8],1'b0};
                    d_ex_rs2<=(hazard_r2_em)? ex_mem_alu_result : (hazard_r2_mw) ? mem_wb_alu_result : RegisterBank[F_D_inst[24:20]];
         
                end
               
             endcase
        
        end  else begin
            //nop
            {d_ex_funct7,d_ex_rs2_addr,d_ex_rs1_addr,d_ex_rd_addr,d_ex_opcode}<=32'b0000000_00000_00000_000_00000_0010011;
             D_E_inst<=F_D_inst;
             d_ex_PC<=F_D_PC;
             d_ex_reg_ret_addr<=1;
             data_write<=32'b0;
             d_ex_mem_wb_result_or_data<=0;
             d_ex_wb_rf_wen<=1;
             d_ex_mem_read<=0;
             d_ex_mem_write<=0;
             d_ex_isbr<=0;
             d_ex_isj<=0;
             isImm<=1;
             d_ex_funct3<=3'b000;
             d_ex_rs2<=32'b0;
             d_ex_rs1<=32'b0;
             d_ex_isLB<=0;
             d_ex_isLH<=0;
             d_ex_isLW<=0;
             d_ex_isLBU<=0;
             d_ex_isLHU<=0;
             d_ex_isSB<=0;
             d_ex_isSH<=0;
             d_ex_isSW<=0;
        
        end

    
         
         
         
    end
    

    //EXECUTE|MEM
    reg jump_taken; //flush
    reg branch_taken;
    reg ex_mem_isload;
    always @(posedge clk)begin
    
        ex_mem_isload<=isload;
         ex_mem_PC<=d_ex_PC;
         ex_m_addr<=d_ex_rd_addr;
         ex_mem_wb_rf_wen<=d_ex_wb_rf_wen;
         ex_mem_mem_write<=d_ex_mem_write;
         ex_mem_mem_read<=d_ex_mem_read;
         ex_mem_reg_ret_addr<=d_ex_reg_ret_addr;
         ex_mem_data_write<=data_write;
         ex_mem_mem_wb_result_or_data<=d_ex_mem_wb_result_or_data;
         ex_mem_isbr<=d_ex_isbr;
         ex_mem_isj<=d_ex_isj;
         ex_mem_opcode<=d_ex_opcode;
         E_M_inst<=D_E_inst;
         ex_mem_isLB<=d_ex_isLB;
         ex_mem_isLH<=d_ex_isLH;
         ex_mem_isLW<=d_ex_isLW;
         ex_mem_isLBU<=d_ex_isLBU;
         ex_mem_isLHU<=d_ex_isLHU; 
         ex_mem_isSB<=d_ex_isSB;
         ex_mem_isSH<=d_ex_isSH;
         ex_mem_isSW<=d_ex_isSW;
         if(d_ex_isbr)begin
            ex_mem_alu_result<=d_ex_PC+branch_imm;
            case(d_ex_funct3)
                3'b000:begin
                    //BEQ
                    branch_taken <= (d_ex_rs1==d_ex_rs2) ? 1:0;
                
                end
                3'b001:begin
                    //BNE
                    branch_taken <= (d_ex_rs1!=d_ex_rs2) ? 1:0;
                end
                3'b100:begin
                    //BLT
                    branch_taken <= ($signed(d_ex_rs1)<$signed(d_ex_rs2)) ? 1:0;
                end
                3'b101:begin
                    //BGE
                    branch_taken <= ($signed(d_ex_rs1)>=$signed(d_ex_rs2)) ? 1:0;
                end
                3'b110:begin
                    //BLTU
                    branch_taken <= (d_ex_rs1<d_ex_rs2) ? 1:0;
                end
                3'b111:begin
                    //BGEU
                    branch_taken <= (d_ex_rs1>=d_ex_rs2) ? 1:0;
                end
            
            endcase
         end else begin
            
            case(d_ex_funct3)
                    3'b000:begin
                        
                       ex_mem_alu_result<=(d_ex_funct7==7'b0100000 && isImm==0)? d_ex_rs1-d_ex_rs2 : d_ex_rs1+d_ex_rs2;
                        
                    end
                    3'b001:begin
                        //SLLI or SLL
                        ex_mem_alu_result <= d_ex_rs1<<d_ex_rs2;
                    end
                    3'b010: begin
                        //slt or slti
                            ex_mem_alu_result<=($signed(d_ex_rs1)<$signed(d_ex_rs2)) ? 1 : 0; 
                    end
                    3'b011: begin
                        //sltu or sltiu
                        
                           ex_mem_alu_result<=(d_ex_rs1<d_ex_rs2) ? 1 : 0;
                        
                    end
                    3'b100: begin
                        //xor or xori
                        ex_mem_alu_result<= d_ex_rs1^d_ex_rs2;
                    end
                     3'b101: begin
                        //srli or srai or srl or sra
                        
                        
                        ex_mem_alu_result <= (d_ex_funct7==7'b0100000) ? $signed(d_ex_rs1) >> d_ex_rs2 : d_ex_rs1 >> d_ex_rs2; 
                    end
                    3'b110: begin
                        //or , ori
                        ex_mem_alu_result<=  d_ex_rs1 | d_ex_rs2;
                    end
                    3'b111: begin
                        //and , andi
                        ex_mem_alu_result<= d_ex_rs1 & d_ex_rs2;
                    end
                endcase
                if(branch_taken)begin
                    branch_taken<=0;
                end
                if(d_ex_opcode==7'b1101111 || d_ex_opcode==7'b1100111)begin
                    jump_taken<=1;
                    
                end else begin
                    jump_taken<=0;
                end
         end 
    end
     
    //MEM|WB
    
    
    //accessing data mem in this stage
    
    reg mem_wb_branch_taken;
    reg [31:0] new_data;
    reg mem_wb_isload;
    always @(posedge clk)begin
        mem_wb_isload<=ex_mem_isload;
        mem_wb_PC<=ex_mem_PC;
        mem_wb_addr<=ex_m_addr;
        mem_wb_wb_rf_wen<=ex_mem_wb_rf_wen;
        mem_wb_reg_ret_addr<=ex_mem_reg_ret_addr;
        mem_wb_alu_imm<=ex_mem_alu_imm;
        mem_wb_mem_wb_result_or_data<=ex_mem_mem_wb_result_or_data;
        mem_wb_isbr<=ex_mem_isbr;
        mem_wb_isj<=ex_mem_isj;
        mem_wb_alu_result<=ex_mem_alu_result;
        mem_wb_opcode<=ex_mem_opcode;
        M_W_inst<=E_M_inst;
        mem_wb_isLB<=ex_mem_isLB;
        mem_wb_isLH<=ex_mem_isLH;
        mem_wb_isLW<=ex_mem_isLW;
        mem_wb_isLBU<=ex_mem_isLBU;
        mem_wb_isLHU<=ex_mem_isLHU;
        mem_wb_data_write<=ex_mem_data_write;
        mem_wb_isSB<=ex_mem_isSB;
        mem_wb_isSH<=ex_mem_isSH;
        mem_wb_isSW<=ex_mem_isSW;
        mem_wb_branch_taken<=branch_taken;
        if(ex_mem_mem_read)begin
            new_data<=mem_data[ex_mem_alu_result];
        end
        
        if(ex_mem_mem_write)begin
            if(ex_mem_isSB)begin
                mem_data[ex_mem_alu_result][7:0]<=ex_mem_data_write[7:0];
            end
            if(ex_mem_isSH)begin
                mem_data[ex_mem_alu_result][15:0]<=ex_mem_data_write[15:0];
            end
            if(ex_mem_isSW)begin
                mem_data[ex_mem_alu_result]<=ex_mem_data_write;
            end
        end
    end
    
    //WB
    
    always @(posedge clk)begin
        
        
        if(mem_wb_wb_rf_wen)begin
            if(mem_wb_mem_wb_result_or_data)begin
            
                if(mem_wb_isLB && mem_wb_isload)begin
                    RegisterBank[mem_wb_addr] <=   {{24{new_data[7]}},new_data[7:0]};
                end else if(mem_wb_isLH && mem_wb_isload)begin
                   RegisterBank[mem_wb_addr] <=   {{16{new_data[15]}},new_data[15:0]};
                end else if(mem_wb_isLW && mem_wb_isload)begin
                    RegisterBank[mem_wb_addr] <=   new_data;
                end else if(mem_wb_isLBU && mem_wb_isload)begin
                    RegisterBank[mem_wb_addr] <=   {24'b0,new_data[7:0]};
                end else if(mem_wb_isLHU && mem_wb_isload)begin
                     RegisterBank[mem_wb_addr] <=   {16'b0,new_data[15:0]};
                end
                
                
            end else if(mem_wb_isj || mem_wb_branch_taken)begin
                
                RegisterBank[mem_wb_addr] <=   mem_wb_PC+1;
            end else begin
                RegisterBank[mem_wb_addr] <=   mem_wb_alu_result;
            end
            
        
        end
        
    end

    
endmodule
