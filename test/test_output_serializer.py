import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles, RisingEdge

@cocotb.test()
async def test_output_serializer(dut):
    clock = Clock(dut.clk, 10, units="ns")
    cocotb.start_soon(clock.start())
    dut.reset_n.value = 0
    await ClockCycles(dut.clk, 5)
    dut.reset_n.value = 1
    await RisingEdge(dut.clk)
    await RisingEdge(dut.clk)

    dut.acc_00.value = 5
    dut.acc_01.value = 2
    dut.acc_10.value = 0b11111101
    dut.acc_11.value = 64
    dut.valid.value = 1
    await RisingEdge(dut.clk)
    await RisingEdge(dut.clk)
    assert dut.data_out.value == 5, f"Expected 5, got {dut.data_out.value}"
    await RisingEdge(dut.clk)
    assert dut.data_out.value == 2, f"Expected 2, got {dut.data_out.value}"
    await RisingEdge(dut.clk)
    assert dut.data_out.value.signed_integer == -3, f"Expected -3, got {dut.data_out.value.signed_integer}"
    await RisingEdge(dut.clk)
    assert dut.data_out.value == 64, f"Expected 64, got {dut.data_out.value}"
