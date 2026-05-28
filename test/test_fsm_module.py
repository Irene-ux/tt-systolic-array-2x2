import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles, RisingEdge

@cocotb.test()
async def test_fsm_module(dut):
    clock = Clock(dut.clk, 10, units="ns")
    cocotb.start_soon(clock.start())
    dut.reset_n.value = 0
    dut.start.value = 0
    await ClockCycles(dut.clk, 5)
    dut.reset_n.value = 1
    await RisingEdge(dut.clk)
    await RisingEdge(dut.clk)

    # IDLE checks
    assert dut.en.value == 0, f"Expected en=0, got {dut.en.value}"
    assert dut.valid.value == 0, f"Expected valid=0, got {dut.valid.value}"
    assert dut.clear.value == 0, f"Expected clear=0, got {dut.clear.value}"

      # pulse start
    dut.start.value = 1
    await RisingEdge(dut.clk)
    dut.start.value = 0
    await RisingEdge(dut.clk)

    # COMPUTE cycle 1
    assert dut.en.value == 1, f"COMPUTE1 en={dut.en.value}"
    await RisingEdge(dut.clk)

    # COMPUTE cycle 2
    assert dut.en.value == 1, f"COMPUTE2 en={dut.en.value}"
    await RisingEdge(dut.clk)

    # DRAIN cycle 1
    assert dut.en.value == 1, f"DRAIN1 en={dut.en.value}"
    assert dut.valid.value == 0, f"DRAIN1 valid={dut.valid.value}"
    await RisingEdge(dut.clk)
    await RisingEdge(dut.clk)

    # DRAIN cycle 2
    assert dut.en.value == 0, f"DRAIN2 en={dut.en.value}"
    assert dut.valid.value == 1, f"DRAIN2 valid={dut.valid.value}"
    await RisingEdge(dut.clk)

    # READ cycle 1
    assert dut.valid.value == 1, f"READ1 valid={dut.valid.value}"
    assert dut.clear.value == 0, f"READ1 clear={dut.clear.value}"
    await RisingEdge(dut.clk)

    # READ cycle 2
    assert dut.valid.value == 1, f"READ2 valid={dut.valid.value}"
    assert dut.clear.value == 0, f"READ2 clear={dut.clear.value}"
    await RisingEdge(dut.clk)

    # READ cycle 3
    assert dut.valid.value == 1, f"READ3 valid={dut.valid.value}"
    assert dut.clear.value == 0, f"READ3 clear={dut.clear.value}"
    await RisingEdge(dut.clk)

    # READ cycle 4 — clear→1, valid→0
    assert dut.valid.value == 0, f"READ4 valid={dut.valid.value}"
    assert dut.clear.value == 1, f"READ4 clear={dut.clear.value}"
    
