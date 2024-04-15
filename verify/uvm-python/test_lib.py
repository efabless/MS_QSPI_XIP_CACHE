import cocotb
from uvm.comps import UVMTest
from uvm import UVMCoreService
from uvm.macros import uvm_component_utils, uvm_fatal, uvm_info
from uvm.base.uvm_config_db import UVMConfigDb
from uvm.base.uvm_printer import UVMTablePrinter
from uvm.base.sv import sv
from uvm.base.uvm_object_globals import UVM_FULL, UVM_LOW, UVM_ERROR
from uvm.base.uvm_globals import run_test
from EF_UVM.top_env import top_env
from flash_interface.flash_if import flash_if
from EF_UVM.bus_env.bus_interface.bus_if import (
    bus_apb_if,
    bus_irq_if,
    bus_ahb_if,
    bus_wb_if,
)
from cocotb_coverage.coverage import coverage_db
from cocotb.triggers import Event, First
from EF_UVM.bus_env.bus_regs import bus_regs
from uvm.base.uvm_report_server import UVMReportServer

# seq
from EF_UVM.bus_env.bus_seq_lib.write_read_regs import write_read_regs
from flash_seq_lib.flash_read_seq import flash_read_seq
from flash_seq_lib.flash_async_reset_seq import flash_async_reset_seq
from flash_seq_lib.flash_rd_wr_seq import flash_rd_wr_seq
from uvm.base import UVMRoot

# override classes
from EF_UVM.ip_env.ip_agent.ip_driver import ip_driver
from flash_agent.flash_driver import flash_driver
from EF_UVM.ip_env.ip_agent.ip_monitor import ip_monitor
from flash_agent.flash_monitor import flash_monitor
from EF_UVM.ref_model.ref_model import ref_model
from ref_model.ref_model import flash_VIP
from EF_UVM.scoreboard import scoreboard
from EF_UVM.ip_env.ip_coverage.ip_coverage import ip_coverage

#
from EF_UVM.bus_env.bus_agent.bus_ahb_driver import bus_ahb_driver
from EF_UVM.bus_env.bus_agent.bus_apb_driver import bus_apb_driver
from EF_UVM.bus_env.bus_agent.bus_wb_driver import bus_wb_driver
from EF_UVM.bus_env.bus_agent.bus_ahb_monitor import bus_ahb_monitor
from EF_UVM.bus_env.bus_agent.bus_apb_monitor import bus_apb_monitor
from EF_UVM.bus_env.bus_agent.bus_wb_monitor import bus_wb_monitor

import os
from EF_UVM.base_test import base_test
from EF_UVM.bus_env.bus_agent.bus_ahb_driver import bus_ahb_driver


@cocotb.test()
async def module_top(dut):
    # profiler = cProfile.Profile()
    # profiler.enable()
    BUS_TYPE = cocotb.plusargs["BUS_TYPE"]
    print(f"plusr agr value = {BUS_TYPE}")
    pif = flash_if(dut)
    if BUS_TYPE == "APB":
        w_if = bus_apb_if(dut)
    elif BUS_TYPE == "AHB":
        w_if = bus_ahb_if(dut)
    elif BUS_TYPE == "WISHBONE":
        w_if = bus_wb_if(dut)
    else:
        uvm_fatal("module_top", f"unknown bus type {BUS_TYPE}")
    yaml_file = []
    UVMRoot().clp.get_arg_values("+YAML_FILE=", yaml_file)
    yaml_file = yaml_file[0]
    regs = bus_regs(yaml_file)
    if regs.get_irq_exist():
        w_irq_if = bus_irq_if(dut)
    else:
        w_irq_if = None
    UVMConfigDb.set(None, "*", "ip_if", pif)
    UVMConfigDb.set(None, "*", "bus_if", w_if)
    UVMConfigDb.set(None, "*", "bus_irq_if", w_irq_if)
    UVMConfigDb.set(None, "*", "bus_regs", regs)
    UVMConfigDb.set(None, "*", "irq_exist", regs.get_irq_exist())
    UVMConfigDb.set(None, "*", "insert_glitches", False)
    UVMConfigDb.set(None, "*", "collect_coverage", True)
    UVMConfigDb.set(None, "*", "disable_logger", False)
    test_path = []
    UVMRoot().clp.get_arg_values("+TEST_PATH=", test_path)
    test_path = test_path[0]
    await run_test()
    coverage_db.export_to_yaml(filename=f"{test_path}/coverage.yalm")
    # profiler.disable()
    # profiler.dump_stats("profile_result.prof")


class flash_base_test(base_test):
    def __init__(self, name="flash_first_test", parent=None):
        BUS_TYPE = cocotb.plusargs["BUS_TYPE"]
        super().__init__(name, bus_type=BUS_TYPE, parent=parent)
        self.tag = name

    def build_phase(self, phase):
        super().build_phase(phase)
        # override
        self.set_type_override_by_type(ip_driver.get_type(), flash_driver.get_type())
        self.set_type_override_by_type(ip_monitor.get_type(), flash_monitor.get_type())
        self.set_type_override_by_type(ref_model.get_type(), flash_VIP.get_type())


uvm_component_utils(flash_base_test)


class flashReadTest(flash_base_test):
    def __init__(self, name="flashReadTest", parent=None):
        super().__init__(name, parent=parent)
        self.tag = name

    def build_phase(self, phase):
        super().build_phase(phase)
        self.memory_size = 0x100000  # 1 MB
        memory_rand_val = os.urandom(self.memory_size)  # 1 MB
        UVMConfigDb.set(None, "*", "flash_memory", memory_rand_val)
        UVMConfigDb.set(None, "*", "flash_size", self.memory_size)

    async def main_phase(self, phase):
        uvm_info(self.tag, f"Starting test {self.__class__.__name__}", UVM_LOW)
        phase.raise_objection(self, f"{self.__class__.__name__} OBJECTED")
        bus_seq = flash_read_seq("flash_read_seq", self.memory_size)
        await bus_seq.start(self.bus_sqr)
        phase.drop_objection(self, f"{self.__class__.__name__} drop objection")


uvm_component_utils(flashReadTest)


class flashResetTest(flash_base_test):
    def __init__(self, name="flashResetTest", parent=None):
        super().__init__(name, parent)
        self.tag = name

    def build_phase(self, phase):
        super().build_phase(phase)
        self.memory_size = 0x100000  # 1 MB
        memory_rand_val = os.urandom(self.memory_size)  # 1 MB
        UVMConfigDb.set(None, "*", "flash_memory", memory_rand_val)
        UVMConfigDb.set(None, "*", "flash_size", self.memory_size)

    async def main_phase(self, phase):
        uvm_info(self.tag, f"Starting test {self.__class__.__name__}", UVM_LOW)
        phase.raise_objection(self, f"{self.__class__.__name__} OBJECTED")
        bus_seq = flash_async_reset_seq("flash_async_reset_seq", self.memory_size)
        await bus_seq.start(self.bus_sqr)
        phase.drop_objection(self, f"{self.__class__.__name__} drop objection")


uvm_component_utils(flashResetTest)


class flashRdWrTest(flash_base_test):
    def __init__(self, name="flashRdWrTest", parent=None):
        super().__init__(name, parent)
        self.tag = name

    def build_phase(self, phase):
        super().build_phase(phase)
        self.memory_size = 0x100000  # 1 MB
        memory_rand_val = os.urandom(self.memory_size)  # 1 MB
        UVMConfigDb.set(None, "*", "flash_memory", memory_rand_val)
        UVMConfigDb.set(None, "*", "flash_size", self.memory_size)

    async def main_phase(self, phase):
        uvm_info(self.tag, f"Starting test {self.__class__.__name__}", UVM_LOW)
        phase.raise_objection(self, f"{self.__class__.__name__} OBJECTED")
        bus_seq = flash_rd_wr_seq("flash_rd_wr_seq", self.memory_size)
        await bus_seq.start(self.bus_sqr)
        phase.drop_objection(self, f"{self.__class__.__name__} drop objection")


uvm_component_utils(flashRdWrTest)
