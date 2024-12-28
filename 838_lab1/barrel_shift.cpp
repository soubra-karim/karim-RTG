
#include "barrel_shift.h"



void barrel_shift::barrel_shift_process(){
			sc_int<8>data;



			//DONE.write(0);


			if(EN.read()==1){
				//amount = amt.read().to_int();
				if(L_R.read()==0){
					//shift left
					cout << "[left]  Data = " << data.to_string(SC_BIN) << endl;

					/*
					for(i = 7; i > 0; i--){
						if(i-amount>=0 && i-amount<=7){
							data[i] = B_in.read()[i-amount];
						} else {
							data[i] = 0;
						}
					}*/
				data = B_in.read() << amt.read();

				} else if(L_R.read()==1){
					//shift right
					cout << "[right] Data = " << data.to_string(SC_BIN) << endl;
					/*
					for(i = 0; i < 7; i++){//shift right
						if(i+amount<=7 && i+amount>=0){
							data[i] = B_in.read()[i+amount];
						}
					}*/

					data = B_in.read() >> amt.read();
				}
			} else {
				data=B_in.read();
			}
			//DONE.write(1);
			OUT.write(data);



}




