import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles, RisingEdge

def build_ui_in(data, sel, load, start):
    return (data & 0xF) << 4 | (sel & 0x3) << 2 | (load & 0x1) << 1 | (start & 0x1)

def build_uio_in(data_c2):
    return (data_c2 & 0xF) << 4

@cocotb.test()
async def test_tt_identity(dut):
    clock = Clock(dut.clk, 10, units="ns")
    cocotb.start_soon(clock.start())

    # reset
    dut.rst_n.value = 0
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    await ClockCycles(dut.clk, 5)
    dut.rst_n.value = 1
    await RisingEdge(dut.clk)

    # load sel=0: a_row0_c1=1, a_row0_c2=0
    dut.ui_in.value  = build_ui_in(data=1, sel=0, load=1, start=0)
    dut.uio_in.value = build_uio_in(data_c2=0)
    await RisingEdge(dut.clk)

    # load sel=1: a_row1_c1=0, a_row1_c2=1
    dut.ui_in.value  = build_ui_in(data=0, sel=1, load=1, start=0)
    dut.uio_in.value = build_uio_in(data_c2=1)
    await RisingEdge(dut.clk)

    # load sel=2: w_col0_c1=1, w_col0_c2=0
    dut.ui_in.value  = build_ui_in(data=1, sel=2, load=1, start=0)
    dut.uio_in.value = build_uio_in(data_c2=0)
    await RisingEdge(dut.clk)

    # load sel=3: w_col1_c1=0, w_col1_c2=1
    dut.ui_in.value  = build_ui_in(data=0, sel=3, load=1, start=0)
    dut.uio_in.value = build_uio_in(data_c2=1)
    await RisingEdge(dut.clk)

    # pulse start
    dut.ui_in.value  = build_ui_in(data=0, sel=0, load=0, start=1)
    dut.uio_in.value = 0
    await RisingEdge(dut.clk)
    dut.ui_in.value  = 0
    await RisingEdge(dut.clk)

    # wait for valid
    while dut.uio_out.value & 0x1 == 0:
        await RisingEdge(dut.clk)

    # read 4 outputs
    await RisingEdge(dut.clk)
    assert dut.uo_out.value == 1, f"Expected 1, got {dut.uo_out.value}"
    await RisingEdge(dut.clk)
    assert dut.uo_out.value == 0, f"Expected 0, got {dut.uo_out.value}"
    await RisingEdge(dut.clk)
    assert dut.uo_out.value == 0, f"Expected 0, got {dut.uo_out.value}"
    await RisingEdge(dut.clk)
    assert dut.uo_out.value == 1, f"Expected 1, got {dut.uo_out.value}"


#test 2 signed

@cocotb.test()
async def test_tt_signed(dut):
    clock = Clock(dut.clk, 10, units="ns")
    cocotb.start_soon(clock.start())

    # reset
    dut.rst_n.value = 0
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    await ClockCycles(dut.clk, 5)
    dut.rst_n.value = 1
    await RisingEdge(dut.clk)


      # load sel=0: a_row0_c1=1, a_row0_c2=0
    dut.ui_in.value  = build_ui_in(data=2, sel=0, load=1, start=0)
    dut.uio_in.value = build_uio_in(data_c2=0b1111)
    await RisingEdge(dut.clk)

    # load sel=1: a_row1_c1=0, a_row1_c2=1
    dut.ui_in.value  = build_ui_in(data=1, sel=1, load=1, start=0)
    dut.uio_in.value = build_uio_in(data_c2=3)
    await RisingEdge(dut.clk)

    # load sel=2: w_col0_c1=1, w_col0_c2=0
    dut.ui_in.value  = build_ui_in(data=3, sel=2, load=1, start=0)
    dut.uio_in.value = build_uio_in(data_c2=0b1110)
    await RisingEdge(dut.clk)

    # load sel=3: w_col1_c1=0, w_col1_c2=1
    dut.ui_in.value  = build_ui_in(data=1, sel=3, load=1, start=0)
    dut.uio_in.value = build_uio_in(data_c2=2)
    await RisingEdge(dut.clk)

    # pulse start
    dut.ui_in.value  = build_ui_in(data=0, sel=0, load=0, start=1)
    dut.uio_in.value = 0
    await RisingEdge(dut.clk)
    dut.ui_in.value  = 0
    await RisingEdge(dut.clk)

    # wait for valid
    while dut.uio_out.value & 0x1 == 0:
        await RisingEdge(dut.clk)

    # read 4 outputs
    await RisingEdge(dut.clk)
    assert dut.uo_out.value == 8, f"Expected 8, got {dut.uo_out.value}"
    await RisingEdge(dut.clk)
    assert dut.uo_out.value == 0, f"Expected 0, got {dut.uo_out.value}"
    await RisingEdge(dut.clk)
    assert dut.uo_out.value.signed_integer == -3, f"Expected -3, got {dut.uo_out.value}"
    await RisingEdge(dut.clk)
    assert dut.uo_out.value == 7, f"Expected 7, got {dut.uo_out.value}"