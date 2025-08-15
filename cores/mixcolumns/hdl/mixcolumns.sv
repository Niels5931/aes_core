function logic [7:0] xtime;
    input logic [7:0] b;
    begin
        xtime = b[7] ? (b << 1) ^ 8'h1b : b << 1;
    end
endfunction

module mixcolumns (
    input logic [31:0] data_in,
    output logic [31:0] data_out
);

    logic [7:0] state [0:3];
    logic [7:0] out_state [0:3];

    always_comb begin
        for (int i = 0; i < 4; i++) begin
            state[i] = data_in[i * 8 +: 8];
        end
    end

    always_comb begin
        out_state[3] = xtime(state[3]) ^ (xtime(state[2]) ^ state[2]) ^ state[1] ^ state[0];
        out_state[2] = state[3] ^ xtime(state[2]) ^ (xtime(state[1]) ^ state[1]) ^ state[0];
        out_state[1] = state[3] ^ state[2] ^ xtime(state[1]) ^ (xtime(state[0]) ^ state[0]);
        out_state[0] = (xtime(state[3]) ^ state[3]) ^ state[2] ^ state[1] ^ xtime(state[0]);
    end

    assign data_out = {out_state[3], out_state[2], out_state[1], out_state[0]};

endmodule