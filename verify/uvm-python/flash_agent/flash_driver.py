from uvm.macros import uvm_component_utils, uvm_fatal, uvm_info, uvm_warning
from uvm.comps.uvm_driver import UVMDriver
from uvm.base.uvm_config_db import UVMConfigDb
from uvm.base.uvm_object_globals import UVM_HIGH, UVM_LOW, UVM_MEDIUM
from cocotb.triggers import Timer, ClockCycles, FallingEdge, Event, RisingEdge, First
import cocotb
import random
from EF_UVM.ip_env.ip_agent.ip_driver import ip_driver


class flash_driver(ip_driver):
    def __init__(self, name="flash_driver", parent=None):
        super().__init__(name, parent)
        self.tag = name

    async def reset_phase(self, phase):
        await self.reset()

    async def pre_configure_phase(self, phase):
        # get memory content
        mem = []
        if (not UVMConfigDb.get(self, "", "flash_memory", mem)):
            uvm_fatal(self.tag, "No content of flash memory passed")
        else:
            mem = mem[0]
        # get memory content
        mem_size = []
        if (not UVMConfigDb.get(self, "", "flash_size", mem_size)):
            uvm_fatal(self.tag, "No size passed for memory")
        else:
            mem_size = mem_size[0]
        # configure the memory here.
        for i in range(0, mem_size):
            self.vif.mem[i].value = mem[i]

    async def run_phase(self, phase):
        return

    async def wait_reset(self):
        await FallingEdge(self.vif.RESETn)

    async def reset(self):
        # trigger vip reset
        return
        self.vif.vip_reset.value = 1
        await Timer(1, "ns")
        self.vif.vip_reset.value = 0


uvm_component_utils(flash_driver)
