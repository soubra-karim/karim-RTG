// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See VSOC.h for the primary calling header

#include "VSOC__pch.h"
#include "VSOC__Syms.h"
#include "VSOC___024root.h"

#ifdef VL_DEBUG
VL_ATTR_COLD void VSOC___024root___dump_triggers__stl(VSOC___024root* vlSelf);
#endif  // VL_DEBUG

VL_ATTR_COLD void VSOC___024root___eval_triggers__stl(VSOC___024root* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    VSOC__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    VSOC___024root___eval_triggers__stl\n"); );
    // Body
    vlSelf->__VstlTriggered.set(0U, (IData)(vlSelf->__VstlFirstIteration));
#ifdef VL_DEBUG
    if (VL_UNLIKELY(vlSymsp->_vm_contextp__->debug())) {
        VSOC___024root___dump_triggers__stl(vlSelf);
    }
#endif
}
