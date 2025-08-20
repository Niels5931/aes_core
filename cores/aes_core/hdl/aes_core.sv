module aes_core #(
    parameter CORENUM = 0
) (
    input logic clk_i,
    input logic rst_ni,
    input logic [127:0] data_in,
    input logic [127:0] key_in,
    output logic [127:0] data_out
);


    logic [127:0] subbytes_out;
    logic [127:0] shiftrows_out;
    logic [31:0] mixcolumns_out [0:3];
    logic [127:0] addkey_out;

    generate
        if (CORENUM == 0) begin
            addkey addkey_core_0_i(
                .data_in(data_in),
                .key_in(key_in),
                .data_out(data_out)
            );
        end else if (CORENUM == 9) begin
            subbyte subbyte_core_9_i(
                .data_in(data_in),
                .data_out(subbytes_out)
            );
            shiftrow shiftrow_core_9_i (
                .data_in(subbytes_out),
                .data_out(shiftrows_out)
            );
            assign data_out = shiftrows_out ^ key_in;
        end else begin
            subbyte subbyte_core_i(
                .data_in(data_in),
                .data_out(subbytes_out)
            );
            shiftrow shiftrow_core_i (
                .data_in(subbytes_out),
                .data_out(shiftrows_out)
            );
            for (genvar i = 0; i < 4; i=i+1) begin : gen_mixcolumns
                mixcolumns mixcolumn_core_i(
                    .data_in(shiftrows_out[i*32 +: 32]),
                    .data_out(mixcolumns_out[i])
                );
            end : gen_mixcolumns
            addkey addkey_core_i(
                .data_in({mixcolumns_out[3], mixcolumns_out[2], mixcolumns_out[1], mixcolumns_out[0]}),
                .key_in(key_in),
                .data_out(data_out)
            );
        end     
    endgenerate
endmodule