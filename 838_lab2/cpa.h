

#ifndef CPA_H_
#define CPA_H_

#include <systemc.h>



SC_MODULE(cpa){
	sc_in<bool> CLK;
	sc_in<sc_logic> A_IN;
	sc_in<sc_logic> B_IN;
	sc_in<sc_logic> C_IN;
	sc_out<sc_logic> S_OUT;
	sc_out<sc_logic> C_OUT;
	void cpa_process();

	SC_CTOR(cpa){
		SC_METHOD(cpa_process);
		dont_initialize();
		sensitive << CLK.pos();
	}

};




#endif /* CPA_H_ */
