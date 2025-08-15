module addkey (
    input logic [127:0] data_in,
    input logic [127:0] key_in,
    output logic [127:0] data_out
);

    assign data_out = data_in ^ key_in;
    
endmodule