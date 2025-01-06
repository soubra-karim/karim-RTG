// main.cpp
#include "systemc.h"
#include <iostream>
#include <stdlib.h>
#include <stdio.h>
#include "packet.h"
#include "source.h"
#include "sink.h"
#include "router.h"


int sc_main(int argc, char *argv[])
{
	sc_signal<sc_uint<4> >  id[16],dest[16];
	sc_signal<bool>en[16];
	for(int i=0;i<16;i++){
		id[i].write(i);
		en[i].write(0);
		cout<<i<< endl;
	}
	
	sc_signal<packet> outN[16],outE[16],outS[16],outW[16],insrc0[16],outsink[16],inzero[100];
	sc_signal<bool> ackoutN[16],ackoutE[16],ackoutS[16],ackoutW[16],outack_insrc0[16],inack_sink[16],ackinzero[100];
	sc_clock s_clock("S_CLOCK", 125, SC_NS, 0.5, 0.0, SC_NS); // source clock
	sc_clock r_clock("R_CLOCK", 5, SC_NS, 0.5, 10.0, SC_NS);	// router clock
	sc_clock d_clock("D_CLOCK", 5, SC_NS, 0.5, 10.0, SC_NS);	// destination clock
	source s0("s0");
	source s1("s1");
	source s2("s2");
	source s3("s3");
	source s4("s4");
	source s5("s5");
	source s6("s6");
	source s7("s7");
	source s8("s8");
	source s9("s9");
	source s10("s10");
	source s11("s11");
	source s12("s12");
	source s13("s13");
	source s14("s14");
	source s15("s15");
	//
	sink si0("si0");
	sink si1("si1");
	sink si2("si2");
	sink si3("si3");
	sink si4("si4");
	sink si5("si5");
	sink si6("si6");
	sink si7("si7");
	sink si8("si8");
	sink si9("si9");
	sink si10("si10");
	sink si11("si11");
	sink si12("si12");
	sink si13("si13");
	sink si14("si14");
	sink si15("si15");
	
	s0(insrc0[0],id[0],outack_insrc0[0],s_clock,dest[0],en[0]);
	s1(insrc0[1],id[1],outack_insrc0[1],s_clock,dest[1],en[1]);
	s2(insrc0[2],id[2],outack_insrc0[2],s_clock,dest[2],en[2]);
	s3(insrc0[3],id[3],outack_insrc0[3],s_clock,dest[3],en[3]);
	s4(insrc0[4],id[4],outack_insrc0[4],s_clock,dest[4],en[4]);
	s5(insrc0[5],id[5],outack_insrc0[5],s_clock,dest[5],en[5]);
	s6(insrc0[6],id[6],outack_insrc0[6],s_clock,dest[6],en[6]);
	s7(insrc0[7],id[7],outack_insrc0[7],s_clock,dest[7],en[7]);
	s8(insrc0[8],id[8],outack_insrc0[8],s_clock,dest[8],en[8]);
	s9(insrc0[9],id[9],outack_insrc0[9],s_clock,dest[9],en[9]);
	s10(insrc0[10],id[10],outack_insrc0[10],s_clock,dest[10],en[10]);
	s11(insrc0[11],id[11],outack_insrc0[11],s_clock,dest[11],en[11]);
	s12(insrc0[12],id[12],outack_insrc0[12],s_clock,dest[12],en[12]);
	s13(insrc0[13],id[13],outack_insrc0[13],s_clock,dest[13],en[13]);
	s14(insrc0[14],id[14],outack_insrc0[14],s_clock,dest[14],en[14]);
	s15(insrc0[15],id[15],outack_insrc0[15],s_clock,dest[15],en[15]);
	si0(outsink[0],inack_sink[0],id[0],d_clock);//sink1(si_sink[1], si_ack_sink[1], id1, d_clock);
	si1(outsink[1],inack_sink[1],id[1],d_clock);
	si2(outsink[2],inack_sink[2],id[2],d_clock);//sink1(si_sink[1], si_ack_sink[1], id1, d_clock);
	si3(outsink[3],inack_sink[3],id[3],d_clock);
	si4(outsink[4],inack_sink[4],id[4],d_clock);//sink1(si_sink[1], si_ack_sink[1], id1, d_clock);
	si5(outsink[5],inack_sink[5],id[5],d_clock);
	si6(outsink[6],inack_sink[6],id[6],d_clock);//sink1(si_sink[1], si_ack_sink[1], id1, d_clock);
	si7(outsink[7],inack_sink[7],id[7],d_clock);
	si8(outsink[8],inack_sink[8],id[8],d_clock);//sink1(si_sink[1], si_ack_sink[1], id1, d_clock);
	si9(outsink[9],inack_sink[9],id[9],d_clock);
	si10(outsink[10],inack_sink[10],id[10],d_clock);//sink1(si_sink[1], si_ack_sink[1], id1, d_clock);
	si11(outsink[11],inack_sink[11],id[11],d_clock);
	si12(outsink[12],inack_sink[12],id[12],d_clock);//sink1(si_sink[1], si_ack_sink[1], id1, d_clock);
	si13(outsink[13],inack_sink[13],id[13],d_clock);
	si14(outsink[14],inack_sink[14],id[14],d_clock);
	si15(outsink[15],inack_sink[15],id[15],d_clock);
	router r0("r0");
	router r1("r1");
	router r2("r2");
	router r3("r3");
	router r4("r4");
	router r5("r5");
	router r6("r6");
	router r7("r7");
	router r8("r8");
	router r9("r9");
	router r10("r10");
	router r11("r11");
	router r12("r12");
	router r13("r13");	
	router r14("r14");
	router r15("r15");
	r0.rclk(r_clock);
	r1.rclk(r_clock);
	r2.rclk(r_clock);
	r3.rclk(r_clock);
	r4.rclk(r_clock);
	r5.rclk(r_clock);
	r6.rclk(r_clock);
	r7.rclk(r_clock);
	r8.rclk(r_clock);
	r9.rclk(r_clock);
	r10.rclk(r_clock);
	r11.rclk(r_clock);
	r12.rclk(r_clock);
	r13.rclk(r_clock);
	r14.rclk(r_clock);
	r15.rclk(r_clock);
	//id
	r0.router_id(id[0]);
	r1.router_id(id[1]);
	r2.router_id(id[2]);
	r3.router_id(id[3]);
	r4.router_id(id[4]);
	r5.router_id(id[5]);
	r6.router_id(id[6]);
	r7.router_id(id[7]);
	r8.router_id(id[8]);
	r9.router_id(id[9]);
	r10.router_id(id[10]);
	r11.router_id(id[11]);
	r12.router_id(id[12]);
	r13.router_id(id[13]);
	r14.router_id(id[14]);
	r15.router_id(id[15]);
	//in0
	r0.in0(insrc0[0]);
	r1.in0(insrc0[1]);
	r2.in0(insrc0[2]);
	r3.in0(insrc0[3]);
	r4.in0(insrc0[4]);
	r5.in0(insrc0[5]);
	r6.in0(insrc0[6]);
	r7.in0(insrc0[7]);
	r8.in0(insrc0[8]);
	r9.in0(insrc0[9]);
	r10.in0(insrc0[10]);
	r11.in0(insrc0[11]);
	r12.in0(insrc0[12]);
	r13.in0(insrc0[13]);
	r14.in0(insrc0[14]);
	r15.in0(insrc0[15]);
	//inack0
	r0.inack0(inack_sink[0]);
	r1.inack0(inack_sink[1]);
	r2.inack0(inack_sink[2]);
	r3.inack0(inack_sink[3]);
	r4.inack0(inack_sink[4]);
	r5.inack0(inack_sink[5]);
	r6.inack0(inack_sink[6]);
	r7.inack0(inack_sink[7]);
	r8.inack0(inack_sink[8]);
	r9.inack0(inack_sink[9]);
	r10.inack0(inack_sink[10]);
	r11.inack0(inack_sink[11]);
	r12.inack0(inack_sink[12]);
	r13.inack0(inack_sink[13]);
	r14.inack0(inack_sink[14]);
	r15.inack0(inack_sink[15]);
	//out0
	r0.out0(outsink[0]);
	r1.out0(outsink[1]);
	r2.out0(outsink[2]);
	r3.out0(outsink[3]);
	r4.out0(outsink[4]);
	r5.out0(outsink[5]);
	r6.out0(outsink[6]);
	r7.out0(outsink[7]);
	r8.out0(outsink[8]);
	r9.out0(outsink[9]);
	r10.out0(outsink[10]);
	r11.out0(outsink[11]);
	r12.out0(outsink[12]);
	r13.out0(outsink[13]);
	r14.out0(outsink[14]);
	r15.out0(outsink[15]);
	//outack0
	r0.outack0(outack_insrc0[0]);
	r1.outack0(outack_insrc0[1]);
	r2.outack0(outack_insrc0[2]);
	r3.outack0(outack_insrc0[3]);
	r4.outack0(outack_insrc0[4]);
	r5.outack0(outack_insrc0[5]);
	r6.outack0(outack_insrc0[6]);
	r7.outack0(outack_insrc0[7]);
	r8.outack0(outack_insrc0[8]);
	r9.outack0(outack_insrc0[9]);
	r10.outack0(outack_insrc0[10]);
	r11.outack0(outack_insrc0[11]);
	r12.outack0(outack_insrc0[12]);
	r13.outack0(outack_insrc0[13]);
	r14.outack0(outack_insrc0[14]);
	r15.outack0(outack_insrc0[15]);
	//in1 North
	r0.in1(inzero[0]);
	r1.in1(inzero[1]);
	r2.in1(inzero[2]);
	r3.in1(inzero[3]);
	r4.in1(outS[0]);
	r5.in1(outS[1]);
	r6.in1(outS[2]);
	r7.in1(outS[3]);
	r8.in1(outS[4]);
	r9.in1(outS[5]);
	r10.in1(outS[6]);
	r11.in1(outS[7]);
	r12.in1(outS[8]);
	r13.in1(outS[9]);
	r14.in1(outS[10]);
	r15.in1(outS[11]);
	//inack1 North
	r0.inack1(ackinzero[0]);
	r1.inack1(ackinzero[1]);
	r2.inack1(ackinzero[2]);
	r3.inack1(ackinzero[3]);
	r4.inack1(ackoutS[0]);
	r5.inack1(ackoutS[1]);
	r6.inack1(ackoutS[2]);
	r7.inack1(ackoutS[3]);
	r8.inack1(ackoutS[4]);
	r9.inack1(ackoutS[5]);
	r10.inack1(ackoutS[6]);
	r11.inack1(ackoutS[7]);
	r12.inack1(ackoutS[8]);
	r13.inack1(ackoutS[9]);
	r14.inack1(ackoutS[10]);
	r15.inack1(ackoutS[11]);
	//in2 East
	r0.in2(outW[1]);
	r1.in2(outW[2]);
	r2.in2(outW[3]);
	r3.in2(inzero[4]);
	r4.in2(outW[5]);
	r5.in2(outW[6]);
	r6.in2(outW[7]);
	r7.in2(inzero[5]);
	r8.in2(outW[9]);
	r9.in2(outW[10]);
	r10.in2(outW[11]);
	r11.in2(inzero[6]);
	r12.in2(outW[13]);
	r13.in2(outW[14]);
	r14.in2(outW[15]);
	r15.in2(inzero[7]);
	//inack2 East
	r0.inack2(ackoutW[1]);
	r1.inack2(ackoutW[2]);
	r2.inack2(ackoutW[3]);
	r3.inack2(ackinzero[4]);
	r4.inack2(ackoutW[5]);
	r5.inack2(ackoutW[6]);
	r6.inack2(ackoutW[7]);
	r7.inack2(ackinzero[5]);
	r8.inack2(ackoutW[9]);
	r9.inack2(ackoutW[10]);
	r10.inack2(ackoutW[11]);
	r11.inack2(ackinzero[6]);
	r12.inack2(ackoutW[13]);
	r13.inack2(ackoutW[14]);
	r14.inack2(ackoutW[15]);
	r15.inack2(ackinzero[7]);
	//in3 South
	r0.in3(outN[4]);
	r1.in3(outN[5]);
	r2.in3(outN[6]);
	r3.in3(outN[7]);
	r4.in3(outN[8]);
	r5.in3(outN[9]);
	r6.in3(outN[10]);
	r7.in3(outN[11]);
	r8.in3(outN[12]);
	r9.in3(outN[13]);
	r10.in3(outN[14]);
	r11.in3(outN[15]);
	r12.in3(inzero[8]);
	r13.in3(inzero[9]);
	r14.in3(inzero[10]);
	r15.in3(inzero[11]);
	//inack3 South
	r0.inack3(ackoutN[4]);
	r1.inack3(ackoutN[5]);
	r2.inack3(ackoutN[6]);
	r3.inack3(ackoutN[7]);
	r4.inack3(ackoutN[8]);
	r5.inack3(ackoutN[9]);
	r6.inack3(ackoutN[10]);
	r7.inack3(ackoutN[11]);
	r8.inack3(ackoutN[12]);
	r9.inack3(ackoutN[13]);
	r10.inack3(ackoutN[14]);
	r11.inack3(ackoutN[15]);
	r12.inack3(ackinzero[8]);
	r13.inack3(ackinzero[9]);
	r14.inack3(ackinzero[10]);
	r15.inack3(ackinzero[11]);
	//in4 West
	r0.in4(inzero[12]);
	r1.in4(outE[0]);
	r2.in4(outE[1]);
	r3.in4(outE[2]);
	r4.in4(inzero[13]);
	r5.in4(outE[4]);
	r6.in4(outE[5]);
	r7.in4(outE[6]);
	r8.in4(inzero[14]);
	r9.in4(outE[8]);
	r10.in4(outE[9]);
	r11.in4(outE[10]);
	r12.in4(inzero[15]);
	r13.in4(outE[12]);
	r14.in4(outE[13]);
	r15.in4(outE[14]);
	//inack4 West
	r0.inack4(ackinzero[12]);
	r1.inack4(ackoutE[0]);
	r2.inack4(ackoutE[1]);
	r3.inack4(ackoutE[2]);
	r4.inack4(ackinzero[13]);
	r5.inack4(ackoutE[4]);
	r6.inack4(ackoutE[5]);
	r7.inack4(ackoutE[6]);
	r8.inack4(ackinzero[14]);
	r9.inack4(ackoutE[8]);
	r10.inack4(ackoutE[9]);
	r11.inack4(ackoutE[10]);
	r12.inack4(ackinzero[15]);
	r13.inack4(ackoutE[12]);
	r14.inack4(ackoutE[13]);
	r15.inack4(ackoutE[14]);
	
	//out1 North
	r0.out1(outN[0]);
	r1.out1(outN[1]);
	r2.out1(outN[2]);
	r3.out1(outN[3]);
	r4.out1(outN[4]);
	r5.out1(outN[5]);
	r6.out1(outN[6]);
	r7.out1(outN[7]);
	r8.out1(outN[8]);
	r9.out1(outN[9]);
	r10.out1(outN[10]);
	r11.out1(outN[11]);
	r12.out1(outN[12]);
	r13.out1(outN[13]);
	r14.out1(outN[14]);
	r15.out1(outN[15]);
	//outack1 North
	r0.outack1(ackoutN[0]);
	r1.outack1(ackoutN[1]);
	r2.outack1(ackoutN[2]);
	r3.outack1(ackoutN[3]);
	r4.outack1(ackoutN[4]);
	r5.outack1(ackoutN[5]);
	r6.outack1(ackoutN[6]);
	r7.outack1(ackoutN[7]);
	r8.outack1(ackoutN[8]);
	r9.outack1(ackoutN[9]);
	r10.outack1(ackoutN[10]);
	r11.outack1(ackoutN[11]);
	r12.outack1(ackoutN[12]);
	r13.outack1(ackoutN[13]);
	r14.outack1(ackoutN[14]);
	r15.outack1(ackoutN[15]);
	//out2 East
	r0.out2(outE[0]);
	r1.out2(outE[1]);
	r2.out2(outE[2]);
	r3.out2(outE[3]);
	r4.out2(outE[4]);
	r5.out2(outE[5]);
	r6.out2(outE[6]);
	r7.out2(outE[7]);
	r8.out2(outE[8]);
	r9.out2(outE[9]);
	r10.out2(outE[10]);
	r11.out2(outE[11]);
	r12.out2(outE[12]);
	r13.out2(outE[13]);
	r14.out2(outE[14]);
	r15.out2(outE[15]);
	//outack2 East
	r0.outack2(ackoutE[0]);
	r1.outack2(ackoutE[1]);
	r2.outack2(ackoutE[2]);
	r3.outack2(ackoutE[3]);
	r4.outack2(ackoutE[4]);
	r5.outack2(ackoutE[5]);
	r6.outack2(ackoutE[6]);
	r7.outack2(ackoutE[7]);
	r8.outack2(ackoutE[8]);
	r9.outack2(ackoutE[9]);
	r10.outack2(ackoutE[10]);
	r11.outack2(ackoutE[11]);
	r12.outack2(ackoutE[12]);
	r13.outack2(ackoutE[13]);
	r14.outack2(ackoutE[14]);
	r15.outack2(ackoutE[15]);
	//out3 South
	r0.out3(outS[0]);
	r1.out3(outS[1]);
	r2.out3(outS[2]);
	r3.out3(outS[3]);
	r4.out3(outS[4]);
	r5.out3(outS[5]);
	r6.out3(outS[6]);
	r7.out3(outS[7]);
	r8.out3(outS[8]);
	r9.out3(outS[9]);
	r10.out3(outS[10]);
	r11.out3(outS[11]);
	r12.out3(outS[12]);
	r13.out3(outS[13]);
	r14.out3(outS[14]);
	r15.out3(outS[15]);
	//outack3 South
	r0.outack3(ackoutS[0]);
	r1.outack3(ackoutS[1]);
	r2.outack3(ackoutS[2]);
	r3.outack3(ackoutS[3]);
	r4.outack3(ackoutS[4]);
	r5.outack3(ackoutS[5]);
	r6.outack3(ackoutS[6]);
	r7.outack3(ackoutS[7]);
	r8.outack3(ackoutS[8]);
	r9.outack3(ackoutS[9]);
	r10.outack3(ackoutS[10]);
	r11.outack3(ackoutS[11]);
	r12.outack3(ackoutS[12]);
	r13.outack3(ackoutS[13]);
	r14.outack3(ackoutS[14]);
	r15.outack3(ackoutS[15]);
	//out4 West
	r0.out4(outW[0]);
	r1.out4(outW[1]);
	r2.out4(outW[2]);
	r3.out4(outW[3]);
	r4.out4(outW[4]);
	r5.out4(outW[5]);
	r6.out4(outW[6]);
	r7.out4(outW[7]);
	r8.out4(outW[8]);
	r9.out4(outW[9]);
	r10.out4(outW[10]);
	r11.out4(outW[11]);
	r12.out4(outW[12]);
	r13.out4(outW[13]);
	r14.out4(outW[14]);
	r15.out4(outW[15]);
	//outack4 West
	r0.outack4(ackoutW[0]);
	r1.outack4(ackoutW[1]);
	r2.outack4(ackoutW[2]);
	r3.outack4(ackoutW[3]);
	r4.outack4(ackoutW[4]);
	r5.outack4(ackoutW[5]);
	r6.outack4(ackoutW[6]);
	r7.outack4(ackoutW[7]);
	r8.outack4(ackoutW[8]);
	r9.outack4(ackoutW[9]);
	r10.outack4(ackoutW[10]);
	r11.outack4(ackoutW[11]);
	r12.outack4(ackoutW[12]);
	r13.outack4(ackoutW[13]);
	r14.outack4(ackoutW[14]);
	r15.outack4(ackoutW[15]);
	/*sc_uint<4 > d=16;
	for(int i=0;i<16;i++){
		//dest[i].write(rand()%16);
		dest[i].write(d);
		d--;
		cout<<"source"<<i<<" sending to sink"<<d<<endl;
	}*/
	int destination_id,enable;
	
	while(true){
		cout<<"enter source"<<endl;
		cin>>enable;
		cout<<"enter destination"<<endl;
		cin>>destination_id;
		dest[enable].write(destination_id);
		en[enable].write(1);
	
		//need codes
		//need codes

		cout << endl;
		cout << "-------------------------------------------------------------------------------" << endl;
		cout << endl << " 1X2 mesh NOC simulator containing 2 5x5 Wormhole router " << endl;
		cout << "-------------------------------------------------------------------------------" << endl;
		cout << "This is the simulation of a 1x2 Wormhole router.  " << endl; 
		cout << "We assume the router has 5 input/output ports, with 4 buffers per input port " << endl;
		cout << "and each flit has 21 bits width " << endl;
		cout << "  Press \"Return\" key to start the simulation..." << endl << endl;

		getchar();
		sc_start(10*125+124, SC_NS); // during [(10*125)+124] ns 10 packets will be sent and received 

		//sc_close_vcd_trace_file(tf);

		cout << endl << endl << "-------------------------------------------------------------------------------" << endl;
		cout << "End of switch operation..." << endl;
		cout << "soure0:Total number of packets sent: " <<  s0.pkt_snt<< endl;//need codes to be added
		cout << "sink0:Total number of packets received: " <<  si0.pkt_recv<< endl;//need codes to be added
		cout << "soure1:Total number of packets sent: " <<  s1.pkt_snt<< endl;//need codes to be added
		cout << "sink1:Total number of packets received: " <<  si1.pkt_recv<< endl;//need codes to be added
		cout << "source2:Total number of packets sent: " <<  s2.pkt_snt<< endl;//need codes to be added
		cout << "sink2:Total number of packets received: " <<  si2.pkt_recv<< endl;//need codes to be added
		cout << "source3:Total number of packets sent: " <<  s3.pkt_snt<< endl;//need codes to be added
		cout << "sink3:Total number of packets received: " <<  si3.pkt_recv<< endl;//need codes to be added
		cout << "source4:Total number of packets sent: " <<  s4.pkt_snt<< endl;//need codes to be added
		cout << "sink4:Total number of packets received: " <<  si4.pkt_recv<< endl;//need codes to be added
		cout << "source5:Total number of packets sent: " <<  s5.pkt_snt<< endl;//need codes to be added
		cout << "sink5:Total number of packets received: " <<  si5.pkt_recv<< endl;//need codes to be added
		cout << "source6:Total number of packets sent: " <<  s6.pkt_snt<< endl;//need codes to be added
		cout << "sink6:Total number of packets received: " <<  si6.pkt_recv<< endl;//need codes to be added
		cout << "source7:Total number of packets sent: " <<  s7.pkt_snt<< endl;//need codes to be added
		cout << "sink7:Total number of packets received: " <<  si7.pkt_recv<< endl;//need codes to be added
		cout << "source8:Total number of packets sent: " <<  s8.pkt_snt<< endl;//need codes to be added
		cout << "sink8:Total number of packets received: " <<  si8.pkt_recv<< endl;//need codes to be added
		cout << "source9:Total number of packets sent: " <<  s9.pkt_snt<< endl;//need codes to be added
		cout << "sink9:Total number of packets received: " <<  si9.pkt_recv<< endl;//need codes to be added
		cout << "source10:Total number of packets sent: " <<  s10.pkt_snt<< endl;//need codes to be added
		cout << "sink10:Total number of packets received: " <<  si10.pkt_recv<< endl;//need codes to be added
		cout << "source11:Total number of packets sent: " <<  s11.pkt_snt<< endl;//need codes to be added
		cout << "sink11:Total number of packets received: " <<  si11.pkt_recv<< endl;//need codes to be added
		cout << "source12:Total number of packets sent: " <<  s12.pkt_snt<< endl;//need codes to be added
		cout << "sink12:Total number of packets received: " <<  si12.pkt_recv<< endl;//need codes to be added
		cout << "source13:Total number of packets sent: " <<  s13.pkt_snt<< endl;//need codes to be added
		cout << "sink13:Total number of packets received: " <<  si13.pkt_recv<< endl;//need codes to be added
		cout << "source14:Total number of packets sent: " <<  s14.pkt_snt<< endl;//need codes to be added
		cout << "sink14:Total number of packets received: " <<  si14.pkt_recv<< endl;//need codes to be added
		cout << "source15:Total number of packets sent: " <<  s15.pkt_snt<< endl;//need codes to be added
		cout << "sink15:Total number of packets received: " <<  si15.pkt_recv<< endl;//need codes to be added
		cout << "-------------------------------------------------------------------------------" << endl;
		cout << "  Press \"Return\" key to end the simulation..." << endl << endl;
		en[enable].write(0);
		getchar();
	}
  return 0;

}

