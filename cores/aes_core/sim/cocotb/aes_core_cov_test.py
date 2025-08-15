import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge
from cocotb_coverage.coverage import CoverPoint, coverage_db, CoverCross
import random as pyrandom

from numpy import random

data_bins = ["all_zero", "all_one", "alt_10", "alt_01", "random"]

@CoverPoint("aes.data_pattern",
            xf=lambda data: classify_pattern(data),
            bins = ["all_zero", "all_one", "alt_10", "alt_01", "random"])
def sample_data_pattern(data):
    pass

@CoverPoint("aes.key_pattern",
            xf=lambda key: classify_pattern(key),
            bins=["all_zero", "all_one", "alt_10", "alt_01", "random"])
def sample_key_pattern(key):
    pass

# check that val is between min and max of range tuple
range_relation = lambda val_, bin_ : bin_[0] <= val_ <= bin_[1]

@CoverPoint(
    "aes.input_bytes",
    xf=lambda data: bin(data).count("1"),  # total number of 1s
    rel = range_relation,
    bins=[(0,48), (49,96), (97, 128)],  # Low/mid/high Hamming weight
    bins_labels = ["low", "med", "high"],
)
def sample_input_bytes(data):
    pass

@CoverCross("aes.data_key_cross",
            items = ["aes.data_pattern", "aes.key_pattern"])
def sample_data_key_cross(data, key):
    pass

@cocotb.test()
async def aes_basic_cov_test(dut):
    cocotb.start_soon(Clock(dut.clk_i, 10, units='ns').start())
    cocotb.log.info("Starting AES basic test")
    dut.rst_ni.value = 0
    await RisingEdge(dut.clk_i)
    await RisingEdge(dut.clk_i)
    dut.rst_ni.value = 1
    await RisingEdge(dut.clk_i)

    for sim_run in range(100):
        data_in, key_in = aes_core_data_gen()
        sample_data_pattern(data_in)
        sample_key_pattern(key_in)
        sample_data_key_cross(data_in, key_in)
        sample_input_bytes(data_in)
        dut.data_in.value = data_in
        dut.key_in.value = key_in
        await RisingEdge(dut.clk_i)
        expected = aes_core_sim(dut)
        result = dut.data_out.value.integer
        assert result == expected, f"Mismatch: {hex(result)} != {hex(expected)}"

    coverage_db.report_coverage(cocotb.log.info, bins=True)
    coverage_db.export_to_yaml("aes_input_coverage.yml")

def classify_pattern(value: int) -> str:
    bin_str = format(value, '0128b')
    if all(b == '0' for b in bin_str):
        return "all_zero"
    elif all(b == '1' for b in bin_str):
        return "all_one"
    elif bin_str == "10" * 64:
        return "alt_10"
    elif bin_str == "01" * 64:
        return "alt_01"
    else:
        return "random"

def aes_core_data_gen():
    data_in_cov = coverage_db["aes.data_pattern"].detailed_coverage
    key_in_cov = coverage_db["aes.key_pattern"].detailed_coverage
    non_tested_data = [label for label, bin in data_in_cov.items() if bin == 0]
    non_tested_key = [label for label, bin in key_in_cov.items() if bin == 0]

    #print(data_in_cov)
    #print(key_in_cov)

    #print(f"Non-tested data patterns: {non_tested_data}")
    #print(f"Non-tested key patterns: {non_tested_key}")

    # Randomly select from non-tested patterns
    if non_tested_data:
        data_in = pyrandom.choice(non_tested_data)
    else:
        data_in = pyrandom.choice(data_bins)

    if non_tested_key:
        key_in = pyrandom.choice(non_tested_key)
    else:
        key_in = pyrandom.choice(data_bins)

    return gen_data_from_bin_label(data_in), gen_data_from_bin_label(key_in)

def gen_data_from_bin_label(bin_label):
    if bin_label == "all_zero":
        return 0
    elif bin_label == "all_one":
        return (1 << 128) - 1
    elif bin_label == "alt_10":
        return int("10" * 64, 2)
    elif bin_label == "alt_01":
        return int("01" * 64, 2)
    else:
        return pyrandom.randint(0, (1 << 128) - 1)

def count_bits(data):
    print(bin(data), bin(data).count("1"))
    return bin(data).count("1")

def aes_core_sim(dut):
    if dut.CORENUM == 0:
        # test initial round
        expected = dut.data_in.value ^ dut.key_in.value
    elif dut.CORENUM == 9:
        # test final round
        pass
    else:
        # test second round
        pass
    return expected