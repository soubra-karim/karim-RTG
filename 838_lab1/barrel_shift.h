/*
 * barrel_shift.h
 *
 *  Created on: Dec 26, 2024
 *      Author: KKS
 */

#ifndef BARREL_SHIFT_H_
#define BARREL_SHIFT_H_




#include <systemc.h>



SC_MODULE(barrel_shift){
	sc_in<sc_int<8>>B_in;
	sc_in<sc_int<3>>amt;
	sc_in<bool> EN;
	sc_in<bool> CLK;
	sc_in<bool> L_R;

	sc_out<sc_int<8>> OUT;

	//sc_out<bool> DONE;
	void barrel_shift_process();

	SC_CTOR(barrel_shift){
		SC_METHOD(barrel_shift_process);
		dont_initialize();
		sensitive << CLK.pos();
	}

};




#endif /* BARREL_SHIFT_H_ */
