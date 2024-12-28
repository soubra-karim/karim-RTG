


#include "alu.h"



void alu::alu_process(){



			sc_int<8> data;

			//wait(START.posedge_event());

				cout << "op = " << OP.read() << " | a_in = " << A.read() << ", b_in = " << B.read() << ", output = ";
				if(OP.read() == 0){
					data=A.read()-B.read();
					OUT.write(A.read()-B.read());
				} else if(OP.read()==1){
					data=A.read()+B.read();
					OUT.write(A.read()+B.read());
				}
				cout << data.to_string() << "\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n" << endl;



}





