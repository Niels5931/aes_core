module subbyte_tb ();
    logic [127:0] data_in;
    logic [127:0] data_out;

    subbyte dut (
        .data_in(data_in),
        .data_out(data_out)
    );

    initial begin
        data_in = 8'h53;
        #2;
        $finish;    
    end

endmodule