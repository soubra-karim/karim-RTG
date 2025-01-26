
#ifndef ALU_H_
#define ALU_H_

#include <systemc.h>

SC_MODULE(alu){
	sc_in<bool> CLK;
	//sc_in<bool> START;
	sc_in<bool> OP;
	sc_in<sc_int<8>> A;
	sc_in<sc_int<8>> B;
	sc_out<sc_int<8>> OUT;

	//0 -> subtract
	//1 -> add
	void alu_process();

	SC_CTOR(alu){
		SC_METHOD(alu_process);
		dont_initialize();
		sensitive << CLK.pos();
	}


};




#endif /* ALU_H_ */
