from uvm.base.sv import sv_if


class flash_if(sv_if):

    #  // Actual Signals
    # wire 		pwm0;
    # wire 		pwm1;

    def __init__(self, dut):
        bus_map = {"CLK": "CLK", "RESETn": "RESETn", "mem": "vip.I0.memory"}
        super().__init__(dut, "", bus_map)
