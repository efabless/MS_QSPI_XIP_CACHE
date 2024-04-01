from uvm.base.uvm_component import UVMComponent
from uvm.macros import uvm_component_utils
from uvm.tlm1.uvm_analysis_port import UVMAnalysisImp
from uvm.base.uvm_object_globals import UVM_HIGH, UVM_LOW, UVM_MEDIUM
from uvm.macros import uvm_component_utils, uvm_fatal, uvm_info
from uvm.base.uvm_config_db import UVMConfigDb
from uvm.tlm1.uvm_analysis_port import UVMAnalysisExport
from EF_UVM.ref_model.ref_model import ref_model
from EF_UVM.bus_env.bus_item import bus_item
from EF_UVM.ip_env.ip_agent.ip_monitor import ip_monitor
from cocotb.triggers import Timer, ClockCycles, FallingEdge, Event, RisingEdge, Combine, First
import cocotb

class flash_VIP(ref_model):
    def __init__(self, name="flash_VIP", parent=None):
        super().__init__(name, parent)
        self._timer_first_flag = False
        self.event_calibrate_tmr = Event("event_calibrate_tmr")

    def build_phase(self, phase):
        super().build_phase(phase)
        arr = []
        if (not UVMConfigDb.get(self, "", "bus_regs", arr)):
            uvm_fatal(self.tag, "No json file wrapper regs")
        else:
            self.regs = arr[0]
        self.bus_write_event = Event("bus_write_event")
        self.clock_period = 10

    async def pre_configure_phase(self, phase):
        mem = []
        if (not UVMConfigDb.get(self, "", "flash_memory", mem)):
            uvm_fatal(self.tag, "No content of flash memory passed")
        else:
            self.flash_memory = mem[0]

    async def run_phase(self, phase):
        await super().run_phase(phase)
        return

    def write_bus(self, tr):
        uvm_info(self.tag, "Vip write: " + tr.convert2string(), UVM_HIGH)
        if tr.kind == bus_item.RESET:
            self.bus_bus_export.write(tr)
            return
        if tr.kind == bus_item.READ:
            data = self.get_memory_value(tr.addr)
            td = tr.do_clone()
            td.data = data
            self.bus_bus_export.write(td)
        elif tr.kind == bus_item.WRITE:
            self.bus_bus_export.write(tr)
        self.bus_write_event.clear()

    def write_ip(self, tr):
        pass

    def get_memory_value(self, address):
        data = self.flash_memory[address] | self.flash_memory[address+1] << 8 | self.flash_memory[address+2] << 16 | self.flash_memory[address+3] << 24
        return data

uvm_component_utils(flash_VIP)
