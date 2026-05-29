# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0
import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles, RisingEdge

def build_ui_in(data, sel, load, start):
    return (data & 0xF) << 4 | (sel & 0x3) << 2 | (load & 0x1) << 1 | (start & 0x1)

def build_uio_in(data_c2):
    return (data_c2 & 0xF) << 4

@cocotb.test()
async def test_project(dut):
    dut._log.info("Start")
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())

    dut._log.info("Reset")
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 5)
    dut.rst_n.value = 1
    await RisingEdge(dut.clk)

    # load identity matrix A=[[1,0],[0,1]] B=[[1,0],[0,1]]
    dut.ui_in.value = build_ui_in(data=1, sel=0, load=1, start=0)
    dut.uio_in.value = build_uio_in(data_c2=0)
    await RisingEdge(dut.clk)

    dut.ui_in.value = build_ui_in(data=0, sel=1, load=1, start=0)
    dut.uio_in.value = build_uio_in(data_c2=1)
    await RisingEdge(dut.clk)

    dut.ui_in.value = build_ui_in(data=1, sel=2, load=1, start=0)
    dut.uio_in.value = build_uio_in(data_c2=0)
    await RisingEdge(dut.clk)

    dut.ui_in.value = build_ui_in(data=0, sel=3, load=1, start=0)
    dut.uio_in.value = build_uio_in(data_c2=1)
    await RisingEdge(dut.clk)

    # pulse start
    dut.ui_in.value = build_ui_in(data=0, sel=0, load=0, start=1)
    dut.uio_in.value = 0
    await RisingEdge(dut.clk)
    dut.ui_in.value = 0
    await RisingEdge(dut.clk)

    # wait for valid
    while int(dut.uio_out.value) & 0x1 == 0:
        await RisingEdge(dut.clk)

    # read 4 outputs — identity x identity = identity
    await RisingEdge(dut.clk)
    assert dut.uo_out.value == 1, f"Expected 1, got {dut.uo_out.value}"
    await RisingEdge(dut.clk)
    assert dut.uo_out.value == 0, f"Expected 0, got {dut.uo_out.value}"
    await RisingEdge(dut.clk)
    assert dut.uo_out.value == 0, f"Expected 0, got {dut.uo_out.value}"
    await RisingEdge(dut.clk)
    assert dut.uo_out.value == 1, f"Expected 1, got {dut.uo_out.value}"

    dut._log.info("PASS")
