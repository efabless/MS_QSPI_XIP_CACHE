from uvm.macros import uvm_component_utils, uvm_fatal, uvm_info, uvm_error, uvm_warning
from uvm.base.uvm_object_globals import UVM_HIGH, UVM_LOW, UVM_MEDIUM
from EF_UVM.ip_env.ip_agent.ip_monitor import ip_monitor


class flash_monitor(ip_monitor):
    def __init__(self, name="flash_monitor", parent=None):
        super().__init__(name, parent)

    async def run_phase(self, phase):
        # the ip monitor is not needed for this design
        return


uvm_component_utils(flash_monitor)
