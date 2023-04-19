import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles
from cocotb.triggers import RisingEdge
from cocotb.triggers import Timer
import ctypes as ct

@cocotb.test()
async def test_dec_1(dut):
    """ Testing the serial multiplier """

    A = 15
    B = 10
    C = A * B

    cocotb.start_soon(Clock(dut.clk, 10, units='ns').start())

    dut.reset.value = 1
    dut.valid.value = 0
    dut.toggle.value = 0
    await ClockCycles(dut.clk, 5, True)
    dut.reset.value = 0

    dut.din.value = B >> 4
    dut.valid.value = 1
    await ClockCycles(dut.clk, 7+1200)
    dut.valid.value = 0
    await ClockCycles(dut.clk, 3+1200)


    dut.din.value = B
    dut.valid.value = 1
    await ClockCycles(dut.clk, 7+1200)
    dut.valid.value = 0
    await ClockCycles(dut.clk, 3+1200)

    dut.din.value = A >> 4
    dut.valid.value = 1
    await ClockCycles(dut.clk, 7+1200)
    dut.valid.value = 0
    await ClockCycles(dut.clk, 3+1200)

    dut.din.value = A
    dut.valid.value = 1
    await ClockCycles(dut.clk, 7+1200)
    dut.valid.value = 0
    await ClockCycles(dut.clk, 3+1200)

    result = dut.dout.value
    await ClockCycles(dut.clk, 500)

    dut.toggle.value = 1
    await ClockCycles(dut.clk, 500)
    result =  result | (dut.dout.value<<8)

    await ClockCycles(dut.clk, 500)

    assert int(result) == C, f"assertion failed expected:{C}, got:{int(result)}"

    await ClockCycles(dut.clk, 500)
