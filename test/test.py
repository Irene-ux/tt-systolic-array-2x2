# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0
import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles, RisingEdge

def build_ui_in(data, sel, load, start):
    return (data & 0xF) << 4 | (sel & 0x3) << 2 | (load & 0x1) << 1 | (start & 0x1)

def build_uio_in(data_c2):
    return (data_c2 & 0xF) << 4

async def reset_dut(dut):
    dut.ena.value   = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 5)
    dut.rst_n.value = 1
    await RisingEdge(dut.clk)

async def load_and_compute(dut, a00, a01, a10, a11, w00, w01, w10, w11):
    """Load A and W registers, pulse start, wait for valid, return 4 signed outputs."""
    # a_row0: c1=a[0][0], c2=a[0][1]
    dut.ui_in.value  = build_ui_in(data=a00, sel=0, load=1, start=0)
    dut.uio_in.value = build_uio_in(data_c2=a01)
    await RisingEdge(dut.clk)

    # a_row1: c1=a[1][0], c2=a[1][1]
    dut.ui_in.value  = build_ui_in(data=a10, sel=1, load=1, start=0)
    dut.uio_in.value = build_uio_in(data_c2=a11)
    await RisingEdge(dut.clk)

    # w_col0: c1=w[0][0], c2=w[1][0]
    dut.ui_in.value  = build_ui_in(data=w00, sel=2, load=1, start=0)
    dut.uio_in.value = build_uio_in(data_c2=w10)
    await RisingEdge(dut.clk)

    # w_col1: c1=w[0][1], c2=w[1][1]
    dut.ui_in.value  = build_ui_in(data=w01, sel=3, load=1, start=0)
    dut.uio_in.value = build_uio_in(data_c2=w11)
    await RisingEdge(dut.clk)

    # pulse start
    dut.ui_in.value  = build_ui_in(data=0, sel=0, load=0, start=1)
    dut.uio_in.value = 0
    await RisingEdge(dut.clk)
    dut.ui_in.value  = 0
    await RisingEdge(dut.clk)

    # wait for valid
    for _ in range(50):
        if int(dut.uio_out.value) & 0x1:
            break
        await RisingEdge(dut.clk)

    # read 4 signed outputs
    results = []
    for _ in range(4):
        await RisingEdge(dut.clk)
        results.append(dut.uo_out.value.to_signed())

    return results


@cocotb.test()
async def test_identity(dut):
    """A=[[1,0],[0,1]] x W=[[1,0],[0,1]] = [[1,0],[0,1]]"""
    dut._log.info("Test 1: Identity x Identity")
    dut._log.info("A=[[1,0],[0,1]] x W=[[1,0],[0,1]] = [[1,0],[0,1]]")
    clock = Clock(dut.clk, 10, unit="us")
    cocotb.start_soon(clock.start())
    await reset_dut(dut)

    results = await load_and_compute(dut,
        a00=1, a01=0, a10=0, a11=1,
        w00=1, w01=0, w10=0, w11=1
    )

    assert results[0] == 1, f"C[0][0]: expected 1, got {results[0]}"
    assert results[1] == 0, f"C[0][1]: expected 0, got {results[1]}"
    assert results[2] == 0, f"C[1][0]: expected 0, got {results[2]}"
    assert results[3] == 1, f"C[1][1]: expected 1, got {results[3]}"
    dut._log.info("Test 1 PASS")


@cocotb.test()
async def test_general(dut):
    """A=[[1,2],[3,4]] x W=[[5,6],[7,8]] = [[19,22],[43,50]]"""
    dut._log.info("Test 2: General matrix multiply")
    dut._log.info("A=[[1,2],[3,4]] x W=[[5,6],[7,8]] = [[19,22],[43,50]]")
    clock = Clock(dut.clk, 10, unit="us")
    cocotb.start_soon(clock.start())
    await reset_dut(dut)

    # W=[[5,6],[7,8]]
    # col0=[5,7] → w00=5, w10=7
    # col1=[6,8] → w01=6, w11=8
    results = await load_and_compute(dut,
        a00=1, a01=2, a10=3, a11=4,
        w00=5, w01=6, w10=7, w11=8
    )

    assert results[0] == 19, f"C[0][0]: expected 19, got {results[0]}"
    assert results[1] == 22, f"C[0][1]: expected 22, got {results[1]}"
    assert results[2] == 43, f"C[1][0]: expected 43, got {results[2]}"
    assert results[3] == 50, f"C[1][1]: expected 50, got {results[3]}"
    dut._log.info("Test 2 PASS")


@cocotb.test()
async def test_zeros(dut):
    """A=[[0,0],[0,0]] x W=[[5,6],[7,8]] = [[0,0],[0,0]]"""
    dut._log.info("Test 3: Zero matrix")
    dut._log.info("A=[[0,0],[0,0]] x W=[[5,6],[7,8]] = [[0,0],[0,0]]")
    clock = Clock(dut.clk, 10, unit="us")
    cocotb.start_soon(clock.start())
    await reset_dut(dut)

    results = await load_and_compute(dut,
        a00=0, a01=0, a10=0, a11=0,
        w00=5, w01=6, w10=7, w11=8
    )

    for i, r in enumerate(results):
        assert r == 0, f"C[{i}]: expected 0, got {r}"
    dut._log.info("Test 3 PASS")


@cocotb.test()
async def test_negative(dut):
    """A=[[1,-1],[2,-2]] x W=[[-1,1],[-2,2]] = [[1,-1],[2,-2]]"""
    dut._log.info("Test 4: Negative values")
    dut._log.info("A=[[1,-1],[2,-2]] x W=[[-1,1],[-2,2]] = [[1,-1],[2,-2]]")
    clock = Clock(dut.clk, 10, unit="us")
    cocotb.start_soon(clock.start())
    await reset_dut(dut)

    # col0=[-1,-2] → w00=-1, w10=-2
    # col1=[1,2]   → w01=1,  w11=2
    results = await load_and_compute(dut,
        a00=1,  a01=-1, a10=2,  a11=-2,
        w00=-1, w01=1,  w10=-2, w11=2
    )

    # C[0][0] = 1×(-1) + (-1)×(-2) = -1+2 =  1
    # C[0][1] = 1×1    + (-1)×2    =  1-2 = -1
    # C[1][0] = 2×(-1) + (-2)×(-2) = -2+4 =  2
    # C[1][1] = 2×1    + (-2)×2    =  2-4 = -2
    assert results[0] ==  1, f"C[0][0]: expected  1, got {results[0]}"
    assert results[1] == -1, f"C[0][1]: expected -1, got {results[1]}"
    assert results[2] ==  2, f"C[1][0]: expected  2, got {results[2]}"
    assert results[3] == -2, f"C[1][1]: expected -2, got {results[3]}"
    dut._log.info("Test 4 PASS")


@cocotb.test()
async def test_max_positive(dut):
    """A=[[7,7],[7,7]] x W=[[7,7],[7,7]] = [[98,98],[98,98]]
    Boundary test: 7x7 + 7x7 = 98, fits in signed 8-bit (max 127)"""
    dut._log.info("Test 5: Max positive values")
    dut._log.info("A=[[7,7],[7,7]] x W=[[7,7],[7,7]] = [[98,98],[98,98]]")
    clock = Clock(dut.clk, 10, unit="us")
    cocotb.start_soon(clock.start())
    await reset_dut(dut)

    results = await load_and_compute(dut,
        a00=7, a01=7, a10=7, a11=7,
        w00=7, w01=7, w10=7, w11=7
    )

    # C[i][j] = 7×7 + 7×7 = 49+49 = 98 for all entries
    for i, r in enumerate(results):
        assert r == 98, f"C[{i}]: expected 98, got {r}"
    dut._log.info("Test 5 PASS")
