import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles, RisingEdge, FallingEdge

@cocotb.test()
async def test_systolic_array_identity(dut):
    clock = Clock(dut.clk, 10, units="ns")
    cocotb.start_soon(clock.start())

    # reset
    dut.reset_n.value = 0
    dut.start.value = 0
    dut.a_row0.value = 0
    dut.a_row1.value = 0
    dut.weight_col0.value = 0
    dut.weight_col1.value = 0
    await ClockCycles(dut.clk, 5)
    dut.reset_n.value = 1
    await RisingEdge(dut.clk)

    # pulse start
    dut.start.value = 1
    await RisingEdge(dut.clk)
    dut.start.value = 0

    # cycle 1 inputs
    dut.a_row0.value = 1
    dut.a_row1.value = 0
    dut.weight_col0.value = 1
    dut.weight_col1.value = 0
    await RisingEdge(dut.clk)

    # cycle 2 inputs
    dut.a_row0.value = 0
    dut.a_row1.value = 1
    dut.weight_col0.value = 0
    dut.weight_col1.value = 1
    await RisingEdge(dut.clk)

    # cycle 3 — drain
    dut.a_row0.value = 0
    dut.a_row1.value = 0
    dut.weight_col0.value = 0
    dut.weight_col1.value = 0
    await RisingEdge(dut.clk)

    # wait for valid
    while dut.valid.value == 0:
        await RisingEdge(dut.clk)

    # read 4 outputs
    await RisingEdge(dut.clk)
    assert dut.data_out.value == 1
    await RisingEdge(dut.clk)
    assert dut.data_out.value == 0
    await RisingEdge(dut.clk)
    assert dut.data_out.value == 0
    await RisingEdge(dut.clk)
    assert dut.data_out.value == 1


#test 2
@cocotb.test()
async def test_systolic_array_signed(dut):
    clock = Clock(dut.clk, 10, units="ns")
    cocotb.start_soon(clock.start())

    # reset
    dut.reset_n.value = 0
    dut.start.value = 0
    dut.a_row0.value = 0
    dut.a_row1.value = 0
    dut.weight_col0.value = 0
    dut.weight_col1.value = 0
    await ClockCycles(dut.clk, 5)
    dut.reset_n.value = 1
    await RisingEdge(dut.clk)

    # pulse start
    dut.start.value = 1
    await RisingEdge(dut.clk)
    dut.start.value = 0


 # cycle 1 inputs
    dut.a_row0.value = 2
    dut.a_row1.value = 1
    dut.weight_col0.value = 3
    dut.weight_col1.value = 1
    await RisingEdge(dut.clk)

    # cycle 2 inputs
    dut.a_row0.value = 0b1111
    dut.a_row1.value = 3
    dut.weight_col0.value = 0b1110
    dut.weight_col1.value = 2
    await RisingEdge(dut.clk)

    # cycle 3 — drain
    dut.a_row0.value = 0
    dut.a_row1.value = 0
    dut.weight_col0.value = 0
    dut.weight_col1.value = 0
    await RisingEdge(dut.clk)

    # wait for valid
    while dut.valid.value == 0:
        await RisingEdge(dut.clk)

    # read 4 outputs
    await RisingEdge(dut.clk)
    assert dut.data_out.value == 8
    await RisingEdge(dut.clk)
    assert dut.data_out.value == 0
    await RisingEdge(dut.clk)
    assert dut.data_out.value.signed_integer ==-3, f"Expected -3, got {dut.data_out.value.signed_integer}"
    await RisingEdge(dut.clk)
    assert dut.data_out.value == 7
