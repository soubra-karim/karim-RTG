/*
 * csa.cpp
 *
 *  Created on: Dec 28, 2024
 *      Author: KKS
 */




#include "csa.h"

void csa::csa_process(){
	sc_logic ab,cin,sin;

	ab=A_IN.read() & B_IN.read();
	sin=S_IN.read();
	cin=C_IN.read();
	S_OUT.write(ab ^ sin ^ cin);

	C_OUT.write((ab&sin)|(sin&cin)|(ab&cin));
}
