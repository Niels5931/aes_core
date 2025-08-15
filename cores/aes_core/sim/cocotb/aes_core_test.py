import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge
import random as pyrandom

from numpy import random

@cocotb.test()
async def aes_basic_test(dut):
    cocotb.start_soon(Clock(dut.clk_i, 10, units='ns').start())
    cocotb.log.info("Starting AES basic test")
    dut.rst_ni.value = 0
    await RisingEdge(dut.clk_i)
    await RisingEdge(dut.clk_i)
    dut.rst_ni.value = 1
    await RisingEdge(dut.clk_i)


    #data_in, key_in = aes_core_data_gen()
    dut.data_in.value = 0x19a09ae93df4c6f8e3e28d48be2b2a08
    dut.key_in.value = 0xa0fafe1788542cb123a339392a6c7605
    await RisingEdge(dut.clk_i)
    print("Sub out",hex(dut.subbytes_out.value))
    expected = aes_core_sim(dut)
    result = dut.data_out.value.integer
    assert result == expected, f"Mismatch: {hex(result)} != {hex(expected)}"

def aes_core_data_gen():
    data_in = int("".join(random.choice(['0', '1']) for _ in range(128)), 2)
    key_in = int("".join(random.choice(['0', '1']) for _ in range(128)), 2)
    return data_in, key_in

sbox = [99, 124, 119, 123, 242, 107, 111, 197, 48, 1, 103, 43, 254, 215, 171, 118, 202, 130, 201, 125, 250, 89, 71, 240, 173, 212, 162, 175, 156, 164, 114, 192, 183, 253, 147, 38, 54, 63, 247, 204, 52, 165, 229, 241, 113, 216, 49, 21, 4, 199, 35, 195, 24, 150, 5, 154, 7, 18, 128, 226, 235, 39, 178, 117, 9, 131, 44, 26, 27, 110, 90, 160, 82, 59, 214, 179, 41, 227, 47, 132, 83, 209, 0, 237, 32, 252, 177, 91, 106, 203, 190, 57, 74, 76, 88, 207, 208, 239, 170, 251, 67, 77, 51, 133, 69, 249, 2, 127, 80, 60, 159, 168, 81, 163, 64, 143, 146, 157, 56, 245, 188, 182, 218, 33, 16, 255, 243, 210, 205, 12, 19, 236, 95, 151, 68, 23, 196, 167, 126, 61, 100, 93, 25, 115, 96, 129, 79, 220, 34, 42, 144, 136, 70, 238, 184, 20, 222, 94, 11, 219, 224, 50, 58, 10, 73, 6, 36, 92, 194, 211, 172, 98, 145, 149, 228, 121, 231, 200, 55, 109, 141, 213, 78, 169, 108, 86, 244, 234, 101, 122, 174, 8, 186, 120, 37, 46, 28, 166, 180, 198, 232, 221, 116, 31, 75, 189, 139, 138, 112, 62, 181, 102, 72, 3, 246, 14, 97, 53, 87, 185, 134, 193, 29, 158, 225, 248, 152, 17, 105, 217, 142, 148, 155, 30, 135, 233, 206, 85, 40, 223, 140, 161, 137, 13, 191, 230, 66, 104, 65, 153, 45, 15, 176, 84, 187, 22]

def aes_core_sim(dut):
    if dut.CORENUM == 0:
        # test initial round
        expected = dut.data_in.value ^ dut.key_in.value
    elif dut.CORENUM == 9:
        #subbytes
        sub = [sbox[(dut.data_in.value >> (i * 8)) & 0xFF] for i in range(16)]
        #print("Python sub out", [hex(x) for x in sub])
        state = [bin(sub[i])[2:].zfill(8) for i in range(16)]
        shiftrow = state[15]+state[10]+state[5]+state[0]+state[11]+state[6]+state[1]+state[12]+state[7]+state[2]+state[13]+state[8]+state[3]+state[14]+state[9]+state[4]
        expected = int(shiftrow, 2) ^ dut.key_in.value
    else:
        # test second round
        pass
    return expected