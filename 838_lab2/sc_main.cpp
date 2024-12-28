/*
 * sc_main.cpp
 *
 *  Created on: Dec 28, 2024
 *      Author: KKS
 */




#include <systemc.h>
#include <random>
#include "csa.h"
#include "cpa.h"
sc_logic my_func() {
	int r = rand() % 2;
    switch(r) {
        case 0:  return SC_LOGIC_0; // '0'
        case 1:  return SC_LOGIC_1; // '1'
        default: return SC_LOGIC_1; // 'Z'
    }
}

int main(int argc,char* argv[]){
	//input and output
	int i;
	sc_signal<sc_logic> a[4];
	sc_signal<sc_logic> b[4];
	sc_signal<sc_logic> cin[4];
	sc_signal<sc_logic> sin[4];
	sc_signal<sc_logic> product[8];
	sc_signal<sc_logic> final_product[8];
	sc_signal<sc_logic> zero;
	//
	zero.write(SC_LOGIC_0);
	sc_signal<sc_logic>  output_co_r1[4];
	sc_signal<sc_logic>  output_co_r2[4];
	sc_signal<sc_logic>  output_co_r3[4];
	sc_signal<sc_logic>  output_co_r4[4];
	sc_signal<sc_logic>  output_co_r5[4];
	sc_signal<sc_logic> output_so_r1[4];
	sc_signal<sc_logic>  output_so_r2[4];
	sc_signal<sc_logic>  output_so_r3[4];
	sc_signal<sc_logic>  output_so_r4[4];




	sc_vector<csa> csa_r1("csa_r1",4);
	sc_vector<csa> csa_r2("csa_r2",4);
	sc_vector<csa> csa_r3("csa_r3",4);
	sc_vector<csa> csa_r4("csa_r4",4);
	sc_vector<cpa> cpa_r5("cpa_r5",4);
	// intermediate signals
	sc_clock  clk("clk",10,SC_NS,0.5);
	sc_trace_file *tf;
	tf = sc_create_vcd_trace_file("trace_file_lab2_multiplier");
		tf->set_time_unit(1, SC_NS);
		sc_trace(tf, clk, "clk");
		sc_trace(tf, a[0], "a0");
		sc_trace(tf, a[1], "a1");
		sc_trace(tf, a[2], "a2");
		sc_trace(tf, a[3], "a3");
		sc_trace(tf, b[0], "b0");
		sc_trace(tf, b[1], "b1");
		sc_trace(tf, b[2], "b2");
		sc_trace(tf, b[3], "b3");
		sc_trace(tf, product[0], "product0");
		sc_trace(tf, product[1], "product1");
		sc_trace(tf, product[2], "product2");
		sc_trace(tf, product[3], "product3");
		sc_trace(tf, product[4], "product4");
		sc_trace(tf, product[5], "product5");
		sc_trace(tf, product[6], "product6");
		sc_trace(tf, product[7], "product7");
		sc_trace(tf, final_product[0], "final_product0");
		sc_trace(tf, final_product[1], "final_product1");
		sc_trace(tf, final_product[2], "final_product2");
		sc_trace(tf, final_product[3], "final_product3");
		sc_trace(tf, final_product[4], "final_product4");
		sc_trace(tf, final_product[5], "final_product5");
		sc_trace(tf, final_product[6], "final_product6");
		sc_trace(tf, final_product[7], "final_product7");

		//row1 setup
	for(i=0;i<4;i++){

		csa_r1[i].CLK(clk);
		csa_r1[i].A_IN(a[i]);
		csa_r1[i].B_IN(b[0]);
		csa_r1[i].C_IN(cin[i]); //cin =0
		csa_r1[i].S_IN(sin[i]); //sin = 0

		csa_r1[i].C_OUT(output_co_r1[i]);
		if(i==0){

			csa_r1[i].S_OUT(product[0]);

		} else {
			csa_r1[i].S_OUT(output_so_r1[i]);
		}
	}


	//row2 setup
	for(i=0;i<4;i++){

		csa_r2[i].CLK(clk);
		csa_r2[i].A_IN(a[i]);
		csa_r2[i].B_IN(b[1]);
		csa_r2[i].C_IN(output_co_r1[i]);

		if(i<3){
			csa_r2[i].S_IN(output_so_r1[i+1]);
		} else if(i==3) {
			csa_r2[i].S_IN(zero);
		}


		csa_r2[i].C_OUT(output_co_r2[i]);
		if(i==0){

			csa_r2[i].S_OUT(product[1]);

		} else{
			csa_r2[i].S_OUT(output_so_r2[i]);
		}
	}
	//row3 setup
	for(i=0;i<4;i++){

		csa_r3[i].CLK(clk);
		csa_r3[i].A_IN(a[i]);
		csa_r3[i].B_IN(b[2]);
		csa_r3[i].C_IN(output_co_r2[i]);

		if(i<3){
			csa_r3[i].S_IN(output_so_r2[i+1]);
		} else {
			csa_r3[i].S_IN(zero);
		}


		csa_r3[i].C_OUT(output_co_r3[i]);
		if(i==0){

			csa_r3[i].S_OUT(product[2]);

		} else {
			csa_r3[i].S_OUT(output_so_r3[i]);
		}
	}
	//row4 setup
	for(i=0;i<4;i++){

		csa_r4[i].CLK(clk);
		csa_r4[i].A_IN(a[i]);
		csa_r4[i].B_IN(b[3]);
		csa_r4[i].C_IN(output_co_r3[i]);

		if(i+1<4){
			csa_r4[i].S_IN(output_so_r3[i+1]);
		} else {
			csa_r4[i].S_IN(zero);
		}


		csa_r4[i].C_OUT(output_co_r4[i]);
		if(i==0){

			csa_r4[i].S_OUT(product[3]);

		} else {
			csa_r4[i].S_OUT(output_so_r4[i]);
		}
	}
	//row5 setup
	for(i=0;i<4;i++){

		cpa_r5[i].CLK(clk);


		if(i==3){
			cpa_r5[i].A_IN(output_co_r4[i]);
			cpa_r5[i].B_IN(output_co_r5[i-1]);
		} else {
			cpa_r5[i].A_IN(output_so_r4[i+1]);
			cpa_r5[i].B_IN(output_co_r4[i]);
		}
		if(i==0 || i==3){
			cpa_r5[i].C_IN(zero);
		} else {
			cpa_r5[i].C_IN(output_co_r5[i-1]);
		}
		cpa_r5[i].S_OUT(product[i+4]);


		cpa_r5[i].C_OUT(output_co_r5[i]);



	}



	for (i = 0; i < 4; ++i) {
		cin[i].write(SC_LOGIC_0);
		sin[i].write(SC_LOGIC_0);
	     a[i].write(my_func());
	     b[i].write(my_func());
	}

	sc_start(65, SC_NS);
	for(int x=0;x<8;x++){
		final_product[x].write(product[x]);
	}
	for (i = 0; i < 4; ++i) {
		     a[i].write(my_func());
		     b[i].write(my_func());
	}
	sc_start(65, SC_NS);
	for(int x=0;x<8;x++){
			final_product[x].write(product[x]);
	}
	for(int x=0;x<8;x++){
			final_product[x].write(product[x]);
	}

	sc_start(100, SC_NS);
	sc_close_vcd_trace_file(tf);
	return 0;

}
