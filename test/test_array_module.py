import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles, RisingEdge

@cocotb.test()
async def test_array_module(dut):
    clock = Clock(dut.clk, 10, units="ns")
    cocotb.start_soon(clock.start())

    dut.reset_n.value = 0
    dut.en.value = 0
    dut.a_row0.value = 0
    dut.a_row1.value = 0
    dut.weight_col0.value = 0
    dut.weight_col1.value = 0
    await ClockCycles(dut.clk, 5)

    dut.reset_n.value = 1
    await RisingEdge(dut.clk)

    #inputs
    dut.en.value = 1
    dut.a_row0.value = 1
    dut.a_row1.value = 0
    dut.weight_col0.value = 1
    dut.weight_col1.value = 0

    await RisingEdge(dut.clk)

    #next cycle
    dut.a_row0.value = 0
    dut.a_row1.value = 1
    dut.weight_col0.value = 0
    dut.weight_col1.value = 1

    await RisingEdge(dut.clk)
    dut.a_row0.value = 0
    dut.a_row1.value = 0
    dut.weight_col0.value = 0
    dut.weight_col1.value = 0
    await RisingEdge(dut.clk)
    await RisingEdge(dut.clk)
    await RisingEdge(dut.clk)

    dut.en.value = 0
    
    assert dut.acc_00.value == 1, f"Expected acc_00 to be 1, got {dut.acc_00.value}"

    assert dut.acc_01.value == 0, f"Expected acc_01 to be 0, got {dut.acc_01.value}"
    assert dut.acc_10.value == 0, f"Expected acc_10 to be 0, got {dut.acc_10.value}"


    assert dut.acc_11.value == 1, f"Expected acc_11 to be 1, got {dut.acc_11.value}"
