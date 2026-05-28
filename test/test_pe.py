import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles, RisingEdge

@cocotb.test()
async def test_pe_basic(dut):
    clock = Clock(dut.clk, 10, units="ns")
    cocotb.start_soon(clock.start())

    dut.reset_n.value = 0
    dut.en.value = 0
    dut.clear.value = 0
    dut.a_in.value = 0
    dut.weight_in.value = 0
    await ClockCycles(dut.clk, 5)

    dut.reset_n.value = 1
    await ClockCycles(dut.clk, 2)

    # test 2x3 = 6
    dut.a_in.value = 2
    dut.weight_in.value = 3
    dut.en.value = 1
    await RisingEdge(dut.clk)
    await RisingEdge(dut.clk)
    assert dut.acc.value == 6, f"Expected 6, got {dut.acc.value}"

    # accumulate again: 6+6=12
    await RisingEdge(dut.clk)
    assert dut.acc.value == 12, f"Expected 12, got {dut.acc.value}"

    # test clear
    dut.clear.value = 1
    await RisingEdge(dut.clk)
    await RisingEdge(dut.clk)
    assert dut.acc.value == 0, f"Expected 0 after clear, got {dut.acc.value}"

    # test passthrough
    assert dut.a_next.value == 2, f"Expected a_next=2, got {dut.a_next.value}"
    assert dut.weight_next.value == 3, f"Expected weight_next=3, got {dut.weight_next.value}"

    # test -2 x -5 = 10
    dut.clear.value = 0
    dut.en.value = 1
    dut.a_in.value = 0b1110
    dut.weight_in.value = 0b1011
    await RisingEdge(dut.clk)
    await RisingEdge(dut.clk)
    assert dut.acc.value == 10, f"Expected 10, got {dut.acc.value}"

    # clear again
    dut.clear.value = 1
    await RisingEdge(dut.clk)
    await RisingEdge(dut.clk)
    assert dut.acc.value == 0, f"Expected 0 after clear, got {dut.acc.value}"

    # test -2 x 3 = -6
    dut.clear.value = 0
    dut.en.value = 1
    dut.a_in.value = 0b1110
    dut.weight_in.value = 3
    await RisingEdge(dut.clk)
    await RisingEdge(dut.clk)
    assert dut.acc.value.signed_integer == -6, f"Expected -6, got {dut.acc.value.signed_integer}"
