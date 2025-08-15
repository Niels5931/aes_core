module shiftrow (
    input logic [127:0] data_in,
    output logic [127:0] data_out
);

    logic [7:0] state [0:15];

    always_comb begin
        for (int i = 0; i < 16; i++) begin
            state[i] = data_in[i * 8 + 7 -: 8];
        end
    end

    assign data_out[127-:32] = {state[15], state[10], state[5], state[0]};
    assign data_out[95-:32] = {state[11], state[6], state[1], state[12]};
    assign data_out[63-:32] = {state[7], state[2], state[13], state[8]};
    assign data_out[31-:32] = {state[3], state[14], state[9], state[4]};

endmodule