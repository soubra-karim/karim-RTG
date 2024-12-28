/*
 * csa.h
 *
 *  Created on: Dec 28, 2024
 *      Author: KKS
 */

#ifndef CSA_H_
#define CSA_H_

#include <systemc.h>



SC_MODULE(csa){
	sc_in<bool> CLK;
	sc_in<sc_logic> A_IN;
	sc_in<sc_logic> B_IN;
	sc_in<sc_logic> C_IN;
	sc_in<sc_logic> S_IN;
	sc_out<sc_logic> S_OUT;
	sc_out<sc_logic> C_OUT;
	void csa_process();

	SC_CTOR(csa){
		SC_METHOD(csa_process);
		dont_initialize();
		sensitive << CLK.pos();
	}

};





#endif /* CSA_H_ */
