


#include "cpa.h"



void cpa::cpa_process(){


	sc_logic a,b,cin;

	a=A_IN.read();
	b=B_IN.read();
	cin=C_IN.read();
	S_OUT.write(a ^ b ^ cin);

	C_OUT.write((a&b)|(b&cin)|(a&cin));
}

