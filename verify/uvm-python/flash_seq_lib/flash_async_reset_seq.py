from uvm.seq import UVMSequence
from uvm.macros.uvm_object_defines import uvm_object_utils
from uvm.macros.uvm_message_defines import uvm_fatal
from EF_UVM.bus_env.bus_item import bus_item
from uvm.base.uvm_config_db import UVMConfigDb
from EF_UVM.bus_env.bus_seq_lib.bus_seq_base import bus_seq_base
from cocotb.triggers import Timer
from uvm.macros.uvm_sequence_defines import uvm_do_with, uvm_do
import random
import cocotb


class flash_async_reset_seq(bus_seq_base):

    def __init__(self, name="flash_async_reset_seq", memory_size=1024):
        super().__init__(name)
        self.memory_size = memory_size

    async def body(self):
        # get register names/address conversion dict
        await super().body()
        await cocotb.start(self.send_async_reset())
        await self.read_rand_addresses()

    async def read_address(self, address):
        self.create_new_item()
        self.req.rand_mode(0)
        self.req.addr = address
        self.req.kind = bus_item.READ
        self.req.data = 0  # needed to add any dummy value
        await uvm_do(self, self.req)

    async def read_rand_addresses(self):
        for _ in range(500):
            address = random.randrange(0, self.memory_size, 4)
            await self.read_address(address=address)

    async def send_async_reset(self):
        while True:
            rand_time = random.randint(10000, 50000)
            await Timer(rand_time, "ns")  # wait random time for async reset
            await self.send_reset()


uvm_object_utils(flash_async_reset_seq)
