#include <systemc.h>
#include "barrel_shift.h"
#include "alu.h"




int main(int argc,char* argv[]){

	sc_signal<sc_int<8>> a,b,shift_out,alu_result;
	sc_signal<bool> op,enable,l_r_en,exe;

	sc_signal<sc_int<3>>amt;
	sc_trace_file *tf;
	sc_clock  clk("clk",10,SC_NS,0.5);

	alu DUT_a1("DUT_a1");
	barrel_shift DUT_b1("DUT_b1");
	tf = sc_create_vcd_trace_file("trace_file_lab1");
	tf->set_time_unit(1, SC_NS);
	sc_trace(tf, clk, "clk");
	    sc_trace(tf, shift_out, "shift_out");
	    sc_trace(tf, op, "op");
	    sc_trace(tf, exe, "exe");
	    sc_trace(tf, a, "a");
	    sc_trace(tf, b, "b");
	    sc_trace(tf, enable, "enable");
	    sc_trace(tf, l_r_en, "l_r_en");
	    sc_trace(tf, amt, "amt");
	    sc_trace(tf, alu_result, "alu_result");

	    cout << "\nExecuting ALU, check .vcd file in GTKWave\n" << endl;

	DUT_b1.CLK(clk);
    DUT_b1.EN(enable);
    DUT_b1.L_R(l_r_en);
    DUT_b1.B_in(b);
    DUT_b1.OUT(shift_out);
    DUT_b1.amt(amt);


    DUT_a1.CLK(clk);
    DUT_a1.OP(op);
    DUT_a1.A(a);
    DUT_a1.B(shift_out);
    DUT_a1.OUT(alu_result);







    // Start testbench, initialize first
    // op         | 0 = sub, 1 = add
    // a_in       | 8-bit integer
    // b_in       | 8-bit integer
    // enable     | 0 = barrelshifter off, 1 = barrelshifter on
    // left_right | 0 = shift left, 1 = shift right


    b.write(2);
    enable.write(1);
    l_r_en.write(0);
    amt.write(1);
    sc_start(10, SC_NS);
    op.write(0);
    a.write(0);

    // Test addition with left shift | 2 + (3<<1) = 8

    b.write(3);
    enable.write(1);
    l_r_en.write(0);
    amt.write(1);
    sc_start(10, SC_NS);
    op.write(1);
    a.write(2);
    // Test subtraction with right shift | 9 - (8>>2) = 7

    b.write(8);
    enable.write(1);
    l_r_en.write(1);
    amt.write(2);
    sc_start(10, SC_NS);
    op.write(0);
    a.write(9);
    // Test above case with enable = 0

    b.write(8);
    enable.write(0);
    l_r_en.write(1);
    amt.write(2);
    sc_start(10, SC_NS);
    op.write(0);
    a.write(9);
    // Test above case with shift_amt = 0

    b.write(8);
    enable.write(1);
    l_r_en.write(1);
    amt.write(0);
    sc_start(10, SC_NS);
    op.write(0);
    a.write(9);
    // Test addition with right shift 8 | 7 + (96>>8) = 7

    b.write(96);
    enable.write(1);
    l_r_en.write(1);
    amt.write(8);
    sc_start(10, SC_NS);
    op.write(1);
    a.write(7);
    // Test addition with bs disabled | 14 + 86 = 100

    b.write(86);
    enable.write(0);
    l_r_en.write(1);
    amt.write(8);
    sc_start(10, SC_NS);
    op.write(1);
    a.write(14);

    sc_start(10, SC_NS);
    sc_close_vcd_trace_file(tf);

	return 0;
}
