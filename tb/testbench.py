import cocotb
import logging
from default_values import *
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles, FallingEdge, RisingEdge, Timer
from cocotb.log import SimColourLogFormatter, SimLog, SimTimeContextFilter

class Tb:
    def __init__(self, dut, log_name):
        self.dut = dut
        self.log = SimLog(log_name)
        self.log.setLevel(logging.DEBUG)

    async def setup_clks(self, clk_mode):
        self.log.info(f"[Setup] Configuring the clocks: {clk_mode}")
        self.dut._log.info("%s",clk_mode)
        if clk_mode == "AXI_>_NoC":
            cocotb.fork(Clock(self.dut.clk_noc, *CLK_100MHz).start())
            cocotb.fork(Clock(self.dut.clk_axi, *CLK_200MHz).start())
        elif clk_mode == "NoC_>_AXI":
            cocotb.fork(Clock(self.dut.clk_axi, *CLK_100MHz).start())
            cocotb.fork(Clock(self.dut.clk_noc, *CLK_200MHz).start())

    async def arst(self, clk_mode):
        self.log.info(f"[Setup] Reset DUT")
        self.dut.arst_axi.setimmediatevalue(0)
        self.dut.arst_noc.setimmediatevalue(0)
        self.dut.arst_axi <= 1
        self.dut.arst_noc <= 1
        if clk_mode == "AXI_>_NoC":
            await ClockCycles(self.dut.clk_axi, RST_CYCLES)
        else:
            await ClockCycles(self.dut.clk_noc, RST_CYCLES)
        self.dut.arst_axi <= 0
        self.dut.arst_noc <= 0