module top_module (
    input clk,
    input w, R, E, L,
    output Q
);
    reg [1:0] sel;
    assign sel={E,L};
    always @(posedge clk) begin
        
        casex(sel)
            2'b00: Q<=Q;
            2'b10 : Q<=w;
            2'bx1 : Q<=R;
        endcase
    end

endmodule
